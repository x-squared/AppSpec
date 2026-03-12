from enum import Enum

from sqlalchemy import Boolean, Column, Date, DateTime, Enum as SqlEnum, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..database import Base
from ..enums import ProcurementSlotKey, ProcurementValueMode


class ProcurementPersonListKey(str, Enum):
    ON_SITE_COORDINATORS = "ON_SITE_COORDINATORS"
    PROCUREMENT_TEAM_INT = "PROCUREMENT_TEAM_INT"


class ProcurementTeamListKey(str, Enum):
    IMPLANT_TEAM = "IMPLANT_TEAM"


class CoordinationProcurement(Base):
    """Procurement-specific 1:1 extension of the coordination core entity."""

    __tablename__ = "COORDINATION_PROCUREMENT"

    id = Column(
        "ID",
        Integer,
        primary_key=True,
        index=True,
        comment="Technical primary key of the coordination procurement row.",
        info={"label": "ID"},
    )
    coordination_id = Column(
        "COORDINATION_ID",
        Integer,
        ForeignKey("COORDINATION.ID"),
        nullable=False,
        unique=True,
        index=True,
        comment="1:1 reference to the coordination core row.",
        info={"label": "Coordination"},
    )
    time_of_death = Column(
        "TIME_OF_DEATH",
        DateTime(timezone=True),
        nullable=True,
        comment="Timestamp of donor death.",
        info={"label": "Time Of Death"},
    )
    moe_performed = Column(
        "MOE_PERFORMED",
        Boolean,
        nullable=False,
        default=False,
        comment="Whether MOE was performed.",
        info={"label": "MOE Performed"},
    )
    moe_time = Column(
        "MOE_TIME",
        DateTime(timezone=True),
        nullable=True,
        comment="Timestamp when MOE was performed.",
        info={"label": "MOE Time"},
    )
    nrp_abdominal_done = Column(
        "NRP_ABDOMINAL_DONE",
        Boolean,
        nullable=False,
        default=False,
        comment="Whether abdominal NRP was performed.",
        info={"label": "NRP Abdominal Done"},
    )
    nrp_thoracic_done = Column(
        "NRP_THORACIC_DONE",
        Boolean,
        nullable=False,
        default=False,
        comment="Whether thoracic NRP was performed.",
        info={"label": "NRP Thoracic Done"},
    )
    nrp_time = Column(
        "NRP_TIME",
        DateTime(timezone=True),
        nullable=True,
        comment="Timestamp when NRP was performed.",
        info={"label": "NRP Time"},
    )
    changed_by_id = Column(
        "CHANGED_BY",
        Integer,
        ForeignKey("USER.ID"),
        nullable=True,
        comment="Last user who changed the coordination procurement row.",
        info={"label": "Changed By"},
    )
    created_by_id = Column(
        "CREATED_BY",
        Integer,
        ForeignKey("USER.ID"),
        nullable=True,
        comment="User who created the coordination procurement row.",
        info={"label": "Created By"},
    )
    created_at = Column(
        "CREATED_AT",
        DateTime(timezone=True),
        server_default=func.now(),
        comment="Creation timestamp of the coordination procurement row.",
        info={"label": "Created At"},
    )
    updated_at = Column(
        "UPDATED_AT",
        DateTime(timezone=True),
        onupdate=func.now(),
        comment="Last update timestamp of the coordination procurement row.",
        info={"label": "Updated At"},
    )

    coordination = relationship("Coordination", back_populates="procurement")
    changed_by_user = relationship("User", foreign_keys=[changed_by_id])
    created_by_user = relationship("User", foreign_keys=[created_by_id])


