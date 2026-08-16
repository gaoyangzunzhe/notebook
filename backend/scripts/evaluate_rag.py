"""RAG 检索质量离线评测。

用法（backend/ 下，venv 已激活）：
    python scripts/evaluate_rag.py
    python scripts/evaluate_rag.py --chunk-sizes "500,1000" --k-values "1,2,4"

设计：
- 语料：scripts/eval_data/corpus/*.{txt,md}；标注集：scripts/eval_data/eval_set.json
- gold 用「原文片段」引用：检索返回的块包含该片段（verbatim）即视为命中。
  无需稳定 chunk id，兼容存量数据，标注直观。
- 每组 (chunk_size, k)：把语料切块后写入同一 Chroma 集合、不同 sentinel user_id
  （复用线上「单集合 + 元数据过滤」隔离路径），再对每个问题跑相似度检索比对。
- 指标：Hit@k / Recall@k / Precision@k / MRR@k / NDCG@k（按问题取均值）。
  只衡量「检索」质量，不涉及生成。
"""
import argparse
import json
import math
import sys
import time
from pathlib import Path

# 保证从任意 cwd 都能 import app 包
BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.core.config import Settings  # noqa: E402
from app.services.rag.loader import load_document  # noqa: E402
from app.services.rag.splitter import split_documents  # noqa: E402
from app.services.rag.vectorstore import COLLECTION_NAME, VectorStoreManager  # noqa: E402

SCRIPTS_DIR = Path(__file__).resolve().parent
DEFAULT_CORPUS = SCRIPTS_DIR / "eval_data" / "corpus"
DEFAULT_EVAL_SET = SCRIPTS_DIR / "eval_data" / "eval_set.json"

# eval 数据用高位哨兵 user_id 隔离，避免与真实用户（>=1）冲突
SENTINEL_BASE = 900

METRIC_KEYS = ["hit", "recall", "precision", "mrr", "ndcg"]


def build_index(
    vs: VectorStoreManager,
    corpus_dir: Path,
    chunk_size: int,
    chunk_overlap: int,
    user_id: int,
) -> int:
    """把语料切块写入集合，返回总块数。"""
    total = 0
    for path in sorted(corpus_dir.iterdir()):
        if path.is_file() and path.suffix.lower() in {".txt", ".md", ".markdown"}:
            docs = load_document(path, path.name)
            chunks = split_documents(docs, chunk_size, chunk_overlap)
            if chunks:
                total += with_retry(lambda: vs.add_documents(chunks, user_id=user_id))
    return total


def cleanup_eval_data(vs: VectorStoreManager, sentinels: set[int]) -> None:
    """删除集合中 eval 哨兵 user_id 的块（幂等；集合不存在则跳过）。"""
    try:
        col = vs.client.get_collection(COLLECTION_NAME)
    except Exception:
        return
    try:
        col.delete(where={"user_id": {"$in": sorted(sentinels)}})
    except Exception as e:  # noqa: BLE001
        print(f"[warn] 清理 eval 数据失败: {e}")


def with_retry(fn, attempts: int = 3, delay: float = 2.0):
    """对外部 provider 的瞬时错误（连接抖动等）做重试。"""
    last: Exception | None = None
    for i in range(attempts):
        try:
            return fn()
        except Exception as e:  # noqa: BLE001
            last = e
            if i < attempts - 1:
                time.sleep(delay)
    raise last  # type: ignore[misc]


def _contains(hay: str, needle: str) -> bool:
    return needle.strip() in hay


def metrics_for_question(search_fn, question: dict, k: int) -> dict:
    """单个问题的检索指标。search_fn(q) -> list[(Document, score)]"""
    results = search_fn(question["question"])
    if not results:
        return {key: 0.0 for key in METRIC_KEYS}
    chunks = [doc for doc, _ in results]
    gold = question["gold_snippets"]

    # 每块相关性是二进制的：命中任一 gold 片段即 1
    relevances = [
        1 if any(_contains(doc.page_content, s) for s in gold) else 0 for doc in chunks
    ]
    matched_snippets = sum(
        1 for s in gold if any(_contains(c.page_content, s) for c in chunks)
    )

    dcg_val = sum(rel / math.log2(i + 2) for i, rel in enumerate(relevances))
    idcg_val = sum(
        rel / math.log2(i + 2) for i, rel in enumerate(sorted(relevances, reverse=True))
    )
    return {
        "hit": 1.0 if any(relevances) else 0.0,
        "recall": matched_snippets / len(gold),
        "precision": sum(relevances) / len(relevances),
        "mrr": next((1.0 / (i + 1) for i, rel in enumerate(relevances) if rel), 0.0),
        "ndcg": dcg_val / idcg_val if idcg_val > 0 else 0.0,
    }


