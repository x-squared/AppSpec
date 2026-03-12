from sqlalchemy import Boolean, Column, Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..database import Base


class Patient(Base):
    """Core patient entity with demographic, language, and linked clinical data."""

    __tablename__ = "PATIENT"

    id = Column(
        "ID",
        Integer,
        primary_key=True,
        index=True,
        comment="Technical primary key of the patient.",
        info={"label": "ID"},
    )
    pid = Column(
        "PID",
        String,
        nullable=False,
        unique=True,
        index=True,
        comment="Institution-specific patient identifier.",
        info={"label": "PID"},
    )
    first_name = Column(
        "FIRST_NAME",
        String,
        nullable=False,
        comment="Given name of the patient.",
        info={"label": "First Name"},
    )
    name = Column(
        "NAME",
        String,
        nullable=False,
        comment="Family name of the patient.",
        info={"label": "Name"},
    )
    date_of_birth = Column(
        "DATE_OF_BIRTH",
        Date,
        nullable=False,
        comment="Date of birth of the patient.",
        info={"label": "Date Of Birth"},
    )
    date_of_death = Column(
        "DATE_OF_DEATH",
        Date,
        nullable=True,
        comment="Date of death of the patient, if applicable.",
        info={"label": "Date Of Death"},
    )
    ahv_nr = Column(
        "AHV_NR",
        String,
        default="",
        comment="AHV insurance number of the patient.",
        info={"label": "AHV Nr."},
    )
    lang = Column(
        "LANG",
        String,
        default="",
        comment="Preferred language code of the patient.",
        info={"label": "Language"},
    )
    sex_id = Column(
        "SEX",
        Integer,
        ForeignKey("CODE.ID"),
        nullable=True,
        comment="Sex reference (`CODE.SEX`).",
        info={"label": "Sex"},
    )
    resp_coord_id = Column(
        "RESP_COORD",
        Integer,
        ForeignKey("USER.ID"),
        nullable=True,
        comment="Responsible coordinator user reference.",
        info={"label": "Responsible Coordinator"},
    )
    translate = Column(
        "TRANSLATE",
        Boolean,
        default=False,
        comment="Whether translation support is required for this patient.",
        info={"label": "Translate"},
    )
    changed_by_id = Column(
        "CHANGED_BY",
        Integer,
        ForeignKey("USER.ID"),
        nullable=True,
        comment="Last user who changed the patient.",
        info={"label": "Changed By"},
    )
    created_by_id = Column(
        "CREATED_BY",
        Integer,
        ForeignKey("USER.ID"),
        nullable=True,
        comment="User who created the patient.",
        info={"label": "Created By"},
    )
    created_at = Column(
        "CREATED_AT",
        DateTime(timezone=True),
        server_default=func.now(),
        comment="Creation timestamp of the patient row.",
        info={"label": "Created At"},
    )
    updated_at = Column(
        "UPDATED_AT",
        DateTime(timezone=True),
        onupdate=func.now(),
        comment="Last update timestamp of the patient row.",
        info={"label": "Updated At"},
    )

    changed_by_user = relationship("User", foreign_keys=[changed_by_id])
    created_by_user = relationship("User", foreign_keys=[created_by_id])
    sex = relationship("Code", foreign_keys=[sex_id])
    resp_coord = relationship("User", foreign_keys=[resp_coord_id])
    contact_infos = relationship("ContactInfo", back_populates="patient", cascade="all, delete-orphan")
    absences = relationship("Absence", back_populates="patient", cascade="all, delete-orphan")
    diagnoses = relationship("Diagnosis", back_populates="patient", cascade="all, delete-orphan")
    medical_values = relationship("MedicalValue", back_populates="patient", cascade="all, delete-orphan")
    episodes = relationship("Episode", back_populates="patient", cascade="all, delete-orphan")
    task_groups = relationship("TaskGroup", back_populates="patient", cascade="all, delete-orphan")


class Absence(Base):
    """Date interval where the patient is marked as absent."""

    __tablename__ = "ABSENCE"

    id = Column(
        "ID",
        Integer,
        primary_key=True,
        index=True,
        comment="Technical primary key of the absence.",
        info={"label": "ID"},
    )
    patient_id = Column(
        "PATIENT_ID",
        Integer,
        ForeignKey("PATIENT.ID"),
        nullable=False,
        index=True,
        comment="Patient reference owning this absence interval.",
        info={"label": "Patient"},
    )
    start = Column(
        "START",
        Date,
        nullable=False,
        comment="Start date of the absence.",
        info={"label": "Start"},
    )
    end = Column(
        "END",
        Date,
        nullable=False,
        comment="End date of the absence.",
        info={"label": "End"},
    )
    comment = Column(
        "COMMENT",
        String(1024),
        default="",
        comment="Optional free-text note for the absence.",
        info={"label": "Comment"},
    )
    changed_by_id = Column(
        "CHANGED_BY",
        Integer,
        ForeignKey("USER.ID"),
        nullable=True,
        comment="Last user who changed the absence.",
        info={"label": "Changed By"},
    )
    created_by_id = Column(
        "CREATED_BY",
        Integer,
        ForeignKey("USER.ID"),
        nullable=True,
        comment="User who created the absence.",
        info={"label": "Created By"},
    )
    created_at = Column(
        "CREATED_AT",
        DateTime(timezone=True),
        server_default=func.now(),
        comment="Creation timestamp of the absence row.",
        info={"label": "Created At"},
    )
    updated_at = Column(
        "UPDATED_AT",
        DateTime(timezone=True),
        onupdate=func.now(),
        comment="Last update timestamp of the absence row.",
        info={"label": "Updated At"},
    )

    patient = relationship("Patient", back_populates="absences")
    changed_by_user = relationship("User", foreign_keys=[changed_by_id])
    created_by_user = relationship("User", foreign_keys=[created_by_id])


