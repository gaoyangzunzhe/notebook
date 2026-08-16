"""注册 / 登录 / 当前用户 / 资料维护（用户名、密码、头像）。"""
import asyncio
import base64
from io import BytesIO

from fastapi import APIRouter, Depends, File, HTTPException, Response, UploadFile
from PIL import Image, ImageOps
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_settings
from app.core.config import Settings
from app.core.security import create_access_token, hash_password, verify_password
from app.db.session import get_db
from app.models import User
from app.schemas.auth import (
    LoginRequest,
    PasswordChange,
    RegisterRequest,
    TokenResponse,
    UsernameUpdate,
    UserOut,
)

router = APIRouter(prefix="/auth", tags=["auth"])

# 账号不存在时也做一次 bcrypt 校验，拉平时序，避免暴露账号是否存在
_DUMMY_HASH = hash_password("timing-equalizer")

_MAX_AVATAR_BYTES = 5 * 1024 * 1024


async def _require_db(db_session: AsyncSession | None) -> AsyncSession:
    if db_session is None:
        raise HTTPException(status_code=503, detail="认证服务不可用：数据库未配置")
    return db_session


@router.post("/register", response_model=UserOut, status_code=201)
async def register(
    body: RegisterRequest,
    db_session: AsyncSession | None = Depends(get_db),
) -> UserOut:
    session = await _require_db(db_session)
    try:
        async with asyncio.timeout(5):
            dup_user = await session.execute(
                select(User.id).where(User.username == body.username)
            )
            dup_email = await session.execute(
                select(User.id).where(func.lower(User.email) == body.email.lower())
            )
        if dup_user.scalar_one_or_none() is not None:
            raise HTTPException(status_code=409, detail="用户名已存在")
        if dup_email.scalar_one_or_none() is not None:
            raise HTTPException(status_code=409, detail="邮箱已被使用")

        user = User(
            username=body.username,
            email=body.email,
            hashed_password=hash_password(body.password),
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return UserOut.model_validate(user)
    except HTTPException:
        raise
    except IntegrityError:
        await session.rollback()
        raise HTTPException(status_code=409, detail="用户名或邮箱已存在")
    except (SQLAlchemyError, TimeoutError):
        await session.rollback()
        raise HTTPException(status_code=503, detail="认证服务不可用：数据库连接失败")


@router.post("/login", response_model=TokenResponse)
async def login(
    body: LoginRequest,
    db_session: AsyncSession | None = Depends(get_db),
    settings: Settings = Depends(get_settings),
) -> TokenResponse:
    session = await _require_db(db_session)
    try:
        async with asyncio.timeout(5):
            if "@" in body.account:
                result = await session.execute(
                    select(User).where(func.lower(User.email) == body.account.lower())
                )
            else:
                result = await session.execute(
                    select(User).where(User.username == body.account)
                )
        user = result.scalar_one_or_none()
        # 统一错误提示（不暴露是账号不存在还是密码错误）
        if user is None:
            verify_password(body.password, _DUMMY_HASH)
            raise HTTPException(status_code=401, detail="账号或密码错误")
        if not verify_password(body.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="账号或密码错误")

        token = create_access_token(user.id, user.username, settings)
        return TokenResponse(access_token=token)
    except HTTPException:
        raise
    except (SQLAlchemyError, TimeoutError):
        raise HTTPException(status_code=503, detail="认证服务不可用：数据库连接失败")


@router.get("/me", response_model=UserOut)
async def me(current_user: User = Depends(get_current_user)) -> UserOut:
    return UserOut.model_validate(current_user)


@router.patch("/me", response_model=UserOut)
async def update_username(
    body: UsernameUpdate,
    db_session: AsyncSession | None = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> UserOut:
    session = await _require_db(db_session)
    try:
        async with asyncio.timeout(5):
            dup = await session.execute(
                select(User.id).where(
                    User.username == body.username, User.id != current_user.id
                )
            )
        if dup.scalar_one_or_none() is not None:
            raise HTTPException(status_code=409, detail="用户名已存在")
        current_user.username = body.username
        await session.commit()
        await session.refresh(current_user)
        # JWT 里的 username 快照会过期，但 get_current_user 按 sub 重查用户，无碍
        return UserOut.model_validate(current_user)
    except HTTPException:
        raise
    except (SQLAlchemyError, TimeoutError):
        await session.rollback()
        raise HTTPException(status_code=503, detail="数据库连接失败")


@router.post("/password", status_code=204)
async def change_password(
    body: PasswordChange,
    db_session: AsyncSession | None = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Response:
    session = await _require_db(db_session)
    if not verify_password(body.old_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="当前密码不正确")
    try:
        current_user.hashed_password = hash_password(body.new_password)
        await session.commit()
        return Response(status_code=204)
    except SQLAlchemyError:
        await session.rollback()
        raise HTTPException(status_code=503, detail="数据库连接失败")


@router.post("/avatar", response_model=UserOut)
async def upload_avatar(
    file: UploadFile = File(...),
    db_session: AsyncSession | None = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> UserOut:
    session = await _require_db(db_session)
    if file.content_type and not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="仅支持图片文件")
    data = await file.read()
    if len(data) > _MAX_AVATAR_BYTES:
        raise HTTPException(status_code=400, detail="图片过大（最大 5MB）")
    try:
        img = Image.open(BytesIO(data))
        img = ImageOps.exif_transpose(img)  # 按 EXIF 方向纠正
        img.thumbnail((256, 256), Image.Resampling.LANCZOS)
        if img.mode != "RGB":
            img = img.convert("RGB")
        buf = BytesIO()
        img.save(buf, format="JPEG", quality=85)
        b64 = base64.b64encode(buf.getvalue()).decode("ascii")
        current_user.avatar = f"data:image/jpeg;base64,{b64}"
        await session.commit()
        await session.refresh(current_user)
        return UserOut.model_validate(current_user)
    except HTTPException:
        raise
    except Exception:  # noqa: BLE001  Pillow 解析失败 / 写库失败统一提示
        await session.rollback()
        raise HTTPException(status_code=400, detail="图片处理失败，请换一张图片")


@router.delete("/avatar", status_code=204)
async def delete_avatar(
    db_session: AsyncSession | None = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Response:
    session = await _require_db(db_session)
    try:
        current_user.avatar = None
        await session.commit()
        return Response(status_code=204)
    except SQLAlchemyError:
        await session.rollback()
        raise HTTPException(status_code=503, detail="数据库连接失败")
