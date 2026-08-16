"""认证相关出入参模型。"""
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field, model_validator


class RegisterRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=20, pattern=r"^[A-Za-z0-9_]+$")
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=72)  # 72 = bcrypt 字节上限
    confirm_password: str

    @model_validator(mode="after")
    def _passwords_match(self) -> "RegisterRequest":
        if self.password != self.confirm_password:
            raise ValueError("两次输入的密码不一致")
        return self


class LoginRequest(BaseModel):
    account: str = Field(..., min_length=1, max_length=255)  # 用户名或邮箱
    password: str


class UsernameUpdate(BaseModel):
    username: str = Field(..., min_length=3, max_length=20, pattern=r"^[A-Za-z0-9_]+$")


class PasswordChange(BaseModel):
    old_password: str
    new_password: str = Field(..., min_length=6, max_length=72)
    confirm_password: str

    @model_validator(mode="after")
    def _passwords_match(self) -> "PasswordChange":
        if self.new_password != self.confirm_password:
            raise ValueError("两次输入的新密码不一致")
        return self


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: str
    avatar: str | None = None  # data URL（data:image/jpeg;base64,…）
    created_at: datetime
