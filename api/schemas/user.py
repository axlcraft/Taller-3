from pydantic import BaseModel
import uuid

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserUpdate(BaseModel):
    username: str | None = None   # ✅ corregido
    password: str | None = None

class UserResponse(UserBase):
    id: uuid.UUID   # ✅ UUID correcto

    class Config:
        from_attributes = True
