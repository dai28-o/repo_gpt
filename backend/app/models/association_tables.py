from sqlalchemy import Column, ForeignKey, Integer, Table

from ..core.database import Base


user_skill_association = Table(
    "user_skill_association",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE")),
    Column("skill_id", Integer, ForeignKey("skills.id", ondelete="CASCADE")),
)
