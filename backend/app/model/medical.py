from sqlalchemy import Boolean, Column, Date, DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..database import Base


class MedicalValueGroupTemplate(Base):
    """Template definition of a named medical-value group/bunch."""

    __tablename__ = "MEDICAL_VALUE_GROUP"

    id = Column(
        "ID",
        Integer,
        primary_key=True,
        index=True,
        comment="Technical primary key of the medical value group.",
        info={"label": "ID"},
    )
    key = Column(
        "KEY",
        String(48),
        nullable=False,
        unique=True,
        comment="Stable key identifier of the medical value group.",
        info={"label": "Key"},
    )
    name_default = Column(
        "NAME_DEFAULT",
        String(128),
        nullable=False,
        default="",
        comment="Display label of the medical value group.",
        info={"label": "Name"},
    )
    pos = Column(
        "POS",
        Integer,
        nullable=False,
        default=0,
        comment="Sort position of the medical value group.",
        info={"label": "Position"},
    )
    renew_date = Column(
        "RENEW_DATE",
        Date,
        nullable=True,
        comment="Optional group-level renewal date.",
        info={"label": "Renew Date"},
    )
    changed_by_id = Column(
        "CHANGED_BY",
        Integer,
        ForeignKey("USER.ID"),
        nullable=True,
        comment="Last user who changed the medical value group.",
        info={"label": "Changed By"},
    )
    created_by_id = Column(
        "CREATED_BY",
        Integer,
        ForeignKey("USER.ID"),
        nullable=True,
        comment="User who created the medical value group.",
        info={"label": "Created By"},
    )
    created_at = Column(
        "CREATED_AT",
        DateTime(timezone=True),
        server_default=func.now(),
        comment="Creation timestamp of the medical value group row.",
        info={"label": "Created At"},
    )
    updated_at = Column(
        "UPDATED_AT",
        DateTime(timezone=True),
        onupdate=func.now(),
        comment="Last update timestamp of the medical value group row.",
        info={"label": "Updated At"},
    )

    changed_by_user = relationship("User", foreign_keys=[changed_by_id])
    created_by_user = relationship("User", foreign_keys=[created_by_id])
    context_templates = relationship(
        "MedicalValueGroupContextTemplate",
        back_populates="medical_value_group_template",
        cascade="all, delete-orphan",
    )


class MedicalValueTemplate(Base):
    """Template definition for medical values."""

    __tablename__ = "MEDICAL_VALUE_TEMPLATE"

    id = Column(
        "ID",
        Integer,
        primary_key=True,
        index=True,
        comment="Technical primary key of the medical value template.",
        info={"label": "ID"},
    )
    lab_key = Column(
        "LAB_KEY",
        String(12),
        nullable=False,
        comment="Laboratory key used to map incoming values.",
        info={"label": "Lab Key"},
    )
    kis_key = Column(
        "KIS_KEY",
        String(64),
        nullable=False,
        comment="KIS key used to map values from clinical systems.",
        info={"label": "KIS Key"},
    )
    loinc_code = Column(
        "LOINC_CODE",
        String(32),
        nullable=True,
        index=True,
        comment="Optional LOINC code identifying the observation concept.",
        info={"label": "LOINC Code"},
    )
    loinc_display_name = Column(
        "LOINC_DISPLAY_NAME",
        String(128),
        nullable=True,
        comment="Optional display title for the configured LOINC code.",
        info={"label": "LOINC Display Name"},
    )
    datatype_id = Column(
        "DATATYPE_ID",
        Integer,
        ForeignKey("CODE.ID"),
        nullable=False,
        comment="Data type reference (`CODE.DATATYPE`) of this template.",
        info={"label": "Datatype"},
    )
    name_default = Column(
        "NAME_DEFAULT",
        String(64),
        default="",
        comment="Default display name of the template.",
        info={"label": "Name"},
    )
    pos = Column(
        "POS",
        Integer,
        nullable=False,
        comment="Sort position among templates.",
        info={"label": "Position"},
    )
    is_main = Column(
        "IS_MAIN",
        Boolean,
        nullable=False,
        default=False,
        comment="Whether this template is highlighted as a primary medical value.",
        info={"label": "Main"},
    )
    medical_value_group_id = Column(
        "MEDICAL_VALUE_GROUP_ID",
        Integer,
        ForeignKey("MEDICAL_VALUE_GROUP.ID"),
        nullable=True,
        comment="Optional default group/bunch reference for this template.",
        info={"label": "Medical Value Group"},
    )
    datatype_def_id = Column(
        "DATATYPE_DEF_ID",
        Integer,
        ForeignKey("MEDICAL_VALUE_DATATYPE.ID"),
        nullable=True,
        comment="Optional explicit datatype-definition row for metadata-driven rendering.",
        info={"label": "Datatype Definition"},
    )

    datatype = relationship("Code", foreign_keys=[datatype_id])
    datatype_definition = relationship("DatatypeDefinition")
    medical_value_group_template = relationship("MedicalValueGroupTemplate")
    context_templates = relationship(
        "MedicalValueTemplateContextTemplate",
        back_populates="medical_value_template",
        cascade="all, delete-orphan",
    )


