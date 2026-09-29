from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    email = Column(String, nullable=False)
    current_stage = Column(String, nullable=False, default="Applied")
    created_at = Column(DateTime, default=datetime.utcnow)

    history = relationship(
        "StageHistory",
        back_populates="candidate",
        cascade="all, delete-orphan"
    )


class StageHistory(Base):
    __tablename__ = "stage_history"

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(
        Integer,
        ForeignKey("candidates.id"),
        nullable=False
    )
    from_stage = Column(String, nullable=True)
    to_stage = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    candidate = relationship(
        "Candidate",
        back_populates="history"
    )