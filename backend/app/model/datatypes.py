from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..database import Base


class DatatypeDefinition(Base):
    """Runtime datatype metadata for validation, formatting and catalogue binding."""

    __tablename__ = "MEDICAL_VALUE_DATATYPE"

    id = Column("ID", Integer, primary_key=True, index=True)
    code_id = Column("CODE_ID", Integer, ForeignKey("CODE.ID"), nullable=False, unique=True)
    primitive_kind = Column("PRIMITIVE_KIND", String(32), nullable=False, default="text")
    unit = Column("UNIT", String(32), nullable=True)
    canonical_unit_ucum = Column("CANONICAL_UNIT_UCUM", String(32), nullable=True)
    allowed_units_ucum_json = Column("ALLOWED_UNITS_UCUM_JSON", String(1024), nullable=True)
    conversion_group = Column("CONVERSION_GROUP", String(32), nullable=True)
    format_pattern = Column("FORMAT_PATTERN", String(128), nullable=True)
    validation_regex = Column("VALIDATION_REGEX", String(256), nullable=True)
    min_value = Column("MIN_VALUE", String(64), nullable=True)
    max_value = Column("MAX_VALUE", String(64), nullable=True)
    precision = Column("PRECISION", Integer, nullable=True)
    changed_by_id = Column("CHANGED_BY", Integer, ForeignKey("USER.ID"), nullable=True)
    created_by_id = Column("CREATED_BY", Integer, ForeignKey("USER.ID"), nullable=True)
    created_at = Column("CREATED_AT", DateTime(timezone=True), server_default=func.now())
    updated_at = Column("UPDATED_AT", DateTime(timezone=True), onupdate=func.now())

    code = relationship("Code")
    changed_by_user = relationship("User", foreign_keys=[changed_by_id])
    created_by_user = relationship("User", foreign_keys=[created_by_id])
