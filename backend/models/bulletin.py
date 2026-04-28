import enum
from datetime import datetime

from sqlalchemy import Enum, Float, ForeignKey, Integer, String, Text, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database import Base


class Trimester(str, enum.Enum):
    T1 = "Trimestre 1"
    T2 = "Trimestre 2"
    T3 = "Trimestre 3"


class Bulletin(Base):
    __tablename__ = "bulletins"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    classe_id: Mapped[int] = mapped_column(ForeignKey("classes.id"), nullable=False)

    trimester: Mapped[Trimester] = mapped_column(Enum(Trimester), nullable=False)
    school_year: Mapped[str] = mapped_column(String(10), nullable=False)
    general_average: Mapped[float] = mapped_column(Float, nullable=True)
    class_average: Mapped[float] = mapped_column(Float, nullable=True)
    rank: Mapped[int] = mapped_column(Integer, nullable=True)
    general_appreciation: Mapped[str] = mapped_column(Text, nullable=True)
    council_decision: Mapped[str] = mapped_column(String(200), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    student = relationship("User", foreign_keys=[student_id])
    classe = relationship("Classe", back_populates="bulletins")
    subject_reports = relationship("SubjectReport", back_populates="bulletin")


class SubjectReport(Base):
    """Ligne de bulletin par matière."""
    __tablename__ = "subject_reports"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    bulletin_id: Mapped[int] = mapped_column(ForeignKey("bulletins.id"), nullable=False)
    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.id"), nullable=False)
    teacher_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    average: Mapped[float] = mapped_column(Float, nullable=True)
    class_average: Mapped[float] = mapped_column(Float, nullable=True)
    appreciation: Mapped[str] = mapped_column(Text, nullable=True)

    bulletin = relationship("Bulletin", back_populates="subject_reports")
    subject = relationship("Subject", foreign_keys=[subject_id])
    teacher = relationship("User", foreign_keys=[teacher_id])
