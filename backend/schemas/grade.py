from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field

from backend.models.grade import GradeType


class GradeCreate(BaseModel):
    student_id: int
    subject_id: int
    classe_id: int
    value: float = Field(..., ge=0, le=20)
    max_value: float = Field(20.0, ge=1)
    coefficient: float = Field(1.0, ge=0)
    grade_type: GradeType
    title: str
    appreciation: Optional[str] = None
    graded_at: date


class GradeOut(BaseModel):
    id: int
    student_id: int
    subject_id: int
    value: float
    max_value: float
    coefficient: float
    grade_type: GradeType
    title: str
    appreciation: Optional[str]
    graded_at: date
    created_at: datetime

    model_config = {"from_attributes": True}
