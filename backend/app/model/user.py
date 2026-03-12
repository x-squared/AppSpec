from sqlalchemy import Column, ForeignKey, Integer, String, Table, Text, UniqueConstraint
from sqlalchemy.orm import relationship

from ..database import Base

user_role_table = Table(
    "USER_ROLE",
    Base.metadata,
    Column("USER_ID", Integer, ForeignKey("USER.ID"), primary_key=True),
    Column("ROLE_ID", Integer, ForeignKey("CODE.ID"), primary_key=True),
    UniqueConstraint("USER_ID", "ROLE_ID"),
)


class User(Base):
    """Application user used for authentication, role assignment, and auditing."""

    __tablename__ = "USER"

    id = Column(
        "ID",
        Integer,
        primary_key=True,
        index=True,
        comment="Technical primary key of the user.",
        info={"label": "ID"},
    )
    ext_id = Column(
        "EXT_ID",
        String,
        nullable=False,
        unique=True,
        comment="External identity of the user used for login mapping.",
        info={"label": "External ID"},
    )
    person_id = Column(
        "PERSON_ID",
        Integer,
        ForeignKey("PERSON.ID"),
        nullable=False,
        unique=True,
        index=True,
        comment="Required linked person record providing canonical user person data.",
        info={"label": "Person"},
    )
    name = Column(
        "NAME",
        String,
        nullable=False,
        comment="Display name of the user.",
        info={"label": "Name"},
    )
    role_id = Column(
        "ROLE",
        Integer,
        ForeignKey("CODE.ID"),
        nullable=True,
        comment="Assigned role code (`CODE.ROLE`) of the user.",
        info={"label": "User Role"},
    )
    preferences_json = Column(
        "PREFERENCES_JSON",
        Text,
        nullable=True,
        comment="User-specific UI preferences as JSON.",
        info={"label": "Preferences JSON"},
    )

    role = relationship("Code", foreign_keys=[role_id])
    roles = relationship("Code", secondary=user_role_table)
    person = relationship("Person", foreign_keys=[person_id], back_populates="user")
    assigned_tasks = relationship("Task", foreign_keys="Task.assigned_to_id", back_populates="assigned_to")
    closed_tasks = relationship("Task", foreign_keys="Task.closed_by_id", back_populates="closed_by")

    @property
    def role_ids(self) -> list[int]:
        ids = [role.id for role in (self.roles or []) if role and role.id is not None]
        if self.role_id is not None and self.role_id not in ids:
            ids.append(self.role_id)
        return ids
