from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from backend.models.absence import AbsenceStatus


class AbsenceCreate(BaseModel):
    student_id: int
    schedule_id: Optional[int] = None
    start_at: datetime
    end_at: datetime
    is_late: bool = False
    reason: Optional[str] = None


class AbsenceJustify(BaseModel):
    reason: str
    justification_doc: Optional[str] = None


class AbsenceOut(BaseModel):
    id: int
    student_id: int
    start_at: datetime
    end_at: datetime
    status: AbsenceStatus
    reason: Optional[str]
    is_late: bool
    created_at: datetime

    model_config = {"from_attributes": True}
