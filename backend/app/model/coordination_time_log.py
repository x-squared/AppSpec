from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..database import Base


class CoordinationTimeLog(Base):
    """User time log entries associated with a coordination case."""

    __tablename__ = "COORDINATION_TIME_LOG"

    id = Column(
        "ID",
        Integer,
        primary_key=True,
        index=True,
        comment="Technical primary key of the coordination time log row.",
        info={"label": "ID"},
    )
    coordination_id = Column(
        "COORDINATION_ID",
        Integer,
        ForeignKey("COORDINATION.ID"),
        nullable=False,
        index=True,
        comment="Reference to the coordination core row.",
        info={"label": "Coordination"},
    )
    user_id = Column(
        "USER_ID",
        Integer,
        ForeignKey("USER.ID"),
        nullable=False,
        index=True,
        comment="User who owns this time log row.",
        info={"label": "User"},
    )
    start = Column(
        "START",
        DateTime(timezone=True),
        nullable=True,
        comment="Start timestamp of the time log interval.",
        info={"label": "Start"},
    )
    end = Column(
        "END",
        DateTime(timezone=True),
        nullable=True,
        comment="End timestamp of the time log interval.",
        info={"label": "End"},
    )
    comment = Column(
        "COMMENT",
        String(1024),
        default="",
        comment="Comment entered for this time log interval.",
        info={"label": "Comment"},
    )
    changed_by_id = Column(
        "CHANGED_BY",
        Integer,
        ForeignKey("USER.ID"),
        nullable=True,
        comment="Last user who changed the coordination time log row.",
        info={"label": "Changed By"},
    )
    created_by_id = Column(
        "CREATED_BY",
        Integer,
        ForeignKey("USER.ID"),
        nullable=True,
        comment="User who created the coordination time log row.",
        info={"label": "Created By"},
    )
    created_at = Column(
        "CREATED_AT",
        DateTime(timezone=True),
        server_default=func.now(),
        comment="Creation timestamp of the coordination time log row.",
        info={"label": "Created At"},
    )
    updated_at = Column(
        "UPDATED_AT",
        DateTime(timezone=True),
        onupdate=func.now(),
        comment="Last update timestamp of the coordination time log row.",
        info={"label": "Updated At"},
    )

    coordination = relationship("Coordination", back_populates="time_logs")
    user = relationship("User", foreign_keys=[user_id])
    changed_by_user = relationship("User", foreign_keys=[changed_by_id])
    created_by_user = relationship("User", foreign_keys=[created_by_id])
