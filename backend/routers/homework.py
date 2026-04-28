from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_db
from backend.dependencies import get_current_user, require_role
from backend.models.homework import Homework
from backend.schemas.homework import HomeworkCreate, HomeworkOut

router = APIRouter(prefix="/api/homework", tags=["Cahier de textes"])


@router.get("/classe/{classe_id}", response_model=List[HomeworkOut])
async def get_classe_homework(
    classe_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    result = await db.execute(
        select(Homework)
        .where(Homework.classe_id == classe_id)
        .order_by(Homework.due_date.asc())
    )
    return result.scalars().all()


@router.post("/", response_model=HomeworkOut, status_code=status.HTTP_201_CREATED)
async def create_homework(
    payload: HomeworkCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_role("teacher", "admin")),
):
    hw = Homework(**payload.model_dump(), teacher_id=current_user["user_id"])
    db.add(hw)
    await db.commit()
    await db.refresh(hw)
    return hw


@router.delete("/{homework_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_homework(
    homework_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_role("teacher", "admin")),
):
    result = await db.execute(select(Homework).where(Homework.id == homework_id))
    hw = result.scalar_one_or_none()
    if not hw:
        raise HTTPException(status_code=404, detail="Devoir introuvable")
    await db.delete(hw)
    await db.commit()
