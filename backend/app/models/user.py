from datetime import datetime
from enum import Enum
from typing import List

from sqlalchemy import Column, DateTime, Enum as SAEnum, Integer, String
from sqlalchemy.orm import relationship

from ..core.database import Base
from .association_tables import user_skill_association


class UserRole(str, Enum):
    PARTICIPANT = "participant"
    ORGANIZER = "organizer"
    ADMIN = "admin"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    role = Column(SAEnum(UserRole), default=UserRole.PARTICIPANT, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    events = relationship("Event", back_populates="organizer")
    enrollments = relationship("Enrollment", back_populates="user")
    feedback = relationship("Feedback", back_populates="author")
    skills: List['SkillTag'] = relationship(
        "SkillTag",
        secondary=user_skill_association,
        back_populates="users",
    )
