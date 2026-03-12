from sqlalchemy import Boolean, Column, Date, DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..database import Base


class CoordinationEpisode(Base):
    """Episode assignments and outcomes within a coordination case."""

    __tablename__ = "COORDINATION_EPISODE"
    __table_args__ = (
        UniqueConstraint(
            "COORDINATION_ID",
            "EPISODE_ID",
            "ORGAN",
            name="uq_coordination_episode_coordination_episode_organ",
        ),
    )

    id = Column(
        "ID",
        Integer,
        primary_key=True,
        index=True,
        comment="Technical primary key of the coordination episode row.",
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
    episode_id = Column(
        "EPISODE_ID",
        Integer,
        ForeignKey("EPISODE.ID"),
        nullable=False,
        index=True,
        comment="Reference to an episode linked to this coordination.",
        info={"label": "Episode"},
    )
    organ_id = Column(
        "ORGAN",
        Integer,
        ForeignKey("CODE.ID"),
        nullable=False,
        comment="Organ reference (`CODE.ORGAN`).",
        info={"label": "Organ"},
    )
    tpl_date = Column(
        "TPL_DATE",
        Date,
        nullable=True,
        comment="Transplantation date for this coordination-episode assignment.",
        info={"label": "TPL Date"},
    )
    procurement_team = Column(
        "PROCUREMENT_TEAM",
        String(1024),
        default="",
        comment="Procurement team notes (max 1024 characters).",
        info={"label": "Procurement Team"},
    )
    exvivo_perfusion_done = Column(
        "EXVIVO_PERFUSION_DONE",
        Boolean,
        nullable=False,
        default=False,
        comment="Whether ex-vivo perfusion was done.",
        info={"label": "Exvivo Perfusion Done"},
    )
    is_organ_rejected = Column(
        "IS_ORGAN_REJECTED",
        Boolean,
        nullable=False,
        default=False,
        comment="Whether the organ was rejected.",
        info={"label": "Is Organ Rejected"},
    )
    organ_rejection_sequel_id = Column(
        "ORGAN_REJECTION_SEQUEL",
        Integer,
        ForeignKey("CODE.ID"),
        nullable=True,
        comment="Organ rejection sequel (`CODE.ORGAN_REJECTION_SEQUEL`).",
        info={"label": "Organ Rejection Sequel"},
    )
    changed_by_id = Column(
        "CHANGED_BY",
        Integer,
        ForeignKey("USER.ID"),
        nullable=True,
        comment="Last user who changed the coordination episode row.",
        info={"label": "Changed By"},
    )
    created_by_id = Column(
        "CREATED_BY",
        Integer,
        ForeignKey("USER.ID"),
        nullable=True,
        comment="User who created the coordination episode row.",
        info={"label": "Created By"},
    )
    created_at = Column(
        "CREATED_AT",
        DateTime(timezone=True),
        server_default=func.now(),
        comment="Creation timestamp of the coordination episode row.",
        info={"label": "Created At"},
    )
    updated_at = Column(
        "UPDATED_AT",
        DateTime(timezone=True),
        onupdate=func.now(),
        comment="Last update timestamp of the coordination episode row.",
        info={"label": "Updated At"},
    )

    coordination = relationship("Coordination", back_populates="coordination_episodes")
    episode = relationship("Episode", back_populates="coordination_episodes")
    organ = relationship("Code", foreign_keys=[organ_id])
    organ_rejection_sequel = relationship("Code", foreign_keys=[organ_rejection_sequel_id])
    changed_by_user = relationship("User", foreign_keys=[changed_by_id])
    created_by_user = relationship("User", foreign_keys=[created_by_id])
