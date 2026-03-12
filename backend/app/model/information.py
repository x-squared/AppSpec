from sqlalchemy import Boolean, Column, Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..database import Base


class Information(Base):
    """Contextual information message editable by users."""

    __tablename__ = "INFORMATION"

    id = Column(
        "ID",
        Integer,
        primary_key=True,
        index=True,
        comment="Technical primary key of the information row.",
        info={"label": "ID"},
    )
    context_id = Column(
        "CONTEXT_ID",
        Integer,
        ForeignKey("CODE.ID"),
        nullable=True,
        comment="Optional context code (`CODE.ORGAN`) for context-specific information.",
        info={"label": "Context"},
    )
    text = Column(
        "TEXT",
        String(1024),
        nullable=False,
        comment="Styled information text (supports bold, italic and underline).",
        info={"label": "Text"},
    )
    author_id = Column(
        "AUTHOR_ID",
        Integer,
        ForeignKey("USER.ID"),
        nullable=False,
        comment="Authoring user for this information row.",
        info={"label": "Author"},
    )
    date = Column(
        "DATE",
        Date,
        nullable=False,
        comment="Business date of the information row.",
        info={"label": "Date"},
    )
    valid_from = Column(
        "VALID_FROM",
        Date,
        nullable=False,
        comment="Date from which the information is considered valid.",
        info={"label": "Valid From"},
    )
    withdrawn = Column(
        "WITHDRAWN",
        Boolean,
        nullable=False,
        default=False,
        comment="Whether the information was withdrawn after being distributed.",
        info={"label": "Withdrawn"},
    )

    context = relationship("Code", foreign_keys=[context_id])
    author = relationship("User", foreign_keys=[author_id])
    user_reads = relationship("InformationUser", back_populates="information")
    context_links = relationship(
        "InformationContext",
        back_populates="information",
        cascade="all, delete-orphan",
        order_by="InformationContext.pos",
    )


class InformationUser(Base):
    """Per-user read marker for information rows."""

    __tablename__ = "INFORMATION_USER"

    information_id = Column(
        "INFORMATION_ID",
        Integer,
        ForeignKey("INFORMATION.ID"),
        primary_key=True,
        comment="Referenced information row.",
        info={"label": "Information"},
    )
    user_id = Column(
        "USER_ID",
        Integer,
        ForeignKey("USER.ID"),
        primary_key=True,
        comment="User who has read the information.",
        info={"label": "User"},
    )
    seen_at = Column(
        "SEEN_AT",
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        comment="Timestamp when the user marked the information as read.",
        info={"label": "Seen At"},
    )

    information = relationship("Information", back_populates="user_reads")
    user = relationship("User", foreign_keys=[user_id])


class InformationContext(Base):
    """N:M relation between information rows and ORGAN context codes."""

    __tablename__ = "INFORMATION_CONTEXT"

    information_id = Column(
        "INFORMATION_ID",
        Integer,
        ForeignKey("INFORMATION.ID"),
        primary_key=True,
        comment="Referenced information row.",
        info={"label": "Information"},
    )
    context_id = Column(
        "CONTEXT_ID",
        Integer,
        ForeignKey("CODE.ID"),
        primary_key=True,
        comment="Referenced context code (`CODE.ORGAN`).",
        info={"label": "Context"},
    )
    pos = Column(
        "POS",
        Integer,
        nullable=False,
        default=0,
        comment="Ordering position for context tags.",
        info={"label": "Position"},
    )

    information = relationship("Information", back_populates="context_links")
    context = relationship("Code", foreign_keys=[context_id])


