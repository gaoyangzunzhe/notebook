"""进程内基础指标（线程安全：事件循环与 to_thread 双写）。

token 计数为 best-effort：能拿到 LangChain usage_metadata 就记，否则按 0。
"""
import threading
import time
from collections import Counter

_lock = threading.Lock()

_requests_total = 0
_requests_ms_total = 0.0
_status_counts: Counter = Counter()

_llm_calls = 0
_llm_errors = 0
_llm_ms_total = 0.0
_llm_tokens_total = 0

_embed_calls = 0
_embed_errors = 0
_embed_ms_total = 0.0


def record_request(path: str, status: int, ms: float) -> None:
    global _requests_total, _requests_ms_total
    with _lock:
        _requests_total += 1
        _requests_ms_total += ms
        _status_counts[status] += 1


def record_llm(ms: float, error: bool = False, usage: int | None = None) -> None:
    global _llm_calls, _llm_errors, _llm_ms_total, _llm_tokens_total
    with _lock:
        _llm_calls += 1
        _llm_ms_total += ms
        if error:
            _llm_errors += 1
        if usage:
            _llm_tokens_total += usage


def record_embed(ms: float, error: bool = False) -> None:
    global _embed_calls, _embed_errors, _embed_ms_total
    with _lock:
        _embed_calls += 1
        _embed_ms_total += ms
        if error:
            _embed_errors += 1


def snapshot() -> dict:
    """进程启动以来的聚合快照（/metrics 返回）。"""
    with _lock:
        return {
            "requests": {
                "total": _requests_total,
                "by_status": dict(_status_counts),
                "avg_ms": round(_requests_ms_total / _requests_total, 2)
                if _requests_total
                else 0.0,
            },
            "llm": {
                "calls": _llm_calls,
                "errors": _llm_errors,
                "avg_ms": round(_llm_ms_total / _llm_calls, 2) if _llm_calls else 0.0,
                "tokens_total": _llm_tokens_total,
            },
            "embed": {
                "calls": _embed_calls,
                "errors": _embed_errors,
                "avg_ms": round(_embed_ms_total / _embed_calls, 2)
                if _embed_calls
                else 0.0,
            },
            "uptime_seconds": round(time.monotonic() - _started),
        }


_started = time.monotonic()
