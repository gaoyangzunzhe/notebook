"""请求上下文：request_id ContextVar（日志格式化器与中间件共用）。

独立成模块避免 logging <-> middleware 循环导入。ContextVar 可随
``asyncio.to_thread`` 传播进线程，日志格式化器在线程里也能读到。
"""
from contextvars import ContextVar

request_id_var: ContextVar[str] = ContextVar("request_id", default="-")
