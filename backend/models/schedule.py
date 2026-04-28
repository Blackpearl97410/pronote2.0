import enum
from datetime import date, time

from sqlalchemy import Date, Enum, ForeignKey, Integer, String, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database import Base


class DayOfWeek(str, enum.Enum):
    MONDAY = "Lundi"
    TUESDAY = "Mardi"
    WEDNESDAY = "Mercredi"
    THURSDAY = "Jeudi"
    FRIDAY = "Vendredi"
    SATURDAY = "Samedi"


class Schedule(Base):
    __tablename__ = "schedules"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    classe_id: Mapped[int] = mapped_column(ForeignKey("classes.id"), nullable=False)
    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.id"), nullable=False)
    teacher_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    day_of_week: Mapped[DayOfWeek] = mapped_column(Enum(DayOfWeek), nullable=False)
    start_time: Mapped[time] = mapped_column(Time, nullable=False)
    end_time: Mapped[time] = mapped_column(Time, nullable=False)
    room: Mapped[str] = mapped_column(String(50), nullable=True)

    # Surcharge ponctuelle (ex: cours annulé, changement de salle)
    override_date: Mapped[date] = mapped_column(Date, nullable=True)
    is_cancelled: Mapped[bool] = mapped_column(default=False)
    cancellation_reason: Mapped[str] = mapped_column(String(255), nullable=True)

    classe = relationship("Classe", back_populates="schedules")
    subject = relationship("Subject", back_populates="schedules")
    teacher = relationship("User", foreign_keys=[teacher_id])
