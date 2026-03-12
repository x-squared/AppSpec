from sqlalchemy import Column, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..database import Base


class CoordinationOrigin(Base):
    """Origin-specific 1:1 extension of the coordination core entity."""

    __tablename__ = "COORDINATION_ORIGIN"

    id = Column(
        "ID",
        Integer,
        primary_key=True,
        index=True,
        comment="Technical primary key of the coordination origin row.",
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
    detection_hospital_id = Column(
        "DETECTION_HOSPITAL",
        Integer,
        ForeignKey("CATALOGUE.ID"),
        nullable=True,
        comment="Detection hospital reference (`CATALOGUE.HOSPITAL`).",
        info={"label": "Detection Hospital"},
    )
    procurement_hospital_id = Column(
        "PROCUREMENT_HOSPITAL",
        Integer,
        ForeignKey("CATALOGUE.ID"),
        nullable=True,
        comment="Procurement hospital reference (`CATALOGUE.HOSPITAL`).",
        info={"label": "Procurement Hospital"},
    )
    changed_by_id = Column(
        "CHANGED_BY",
        Integer,
        ForeignKey("USER.ID"),
        nullable=True,
        comment="Last user who changed the coordination origin row.",
        info={"label": "Changed By"},
    )
    created_by_id = Column(
        "CREATED_BY",
        Integer,
        ForeignKey("USER.ID"),
        nullable=True,
        comment="User who created the coordination origin row.",
        info={"label": "Created By"},
    )
    created_at = Column(
        "CREATED_AT",
        DateTime(timezone=True),
        server_default=func.now(),
        comment="Creation timestamp of the coordination origin row.",
        info={"label": "Created At"},
    )
    updated_at = Column(
        "UPDATED_AT",
        DateTime(timezone=True),
        onupdate=func.now(),
        comment="Last update timestamp of the coordination origin row.",
        info={"label": "Updated At"},
    )

    coordination = relationship("Coordination", back_populates="origin")
    detection_hospital = relationship("Catalogue", foreign_keys=[detection_hospital_id])
    procurement_hospital = relationship("Catalogue", foreign_keys=[procurement_hospital_id])
    changed_by_user = relationship("User", foreign_keys=[changed_by_id])
    created_by_user = relationship("User", foreign_keys=[created_by_id])
