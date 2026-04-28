from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_db
from backend.dependencies import get_current_user, require_role
from backend.models.absence import Absence, AbsenceStatus
from backend.schemas.absence import AbsenceCreate, AbsenceJustify, AbsenceOut

router = APIRouter(prefix="/api/absences", tags=["Absences"])


@router.get("/student/{student_id}", response_model=List[AbsenceOut])
async def get_student_absences(
    student_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    result = await db.execute(
        select(Absence).where(Absence.student_id == student_id).order_by(Absence.start_at.desc())
    )
    return result.scalars().all()


@router.post("/", response_model=AbsenceOut, status_code=status.HTTP_201_CREATED)
async def report_absence(
    payload: AbsenceCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_role("teacher", "admin")),
):
    absence = Absence(**payload.model_dump(), reported_by=current_user["user_id"])
    db.add(absence)
    await db.commit()
    await db.refresh(absence)
    return absence


@router.patch("/{absence_id}/justify", response_model=AbsenceOut)
async def justify_absence(
    absence_id: int,
    payload: AbsenceJustify,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_role("parent", "admin")),
):
    result = await db.execute(select(Absence).where(Absence.id == absence_id))
    absence = result.scalar_one_or_none()
    if not absence:
        raise HTTPException(status_code=404, detail="Absence introuvable")

    absence.reason = payload.reason
    absence.justification_doc = payload.justification_doc
    absence.status = AbsenceStatus.JUSTIFIED
    await db.commit()
    await db.refresh(absence)
    return absence