class CoordinationProcurementOrganRejection(Base):
    """Per-organ rejection state for a coordination case."""

    __tablename__ = "COORDINATION_PROCUREMENT_ORGAN_REJECTION"
    __table_args__ = (
        UniqueConstraint(
            "COORDINATION_ID",
            "ORGAN_ID",
            name="uq_coordination_procurement_organ_rejection",
        ),
    )

    id = Column("ID", Integer, primary_key=True, index=True)
    coordination_id = Column("COORDINATION_ID", Integer, ForeignKey("COORDINATION.ID"), nullable=False, index=True)
    organ_id = Column("ORGAN_ID", Integer, ForeignKey("CODE.ID"), nullable=False, index=True)
    is_rejected = Column("IS_REJECTED", Boolean, nullable=False, default=False)
    rejection_comment = Column("REJECTION_COMMENT", String(1024), nullable=False, default="")
    changed_by_id = Column("CHANGED_BY", Integer, ForeignKey("USER.ID"), nullable=True)
    created_by_id = Column("CREATED_BY", Integer, ForeignKey("USER.ID"), nullable=True)
    created_at = Column("CREATED_AT", DateTime(timezone=True), server_default=func.now())
    updated_at = Column("UPDATED_AT", DateTime(timezone=True), onupdate=func.now())

    organ = relationship("Code", foreign_keys=[organ_id])
    changed_by_user = relationship("User", foreign_keys=[changed_by_id])
    created_by_user = relationship("User", foreign_keys=[created_by_id])


class CoordinationProcurementFieldTemplate(Base):
    """Template definition of flexible procurement fields."""

    __tablename__ = "COORDINATION_PROCUREMENT_FIELD_TEMPLATE"

    id = Column("ID", Integer, primary_key=True, index=True)
    key = Column("KEY", String(64), nullable=False, unique=True, index=True)
    name_default = Column("NAME_DEFAULT", String(128), nullable=False, default="")
    comment = Column("COMMENT", String(512), nullable=False, default="")
    is_active = Column("IS_ACTIVE", Boolean, nullable=False, default=True)
    pos = Column("POS", Integer, nullable=False, default=0)
    group_template_id = Column(
        "GROUP_TEMPLATE_ID",
        Integer,
        ForeignKey("COORDINATION_PROCUREMENT_FIELD_GROUP_TEMPLATE.ID"),
        nullable=True,
        index=True,
    )
    value_mode = Column(
        "VALUE_MODE",
        SqlEnum(
            ProcurementValueMode,
            native_enum=False,
            validate_strings=True,
            values_callable=lambda enum_cls: [entry.value for entry in enum_cls],
            length=24,
        ),
        nullable=False,
        default=ProcurementValueMode.SCALAR.value,
    )
    datatype_def_id = Column("DATATYPE_DEF_ID", Integer, ForeignKey("MEDICAL_VALUE_DATATYPE.ID"), nullable=False, index=True)
    changed_by_id = Column("CHANGED_BY", Integer, ForeignKey("USER.ID"), nullable=True)
    created_by_id = Column("CREATED_BY", Integer, ForeignKey("USER.ID"), nullable=True)
    created_at = Column("CREATED_AT", DateTime(timezone=True), server_default=func.now())
    updated_at = Column("UPDATED_AT", DateTime(timezone=True), onupdate=func.now())

    datatype_definition = relationship("DatatypeDefinition")
    group_template = relationship("CoordinationProcurementFieldGroupTemplate", back_populates="field_templates")
    changed_by_user = relationship("User", foreign_keys=[changed_by_id])
    created_by_user = relationship("User", foreign_keys=[created_by_id])
    scopes = relationship(
        "CoordinationProcurementFieldScopeTemplate",
        back_populates="field_template",
        cascade="all, delete-orphan",
    )


class CoordinationProcurementFieldScopeTemplate(Base):
    """Applicability scope of procurement field templates by organ and slot."""

    __tablename__ = "COORDINATION_PROCUREMENT_FIELD_SCOPE_TEMPLATE"
    __table_args__ = (
        UniqueConstraint("FIELD_TEMPLATE_ID", "ORGAN_ID", "SLOT_KEY", name="uq_coordination_procurement_field_scope"),
    )

    id = Column("ID", Integer, primary_key=True, index=True)
    field_template_id = Column("FIELD_TEMPLATE_ID", Integer, ForeignKey("COORDINATION_PROCUREMENT_FIELD_TEMPLATE.ID"), nullable=False, index=True)
    organ_id = Column("ORGAN_ID", Integer, ForeignKey("CODE.ID"), nullable=True, index=True)
    slot_key = Column(
        "SLOT_KEY",
        SqlEnum(
            ProcurementSlotKey,
            native_enum=False,
            validate_strings=True,
            values_callable=lambda enum_cls: [entry.value for entry in enum_cls],
            length=16,
        ),
        nullable=False,
        default=ProcurementSlotKey.MAIN.value,
    )
    changed_by_id = Column("CHANGED_BY", Integer, ForeignKey("USER.ID"), nullable=True)
    created_by_id = Column("CREATED_BY", Integer, ForeignKey("USER.ID"), nullable=True)
    created_at = Column("CREATED_AT", DateTime(timezone=True), server_default=func.now())
    updated_at = Column("UPDATED_AT", DateTime(timezone=True), onupdate=func.now())

    field_template = relationship("CoordinationProcurementFieldTemplate", back_populates="scopes")
    organ = relationship("Code", foreign_keys=[organ_id])
    changed_by_user = relationship("User", foreign_keys=[changed_by_id])
    created_by_user = relationship("User", foreign_keys=[created_by_id])


