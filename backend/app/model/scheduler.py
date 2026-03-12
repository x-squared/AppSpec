from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..database import Base


class ScheduledJob(Base):
    __tablename__ = "SCHEDULED_JOB"
    __table_args__ = (UniqueConstraint("JOB_KEY"),)

    id = Column("ID", Integer, primary_key=True, index=True)
    job_key = Column("JOB_KEY", String(128), nullable=False)
    name = Column("NAME", String(256), nullable=False, default="")
    description = Column("DESCRIPTION", String(1024), nullable=False, default="")
    is_enabled = Column("IS_ENABLED", Boolean, nullable=False, default=True)
    interval_seconds = Column("INTERVAL_SECONDS", Integer, nullable=False, default=900)
    next_run_at = Column("NEXT_RUN_AT", DateTime(timezone=True), nullable=True)
    max_retries = Column("MAX_RETRIES", Integer, nullable=False, default=0)
    retry_delay_seconds = Column("RETRY_DELAY_SECONDS", Integer, nullable=False, default=60)
    last_started_at = Column("LAST_STARTED_AT", DateTime(timezone=True), nullable=True)
    last_finished_at = Column("LAST_FINISHED_AT", DateTime(timezone=True), nullable=True)
    last_status = Column("LAST_STATUS", String(32), nullable=True)
    changed_by_id = Column("CHANGED_BY", Integer, ForeignKey("USER.ID"), nullable=True)
    created_by_id = Column("CREATED_BY", Integer, ForeignKey("USER.ID"), nullable=True)
    created_at = Column("CREATED_AT", DateTime(timezone=True), server_default=func.now())
    updated_at = Column("UPDATED_AT", DateTime(timezone=True), onupdate=func.now())

    changed_by_user = relationship("User", foreign_keys=[changed_by_id])
    created_by_user = relationship("User", foreign_keys=[created_by_id])
    runs = relationship("ScheduledJobRun", back_populates="job", cascade="all, delete-orphan")


class ScheduledJobRun(Base):
    __tablename__ = "SCHEDULED_JOB_RUN"

    id = Column("ID", Integer, primary_key=True, index=True)
    job_id = Column("JOB_ID", Integer, ForeignKey("SCHEDULED_JOB.ID"), nullable=False, index=True)
    trigger_type = Column("TRIGGER_TYPE", String(32), nullable=False)
    status = Column("STATUS", String(32), nullable=False)
    attempt = Column("ATTEMPT", Integer, nullable=False, default=1)
    correlation_id = Column("CORRELATION_ID", String(128), nullable=False, default="")
    summary = Column("SUMMARY", String(1024), nullable=False, default="")
    error_text = Column("ERROR_TEXT", String(4096), nullable=False, default="")
    metrics_json = Column("METRICS_JSON", String(4096), nullable=False, default="{}")
    started_at = Column("STARTED_AT", DateTime(timezone=True), nullable=False, server_default=func.now())
    finished_at = Column("FINISHED_AT", DateTime(timezone=True), nullable=True)
    duration_ms = Column("DURATION_MS", Integer, nullable=True)
    changed_by_id = Column("CHANGED_BY", Integer, ForeignKey("USER.ID"), nullable=True)
    created_by_id = Column("CREATED_BY", Integer, ForeignKey("USER.ID"), nullable=True)
    created_at = Column("CREATED_AT", DateTime(timezone=True), server_default=func.now())
    updated_at = Column("UPDATED_AT", DateTime(timezone=True), onupdate=func.now())

    job = relationship("ScheduledJob", back_populates="runs")
    changed_by_user = relationship("User", foreign_keys=[changed_by_id])
    created_by_user = relationship("User", foreign_keys=[created_by_id])
