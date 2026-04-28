from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_db
from backend.dependencies import get_current_user, require_role
from backend.models.grade import Grade
from backend.schemas.grade import GradeCreate, GradeOut

router = APIRouter(prefix="/api/grades", tags=["Notes"])


@router.get("/student/{student_id}", response_model=List[GradeOut])
async def get_student_grades(
    student_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Récupère toutes les notes d'un élève. Accessible par l'élève lui-même, ses parents, les profs et l'admin."""
    result = await db.execute(
        select(Grade).where(Grade.student_id == student_id).order_by(Grade.graded_at.desc())
    )
    return result.scalars().all()


@router.post("/", response_model=GradeOut, status_code=status.HTTP_201_CREATED)
async def create_grade(
    payload: GradeCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_role("teacher", "admin")),
):
    """Saisie d'une note par un enseignant ou l'admin."""
    grade = Grade(**payload.model_dump(), teacher_id=current_user["user_id"])
    db.add(grade)
    await db.commit()
    await db.refresh(grade)
    return grade


@router.delete("/{grade_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_grade(
    grade_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_role("teacher", "admin")),
):
    result = await db.execute(select(Grade).where(Grade.id == grade_id))
    grade = result.scalar_one_or_none()
    if not grade:
        raise HTTPException(status_code=404, detail="Note introuvable")
    await db.delete(grade)
    await db.commit()