class CoordinationProcurementData(Base):
    """Unified runtime procurement data row per coordination, organ, slot and field."""

    __tablename__ = "COORDINATION_PROCUREMENT_DATA"
    __table_args__ = (
        UniqueConstraint(
            "COORDINATION_ID",
            "ORGAN_ID",
            "SLOT_KEY",
            "FIELD_TEMPLATE_ID",
            name="uq_coordination_procurement_data",
        ),
    )

    id = Column("ID", Integer, primary_key=True, index=True)
    coordination_id = Column("COORDINATION_ID", Integer, ForeignKey("COORDINATION.ID"), nullable=False, index=True)
    organ_id = Column("ORGAN_ID", Integer, ForeignKey("CODE.ID"), nullable=False, index=True)
    slot_key = Column(
        "SLOT_KEY",
        SqlEnum(
            ProcurementSlotKey,
            native_enum=False,
            validate_strings=True,
            values_callable=lambda enum_cls: [entry.value for entry in enum_cls],
            length=16,
        ),
        nullable=False,
        default=ProcurementSlotKey.MAIN.value,
    )
    field_template_id = Column(
        "FIELD_TEMPLATE_ID",
        Integer,
        ForeignKey("COORDINATION_PROCUREMENT_FIELD_TEMPLATE.ID"),
        nullable=False,
        index=True,
    )
    value = Column("VALUE", String, nullable=False, default="")
    episode_id = Column("EPISODE_ID", Integer, ForeignKey("EPISODE.ID"), nullable=True, index=True)
    changed_by_id = Column("CHANGED_BY", Integer, ForeignKey("USER.ID"), nullable=True)
    created_by_id = Column("CREATED_BY", Integer, ForeignKey("USER.ID"), nullable=True)
    created_at = Column("CREATED_AT", DateTime(timezone=True), server_default=func.now())
    updated_at = Column("UPDATED_AT", DateTime(timezone=True), onupdate=func.now())

    coordination = relationship("Coordination")
    organ = relationship("Code", foreign_keys=[organ_id])
    field_template = relationship("CoordinationProcurementFieldTemplate")
    episode = relationship("Episode", foreign_keys=[episode_id])
    changed_by_user = relationship("User", foreign_keys=[changed_by_id])
    created_by_user = relationship("User", foreign_keys=[created_by_id])
    persons = relationship(
        "CoordinationProcurementDataPerson",
        back_populates="data_row",
        cascade="all, delete-orphan",
    )
    teams = relationship(
        "CoordinationProcurementDataTeam",
        back_populates="data_row",
        cascade="all, delete-orphan",
    )


class CoordinationProcurementDataPerson(Base):
    """Person references attached to a unified procurement data row."""

    __tablename__ = "COORDINATION_PROCUREMENT_DATA_PERSON"
    __table_args__ = (
        UniqueConstraint("DATA_ID", "PERSON_ID", name="uq_coordination_procurement_data_person"),
    )

    id = Column("ID", Integer, primary_key=True, index=True)
    data_id = Column("DATA_ID", Integer, ForeignKey("COORDINATION_PROCUREMENT_DATA.ID"), nullable=False, index=True)
    person_id = Column("PERSON_ID", Integer, ForeignKey("PERSON.ID"), nullable=False, index=True)
    pos = Column("POS", Integer, nullable=False, default=0)
    changed_by_id = Column("CHANGED_BY", Integer, ForeignKey("USER.ID"), nullable=True)
    created_by_id = Column("CREATED_BY", Integer, ForeignKey("USER.ID"), nullable=True)
    created_at = Column("CREATED_AT", DateTime(timezone=True), server_default=func.now())
    updated_at = Column("UPDATED_AT", DateTime(timezone=True), onupdate=func.now())

    data_row = relationship("CoordinationProcurementData", back_populates="persons")
    person = relationship("Person")
    changed_by_user = relationship("User", foreign_keys=[changed_by_id])
    created_by_user = relationship("User", foreign_keys=[created_by_id])


