"""建表逻辑：幂等迁移 + create_all，失败只告警不崩溃。"""
import logging

from sqlalchemy import text

import app.models  # noqa: F401  确保 ORM 模型注册到 Base.metadata
from app.core.config import Settings
from app.db import session
from app.db.base import Base

logger = logging.getLogger(__name__)

# 为历史表补 user_id 列的幂等迁移（to_regclass 判断表存在才执行）：
# 新库空表直接跳过迁移，由 create_all 按模型建表；老库补列补索引，非破坏性。
# users 迁移顺序必须是：加列 -> 回填邮箱 -> SET NOT NULL -> 建唯一索引
#（先 NOT NULL 会因存量 NULL 行失败；create_all 对已有表跳过，索引只能在此建）。
_MIGRATIONS = [
    text(
        """
        DO $mig$
        BEGIN
            IF to_regclass('public.documents') IS NOT NULL THEN
                ALTER TABLE documents ADD COLUMN IF NOT EXISTS user_id INTEGER;
                CREATE INDEX IF NOT EXISTS ix_documents_user_id ON documents (user_id);
                ALTER TABLE documents ADD COLUMN IF NOT EXISTS stored_name VARCHAR(255);
            END IF;
            IF to_regclass('public.chat_messages') IS NOT NULL THEN
                ALTER TABLE chat_messages ADD COLUMN IF NOT EXISTS user_id INTEGER;
                CREATE INDEX IF NOT EXISTS ix_chat_messages_user_id ON chat_messages (user_id);
            END IF;
            IF to_regclass('public.users') IS NOT NULL THEN
                ALTER TABLE users ADD COLUMN IF NOT EXISTS email VARCHAR(255);
                ALTER TABLE users ADD COLUMN IF NOT EXISTS avatar TEXT;
                -- 回填用原始 username（而非小写）：username 本身唯一，直接拼 @local.invalid 不撞车
                UPDATE users SET email = username || '@local.invalid' WHERE email IS NULL;
                ALTER TABLE users ALTER COLUMN email SET NOT NULL;
                CREATE UNIQUE INDEX IF NOT EXISTS uq_users_email ON users (email);
            END IF;
            IF to_regclass('public.user_settings') IS NOT NULL THEN
                ALTER TABLE user_settings ADD COLUMN IF NOT EXISTS embed_provider VARCHAR(32);
                ALTER TABLE user_settings ADD COLUMN IF NOT EXISTS embed_model VARCHAR(64);
                ALTER TABLE user_settings ADD COLUMN IF NOT EXISTS embed_api_key_encrypted VARCHAR(512);
            END IF;
        END
        $mig$
        """
    ),
    # 架构重构：去掉 Notebook 概念 + 知识库分类。
    # 破坏性不可逆（DROP notebooks/note_documents），笔记内容全部保留。
    text(
        """
        DO $mig$
        BEGIN
            DROP TABLE IF EXISTS note_documents;
            DROP TABLE IF EXISTS notebooks;
            IF to_regclass('public.notes') IS NOT NULL THEN
                ALTER TABLE notes DROP COLUMN IF EXISTS notebook_id;  -- 连带删 ix_notes_notebook_id
            END IF;
            IF to_regclass('public.documents') IS NOT NULL THEN
                ALTER TABLE documents ADD COLUMN IF NOT EXISTS category VARCHAR(50) NOT NULL DEFAULT '未分类';
            END IF;
            IF to_regclass('public.user_settings') IS NOT NULL THEN
                ALTER TABLE user_settings ADD COLUMN IF NOT EXISTS doc_categories TEXT DEFAULT '[]';
            END IF;
        END
        $mig$
        """
    ),
    # 模型配置重构：env 统一前缀 + 设置页支持自定义接口地址（网关/代理）。
    text(
        """
        DO $mig$
        BEGIN
            IF to_regclass('public.user_settings') IS NOT NULL THEN
                ALTER TABLE user_settings ADD COLUMN IF NOT EXISTS llm_base_url VARCHAR(256);
                ALTER TABLE user_settings ADD COLUMN IF NOT EXISTS embed_base_url VARCHAR(256);
            END IF;
        END
        $mig$
        """
    ),
]


async def init_db(settings: Settings) -> bool:
    """先跑幂等迁移，再 create_all 建缺失的表。返回是否成功；失败返回 False。"""
    engine = session.get_engine()
    if engine is None:
        logger.info("数据库未配置，跳过建表。")
        return False
    try:
        async with engine.begin() as conn:
            for stmt in _MIGRATIONS:
                await conn.execute(stmt)
            await conn.run_sync(Base.metadata.create_all)
        logger.info("数据库 schema 已就绪。")
        return True
    except Exception as e:  # noqa: BLE001
        logger.warning("数据库建表失败（应用继续以无 DB 模式运行）：%s", e)
        return False
