from sqlalchemy import Boolean, Column, Date, DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..database import Base


class Episode(Base):
    """Patient episode covering evaluation, listing, transplantation and follow-up."""

    __tablename__ = "EPISODE"

    id = Column(
        "ID",
        Integer,
        primary_key=True,
        index=True,
        comment="Technical primary key of the episode.",
        info={"label": "ID"},
    )
    patient_id = Column(
        "PATIENT_ID",
        Integer,
        ForeignKey("PATIENT.ID"),
        nullable=False,
        index=True,
        comment="Patient reference owning this episode.",
        info={"label": "Patient"},
    )
    organ_id = Column(
        "ORGAN_ID",
        Integer,
        ForeignKey("CODE.ID"),
        nullable=False,
        comment="Organ reference (`CODE.ORGAN`) for this episode.",
        info={"label": "Episode Organ"},
    )
    start = Column(
        "START",
        Date,
        nullable=True,
        comment="Start date of the episode.",
        info={"label": "Start"},
    )
    end = Column(
        "END",
        Date,
        nullable=True,
        comment="End date of the episode.",
        info={"label": "End"},
    )
    fall_nr = Column(
        "FALL_NR",
        String(24),
        default="",
        comment="Administrative case number of the episode.",
        info={"label": "Fall Nr."},
    )
    status_id = Column(
        "STATUS_ID",
        Integer,
        ForeignKey("CODE.ID"),
        nullable=True,
        comment="Episode status reference (`CODE.EPISODE_STATUS`).",
        info={"label": "Episode Status"},
    )
    phase_id = Column(
        "PHASE_ID",
        Integer,
        ForeignKey("CODE.ID"),
        nullable=True,
        comment="Episode phase reference (`CODE.TPL_PHASE`).",
        info={"label": "Episode Phase"},
    )
    closed = Column(
        "CLOSED",
        Boolean,
        default=False,
        comment="Whether the episode is currently closed.",
        info={"label": "Closed"},
    )
    comment = Column(
        "COMMENT",
        String(1024),
        default="",
        comment="General free-text comment for the episode.",
        info={"label": "Comment"},
    )
    cave = Column(
        "CAVE",
        String(512),
        default="",
        comment="Safety/caveat notes related to the episode.",
        info={"label": "Cave"},
    )
    eval_start = Column(
        "EVAL_START",
        Date,
        nullable=True,
        comment="Start date of evaluation phase.",
        info={"label": "Eval Start"},
    )
    eval_end = Column(
        "EVAL_END",
        Date,
        nullable=True,
        comment="End date of evaluation phase.",
        info={"label": "Eval End"},
    )
    eval_assigned_to = Column(
        "EVAL_ASSIGNED_TO",
        String,
        default="",
        comment="Person assigned to evaluation.",
        info={"label": "Eval Assigned To"},
    )
    eval_stat = Column(
        "EVAL_STAT",
        String,
        default="",
        comment="Evaluation status text value.",
        info={"label": "Eval Stat"},
    )
    eval_register_date = Column(
        "EVAL_REGISTER_DATE",
        Date,
        nullable=True,
        comment="Date the evaluation was registered.",
        info={"label": "Eval Register Date"},
    )
    eval_excluded = Column(
        "EVAL_EXCLUDED",
        Boolean,
        default=False,
        comment="Whether the patient was excluded during evaluation.",
        info={"label": "Eval Excluded"},
    )
    eval_non_list_sent = Column(
        "EVAL_NON_LIST_SENT",
        Date,
        nullable=True,
        comment="Date the non-listing message was sent.",
        info={"label": "Eval Non List Sent"},
    )
    list_start = Column(
        "LIST_START",
        Date,
        nullable=True,
        comment="Start date of listing phase.",
        info={"label": "List Start"},
    )
    list_end = Column(
        "LIST_END",
        Date,
        nullable=True,
        comment="End date of listing phase.",
        info={"label": "List End"},
    )
    list_rs_nr = Column(
        "LIST_RS_NR",
        String(12),
        default="",
        comment="Listing registry number.",
        info={"label": "List RS Nr."},
    )
    list_reason_delist = Column(
        "LIST_REASON_DELIST",
        String,
        default="",
        comment="Reason code/text for delisting.",
        info={"label": "List Reason Delist"},
    )
    list_expl_delist = Column(
        "LIST_EXPL_DELIST",
        String(1024),
        default="",
        comment="Detailed explanation of delisting.",
        info={"label": "List Expl Delist"},
    )
    list_delist_sent = Column(
        "LIST_DELIST_SENT",
        Date,
        nullable=True,
        comment="Date the delisting communication was sent.",
        info={"label": "List Delist Sent"},
    )
    tpl_date = Column(
        "TPL_DATE",
        Date,
        nullable=True,
        comment="Transplantation date for the episode.",
        info={"label": "TPL Date"},
    )
    fup_recipient_card_done = Column(
        "FUP_RECIPIENT_CARD_DONE",
        Boolean,
        default=False,
        comment="Whether follow-up recipient card was completed.",
        info={"label": "FUP Recipient Card Done"},
    )
    fup_recipient_card_date = Column(
        "FUP_RECIPIENT_CARD_DATE",
        Date,
        nullable=True,
        comment="Date the follow-up recipient card was completed.",
        info={"label": "FUP Recipient Card Date"},
    )
    changed_by_id = Column(
        "CHANGED_BY",
        Integer,
        ForeignKey("USER.ID"),
        nullable=True,
        comment="Last user who changed the episode.",
        info={"label": "Changed By"},
    )
    created_by_id = Column(
        "CREATED_BY",
        Integer,
        ForeignKey("USER.ID"),
        nullable=True,
        comment="User who created the episode.",
        info={"label": "Created By"},
    )
    created_at = Column(
        "CREATED_AT",
        DateTime(timezone=True),
        server_default=func.now(),
        comment="Creation timestamp of the episode row.",
        info={"label": "Created At"},
    )
    updated_at = Column(
        "UPDATED_AT",
        DateTime(timezone=True),
        onupdate=func.now(),
        comment="Last update timestamp of the episode row.",
        info={"label": "Updated At"},
    )

    patient = relationship("Patient", back_populates="episodes")
    organ = relationship("Code", foreign_keys=[organ_id])
    status = relationship("Code", foreign_keys=[status_id])
    phase = relationship("Code", foreign_keys=[phase_id])
    changed_by_user = relationship("User", foreign_keys=[changed_by_id])
    created_by_user = relationship("User", foreign_keys=[created_by_id])
    coordination_episodes = relationship("CoordinationEpisode", back_populates="episode")
    task_groups = relationship("TaskGroup", back_populates="episode")
    organ_links = relationship("EpisodeOrgan", back_populates="episode", cascade="all, delete-orphan")
    organs = relationship(
        "Code",
        secondary="EPISODE_ORGAN",
        primaryjoin="Episode.id == EpisodeOrgan.episode_id",
        secondaryjoin="and_(Code.id == EpisodeOrgan.organ_id, EpisodeOrgan.is_active == True)",
        viewonly=True,
    )

    @property
    def organ_ids(self) -> list[int]:
        if self.organs:
            return [organ.id for organ in self.organs if organ and organ.id is not None]
        if self.organ_links:
            return []
        if self.organ_id is not None:
            return [self.organ_id]
        return []

    @property
    def episode_organs(self) -> list["EpisodeOrgan"]:
        return self.organ_links


