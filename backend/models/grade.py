import enum
from datetime import date, datetime

from sqlalchemy import Date, DateTime, Enum, Float, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database import Base


class GradeType(str, enum.Enum):
    INTERROGATION = "Interrogation"
    DEVOIR = "Devoir surveillé"
    TP = "Travaux pratiques"
    ORAL = "Oral"
    PROJET = "Projet"
    CONTROLE = "Contrôle"


class Grade(Base):
    __tablename__ = "grades"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.id"), nullable=False)
    classe_id: Mapped[int] = mapped_column(ForeignKey("classes.id"), nullable=False)
    teacher_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    value: Mapped[float] = mapped_column(Float, nullable=False)           # note obtenue
    max_value: Mapped[float] = mapped_column(Float, default=20.0)         # note max (défaut /20)
    coefficient: Mapped[float] = mapped_column(Float, default=1.0)
    grade_type: Mapped[GradeType] = mapped_column(Enum(GradeType), nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    appreciation: Mapped[str] = mapped_column(String(500), nullable=True)
    graded_at: Mapped[date] = mapped_column(Date, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    student = relationship("User", foreign_keys=[student_id])
    subject = relationship("Subject", back_populates="grades")
    classe = relationship("Classe", back_populates="grades")
    teacher = relationship("User", foreign_keys=[teacher_id])
