from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..database import Base


class ColloqiumType(Base):
    __tablename__ = "COLLOQIUM_TYPE"

    id = Column(
        "ID",
        Integer,
        primary_key=True,
        index=True,
        comment="Technical primary key of the colloquium type.",
        info={"label": "ID"},
    )
    name = Column(
        "NAME",
        String(64),
        nullable=False,
        comment="Business name of the colloquium type.",
        info={"label": "Name"},
    )
    organ_id = Column(
        "ORGAN_ID",
        Integer,
        ForeignKey("CODE.ID"),
        nullable=False,
        comment="Organ reference (`CODE.ORGAN`) for this type.",
        info={"label": "Colloquium Organ"},
    )
    participants = Column(
        "PARTICIPANTS",
        String(1024),
        default="",
        comment="Default participant list/template for this type.",
        info={"label": "Participants"},
    )
    changed_by_id = Column(
        "CHANGED_BY",
        Integer,
        ForeignKey("USER.ID"),
        nullable=True,
        comment="Last user who changed the colloquium type.",
        info={"label": "Changed By"},
    )
    created_by_id = Column(
        "CREATED_BY",
        Integer,
        ForeignKey("USER.ID"),
        nullable=True,
        comment="User who created the colloquium type.",
        info={"label": "Created By"},
    )
    created_at = Column(
        "CREATED_AT",
        DateTime(timezone=True),
        server_default=func.now(),
        comment="Creation timestamp of the colloquium type row.",
        info={"label": "Created At"},
    )
    updated_at = Column(
        "UPDATED_AT",
        DateTime(timezone=True),
        onupdate=func.now(),
        comment="Last update timestamp of the colloquium type row.",
        info={"label": "Updated At"},
    )

    organ = relationship("Code", foreign_keys=[organ_id])
    changed_by_user = relationship("User", foreign_keys=[changed_by_id])
    created_by_user = relationship("User", foreign_keys=[created_by_id])
    colloqiums = relationship("Colloqium", back_populates="colloqium_type")
    participant_links = relationship(
        "ColloqiumTypeParticipant",
        back_populates="colloqium_type",
        cascade="all, delete-orphan",
        order_by="ColloqiumTypeParticipant.pos.asc()",
    )

    @property
    def participant_ids(self) -> list[int]:
        return [link.person_id for link in (self.participant_links or []) if link.person_id is not None]

    @property
    def participants_people(self) -> list["Person"]:
        return [link.person for link in (self.participant_links or []) if link.person is not None]


class Colloqium(Base):
    __tablename__ = "COLLOQIUM"
    __table_args__ = (UniqueConstraint("TYPE_ID", "DATE"),)

    id = Column(
        "ID",
        Integer,
        primary_key=True,
        index=True,
        comment="Technical primary key of the colloquium.",
        info={"label": "ID"},
    )
    colloqium_type_id = Column(
        "TYPE_ID",
        Integer,
        ForeignKey("COLLOQIUM_TYPE.ID"),
        nullable=False,
        comment="Colloquium type reference for this colloquium.",
        info={"label": "Colloquium Type"},
    )
    date = Column(
        "DATE",
        Date,
        nullable=False,
        comment="Date on which the colloquium is held.",
        info={"label": "Date"},
    )
    participants = Column(
        "PARTICIPANTS",
        String(1024),
        default="",
        comment="Participant list for this colloquium instance.",
        info={"label": "Participants"},
    )
    changed_by_id = Column(
        "CHANGED_BY",
        Integer,
        ForeignKey("USER.ID"),
        nullable=True,
        comment="Last user who changed the colloquium.",
        info={"label": "Changed By"},
    )
    created_by_id = Column(
        "CREATED_BY",
        Integer,
        ForeignKey("USER.ID"),
        nullable=True,
        comment="User who created the colloquium.",
        info={"label": "Created By"},
    )
    created_at = Column(
        "CREATED_AT",
        DateTime(timezone=True),
        server_default=func.now(),
        comment="Creation timestamp of the colloquium row.",
        info={"label": "Created At"},
    )
    updated_at = Column(
        "UPDATED_AT",
        DateTime(timezone=True),
        onupdate=func.now(),
        comment="Last update timestamp of the colloquium row.",
        info={"label": "Updated At"},
    )

    colloqium_type = relationship("ColloqiumType", back_populates="colloqiums")
    changed_by_user = relationship("User", foreign_keys=[changed_by_id])
    created_by_user = relationship("User", foreign_keys=[created_by_id])
    agendas = relationship("ColloqiumAgenda", back_populates="colloqium", cascade="all, delete-orphan")
    participant_links = relationship(
        "ColloqiumParticipant",
        back_populates="colloqium",
        cascade="all, delete-orphan",
        order_by="ColloqiumParticipant.pos.asc()",
    )

    @property
    def participant_ids(self) -> list[int]:
        return [link.person_id for link in (self.participant_links or []) if link.person_id is not None]

    @property
    def participants_people(self) -> list["Person"]:
        return [link.person for link in (self.participant_links or []) if link.person is not None]