def aggregate(results: list[dict]) -> dict:
    n = len(results)
    return {key: sum(r[key] for r in results) / n for key in METRIC_KEYS}


def parse_csv(value: str):
    return [int(x.strip()) for x in value.split(",") if x.strip()]


def main() -> int:
    parser = argparse.ArgumentParser(description="RAG 检索质量离线评测")
    parser.add_argument("--corpus", default=str(DEFAULT_CORPUS), help="语料目录")
    parser.add_argument("--eval-set", default=str(DEFAULT_EVAL_SET), help="标注集 JSON")
    parser.add_argument("--chunk-sizes", default="500,1000", help="逗号分隔的 chunk_size")
    parser.add_argument("--k-values", default="1,2,4", help="逗号分隔的 top-k")
    parser.add_argument(
        "--keep-data", action="store_true", help="评测结束后不清理 eval 块（默认清理）"
    )
    parser.add_argument(
        "--report", nargs="?", const="", help="把评测报告写入 Markdown 文件（不填则默认 scripts/eval_data/last_report.md）"
    )
    args = parser.parse_args()

    corpus_dir = Path(args.corpus)
    if not corpus_dir.is_dir():
        print(f"错误：语料目录不存在 {corpus_dir}")
        return 1
    with open(args.eval_set, encoding="utf-8") as f:
        questions = json.load(f)
    if not questions:
        print("错误：标注集为空")
        return 1

    chunk_sizes = parse_csv(args.chunk_sizes)
    k_values = parse_csv(args.k_values)
    sentinels = {SENTINEL_BASE + i for i in range(len(chunk_sizes))}

    settings = Settings()
    vs = VectorStoreManager(settings)

    report: list[str] = []

    def emit(line: str = "") -> None:
        report.append(line)
        print(line)

    emit("=== RAG 检索质量评测 ===")
    emit(f"语料     : {corpus_dir}")
    emit(f"标注集   : {len(questions)} 个问题")
    emit(f"chunk_size: {chunk_sizes}（overlap={settings.chunk_overlap}）")
    emit(f"k        : {k_values}")
    emit()

    # 清理历史残留，保证本次评测环境干净
    cleanup_eval_data(vs, sentinels)
    try:
        uid_by_size = {cs: SENTINEL_BASE + i for i, cs in enumerate(sorted(chunk_sizes))}

        emit("| chunk_size | k | 语料块数 | Hit@k | Recall@k | Precision@k | MRR@k | NDCG@k |")
        emit("|---|---|---|---|---|---|---|---|")
        detail = None  # 默认配置（最小 chunk_size + 最大 k）的逐题明细
        for cs in sorted(chunk_sizes):
            uid = uid_by_size[cs]
            n_chunks = build_index(vs, corpus_dir, cs, settings.chunk_overlap, uid)
            for k in sorted(k_values, reverse=True):
                search_fn = lambda q, uid=uid, k=k: with_retry(
                    lambda: vs.search(q, k, user_id=uid)
                )
                per_q = [metrics_for_question(search_fn, q, k) for q in questions]
                agg = aggregate(per_q)
                emit(
                    f"| {cs} | {k} | {n_chunks} | {agg['hit']:.3f} | {agg['recall']:.3f} "
                    f"| {agg['precision']:.3f} | {agg['mrr']:.3f} | {agg['ndcg']:.3f} |"
                )
                if detail is None:
                    detail = (cs, k, per_q)

        if detail is not None:
            cs, k, per_q = detail
            emit()
            emit(f"逐题明细（chunk_size={cs}, k={k}）：")
            for q, r in zip(questions, per_q):
                flag = "OK  " if r["hit"] else "MISS"
                emit(
                    f"  [{flag}] Q{q['id']:>2} hit={int(r['hit'])} "
                    f"recall={r['recall']:.2f}  {q['question']}"
                )
    finally:
        if not args.keep_data:
            cleanup_eval_data(vs, sentinels)
            emit()
            emit("（已清理本轮 eval 数据）")

    if args.report is not None:
        out = Path(args.report or (SCRIPTS_DIR / "eval_data" / "last_report.md"))
        out.write_text("\n".join(report) + "\n", encoding="utf-8")
        print(f"\n报告已写入: {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
