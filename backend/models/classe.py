from sqlalchemy import ForeignKey, Integer, String, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database import Base

# Table d'association élèves <-> classes
student_classe = Table(
    "student_classe",
    Base.metadata,
    Column("student_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("classe_id", Integer, ForeignKey("classes.id"), primary_key=True),
)


class Classe(Base):
    __tablename__ = "classes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)        # ex: "3ème A"
    level: Mapped[str] = mapped_column(String(50), nullable=False)       # ex: "3ème"
    school_year: Mapped[str] = mapped_column(String(10), nullable=False) # ex: "2025-2026"

    students = relationship("User", secondary=student_classe, backref="classes")
    schedules = relationship("Schedule", back_populates="classe")
    grades = relationship("Grade", back_populates="classe")
    bulletins = relationship("Bulletin", back_populates="classe")