class MedicalValueGroupContextTemplate(Base):
    """Applicability context template for group templates (STATIC, DONOR, ORGAN)."""

    __tablename__ = "MEDICAL_VALUE_GROUP_CONTEXT_TEMPLATE"
    __table_args__ = (
        UniqueConstraint("MEDICAL_VALUE_GROUP_ID", "CONTEXT_KIND", "ORGAN_ID"),
    )

    id = Column("ID", Integer, primary_key=True, index=True)
    medical_value_group_id = Column("MEDICAL_VALUE_GROUP_ID", Integer, ForeignKey("MEDICAL_VALUE_GROUP.ID"), nullable=False, index=True)
    context_kind = Column("CONTEXT_KIND", String(16), nullable=False)
    organ_id = Column("ORGAN_ID", Integer, ForeignKey("CODE.ID"), nullable=True, index=True)
    changed_by_id = Column("CHANGED_BY", Integer, ForeignKey("USER.ID"), nullable=True)
    created_by_id = Column("CREATED_BY", Integer, ForeignKey("USER.ID"), nullable=True)
    created_at = Column("CREATED_AT", DateTime(timezone=True), server_default=func.now())
    updated_at = Column("UPDATED_AT", DateTime(timezone=True), onupdate=func.now())

    medical_value_group_template = relationship("MedicalValueGroupTemplate", back_populates="context_templates")
    organ = relationship("Code", foreign_keys=[organ_id])
    changed_by_user = relationship("User", foreign_keys=[changed_by_id])
    created_by_user = relationship("User", foreign_keys=[created_by_id])


class MedicalValueTemplateContextTemplate(Base):
    """Applicability context template for value templates (STATIC, DONOR, ORGAN)."""

    __tablename__ = "MEDICAL_VALUE_TEMPLATE_CONTEXT_TEMPLATE"
    __table_args__ = (
        UniqueConstraint("MEDICAL_VALUE_TEMPLATE_ID", "CONTEXT_KIND", "ORGAN_ID"),
    )

    id = Column("ID", Integer, primary_key=True, index=True)
    medical_value_template_id = Column("MEDICAL_VALUE_TEMPLATE_ID", Integer, ForeignKey("MEDICAL_VALUE_TEMPLATE.ID"), nullable=False, index=True)
    context_kind = Column("CONTEXT_KIND", String(16), nullable=False)
    organ_id = Column("ORGAN_ID", Integer, ForeignKey("CODE.ID"), nullable=True, index=True)
    changed_by_id = Column("CHANGED_BY", Integer, ForeignKey("USER.ID"), nullable=True)
    created_by_id = Column("CREATED_BY", Integer, ForeignKey("USER.ID"), nullable=True)
    created_at = Column("CREATED_AT", DateTime(timezone=True), server_default=func.now())
    updated_at = Column("UPDATED_AT", DateTime(timezone=True), onupdate=func.now())

    medical_value_template = relationship("MedicalValueTemplate", back_populates="context_templates")
    organ = relationship("Code", foreign_keys=[organ_id])
    changed_by_user = relationship("User", foreign_keys=[changed_by_id])
    created_by_user = relationship("User", foreign_keys=[created_by_id])


