from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field

from ..models.user import UserRole


class SkillTag(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    role: UserRole = UserRole.PARTICIPANT


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserRead(UserBase):
    id: int
    created_at: datetime
    skills: List[SkillTag] = Field(default_factory=list)

    class Config:
        orm_mode = True
