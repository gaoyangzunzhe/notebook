"""密码哈希（bcrypt）与 JWT 编解码（PyJWT）。"""
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

from app.core.config import Settings


def hash_password(plain: str) -> str:
    """bcrypt 哈希；自动加盐。"""
    return bcrypt.hashpw(plain.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))
    except ValueError:
        # bcrypt 对 >72 字节口令抛 ValueError，按不匹配处理
        return False


def create_access_token(user_id: int, username: str, settings: Settings) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes
    )
    payload = {"sub": str(user_id), "username": username, "exp": expire}
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)


def decode_access_token(token: str, settings: Settings) -> dict:
    """解码并校验签名/过期。

    失败抛 jwt.ExpiredSignatureError / jwt.InvalidTokenError（由调用方转 401）。
    """
    return jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