class MedicalValueGroup(Base):
    """Per-patient, per-context runtime group instance derived from group template."""

    __tablename__ = "MEDICAL_VALUE_GROUP_INSTANCE"
    __table_args__ = (
        UniqueConstraint("PATIENT_ID", "MEDICAL_VALUE_GROUP_ID", "CONTEXT_KEY"),
    )

    id = Column("ID", Integer, primary_key=True, index=True)
    patient_id = Column("PATIENT_ID", Integer, ForeignKey("PATIENT.ID"), nullable=False, index=True)
    medical_value_group_id = Column("MEDICAL_VALUE_GROUP_ID", Integer, ForeignKey("MEDICAL_VALUE_GROUP.ID"), nullable=False, index=True)
    context_key = Column("CONTEXT_KEY", String(128), nullable=False, index=True)
    episode_id = Column("EPISODE_ID", Integer, ForeignKey("EPISODE.ID"), nullable=True, index=True)
    organ_id = Column("ORGAN_ID", Integer, ForeignKey("CODE.ID"), nullable=True, index=True)
    is_donor_context = Column("IS_DONOR_CONTEXT", Boolean, nullable=False, default=False)
    renew_date = Column("RENEW_DATE", Date, nullable=True)
    changed_by_id = Column("CHANGED_BY", Integer, ForeignKey("USER.ID"), nullable=True)
    created_by_id = Column("CREATED_BY", Integer, ForeignKey("USER.ID"), nullable=True)
    created_at = Column("CREATED_AT", DateTime(timezone=True), server_default=func.now())
    updated_at = Column("UPDATED_AT", DateTime(timezone=True), onupdate=func.now())

    patient = relationship("Patient")
    medical_value_group_template = relationship("MedicalValueGroupTemplate")
    episode = relationship("Episode")
    organ = relationship("Code", foreign_keys=[organ_id])
    changed_by_user = relationship("User", foreign_keys=[changed_by_id])
    created_by_user = relationship("User", foreign_keys=[created_by_id])


