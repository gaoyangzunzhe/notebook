"""工程化加固冒烟：护栏（信号量/限流）+ request_id + metrics + 事件循环卸载 + 模型缓存。

HTTP 部分依赖运行中的后端（127.0.0.1:8000）。
配额 429 检查为条件执行：仅当 .env 的 AI_QUOTA_LIMIT 被临时调成 2 时才跑
（连发 3 次 /notes/{id}/tags，第 3 次应 429），否则 SKIP 不影响结果。
"""
import asyncio
import io
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # 保证 import app.*

from app.core.config import Settings
from app.core.errors import RateLimitExceeded
from app.core.guard import (
    SlidingWindowLimiter,
    get_llm_semaphore,
    init_guard,
    llm_slot,
)

BASE = "http://127.0.0.1:8000/api/v1"
PASS, FAIL, SKIP = 0, 0, 0


def check(name, cond, extra=""):
    global PASS, FAIL
    if cond:
        PASS += 1
        print(f"  ok  {name} {extra}")
    else:
        FAIL += 1
        print(f"FAIL  {name} {extra}")


def skip(name, extra=""):
    global SKIP
    SKIP += 1
    print(f" SKIP {name} {extra}")


def req(method, path, token=None, body=None, files=None, timeout=180, params=None):
    """返回 (status, json)。files: {字段名: (文件名, 字节) 或 str}。"""
    url = BASE + path
    if params:
        url += "?" + urllib.parse.urlencode(params)
    headers = {}
    data = None
    if token:
        headers["Authorization"] = f"Bearer {token}"
    if files is not None:
        boundary = uuid.uuid4().hex
        buf = io.BytesIO()
        for k, v in files.items():
            buf.write(f'--{boundary}\r\nContent-Disposition: form-data; name="{k}"'.encode())
            if isinstance(v, tuple):
                buf.write(f'; filename="{v[0]}"\r\nContent-Type: text/plain\r\n\r\n'.encode())
                buf.write(v[1])
            else:
                buf.write(b"\r\n\r\n")
                buf.write(v.encode())
            buf.write(b"\r\n")
        buf.write(f"--{boundary}--\r\n".encode())
        data = buf.getvalue()
        headers["Content-Type"] = f"multipart/form-data; boundary={boundary}"
    elif body is not None:
        data = json.dumps(body, ensure_ascii=False).encode()
        headers["Content-Type"] = "application/json"
    r = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(r, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8")
            rid = resp.headers.get("X-Request-Id", "")
            return resp.status, (json.loads(raw) if raw else None), rid
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", errors="replace")
        try:
            return e.code, json.loads(raw), e.headers.get("X-Request-Id", "")
        except Exception:
            return e.code, {"detail": raw}, e.headers.get("X-Request-Id", "")


# ---------- 1) 护栏单元检查（进程内，无需服务） ----------
async def guard_checks():
    # 滑动窗口限流：limit=2 -> 第 3 次抛 RateLimitExceeded
    lim = SlidingWindowLimiter(limit=2, window_seconds=3600)
    lim.hit("u:1")
    lim.hit("u:1")
    raised = False
    try:
        lim.hit("u:1")
    except RateLimitExceeded:
        raised = True
    check("限流: limit=2 第3次抛 RateLimitExceeded", raised)

    # 不同 key 独立计数（并发窗口内不同用户互不影响）
    lim2 = SlidingWindowLimiter(limit=1, window_seconds=3600)
    lim2.hit("a")
    ok = False
    try:
        lim2.hit("b")  # 另一用户应放行
        ok = True
    except RateLimitExceeded:
        pass
    check("限流: 不同用户独立计数", ok)

    # 关闭态：limit=0 恒放行
    lim0 = SlidingWindowLimiter(limit=0, window_seconds=3600)
    no_raise = True
    for _ in range(5):
        try:
            lim0.hit("any")
        except RateLimitExceeded:
            no_raise = False
    check("限流: limit=0 关闭恒放行", no_raise)

    # init_guard + 信号量：并发上限 = AI_MAX_CONCURRENT_LLM -> 超出部分排队
    settings = Settings()
    init_guard(settings)
    sem = get_llm_semaphore()
    expected = max(1, settings.ai_max_concurrent_llm)
    check("护栏: init_guard 后信号量可取", isinstance(sem, asyncio.Semaphore))

    # llm_slot 正常获取/释放：串行进 3 次不互斥阻塞（每次用完释放）
    done = 0
    for _ in range(3):
        async with llm_slot():
            done += 1
    check("护栏: llm_slot 连续进出正常", done == 3)

    # 并发占满后新增请求排队而非并发（计数验证同一时刻持槽数不超过配置上限）
    peak = 0
    current = 0
    done_count = 0

    async def worker():
        nonlocal peak, current, done_count
        async with llm_slot():
            current += 1
            peak = max(peak, current)
            await asyncio.sleep(0.05)
            current -= 1
        done_count += 1

    await asyncio.gather(*[worker() for _ in range(expected + 3)])
    check(f"护栏: 并发持槽峰值 <= {expected} (峰值={peak})",
          peak <= expected and done_count == expected + 3)


asyncio.run(guard_checks())

# ---------- 2) 中间件 / 指标 / 健康 ----------
st, r, rid = req("GET", "/health")
check("health 200", st == 200, f"->{st}")
check("响应带 X-Request-Id", bool(rid) and len(rid) == 12, f"->{rid!r}")

st, r, _ = req("GET", "/metrics")
check("GET /metrics 200", st == 200 and isinstance(r, dict), f"->{st}")
for key in ("requests", "llm", "embed", "uptime_seconds"):
    check(f"/metrics 含 {key}", key in (r or {}), f"->{(r or {}).get(key) is not None}")
check("/metrics.requests.total 为 int", isinstance((r or {}).get("requests", {}).get("total"), int))

# ---------- 3) 注册 / 登录 ----------
suffix = uuid.uuid4().hex[:6]
uname, pwd = f"guard_{suffix}", "smoke-pass-123"
st, _, _ = req("POST", "/auth/register", body={
    "username": uname, "email": f"{uname}@t.com",
    "password": pwd, "confirm_password": pwd,
})
check("注册", st in (200, 201), f"->{st}")
st, tok, _ = req("POST", "/auth/login", body={"account": uname, "password": pwd})
token = (tok or {}).get("access_token", "")
check("登录", bool(token), "->ok")

# ---------- 4) 上传（to_thread + 信号量 + 嵌入指标） ----------
sample = Path(__file__).resolve().parents[1] / "sample_data" / "note_sample.txt"
with open(sample, "rb") as f:
    content = f.read()
st, r, _ = req("POST", "/documents/upload", token,
               files={"file": ("note_sample.txt", content), "category": "工程化冒烟"})
check("上传 txt 摄取 201", st == 201 and (r or {}).get("chunk_count", 0) > 0,
      f"->{st} chunks={ (r or {}).get('chunk_count') }")
doc_id = (r or {}).get("doc_id", "")

# ---------- 5) 相关文档（a_search 异步路径） ----------
st, r, _ = req("POST", "/notes", token, body={"title": "冒烟笔记", "content": "这是我上传的工程化冒烟文档内容，用于测试相关文档推荐是否走异步检索。"})
note_id = (r or {}).get("id", 0)
st, r, _ = req("GET", f"/notes/{note_id}/related-documents", token)
check("相关文档 200（a_search）", st == 200, f"->{st} n={len((r or {}).get('related', []))}")

# ---------- 6) 模型列表（缓存安全：连拉两次均成功；Redis 可用时第二次命中缓存） ----------
st1, r1, _ = req("GET", "/settings/providers/llm/deepseek/models", token)
st2, r2, _ = req("GET", "/settings/providers/llm/deepseek/models", token)
check("模型列表连拉两次均 200", st1 == 200 and st2 == 200, f"->{st1}/{st2}")
check("模型列表有数据", (r1 or {}).get("models") and (r1 or {}).get("models") == (r2 or {}).get("models"),
      f"n={len((r1 or {}).get('models', []))}")

# ---------- 7) 配额 429（条件：仅当 AI_QUOTA_LIMIT 被临时调成 2 才跑） ----------
quota_limit = Settings().ai_quota_limit
if quota_limit == 2:
    # 用全新用户，避免前面 upload 已消耗的配额影响计数（上传消耗 1 次）
    q_uname, q_pwd = f"guardq_{uuid.uuid4().hex[:6]}", "smoke-pass-123"
    req("POST", "/auth/register", body={
        "username": q_uname, "email": f"{q_uname}@t.com",
        "password": q_pwd, "confirm_password": q_pwd,
    })
    st, q_tok, _ = req("POST", "/auth/login", body={"account": q_uname, "password": q_pwd})
    q_token = (q_tok or {}).get("access_token", "")
    st, r, _ = req("POST", "/notes", q_token, body={"title": "配额冒烟", "content": "配额测试"})
    q_note_id = (r or {}).get("id", 0)
    check("配额: 前置建笔记 200/201", st in (200, 201), f"->{st}")
    statuses = []
    for _ in range(3):
        st, r, _ = req("POST", f"/notes/{q_note_id}/tags", q_token, body={})
        statuses.append(st)
    check("配额: 前 2 次 200（真实 LLM 调用）", statuses[:2] == [200, 200], f"->{statuses}")
    check("配额: 第 3 次 429", statuses[2] == 429, f"->{statuses}")
    req("DELETE", f"/notes/{q_note_id}", q_token)
else:
    skip(f"配额 429（AI_QUOTA_LIMIT={quota_limit}，非 2，跳过真实 429 验证）",
         "需临时调成 2 重启后端后跑")

# ---------- 8) 清理（尽力删除测试文档） ----------
if doc_id:
    req("DELETE", f"/documents/{doc_id}", token)
if note_id:
    req("DELETE", f"/notes/{note_id}", token)

print(f"\n结果: PASS={PASS} FAIL={FAIL} SKIP={SKIP}")
raise SystemExit(1 if FAIL else 0)
