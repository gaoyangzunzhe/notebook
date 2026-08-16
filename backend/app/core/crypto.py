"""对称加密：用户级 API Key 的 Fernet 加解密。

密钥由 settings.secret_key 确定性派生（sha256 -> urlsafe_b64encode），
不额外落盘密钥文件。注意：轮换 SECRET_KEY 会使已加密的 key 无法解密
（decrypt_secret 捕获 InvalidToken 返回 None，调用方回退全局 .env key）。
"""

import base64
import hashlib
import logging

from cryptography.fernet import Fernet, InvalidToken

from app.core.config import Settings

logger = logging.getLogger(__name__)


def _fernet(settings: Settings) -> Fernet:
    digest = hashlib.sha256(settings.secret_key.encode("utf-8")).digest()
    key = base64.urlsafe_b64encode(digest)
    return Fernet(key)


def encrypt_secret(settings: Settings, plain: str) -> str:
    """加密明文字符串，返回 Fernet token（str）。"""
    return _fernet(settings).encrypt(plain.encode("utf-8")).decode("utf-8")


def decrypt_secret(settings: Settings, token: str) -> str | None:
    """解密 Fernet token；SECRET_KEY 已轮换等导致失败时返回 None（不回抛，不泄漏明文）。"""
    try:
        return _fernet(settings).decrypt(token.encode("utf-8")).decode("utf-8")
    except InvalidToken:
        logger.warning("API Key 解密失败（SECRET_KEY 可能已轮换），回退全局默认。")
        return None