class CoordinationProcurementDataTeam(Base):
    """Team references attached to a unified procurement data row."""

    __tablename__ = "COORDINATION_PROCUREMENT_DATA_TEAM"
    __table_args__ = (
        UniqueConstraint("DATA_ID", "TEAM_ID", name="uq_coordination_procurement_data_team"),
    )

    id = Column("ID", Integer, primary_key=True, index=True)
    data_id = Column("DATA_ID", Integer, ForeignKey("COORDINATION_PROCUREMENT_DATA.ID"), nullable=False, index=True)
    team_id = Column("TEAM_ID", Integer, ForeignKey("PERSON_TEAM.ID"), nullable=False, index=True)
    pos = Column("POS", Integer, nullable=False, default=0)
    changed_by_id = Column("CHANGED_BY", Integer, ForeignKey("USER.ID"), nullable=True)
    created_by_id = Column("CREATED_BY", Integer, ForeignKey("USER.ID"), nullable=True)
    created_at = Column("CREATED_AT", DateTime(timezone=True), server_default=func.now())
    updated_at = Column("UPDATED_AT", DateTime(timezone=True), onupdate=func.now())

    data_row = relationship("CoordinationProcurementData", back_populates="teams")
    team = relationship("PersonTeam")
    changed_by_user = relationship("User", foreign_keys=[changed_by_id])
    created_by_user = relationship("User", foreign_keys=[created_by_id])


class CoordinationProcurementTypedData(Base):
    """Typed runtime procurement data row per coordination, organ and slot."""

    __tablename__ = "COORDINATION_PROCUREMENT_TYPED_DATA"
    __table_args__ = (
        UniqueConstraint(
            "COORDINATION_ID",
            "ORGAN_ID",
            "SLOT_KEY",
            name="uq_coordination_procurement_typed_data",
        ),
    )

    id = Column("ID", Integer, primary_key=True, index=True)
    coordination_id = Column("COORDINATION_ID", Integer, ForeignKey("COORDINATION.ID"), nullable=False, index=True)
    organ_id = Column("ORGAN_ID", Integer, ForeignKey("CODE.ID"), nullable=False, index=True)
    slot_key = Column(
        "SLOT_KEY",
        SqlEnum(
            ProcurementSlotKey,
            native_enum=False,
            validate_strings=True,
            values_callable=lambda enum_cls: [entry.value for entry in enum_cls],
            length=16,
        ),
        nullable=False,
        default=ProcurementSlotKey.MAIN.value,
    )

    # Explicit typed procurement attributes (catalog-backed).
    incision_time = Column("INCISION_TIME", DateTime(timezone=True), nullable=True)
    cardiac_arrest_time = Column("CARDIAC_ARREST_TIME", DateTime(timezone=True), nullable=True)
    cold_perfusion = Column("COLD_PERFUSION", DateTime(timezone=True), nullable=True)
    cold_perfusion_abdominal = Column("COLD_PERFUSION_ABDOMINAL", DateTime(timezone=True), nullable=True)
    ehb_box_nr = Column("EHB_BOX_NR", String, nullable=False, default="")
    ehb_nr = Column("EHB_NR", String, nullable=False, default="")
    incision_donor_time = Column("INCISION_DONOR_TIME", DateTime(timezone=True), nullable=True)
    nmp_used = Column("NMP_USED", Boolean, nullable=True, default=None)
    cross_clamp_time = Column("CROSS_CLAMP_TIME", DateTime(timezone=True), nullable=True)
    procurement_team_departure_time = Column("PROCUREMENT_TEAM_DEPARTURE_TIME", DateTime(timezone=True), nullable=True)
    evlp_used = Column("EVLP_USED", Boolean, nullable=True, default=None)
    departure_donor_time = Column("DEPARTURE_DONOR_TIME", DateTime(timezone=True), nullable=True)
    hope_used = Column("HOPE_USED", Boolean, nullable=True, default=None)
    arrival_time = Column("ARRIVAL_TIME", DateTime(timezone=True), nullable=True)
    lifeport_used = Column("LIFEPORT_USED", Boolean, nullable=True, default=None)

    # Explicit single-reference attributes.
    arzt_responsible_person_id = Column("ARZT_RESPONSIBLE_PERSON_ID", Integer, ForeignKey("PERSON.ID"), nullable=True, index=True)
    chirurg_responsible_person_id = Column("CHIRURG_RESPONSIBLE_PERSON_ID", Integer, ForeignKey("PERSON.ID"), nullable=True, index=True)
    procurment_team_team_id = Column("PROCURMENT_TEAM_TEAM_ID", Integer, ForeignKey("PERSON_TEAM.ID"), nullable=True, index=True)
    recipient_episode_id = Column("RECIPIENT_EPISODE_ID", Integer, ForeignKey("EPISODE.ID"), nullable=True, index=True)

    changed_by_id = Column("CHANGED_BY", Integer, ForeignKey("USER.ID"), nullable=True)
    created_by_id = Column("CREATED_BY", Integer, ForeignKey("USER.ID"), nullable=True)
    created_at = Column("CREATED_AT", DateTime(timezone=True), server_default=func.now())
    updated_at = Column("UPDATED_AT", DateTime(timezone=True), onupdate=func.now())

    coordination = relationship("Coordination")
    organ = relationship("Code", foreign_keys=[organ_id])
    arzt_responsible_person = relationship("Person", foreign_keys=[arzt_responsible_person_id])
    chirurg_responsible_person = relationship("Person", foreign_keys=[chirurg_responsible_person_id])
    procurment_team_team = relationship("PersonTeam", foreign_keys=[procurment_team_team_id])
    recipient_episode = relationship("Episode", foreign_keys=[recipient_episode_id])
    changed_by_user = relationship("User", foreign_keys=[changed_by_id])
    created_by_user = relationship("User", foreign_keys=[created_by_id])
    person_lists = relationship(
        "CoordinationProcurementTypedDataPersonList",
        back_populates="data_row",
        cascade="all, delete-orphan",
    )
    team_lists = relationship(
        "CoordinationProcurementTypedDataTeamList",
        back_populates="data_row",
        cascade="all, delete-orphan",
    )


