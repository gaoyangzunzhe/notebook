"""架构重构后端冒烟脚本：迁移生效 + 文档分类 + rag 分类过滤 + 笔记独立。"""
import io
import json
import time
import urllib.error
import urllib.request
import uuid

BASE = "http://127.0.0.1:8001/api/v1"

PASS, FAIL = 0, 0


def check(name, cond, extra=""):
    global PASS, FAIL
    if cond:
        PASS += 1
        print(f"  ok  {name} {extra}")
    else:
        FAIL += 1
        print(f"FAIL  {name} {extra}")


def req(method, path, token=None, body=None, files=None, timeout=180, params=None):
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
            buf.write(f"--{boundary}\r\nContent-Disposition: form-data; name=\"{k}\"".encode())
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
            return resp.status, (json.loads(raw) if raw else None)
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", errors="replace")
        try:
            return e.code, json.loads(raw)
        except Exception:
            return e.code, {"detail": raw}


# ---------- 0) 迁移生效（DB 层） ----------
import asyncio
import asyncpg
from app.core.config import Settings

s = Settings()


async def _db_check():
    conn = await asyncpg.connect(
        s.database_url.replace("postgresql+asyncpg://", "postgresql://")
    )
    try:
        tables = {r["tablename"] for r in
                  await conn.fetch("SELECT tablename FROM pg_tables WHERE schemaname='public'")}
        check("迁移: notebooks 表已删", "notebooks" not in tables)
        check("迁移: note_documents 表已删", "note_documents" not in tables)
        cols = {r["column_name"] for r in
                await conn.fetch("SELECT column_name FROM information_schema.columns WHERE table_name='documents'")}
        check("迁移: documents.category 存在", "category" in cols)
        ncols = {r["column_name"] for r in
                 await conn.fetch("SELECT column_name FROM information_schema.columns WHERE table_name='notes'")}
        check("迁移: notes.notebook_id 已删", "notebook_id" not in ncols)
        scols = {r["column_name"] for r in
                 await conn.fetch("SELECT column_name FROM information_schema.columns WHERE table_name='user_settings'")}
        check("迁移: user_settings.doc_categories 存在", "doc_categories" in scols)
        dc = await conn.fetch("SELECT category, COUNT(*) AS n FROM documents GROUP BY category")
        print("  documents.category 分布:", {r["category"]: r["n"] for r in dc})
    finally:
        await conn.close()


asyncio.run(_db_check())

# ---------- 1) 注册 / 登录 ----------
suffix = uuid.uuid4().hex[:6]
uname, pwd = f"smoke_{suffix}", "smoke-pass-123"
st, _ = req("POST", "/auth/register", body={
    "username": uname, "email": f"{uname}@t.com",
    "password": pwd, "confirm_password": pwd,
})
check("注册", st in (200, 201), f"->{st}")
st, tok = req("POST", "/auth/login", body={"account": uname, "password": pwd})
check("登录", st in (200, 201), f"->{st}")
token = tok["access_token"]
uname2, pwd2 = f"smoke2_{suffix}", "smoke-pass-123"
req("POST", "/auth/register", body={
    "username": uname2, "email": f"{uname2}@t.com",
    "password": pwd2, "confirm_password": pwd2,
})
st, tok2 = req("POST", "/auth/login", body={"account": uname2, "password": pwd2})
token2 = tok2["access_token"]

# ---------- 2) 上传（带分类 / 缺省） ----------
rep_text = "SQL Server 数据库性能优化：使用索引覆盖避免回表，关注执行计划中的嵌套循环与哈希连接，合理设置填充因子。"
gen_text = "Python 学习笔记：理解生成器与迭代器协议，yield 关键字把函数变为生成器，惰性求值节省内存。"
st, r = req("POST", "/documents/upload", token,
            files={"file": ("sql_report.txt", rep_text.encode()), "category": "报告"})
check("上传带分类=报告", st == 201 and r["doc_id"], f"->{st} chunk={r['chunk_count']}")
rep_id = r["doc_id"]
st, r = req("POST", "/documents/upload", token,
            files={"file": ("python_note.txt", gen_text.encode())})
check("上传缺省=未分类", st == 201, f"->{st}")
gen_id = r["doc_id"]

st, r = req("GET", "/documents", token, params={"category": "报告"})
check("GET /documents?category=报告 只回报告文档",
      st == 200 and len(r["documents"]) == 1 and r["documents"][0]["doc_id"] == rep_id
      and r["documents"][0]["category"] == "报告", f"total={r.get('total')}")
st, r = req("GET", "/documents", token)
cats = {d["category"] for d in r["documents"]}
check("GET /documents 全列且分类正确", st == 200 and {"报告", "未分类"} <= cats, f"cats={cats}")

