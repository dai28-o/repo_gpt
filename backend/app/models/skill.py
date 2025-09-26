from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from ..core.database import Base
from .association_tables import user_skill_association


class SkillTag(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    users = relationship(
        "User",
        secondary=user_skill_association,
        back_populates="skills",
    )
