from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..database import Base


class DevRequest(Base):
    """Developer forum request with captured context and review lifecycle."""

    __tablename__ = "DEV_REQUEST"

    id = Column(
        "ID",
        Integer,
        primary_key=True,
        index=True,
        comment="Technical primary key of the dev request.",
        info={"label": "ID"},
    )
    parent_request_id = Column(
        "PARENT_REQUEST_ID",
        Integer,
        ForeignKey("DEV_REQUEST.ID"),
        nullable=True,
        index=True,
        comment="Optional parent request id when created as linked follow-up.",
        info={"label": "Parent Request"},
    )
    submitter_user_id = Column(
        "SUBMITTER_USER_ID",
        Integer,
        ForeignKey("USER.ID"),
        nullable=False,
        index=True,
        comment="User who submitted the request.",
        info={"label": "Submitter User"},
    )
    claimed_by_user_id = Column(
        "CLAIMED_BY_USER_ID",
        Integer,
        ForeignKey("USER.ID"),
        nullable=True,
        index=True,
        comment="Developer user currently claiming this request.",
        info={"label": "Claimed By User"},
    )
    decided_by_user_id = Column(
        "DECIDED_BY_USER_ID",
        Integer,
        ForeignKey("USER.ID"),
        nullable=True,
        index=True,
        comment="Developer user who submitted the latest development decision.",
        info={"label": "Decided By User"},
    )
    status = Column(
        "STATUS",
        String(48),
        nullable=False,
        default="PENDING",
        index=True,
        comment="Current lifecycle status of the dev request.",
        info={"label": "Status"},
    )
    decision = Column(
        "DECISION",
        String(48),
        nullable=True,
        comment="Latest development decision marker (REJECTED or IMPLEMENTED).",
        info={"label": "Decision"},
    )
    capture_url = Column(
        "CAPTURE_URL",
        String(1024),
        nullable=False,
        default="",
        comment="Captured deep link URL for reopening app context.",
        info={"label": "Capture URL"},
    )
    capture_gui_part = Column(
        "CAPTURE_GUI_PART",
        String(256),
        nullable=False,
        default="",
        comment="Captured GUI area hint for user/developer orientation.",
        info={"label": "Capture GUI Part"},
    )
    capture_state_json = Column(
        "CAPTURE_STATE_JSON",
        Text,
        nullable=False,
        default="{}",
        comment="Structured captured app state payload (IDs and route context).",
        info={"label": "Capture State JSON"},
    )
    request_text = Column(
        "REQUEST_TEXT",
        Text,
        nullable=False,
        default="",
        comment="User-authored request text.",
        info={"label": "Request Text"},
    )
    developer_note_text = Column(
        "DEVELOPER_NOTE_TEXT",
        Text,
        nullable=True,
        comment="Developer working notes text.",
        info={"label": "Developer Note Text"},
    )
    developer_response_text = Column(
        "DEVELOPER_RESPONSE_TEXT",
        Text,
        nullable=True,
        comment="Developer response text shown to submitting user.",
        info={"label": "Developer Response Text"},
    )
    user_review_text = Column(
        "USER_REVIEW_TEXT",
        Text,
        nullable=True,
        comment="User review feedback text after developer response.",
        info={"label": "User Review Text"},
    )
    closed_at = Column(
        "CLOSED_AT",
        DateTime(timezone=True),
        nullable=True,
        comment="Timestamp when request was closed.",
        info={"label": "Closed At"},
    )
    created_at = Column(
        "CREATED_AT",
        DateTime(timezone=True),
        server_default=func.now(),
        comment="Creation timestamp of the dev request row.",
        info={"label": "Created At"},
    )
    updated_at = Column(
        "UPDATED_AT",
        DateTime(timezone=True),
        onupdate=func.now(),
        comment="Last update timestamp of the dev request row.",
        info={"label": "Updated At"},
    )

    parent_request = relationship("DevRequest", remote_side=[id], backref="follow_up_requests")
    submitter_user = relationship("User", foreign_keys=[submitter_user_id])
    claimed_by_user = relationship("User", foreign_keys=[claimed_by_user_id])
    decided_by_user = relationship("User", foreign_keys=[decided_by_user_id])
