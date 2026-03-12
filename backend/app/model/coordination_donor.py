from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..database import Base


class CoordinationDonor(Base):
    """Donor-specific 1:1 extension of the coordination core entity."""

    __tablename__ = "COORDINATION_DONOR"

    id = Column(
        "ID",
        Integer,
        primary_key=True,
        index=True,
        comment="Technical primary key of the coordination donor row.",
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
    full_name = Column(
        "FULL_NAME",
        String(128),
        default="",
        comment="Full donor name (max 128 characters).",
        info={"label": "Full Name"},
    )
    sex_id = Column(
        "SEX",
        Integer,
        ForeignKey("CODE.ID"),
        nullable=True,
        comment="Sex reference (`CODE.SEX`).",
        info={"label": "Sex"},
    )
    birth_date = Column(
        "BIRTH_DATE",
        Date,
        nullable=True,
        comment="Donor birth date.",
        info={"label": "Birth Date"},
    )
    blood_type_id = Column(
        "BLOOD_TYPE",
        Integer,
        ForeignKey("CODE.ID"),
        nullable=True,
        comment="Blood type reference (`CODE.BLOOD_TYPE`).",
        info={"label": "Blood Type"},
    )
    height = Column(
        "HEIGHT",
        Integer,
        nullable=True,
        comment="Height in centimeters.",
        info={"label": "Height (cm)"},
    )
    weight = Column(
        "WEIGHT",
        Integer,
        nullable=True,
        comment="Weight in kilograms.",
        info={"label": "Weight (kg)"},
    )
    organ_fo = Column(
        "ORGAN_FO",
        String(128),
        default="",
        comment="Organ FO free-text field (max 128 characters).",
        info={"label": "Organ FO"},
    )
    diagnosis_id = Column(
        "DIAGNOSIS",
        Integer,
        ForeignKey("CODE.ID"),
        nullable=True,
        comment="Diagnosis reference (`CODE.DIAGNOSIS_DONOR`).",
        info={"label": "Diagnosis"},
    )
    death_kind_id = Column(
        "DEATH_KIND",
        Integer,
        ForeignKey("CODE.ID"),
        nullable=True,
        comment="Death kind reference (`CODE.DEATH_KIND`).",
        info={"label": "Death Kind"},
    )
    changed_by_id = Column(
        "CHANGED_BY",
        Integer,
        ForeignKey("USER.ID"),
        nullable=True,
        comment="Last user who changed the coordination donor row.",
        info={"label": "Changed By"},
    )
    created_by_id = Column(
        "CREATED_BY",
        Integer,
        ForeignKey("USER.ID"),
        nullable=True,
        comment="User who created the coordination donor row.",
        info={"label": "Created By"},
    )
    created_at = Column(
        "CREATED_AT",
        DateTime(timezone=True),
        server_default=func.now(),
        comment="Creation timestamp of the coordination donor row.",
        info={"label": "Created At"},
    )
    updated_at = Column(
        "UPDATED_AT",
        DateTime(timezone=True),
        onupdate=func.now(),
        comment="Last update timestamp of the coordination donor row.",
        info={"label": "Updated At"},
    )

    coordination = relationship("Coordination", back_populates="donor")
    sex = relationship("Code", foreign_keys=[sex_id])
    blood_type = relationship("Code", foreign_keys=[blood_type_id])
    diagnosis = relationship("Code", foreign_keys=[diagnosis_id])
    death_kind = relationship("Code", foreign_keys=[death_kind_id])
    changed_by_user = relationship("User", foreign_keys=[changed_by_id])
    created_by_user = relationship("User", foreign_keys=[created_by_id])
