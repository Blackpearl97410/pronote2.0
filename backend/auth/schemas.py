from typing import Optional

from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
    full_name: str
    user_id: int
    student_id: Optional[int] = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
