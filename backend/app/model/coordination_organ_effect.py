from sqlalchemy import Column, DateTime, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..database import Base


class CoordinationOrganEffect(Base):
    """Per-organ procurement effect rows for a coordination case."""

    __tablename__ = "COORDINATION_ORGAN_EFFECT"
    __table_args__ = (
        UniqueConstraint(
            "COORDINATION_ID",
            "ORGAN",
            name="uq_coordination_organ_effect_coordination_organ",
        ),
    )

    id = Column(
        "ID",
        Integer,
        primary_key=True,
        index=True,
        comment="Technical primary key of the coordination organ effect row.",
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
    organ_id = Column(
        "ORGAN",
        Integer,
        ForeignKey("CODE.ID"),
        nullable=False,
        comment="Organ reference (`CODE.ORGAN`).",
        info={"label": "Organ"},
    )
    procurement_effect_id = Column(
        "PROCUREMENT_EFFECT",
        Integer,
        ForeignKey("CODE.ID"),
        nullable=True,
        comment="Procurement effect reference (`CODE.PROCUREMENT_EFFECT`).",
        info={"label": "Procurement Effect"},
    )
    changed_by_id = Column(
        "CHANGED_BY",
        Integer,
        ForeignKey("USER.ID"),
        nullable=True,
        comment="Last user who changed the coordination organ effect row.",
        info={"label": "Changed By"},
    )
    created_by_id = Column(
        "CREATED_BY",
        Integer,
        ForeignKey("USER.ID"),
        nullable=True,
        comment="User who created the coordination organ effect row.",
        info={"label": "Created By"},
    )
    created_at = Column(
        "CREATED_AT",
        DateTime(timezone=True),
        server_default=func.now(),
        comment="Creation timestamp of the coordination organ effect row.",
        info={"label": "Created At"},
    )
    updated_at = Column(
        "UPDATED_AT",
        DateTime(timezone=True),
        onupdate=func.now(),
        comment="Last update timestamp of the coordination organ effect row.",
        info={"label": "Updated At"},
    )

    coordination = relationship("Coordination", back_populates="organ_effects")
    organ = relationship("Code", foreign_keys=[organ_id])
    procurement_effect = relationship("Code", foreign_keys=[procurement_effect_id])
    changed_by_user = relationship("User", foreign_keys=[changed_by_id])
    created_by_user = relationship("User", foreign_keys=[created_by_id])
