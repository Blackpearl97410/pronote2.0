from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.auth.schemas import Token
from backend.auth.utils import create_access_token, verify_password
from backend.database import get_db
from backend.models.user import User

router = APIRouter(prefix="/api/auth", tags=["Authentification"])


@router.post("/token", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(User).where(User.email == form_data.username))
    user = result.scalar_one_or_none()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect",
        )
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Compte désactivé")

    token = create_access_token(user_id=user.id, role=user.role.value)
    return Token(
        access_token=token,
        role=user.role.value,
        full_name=user.full_name,
        user_id=user.id,
        student_id=user.linked_student_id or user.id,
    )
