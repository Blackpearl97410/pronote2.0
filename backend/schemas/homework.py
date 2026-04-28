from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel


class HomeworkCreate(BaseModel):
    subject_id: int
    classe_id: int
    title: str
    description: Optional[str] = None
    due_date: date
    is_graded: bool = False
    attachment_url: Optional[str] = None


class HomeworkOut(BaseModel):
    id: int
    subject_id: int
    classe_id: int
    teacher_id: int
    title: str
    description: Optional[str]
    due_date: date
    is_graded: bool
    attachment_url: Optional[str]
    created_at: datetime

    model_config = {"from_attributes": True}
