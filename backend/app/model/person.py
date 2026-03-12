from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..database import Base

person_team_member_table = Table(
    "PERSON_TEAM_MEMBER",
    Base.metadata,
    Column("PERSON_ID", Integer, ForeignKey("PERSON.ID"), primary_key=True),
    Column("TEAM_ID", Integer, ForeignKey("PERSON_TEAM.ID"), primary_key=True),
    UniqueConstraint("PERSON_ID", "TEAM_ID"),
)


class Person(Base):
    """Person reference for colloquium participants and team grouping."""

    __tablename__ = "PERSON"

    id = Column(
        "ID",
        Integer,
        primary_key=True,
        index=True,
        comment="Technical primary key of the person.",
        info={"label": "ID"},
    )
    first_name = Column(
        "FIRST_NAME",
        String(128),
        nullable=False,
        comment="Given name of the person.",
        info={"label": "First Name"},
    )
    surname = Column(
        "SURNAME",
        String(128),
        nullable=False,
        comment="Family name of the person.",
        info={"label": "Surname"},
    )
    user_id = Column(
        "USER_ID",
        String(12),
        unique=True,
        nullable=True,
        index=True,
        comment="Optional external employee/user identifier.",
        info={"label": "User ID"},
    )
    changed_by_id = Column(
        "CHANGED_BY",
        Integer,
        ForeignKey("USER.ID"),
        nullable=True,
        comment="Last user who changed the person.",
        info={"label": "Changed By"},
    )
    created_by_id = Column(
        "CREATED_BY",
        Integer,
        ForeignKey("USER.ID"),
        nullable=True,
        comment="User who created the person.",
        info={"label": "Created By"},
    )
    created_at = Column(
        "CREATED_AT",
        DateTime(timezone=True),
        server_default=func.now(),
        comment="Creation timestamp of the person row.",
        info={"label": "Created At"},
    )
    updated_at = Column(
        "UPDATED_AT",
        DateTime(timezone=True),
        onupdate=func.now(),
        comment="Last update timestamp of the person row.",
        info={"label": "Updated At"},
    )

    changed_by_user = relationship("User", foreign_keys=[changed_by_id])
    created_by_user = relationship("User", foreign_keys=[created_by_id])
    user = relationship("User", back_populates="person", foreign_keys="User.person_id", uselist=False)
    teams = relationship("PersonTeam", secondary=person_team_member_table, back_populates="members")


class PersonTeam(Base):
    """Named team containing people."""

    __tablename__ = "PERSON_TEAM"

    id = Column(
        "ID",
        Integer,
        primary_key=True,
        index=True,
        comment="Technical primary key of the person team.",
        info={"label": "ID"},
    )
    name = Column(
        "NAME",
        String(128),
        nullable=False,
        unique=True,
        index=True,
        comment="Display name of the team.",
        info={"label": "Name"},
    )
    changed_by_id = Column(
        "CHANGED_BY",
        Integer,
        ForeignKey("USER.ID"),
        nullable=True,
        comment="Last user who changed the team.",
        info={"label": "Changed By"},
    )
    created_by_id = Column(
        "CREATED_BY",
        Integer,
        ForeignKey("USER.ID"),
        nullable=True,
        comment="User who created the team.",
        info={"label": "Created By"},
    )
    created_at = Column(
        "CREATED_AT",
        DateTime(timezone=True),
        server_default=func.now(),
        comment="Creation timestamp of the person team row.",
        info={"label": "Created At"},
    )
    updated_at = Column(
        "UPDATED_AT",
        DateTime(timezone=True),
        onupdate=func.now(),
        comment="Last update timestamp of the person team row.",
        info={"label": "Updated At"},
    )

    changed_by_user = relationship("User", foreign_keys=[changed_by_id])
    created_by_user = relationship("User", foreign_keys=[created_by_id])
    members = relationship("Person", secondary=person_team_member_table, back_populates="teams")