class MedicalValue(Base):
    """Patient-specific medical value instance created from template or custom input."""

    __tablename__ = "MEDICAL_VALUE"

    id = Column(
        "ID",
        Integer,
        primary_key=True,
        index=True,
        comment="Technical primary key of the medical value.",
        info={"label": "ID"},
    )
    patient_id = Column(
        "PATIENT_ID",
        Integer,
        ForeignKey("PATIENT.ID"),
        nullable=False,
        index=True,
        comment="Patient reference owning this medical value.",
        info={"label": "Patient"},
    )
    medical_value_template_id = Column(
        "MEDICAL_VALUE_TEMPLATE_ID",
        Integer,
        ForeignKey("MEDICAL_VALUE_TEMPLATE.ID"),
        nullable=True,
        comment="Optional source template reference for this value.",
        info={"label": "Medical Value Template"},
    )
    datatype_id = Column(
        "DATATYPE_ID",
        Integer,
        ForeignKey("CODE.ID"),
        nullable=True,
        comment="Data type reference (`CODE.DATATYPE`) of this value.",
        info={"label": "Datatype"},
    )
    name = Column(
        "NAME",
        String(64),
        default="",
        comment="Display name of the medical value.",
        info={"label": "Name"},
    )
    pos = Column(
        "POS",
        Integer,
        default=0,
        comment="Sort position among patient medical values.",
        info={"label": "Position"},
    )
    value = Column(
        "VALUE",
        String,
        default="",
        comment="Stored value payload as text.",
        info={"label": "Value"},
    )
    value_input = Column(
        "VALUE_INPUT",
        String,
        default="",
        comment="Raw user-entered value before normalization.",
        info={"label": "Value Input"},
    )
    unit_input_ucum = Column(
        "UNIT_INPUT_UCUM",
        String(32),
        nullable=True,
        comment="UCUM unit used during value input.",
        info={"label": "Input Unit UCUM"},
    )
    value_canonical = Column(
        "VALUE_CANONICAL",
        String,
        default="",
        comment="Canonical value payload used for computations.",
        info={"label": "Canonical Value"},
    )
    unit_canonical_ucum = Column(
        "UNIT_CANONICAL_UCUM",
        String(32),
        nullable=True,
        comment="Canonical UCUM unit used for computations.",
        info={"label": "Canonical Unit UCUM"},
    )
    normalization_status = Column(
        "NORMALIZATION_STATUS",
        String(32),
        nullable=False,
        default="UNSPECIFIED",
        comment="Normalization state for this value payload.",
        info={"label": "Normalization Status"},
    )
    normalization_error = Column(
        "NORMALIZATION_ERROR",
        String(512),
        nullable=False,
        default="",
        comment="Normalization error details if normalization failed.",
        info={"label": "Normalization Error"},
    )
    renew_date = Column(
        "RENEW_DATE",
        Date,
        nullable=True,
        comment="Next renewal date for this medical value.",
        info={"label": "Renew Date"},
    )
    medical_value_group_id = Column(
        "MEDICAL_VALUE_GROUP_ID",
        Integer,
        ForeignKey("MEDICAL_VALUE_GROUP.ID"),
        nullable=True,
        comment="Optional group/bunch reference for this value.",
        info={"label": "Medical Value Group"},
    )
    medical_value_group_instance_id = Column(
        "MEDICAL_VALUE_GROUP_INSTANCE_ID",
        Integer,
        ForeignKey("MEDICAL_VALUE_GROUP_INSTANCE.ID"),
        nullable=True,
        index=True,
        comment="Runtime group-instance reference for this value/context.",
        info={"label": "Medical Value Group Instance"},
    )
    episode_id = Column(
        "EPISODE_ID",
        Integer,
        ForeignKey("EPISODE.ID"),
        nullable=True,
        index=True,
        comment="Optional episode context reference for this instantiated value.",
        info={"label": "Episode Context"},
    )
    organ_id = Column(
        "ORGAN_ID",
        Integer,
        ForeignKey("CODE.ID"),
        nullable=True,
        index=True,
        comment="Optional organ context reference for this instantiated value.",
        info={"label": "Organ Context"},
    )
    is_donor_context = Column(
        "IS_DONOR_CONTEXT",
        Boolean,
        nullable=False,
        default=False,
        comment="Marks value as instantiated for donor context.",
        info={"label": "Donor Context"},
    )
    context_key = Column(
        "CONTEXT_KEY",
        String(128),
        nullable=True,
        index=True,
        comment="Deterministic context key (e.g. STATIC, EPISODE:12:ORGAN:3, DONOR).",
        info={"label": "Context Key"},
    )
    changed_by_id = Column(
        "CHANGED_BY",
        Integer,
        ForeignKey("USER.ID"),
        nullable=True,
        comment="Last user who changed the medical value.",
        info={"label": "Changed By"},
    )
    created_by_id = Column(
        "CREATED_BY",
        Integer,
        ForeignKey("USER.ID"),
        nullable=True,
        comment="User who created the medical value.",
        info={"label": "Created By"},
    )
    created_at = Column(
        "CREATED_AT",
        DateTime(timezone=True),
        server_default=func.now(),
        comment="Creation timestamp of the medical value row.",
        info={"label": "Created At"},
    )
    updated_at = Column(
        "UPDATED_AT",
        DateTime(timezone=True),
        onupdate=func.now(),
        comment="Last update timestamp of the medical value row.",
        info={"label": "Updated At"},
    )

    patient = relationship("Patient", back_populates="medical_values")
    medical_value_template = relationship("MedicalValueTemplate")
    medical_value_group_template = relationship("MedicalValueGroupTemplate")
    medical_value_group = relationship("MedicalValueGroup")
    datatype = relationship("Code", foreign_keys=[datatype_id])
    episode = relationship("Episode")
    organ = relationship("Code", foreign_keys=[organ_id])
    changed_by_user = relationship("User", foreign_keys=[changed_by_id])
    created_by_user = relationship("User", foreign_keys=[created_by_id])