class CoordinationProcurementTypedDataPersonList(Base):
    """Typed person-list references attached to a typed procurement data row."""

    __tablename__ = "COORDINATION_PROCUREMENT_TYPED_DATA_PERSON_LIST"
    __table_args__ = (
        UniqueConstraint("DATA_ID", "LIST_KEY", "PERSON_ID", name="uq_coordination_procurement_typed_data_person"),
    )

    id = Column("ID", Integer, primary_key=True, index=True)
    data_id = Column("DATA_ID", Integer, ForeignKey("COORDINATION_PROCUREMENT_TYPED_DATA.ID"), nullable=False, index=True)
    list_key = Column(
        "LIST_KEY",
        SqlEnum(
            ProcurementPersonListKey,
            native_enum=False,
            validate_strings=True,
            values_callable=lambda enum_cls: [entry.value for entry in enum_cls],
            length=32,
        ),
        nullable=False,
    )
    person_id = Column("PERSON_ID", Integer, ForeignKey("PERSON.ID"), nullable=False, index=True)
    pos = Column("POS", Integer, nullable=False, default=0)
    changed_by_id = Column("CHANGED_BY", Integer, ForeignKey("USER.ID"), nullable=True)
    created_by_id = Column("CREATED_BY", Integer, ForeignKey("USER.ID"), nullable=True)
    created_at = Column("CREATED_AT", DateTime(timezone=True), server_default=func.now())
    updated_at = Column("UPDATED_AT", DateTime(timezone=True), onupdate=func.now())

    data_row = relationship("CoordinationProcurementTypedData", back_populates="person_lists")
    person = relationship("Person")
    changed_by_user = relationship("User", foreign_keys=[changed_by_id])
    created_by_user = relationship("User", foreign_keys=[created_by_id])


