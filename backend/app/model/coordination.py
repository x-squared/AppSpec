from sqlalchemy import Boolean, Column, Date, DateTime, Enum as SqlEnum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..database import Base
from ..enums import CoordinationStatusKey


class Coordination(Base):
    """Core coordination entity, extensible via future 1:1 organ-specific tables."""

    __tablename__ = "COORDINATION"

    id = Column(
        "ID",
        Integer,
        primary_key=True,
        index=True,
        comment="Technical primary key of the coordination row.",
        info={"label": "ID"},
    )
    start = Column(
        "START",
        Date,
        nullable=True,
        comment="Start date of the coordination process.",
        info={"label": "Start"},
    )
    end = Column(
        "END",
        Date,
        nullable=True,
        comment="End date of the coordination process.",
        info={"label": "End"},
    )
    status_id = Column(
        "STATUS",
        Integer,
        ForeignKey("CODE.ID"),
        nullable=False,
        comment="Status reference (`CODE.COORDINATION_STATUS`).",
        info={"label": "Status"},
    )
    status_key = Column(
        "STATUS_KEY",
        SqlEnum(
            CoordinationStatusKey,
            native_enum=False,
            validate_strings=True,
            values_callable=lambda enum_cls: [entry.value for entry in enum_cls],
            length=16,
        ),
        nullable=True,
        comment="Status enum key mirror of `status_id`.",
        info={"label": "Status Key"},
    )
    donor_nr = Column(
        "DONOR_NR",
        String(12),
        default="",
        comment="Donor number (max 12 characters).",
        info={"label": "Donor Nr"},
    )
    swtpl_nr = Column(
        "SWTPL_NR",
        String(8),
        default="",
        comment="Swiss transplant number (max 8 characters).",
        info={"label": "SWTPL Nr"},
    )
    national_coordinator = Column(
        "NATIONAL_COORDINATOR",
        String(64),
        default="",
        comment="National coordinator name (max 64 characters).",
        info={"label": "National Coordinator"},
    )
    comment = Column(
        "COMMENT",
        String(1024),
        default="",
        comment="Free-text comment (max 1024 characters).",
        info={"label": "Comment"},
    )
    completion_confirmed = Column(
        "COMPLETION_CONFIRMED",
        Boolean,
        nullable=False,
        default=False,
        comment="Whether final coordination completion has been confirmed.",
        info={"label": "Completion Confirmed"},
    )
    completion_comment = Column(
        "COMPLETION_COMMENT",
        String(1024),
        default="",
        comment="Completion confirmation comment.",
        info={"label": "Completion Comment"},
    )
    completion_confirmed_at = Column(
        "COMPLETION_CONFIRMED_AT",
        DateTime(timezone=True),
        nullable=True,
        comment="Timestamp when completion was confirmed.",
        info={"label": "Completion Confirmed At"},
    )
    completion_confirmed_by_id = Column(
        "COMPLETION_CONFIRMED_BY",
        Integer,
        ForeignKey("USER.ID"),
        nullable=True,
        comment="User who confirmed completion.",
        info={"label": "Completion Confirmed By"},
    )
    changed_by_id = Column(
        "CHANGED_BY",
        Integer,
        ForeignKey("USER.ID"),
        nullable=True,
        comment="Last user who changed the coordination row.",
        info={"label": "Changed By"},
    )
    created_by_id = Column(
        "CREATED_BY",
        Integer,
        ForeignKey("USER.ID"),
        nullable=True,
        comment="User who created the coordination row.",
        info={"label": "Created By"},
    )
    created_at = Column(
        "CREATED_AT",
        DateTime(timezone=True),
        server_default=func.now(),
        comment="Creation timestamp of the coordination row.",
        info={"label": "Created At"},
    )
    updated_at = Column(
        "UPDATED_AT",
        DateTime(timezone=True),
        onupdate=func.now(),
        comment="Last update timestamp of the coordination row.",
        info={"label": "Updated At"},
    )

    status = relationship("Code", foreign_keys=[status_id])
    changed_by_user = relationship("User", foreign_keys=[changed_by_id])
    created_by_user = relationship("User", foreign_keys=[created_by_id])
    completion_confirmed_by_user = relationship("User", foreign_keys=[completion_confirmed_by_id])
    donor = relationship(
        "CoordinationDonor",
        back_populates="coordination",
        uselist=False,
        cascade="all, delete-orphan",
    )
    origin = relationship(
        "CoordinationOrigin",
        back_populates="coordination",
        uselist=False,
        cascade="all, delete-orphan",
    )
    procurement = relationship(
        "CoordinationProcurement",
        back_populates="coordination",
        uselist=False,
        cascade="all, delete-orphan",
    )
    coordination_episodes = relationship(
        "CoordinationEpisode",
        back_populates="coordination",
        cascade="all, delete-orphan",
    )
    time_logs = relationship(
        "CoordinationTimeLog",
        back_populates="coordination",
        cascade="all, delete-orphan",
    )
    organ_effects = relationship(
        "CoordinationOrganEffect",
        back_populates="coordination",
        cascade="all, delete-orphan",
    )
    protocol_event_logs = relationship(
        "CoordinationProtocolEventLog",
        back_populates="coordination",
        cascade="all, delete-orphan",
    )
    task_groups = relationship(
        "TaskGroup",
        back_populates="coordination",
        cascade="all, delete-orphan",
    )


class CoordinationProtocolEventLog(Base):
    """Per-organ protocol event log entries for a coordination case."""

    __tablename__ = "COORDINATION_PROTOCOL_EVENT_LOG"

    id = Column("ID", Integer, primary_key=True, index=True)
    coordination_id = Column("COORDINATION_ID", Integer, ForeignKey("COORDINATION.ID"), nullable=False, index=True)
    organ_id = Column("ORGAN_ID", Integer, ForeignKey("CODE.ID"), nullable=False, index=True)
    event = Column("EVENT", String(128), nullable=False, default="")
    time = Column("TIME", DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    task_id = Column("TASK_ID", Integer, ForeignKey("TASK.ID"), nullable=True, index=True)
    task_text = Column("TASK_TEXT", String(512), nullable=True)
    task_comment = Column("TASK_COMMENT", String(512), nullable=True)
    changed_by_id = Column("CHANGED_BY", Integer, ForeignKey("USER.ID"), nullable=True)
    created_by_id = Column("CREATED_BY", Integer, ForeignKey("USER.ID"), nullable=True)
    created_at = Column("CREATED_AT", DateTime(timezone=True), server_default=func.now())
    updated_at = Column("UPDATED_AT", DateTime(timezone=True), onupdate=func.now())

    coordination = relationship("Coordination", back_populates="protocol_event_logs")
    organ = relationship("Code", foreign_keys=[organ_id])
    task = relationship("Task", foreign_keys=[task_id])
    changed_by_user = relationship("User", foreign_keys=[changed_by_id])
    created_by_user = relationship("User", foreign_keys=[created_by_id])
