from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_db
from backend.dependencies import get_current_user, require_role
from backend.models.schedule import Schedule, DayOfWeek
from pydantic import BaseModel
from typing import Optional
from datetime import time

router = APIRouter(prefix="/api/schedule", tags=["Emploi du temps"])


class ScheduleOut(BaseModel):
    id: int
    classe_id: int
    subject_id: int
    teacher_id: int
    day_of_week: DayOfWeek
    start_time: time
    end_time: time
    room: Optional[str]
    is_cancelled: bool
    cancellation_reason: Optional[str]

    model_config = {"from_attributes": True}


class ScheduleCreate(BaseModel):
    classe_id: int
    subject_id: int
    day_of_week: DayOfWeek
    start_time: time
    end_time: time
    room: Optional[str] = None


@router.get("/classe/{classe_id}", response_model=List[ScheduleOut])
async def get_classe_schedule(
    classe_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    result = await db.execute(
        select(Schedule)
        .where(Schedule.classe_id == classe_id)
        .order_by(Schedule.day_of_week, Schedule.start_time)
    )
    return result.scalars().all()


@router.post("/", response_model=ScheduleOut, status_code=status.HTTP_201_CREATED)
async def create_schedule_slot(
    payload: ScheduleCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_role("admin")),
):
    slot = Schedule(**payload.model_dump(), teacher_id=current_user["user_id"])
    db.add(slot)
    await db.commit()
    await db.refresh(slot)
    return slot
