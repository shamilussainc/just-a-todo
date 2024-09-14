from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, EmailStr, SecretStr


class UserBase(BaseModel):
    username: str = Field(max_length=62)
    email: EmailStr


class UserCreate(UserBase):
    password: SecretStr


class UserOut(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    is_active: bool = True
    created_at: datetime
    updated_at: datetime


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    username: str | None = None
