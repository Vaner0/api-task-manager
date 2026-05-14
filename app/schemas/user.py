from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserCreate(BaseModel):
    nom: str
    email: EmailStr
    mot_de_passe: str


class UserResponse(BaseModel):
    id: int
    nom: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    email: EmailStr
    mot_de_passe: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"