"""模型配置重构冒烟：env 统一前缀 + 自定义 base_url + key 回退 warning + 在线模型拉取。"""
import asyncio
import io
import json
import sys
import uuid
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # 保证 import app.*

import asyncpg

from app.core.config import Settings

BASE = "http://127.0.0.1:8000/api/v1"
PASS, FAIL = 0, 0


def check(name, cond, extra=""):
    global PASS, FAIL
    if cond:
        PASS += 1
        print(f"  ok  {name} {extra}")
    else:
        FAIL += 1
        print(f"FAIL  {name} {extra}")


def req(method, path, token=None, body=None, timeout=120, params=None):
    url = BASE + path
    if params:
        url += "?" + urllib.parse.urlencode(params)
    headers = {}
    data = None
    if token:
        headers["Authorization"] = f"Bearer {token}"
    if body is not None:
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
async def _db_check():
    conn = await asyncpg.connect(
        Settings().database_url.replace("postgresql+asyncpg://", "postgresql://")
    )
    try:
        cols = {r["column_name"] for r in await conn.fetch(
            "SELECT column_name FROM information_schema.columns WHERE table_name='user_settings'")}
        check("迁移: user_settings.llm_base_url 存在", "llm_base_url" in cols)
        check("迁移: user_settings.embed_base_url 存在", "embed_base_url" in cols)
    finally:
        await conn.close()


asyncio.run(_db_check())

# ---------- 1) 注册 / 登录 ----------
suffix = uuid.uuid4().hex[:6]
uname, pwd = f"cfg_{suffix}", "smoke-pass-123"
st, _ = req("POST", "/auth/register", body={
    "username": uname, "email": f"{uname}@t.com",
    "password": pwd, "confirm_password": pwd,
})
check("注册", st in (200, 201), f"->{st}")
st, tok = req("POST", "/auth/login", body={"account": uname, "password": pwd})
token = tok["access_token"]
check("登录", bool(token), "->ok")

# ---------- 2) GET /settings 新字段 ----------
st, r = req("GET", "/settings", token)
check("GET /settings 200", st == 200, f"->{st}")
llm, kb = r["llm"], r["kb"]
emb = kb["embed"]
check("llm.base_url 初始为 null", llm.get("base_url") is None, f"->{llm.get('base_url')!r}")
check("llm.effective.warning 存在", "warning" in llm["effective"], f"->{llm['effective'].get('warning')!r}")
check("llm.effective.base_url = env 默认", llm["effective"]["base_url"] == "https://api.deepseek.com",
      f"->{llm['effective']['base_url']!r}")
check("embed.effective.warning 存在", "warning" in emb["effective"], f"->{emb['effective'].get('warning')!r}")
check("embed.effective.base_url = dashscope", emb["effective"]["base_url"].startswith("https://dashscope.aliyuncs.com"),
      f"->{emb['effective']['base_url']!r}")

# ---------- 3) 在线模型拉取 ----------
st, r = req("GET", "/settings/providers/llm/deepseek/models", token)
check("llm/deepseek/models 拉取", st == 200 and r["models"] and r["source"] in ("live", "fallback"),
      f"->{st} source={r.get('source')} n={len(r.get('models', []))} note={r.get('note')!r}")
st, r = req("GET", "/settings/providers/embed/dashscope/models", token)
check("embed/dashscope/models 拉取", st == 200 and r["models"] and r["source"] in ("live", "fallback"),
      f"->{st} source={r.get('source')} n={len(r.get('models', []))}")
st, r = req("GET", "/settings/providers/llm/ollama/models", token)
check("llm/ollama/models 可用（live 或 fallback 均可）", st == 200 and r["models"] and r["source"] in ("live", "fallback"),
      f"->{st} source={r.get('source')} n={len(r.get('models', []))}")
st, r = req("GET", "/settings/providers/llm/openai/models", token,
            params={"base_url": "http://127.0.0.1:1/v1"})
check("不可达预览地址 → fallback 建议列表", st == 200 and r["source"] == "fallback" and r["models"] and r["note"],
      f"->{st} source={r.get('source')} note={r.get('note')!r}")
st, r = req("GET", "/settings/providers/bad/x/models", token)
check("kind 非法 422", st == 422, f"->{st}")
st, r = req("GET", "/settings/providers/llm/notexist/models", token)
check("provider 不存在 404", st == 404, f"->{st}")

# ---------- 4) key 回退 warning：选非 env 提供商且不填 key ----------
st, r = req("PUT", "/settings", token, body={"llm": {"provider": "openai"}})
eff = r["llm"]["effective"]
check("PUT openai 无 key 生效 provider=openai", st == 200 and eff["provider"] == "openai", f"->{st}")
check("PUT openai 无 key 触发 warning（key 与端点不匹配）",
      eff["warning"] is not None and "不匹配" in eff["warning"], f"->{eff['warning']!r}")
check("非法 provider 422", req("PUT", "/settings", token, body={"llm": {"provider": "notexist"}})[0] == 422)

# ---------- 5) 自定义 base_url 保存 / 回显 / 清除 ----------
st, r = req("PUT", "/settings", token,
            body={"llm": {"provider": "openai", "base_url": "https://api.example.com/v1"}})
check("PUT 自定义 base_url 200", st == 200 and r["llm"]["base_url"] == "https://api.example.com/v1",
      f"->{st} {r['llm'].get('base_url')!r}")
check("effective.base_url = 自定义", r["llm"]["effective"]["base_url"] == "https://api.example.com/v1",
      f"->{r['llm']['effective'].get('base_url')!r}")
st, r = req("GET", "/settings", token)
check("GET 回读 stored base_url", st == 200 and r["llm"]["base_url"] == "https://api.example.com/v1", f"->{r['llm'].get('base_url')!r}")
st, r = req("PUT", "/settings", token, body={"llm": {"base_url": ""}})
check("base_url 清空回 null", st == 200 and r["llm"]["base_url"] is None, f"->{r['llm'].get('base_url')!r}")

# ---------- 6) 嵌入 base_url ----------
st, r = req("PUT", "/settings", token,
            body={"kb": {"embed": {"provider": "dashscope", "base_url": "http://127.0.0.1:9998/v1"}}})
check("PUT embed 自定义 base_url", st == 200 and r["kb"]["embed"]["base_url"] == "http://127.0.0.1:9998/v1",
      f"->{st} {r['kb']['embed'].get('base_url')!r}")
check("embed effective.base_url = 自定义", r["kb"]["embed"]["effective"]["base_url"] == "http://127.0.0.1:9998/v1",
      f"->{r['kb']['embed']['effective'].get('base_url')!r}")

# ---------- 7) 恢复默认（全清除） ----------
st, r = req("PUT", "/settings", token, body={
    "llm": {"provider": None, "model": None, "base_url": None, "api_key": "", "temperature": None},
    "kb": {"embed": {"provider": None, "model": None, "base_url": None, "api_key": ""}},
})
check("恢复默认后 llm/base_url/embed 全 null", st == 200
      and r["llm"]["base_url"] is None and r["kb"]["embed"]["base_url"] is None
      and r["llm"]["provider"] is None and r["kb"]["embed"]["provider"] is None, f"->{st}")
check("恢复后 warning 为 null", r["llm"]["effective"]["warning"] is None
      and r["kb"]["embed"]["effective"]["warning"] is None,
      f"->{r['llm']['effective'].get('warning')!r} / {r['kb']['embed']['effective'].get('warning')!r}")

print(f"\n结果: PASS={PASS} FAIL={FAIL}")
raise SystemExit(1 if FAIL else 0)