# ---------- 3) categories 并集 / 新建 ----------
st, r = req("GET", "/documents/categories", token)
check("GET /documents/categories 并集", st == 200 and r["categories"] == ["报告", "未分类"],
      f"->{r['categories']}")
st, r = req("POST", "/documents/categories", token, body={"category": "待整理"})
check("POST categories 新建待整理", st == 201 and "待整理" in r["categories"], f"->{r['categories']}")
st, r2 = req("POST", "/documents/categories", token, body={"category": "待整理"})
check("重复新建幂等", r2["categories"] == r["categories"], f"->{r2['categories']}")
st, r = req("POST", "/documents/categories", token, body={"category": "未分类"})
check("未分类不可建", st == 400, f"->{st}")

# ---------- 4) PATCH 改分类（Chroma-first + DB） ----------
st, r = req("PATCH", f"/documents/{rep_id}", token, body={"category": "重要"})
check("PATCH 改分类=重要", st == 200 and r["category"] == "重要", f"->{st} {r.get('category')}")
st, r = req("GET", "/documents/categories", token)
check("categories 含重要", "重要" in r["categories"], f"->{r['categories']}")

# ---------- 5) rag 按分类过滤（核对 sources 与 retriever 一致） ----------
q = "SQL Server 数据库性能优化有哪些手段？"
st, r = req("POST", "/rag/query", token, body={"question": q, "k": 3, "category": "重要"})
if st == 200:
    srcs = [s["source"] for s in r["sources"]]
    ok = len(r["sources"]) > 0 and all("sql_report" in s for s in srcs)
    check("rag category=重要 时 sources 全部来自重要文档", ok, f"srcs={srcs}")
    print(f"      answer 前 60 字: {r['answer'][:60]!r}")
else:
    check("rag category=重要", False, f"->{st} {r}")
st, r = req("POST", "/rag/query", token, body={"question": q, "k": 3})
if st == 200:
    check("rag 无 category 全库检索", len(r["sources"]) > 0, f"srcs={[s['source'] for s in r['sources']]}")
else:
    check("rag 无 category", False, f"->{st} {r}")

# ---------- 6) 笔记独立 + assist + related ----------
st, r = req("GET", "/notes", token)
check("GET /notes 空列表", st == 200 and r["total"] == 0, f"total={r.get('total')}")
st, r = req("POST", "/notes", token, body={"title": "SQL Server 优化随记", "content": rep_text})
check("POST /notes 201 无 notebook_id", st == 201 and "notebook_id" not in r, f"->{st}")
note_id = r["id"]

st, r = req("GET", "/notes/{}/related-documents".format(note_id), token)
check("related-documents 返回相关文档", st == 200 and len(r["related"]) >= 1,
      f"related={[(x['filename'], x['score']) for x in r['related']]}")
if st == 200:
    rd = [x["doc_id"] for x in r["related"]]
    check("related 含 rep 文档", rep_id in rd, f"ids={rd}")

# assist SSE：只取状态码 + 首行，验证快速返回（无向量检索）
start = time.time()
import urllib.parse
aid = urllib.parse.quote(json.dumps({"action": "continue"}), safe="")
url = f"{BASE}/notes/{note_id}/assist"
rr = urllib.request.Request(url, data=json.dumps({"action": "continue"}).encode(),
                            headers={"Authorization": f"Bearer {token}",
                                     "Content-Type": "application/json"}, method="POST")
with urllib.request.urlopen(rr, timeout=120) as resp:
    first = resp.read(40).decode("utf-8", errors="replace")
elapsed = time.time() - start
check("assist SSE 快速返回（无向量检索）", resp.status == 200 and elapsed < 60,
      f"->{resp.status} {elapsed:.1f}s first={first[:30]!r}")

# ---------- 7) 用户隔离 ----------
st, r = req("GET", "/documents/categories", token2)
check("B 用户 categories 隔离（仅未分类）", st == 200 and r["categories"] == ["未分类"],
      f"->{r['categories']}")
st, r = req("PATCH", f"/documents/{rep_id}", token2, body={"category": "重要"})
check("B 用户 PATCH A 文档 -> 404", st == 404, f"->{st}")
st, r = req("GET", "/documents", token2, params={"category": "报告"})
check("B 用户 list 不泄露 A 文档", r["total"] == 0, f"total={r.get('total')}")
st, r = req("GET", "/notes/{}/related-documents".format(note_id), token2)
check("B 用户访问 A 笔记 related -> 404", st == 404, f"->{st}")

print(f"\n== 结果: {PASS} passed, {FAIL} failed ==")
raise SystemExit(1 if FAIL else 0)