class ColloqiumAgenda(Base):
    __tablename__ = "COLLOQIUM_AGENDA"

    id = Column(
        "ID",
        Integer,
        primary_key=True,
        index=True,
        comment="Technical primary key of the colloquium agenda entry.",
        info={"label": "ID"},
    )
    colloqium_id = Column(
        "COLLOQIUM_ID",
        Integer,
        ForeignKey("COLLOQIUM.ID"),
        nullable=False,
        comment="Colloquium reference owning this agenda entry.",
        info={"label": "Colloquium"},
    )
    episode_id = Column(
        "EPISODE_ID",
        Integer,
        ForeignKey("EPISODE.ID"),
        nullable=False,
        comment="Episode reference discussed in this agenda entry.",
        info={"label": "Episode"},
    )
    presented_by = Column(
        "PRESENTED_BY",
        String(64),
        default="",
        comment="Name/identifier of the person presenting this agenda item.",
        info={"label": "Presented By"},
    )
    decision = Column(
        "DECISION",
        String(64),
        default="",
        comment="Decision catalogue key captured for this agenda item.",
        info={"label": "Decision"},
    )
    decision_reason = Column(
        "DECISION_REASON",
        String(128),
        default="",
        comment="Reason/justification for the selected decision.",
        info={"label": "Decision Reason"},
    )
    comment = Column(
        "COMMENT",
        String(1024),
        default="",
        comment="Additional free-text comment for this agenda item.",
        info={"label": "Comment"},
    )
    changed_by_id = Column(
        "CHANGED_BY",
        Integer,
        ForeignKey("USER.ID"),
        nullable=True,
        comment="Last user who changed the agenda entry.",
        info={"label": "Changed By"},
    )
    created_by_id = Column(
        "CREATED_BY",
        Integer,
        ForeignKey("USER.ID"),
        nullable=True,
        comment="User who created the agenda entry.",
        info={"label": "Created By"},
    )
    created_at = Column(
        "CREATED_AT",
        DateTime(timezone=True),
        server_default=func.now(),
        comment="Creation timestamp of the agenda row.",
        info={"label": "Created At"},
    )
    updated_at = Column(
        "UPDATED_AT",
        DateTime(timezone=True),
        onupdate=func.now(),
        comment="Last update timestamp of the agenda row.",
        info={"label": "Updated At"},
    )

    colloqium = relationship("Colloqium", back_populates="agendas")
    episode = relationship("Episode")
    changed_by_user = relationship("User", foreign_keys=[changed_by_id])
    created_by_user = relationship("User", foreign_keys=[created_by_id])


class ColloqiumTypeParticipant(Base):
    __tablename__ = "COLLOQIUM_TYPE_PARTICIPANT"
    __table_args__ = (UniqueConstraint("COLLOQIUM_TYPE_ID", "PERSON_ID"),)

    id = Column(
        "ID",
        Integer,
        primary_key=True,
        index=True,
        comment="Technical primary key of the colloquium type participant link.",
        info={"label": "ID"},
    )
    colloqium_type_id = Column(
        "COLLOQIUM_TYPE_ID",
        Integer,
        ForeignKey("COLLOQIUM_TYPE.ID"),
        nullable=False,
        comment="Owning colloquium type.",
        info={"label": "Colloquium Type"},
    )
    person_id = Column(
        "PERSON_ID",
        Integer,
        ForeignKey("PERSON.ID"),
        nullable=False,
        comment="Linked person.",
        info={"label": "Person"},
    )
    pos = Column(
        "POS",
        Integer,
        nullable=False,
        default=1,
        comment="Sort position among participants.",
        info={"label": "Position"},
    )

    colloqium_type = relationship("ColloqiumType", back_populates="participant_links")
    person = relationship("Person")


class ColloqiumParticipant(Base):
    __tablename__ = "COLLOQIUM_PARTICIPANT"
    __table_args__ = (UniqueConstraint("COLLOQIUM_ID", "PERSON_ID"),)

    id = Column(
        "ID",
        Integer,
        primary_key=True,
        index=True,
        comment="Technical primary key of the colloquium participant link.",
        info={"label": "ID"},
    )
    colloqium_id = Column(
        "COLLOQIUM_ID",
        Integer,
        ForeignKey("COLLOQIUM.ID"),
        nullable=False,
        comment="Owning colloquium instance.",
        info={"label": "Colloquium"},
    )
    person_id = Column(
        "PERSON_ID",
        Integer,
        ForeignKey("PERSON.ID"),
        nullable=False,
        comment="Linked person.",
        info={"label": "Person"},
    )
    pos = Column(
        "POS",
        Integer,
        nullable=False,
        default=1,
        comment="Sort position among participants.",
        info={"label": "Position"},
    )

    colloqium = relationship("Colloqium", back_populates="participant_links")
    person = relationship("Person")