class CoordinationProcurementTypedDataTeamList(Base):
    """Typed team-list references attached to a typed procurement data row."""

    __tablename__ = "COORDINATION_PROCUREMENT_TYPED_DATA_TEAM_LIST"
    __table_args__ = (
        UniqueConstraint("DATA_ID", "LIST_KEY", "TEAM_ID", name="uq_coordination_procurement_typed_data_team"),
    )

    id = Column("ID", Integer, primary_key=True, index=True)
    data_id = Column("DATA_ID", Integer, ForeignKey("COORDINATION_PROCUREMENT_TYPED_DATA.ID"), nullable=False, index=True)
    list_key = Column(
        "LIST_KEY",
        SqlEnum(
            ProcurementTeamListKey,
            native_enum=False,
            validate_strings=True,
            values_callable=lambda enum_cls: [entry.value for entry in enum_cls],
            length=32,
        ),
        nullable=False,
    )
    team_id = Column("TEAM_ID", Integer, ForeignKey("PERSON_TEAM.ID"), nullable=False, index=True)
    pos = Column("POS", Integer, nullable=False, default=0)
    changed_by_id = Column("CHANGED_BY", Integer, ForeignKey("USER.ID"), nullable=True)
    created_by_id = Column("CREATED_BY", Integer, ForeignKey("USER.ID"), nullable=True)
    created_at = Column("CREATED_AT", DateTime(timezone=True), server_default=func.now())
    updated_at = Column("UPDATED_AT", DateTime(timezone=True), onupdate=func.now())

    data_row = relationship("CoordinationProcurementTypedData", back_populates="team_lists")
    team = relationship("PersonTeam")
    changed_by_user = relationship("User", foreign_keys=[changed_by_id])
    created_by_user = relationship("User", foreign_keys=[created_by_id])


class CoordinationProcurementFieldGroupTemplate(Base):
    """Template grouping for procurement field rendering and grouped capture."""

    __tablename__ = "COORDINATION_PROCUREMENT_FIELD_GROUP_TEMPLATE"

    id = Column("ID", Integer, primary_key=True, index=True)
    key = Column("KEY", String(64), nullable=False, unique=True, index=True)
    name_default = Column("NAME_DEFAULT", String(128), nullable=False, default="")
    comment = Column("COMMENT", String(512), nullable=False, default="")
    is_active = Column("IS_ACTIVE", Boolean, nullable=False, default=True)
    display_lane = Column("DISPLAY_LANE", String(16), nullable=False, default="PRIMARY")
    pos = Column("POS", Integer, nullable=False, default=0)
    changed_by_id = Column("CHANGED_BY", Integer, ForeignKey("USER.ID"), nullable=True)
    created_by_id = Column("CREATED_BY", Integer, ForeignKey("USER.ID"), nullable=True)
    created_at = Column("CREATED_AT", DateTime(timezone=True), server_default=func.now())
    updated_at = Column("UPDATED_AT", DateTime(timezone=True), onupdate=func.now())

    changed_by_user = relationship("User", foreign_keys=[changed_by_id])
    created_by_user = relationship("User", foreign_keys=[created_by_id])
    field_templates = relationship("CoordinationProcurementFieldTemplate", back_populates="group_template")


class CoordinationProcurementProtocolTaskGroupSelection(Base):
    """Overlay config selecting protocol task-group templates and their display order."""

    __tablename__ = "COORDINATION_PROCUREMENT_PROTOCOL_TASK_GROUP_SELECTION"
    __table_args__ = (
        UniqueConstraint(
            "TASK_GROUP_TEMPLATE_ID",
            "ORGAN_ID",
            name="uq_coordination_procurement_protocol_task_group_selection",
        ),
    )

    id = Column("ID", Integer, primary_key=True, index=True)
    task_group_template_id = Column(
        "TASK_GROUP_TEMPLATE_ID",
        Integer,
        ForeignKey("TASK_GROUP_TEMPLATE.ID"),
        nullable=False,
        index=True,
    )
    organ_id = Column("ORGAN_ID", Integer, ForeignKey("CODE.ID"), nullable=True, index=True)
    pos = Column("POS", Integer, nullable=False, default=0)
    changed_by_id = Column("CHANGED_BY", Integer, ForeignKey("USER.ID"), nullable=True)
    created_by_id = Column("CREATED_BY", Integer, ForeignKey("USER.ID"), nullable=True)
    created_at = Column("CREATED_AT", DateTime(timezone=True), server_default=func.now())
    updated_at = Column("UPDATED_AT", DateTime(timezone=True), onupdate=func.now())

    task_group_template = relationship("TaskGroupTemplate")
    organ = relationship("Code", foreign_keys=[organ_id])
    changed_by_user = relationship("User", foreign_keys=[changed_by_id])
    created_by_user = relationship("User", foreign_keys=[created_by_id])