class Diagnosis(Base):
    """Patient diagnosis linked to diagnosis catalogue entries."""

    __tablename__ = "DIAGNOSIS"

    id = Column(
        "ID",
        Integer,
        primary_key=True,
        index=True,
        comment="Technical primary key of the diagnosis row.",
        info={"label": "ID"},
    )
    patient_id = Column(
        "PATIENT_ID",
        Integer,
        ForeignKey("PATIENT.ID"),
        nullable=False,
        index=True,
        comment="Patient reference owning this diagnosis.",
        info={"label": "Patient"},
    )
    catalogue_id = Column(
        "CATALOGUE_ID",
        Integer,
        ForeignKey("CATALOGUE.ID"),
        nullable=False,
        comment="Diagnosis catalogue reference (`CATALOGUE.DIAGNOSIS`).",
        info={"label": "Diagnosis Catalogue"},
    )
    comment = Column(
        "COMMENT",
        String(128),
        default="",
        comment="Optional diagnosis note.",
        info={"label": "Comment"},
    )
    is_main = Column(
        "IS_MAIN",
        Boolean,
        default=False,
        nullable=False,
        comment="Whether this diagnosis is flagged as the main diagnosis.",
        info={"label": "Main"},
    )
    changed_by_id = Column(
        "CHANGED_BY",
        Integer,
        ForeignKey("USER.ID"),
        nullable=True,
        comment="Last user who changed the diagnosis.",
        info={"label": "Changed By"},
    )
    created_by_id = Column(
        "CREATED_BY",
        Integer,
        ForeignKey("USER.ID"),
        nullable=True,
        comment="User who created the diagnosis.",
        info={"label": "Created By"},
    )
    created_at = Column(
        "CREATED_AT",
        DateTime(timezone=True),
        server_default=func.now(),
        comment="Creation timestamp of the diagnosis row.",
        info={"label": "Created At"},
    )
    updated_at = Column(
        "UPDATED_AT",
        DateTime(timezone=True),
        onupdate=func.now(),
        comment="Last update timestamp of the diagnosis row.",
        info={"label": "Updated At"},
    )

    patient = relationship("Patient", back_populates="diagnoses")
    catalogue = relationship("Catalogue")
    changed_by_user = relationship("User", foreign_keys=[changed_by_id])
    created_by_user = relationship("User", foreign_keys=[created_by_id])


class ContactInfo(Base):
    """Patient contact channel row including type, value, and sort position."""

    __tablename__ = "CONTACT_INFO"

    id = Column(
        "ID",
        Integer,
        primary_key=True,
        index=True,
        comment="Technical primary key of the contact info row.",
        info={"label": "ID"},
    )
    patient_id = Column(
        "PATIENT_ID",
        Integer,
        ForeignKey("PATIENT.ID"),
        nullable=False,
        index=True,
        comment="Patient reference owning this contact row.",
        info={"label": "Patient"},
    )
    type_id = Column(
        "TYPE_ID",
        Integer,
        ForeignKey("CODE.ID"),
        nullable=False,
        comment="Contact channel type (`CODE.CONTACT_INFO_TYPE`).",
        info={"label": "Contact Type"},
    )
    data = Column(
        "DATA",
        String(128),
        nullable=False,
        comment="Contact value, e.g. phone number or email.",
        info={"label": "Data"},
    )
    comment = Column(
        "COMMENT",
        String(128),
        default="",
        comment="Optional contact note.",
        info={"label": "Comment"},
    )
    main = Column(
        "MAIN",
        Boolean,
        default=False,
        comment="Marks this row as the preferred main contact.",
        info={"label": "Main"},
    )
    pos = Column(
        "POS",
        Integer,
        default=0,
        comment="Sort position for displaying contact rows.",
        info={"label": "Position"},
    )
    changed_by_id = Column(
        "CHANGED_BY",
        Integer,
        ForeignKey("USER.ID"),
        nullable=True,
        comment="Last user who changed the contact info.",
        info={"label": "Changed By"},
    )
    created_by_id = Column(
        "CREATED_BY",
        Integer,
        ForeignKey("USER.ID"),
        nullable=True,
        comment="User who created the contact info.",
        info={"label": "Created By"},
    )
    created_at = Column(
        "CREATED_AT",
        DateTime(timezone=True),
        server_default=func.now(),
        comment="Creation timestamp of the contact info row.",
        info={"label": "Created At"},
    )
    updated_at = Column(
        "UPDATED_AT",
        DateTime(timezone=True),
        onupdate=func.now(),
        comment="Last update timestamp of the contact info row.",
        info={"label": "Updated At"},
    )

    patient = relationship("Patient", back_populates="contact_infos")
    type = relationship("Code")
    changed_by_user = relationship("User", foreign_keys=[changed_by_id])
    created_by_user = relationship("User", foreign_keys=[created_by_id])