class EpisodeOrgan(Base):
    """Link table mapping episodes to one or more organs."""

    __tablename__ = "EPISODE_ORGAN"
    __table_args__ = (UniqueConstraint("EPISODE_ID", "ORGAN_ID"),)

    id = Column(
        "ID",
        Integer,
        primary_key=True,
        index=True,
        comment="Technical primary key of the episode-organ link.",
        info={"label": "ID"},
    )
    episode_id = Column(
        "EPISODE_ID",
        Integer,
        ForeignKey("EPISODE.ID"),
        nullable=False,
        index=True,
        comment="Episode reference.",
        info={"label": "Episode"},
    )
    organ_id = Column(
        "ORGAN_ID",
        Integer,
        ForeignKey("CODE.ID"),
        nullable=False,
        index=True,
        comment="Organ reference (`CODE.ORGAN`).",
        info={"label": "Organ"},
    )
    date_added = Column(
        "DATE_ADDED",
        Date,
        nullable=True,
        comment="Date when this organ was added to the episode.",
        info={"label": "Date Added"},
    )
    comment = Column(
        "COMMENT",
        String(512),
        default="",
        comment="Comment for this episode-organ relation row.",
        info={"label": "Comment"},
    )
    is_active = Column(
        "IS_ACTIVE",
        Boolean,
        default=True,
        nullable=False,
        comment="Whether this organ relation is currently active for the episode.",
        info={"label": "Is Active"},
    )
    date_inactivated = Column(
        "DATE_INACTIVATED",
        Date,
        nullable=True,
        comment="Date when this organ relation was inactivated.",
        info={"label": "Date Inactivated"},
    )
    reason_activation_change = Column(
        "REASON_ACTIVATION_CHANGE",
        String(128),
        default="",
        comment="Reason for activation status change.",
        info={"label": "Reason Activation Change"},
    )

    episode = relationship("Episode", back_populates="organ_links")
    organ = relationship("Code", foreign_keys=[organ_id])
