from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database import Base


class Subject(Base):
    __tablename__ = "subjects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)       # ex: "Mathématiques"
    code: Mapped[str] = mapped_column(String(10), nullable=False)        # ex: "MATH"
    coefficient: Mapped[float] = mapped_column(default=1.0)

    schedules = relationship("Schedule", back_populates="subject")
    grades = relationship("Grade", back_populates="subject")
    homeworks = relationship("Homework", back_populates="subject")
