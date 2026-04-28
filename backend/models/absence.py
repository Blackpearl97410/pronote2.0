import enum
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database import Base


class AbsenceStatus(str, enum.Enum):
    PENDING = "En attente"
    JUSTIFIED = "Justifiée"
    UNJUSTIFIED = "Non justifiée"


class Absence(Base):
    __tablename__ = "absences"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    schedule_id: Mapped[int] = mapped_column(ForeignKey("schedules.id"), nullable=True)
    reported_by: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)  # enseignant ou admin

    start_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    status: Mapped[AbsenceStatus] = mapped_column(Enum(AbsenceStatus), default=AbsenceStatus.PENDING)
    reason: Mapped[str] = mapped_column(Text, nullable=True)
    justification_doc: Mapped[str] = mapped_column(String(500), nullable=True)
    is_late: Mapped[bool] = mapped_column(Boolean, default=False)  # True = retard
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    student = relationship("User", back_populates="absences", foreign_keys=[student_id])
    reporter = relationship("User", foreign_keys=[reported_by])
