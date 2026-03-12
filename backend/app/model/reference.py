from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..database import Base


class Code(Base):
    """Reference code table for typed key/value dictionaries."""

    __tablename__ = "CODE"
    __table_args__ = (UniqueConstraint("TYPE", "KEY"),)

    id = Column(
        "ID",
        Integer,
        primary_key=True,
        index=True,
        comment="Technical primary key of the code entry.",
        info={"label": "ID"},
    )
    type = Column(
        "TYPE",
        String,
        nullable=False,
        index=True,
        comment="Logical code namespace (e.g. DATATYPE, ROLE, ORGAN).",
        info={"label": "Code Type"},
    )
    key = Column(
        "KEY",
        String,
        nullable=False,
        comment="Stable technical key unique within a type.",
        info={"label": "Key"},
    )
    pos = Column(
        "POS",
        Integer,
        nullable=False,
        comment="Display/sort order inside one code type.",
        info={"label": "Position"},
    )
    ext_sys = Column(
        "EXT_SYS",
        String(24),
        default="",
        comment="Optional external source system identifier.",
        info={"label": "External System"},
    )
    ext_key = Column(
        "EXT_KEY",
        String,
        default="",
        comment="Optional key of this code in an external system.",
        info={"label": "External Key"},
    )
    name_default = Column(
        "NAME_DEFAULT",
        String,
        default="",
        comment="Default display name for the code entry.",
        info={"label": "Name"},
    )

    permissions = relationship("AccessPermission", secondary="ROLE_PERMISSION", back_populates="roles")


class Catalogue(Base):
    """Reference catalogue table for structured, maintainable value lists."""

    __tablename__ = "CATALOGUE"
    __table_args__ = (UniqueConstraint("TYPE", "KEY"),)

    id = Column(
        "ID",
        Integer,
        primary_key=True,
        index=True,
        comment="Technical primary key of the catalogue entry.",
        info={"label": "ID"},
    )
    type = Column(
        "TYPE",
        String,
        nullable=False,
        index=True,
        comment="Logical catalogue namespace (e.g. LANGUAGE, DIAGNOSIS, BLOOD_TYPE).",
        info={"label": "Catalogue Type"},
    )
    key = Column(
        "KEY",
        String,
        nullable=False,
        comment="Stable technical key unique within a catalogue type.",
        info={"label": "Key"},
    )
    pos = Column(
        "POS",
        Integer,
        nullable=False,
        comment="Display/sort order inside one catalogue type.",
        info={"label": "Position"},
    )
    ext_sys = Column(
        "EXT_SYS",
        String(24),
        default="",
        comment="Optional external source system identifier.",
        info={"label": "External System"},
    )
    ext_key = Column(
        "EXT_KEY",
        String,
        default="",
        comment="Optional key of this catalogue entry in an external system.",
        info={"label": "External Key"},
    )
    name_default = Column(
        "NAME_DEFAULT",
        String,
        default="",
        comment="Default display name for the catalogue entry.",
        info={"label": "Name"},
    )
    name_en = Column(
        "NAME_EN",
        String,
        default="",
        comment="English display name for the catalogue entry.",
        info={"label": "Name (EN)"},
    )
    name_de = Column(
        "NAME_DE",
        String,
        default="",
        comment="German display name for the catalogue entry.",
        info={"label": "Name (DE)"},
    )


class TranslationBundle(Base):
    """Admin-managed translation JSON bundle per locale."""

    __tablename__ = "TRANSLATION_BUNDLE"
    __table_args__ = (UniqueConstraint("LOCALE"),)

    id = Column("ID", Integer, primary_key=True, index=True)
    locale = Column("LOCALE", String(16), nullable=False, index=True)
    payload_json = Column("PAYLOAD_JSON", String, nullable=False, default="{}")
    changed_by_id = Column("CHANGED_BY", Integer, ForeignKey("USER.ID"), nullable=True)
    created_by_id = Column("CREATED_BY", Integer, ForeignKey("USER.ID"), nullable=True)
    created_at = Column("CREATED_AT", DateTime(timezone=True), server_default=func.now())
    updated_at = Column("UPDATED_AT", DateTime(timezone=True), onupdate=func.now())

    changed_by_user = relationship("User", foreign_keys=[changed_by_id])
    created_by_user = relationship("User", foreign_keys=[created_by_id])
