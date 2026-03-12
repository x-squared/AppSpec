from sqlalchemy import Column, ForeignKey, Integer, String, Table, UniqueConstraint
from sqlalchemy.orm import relationship

from ..database import Base

role_permission_table = Table(
    "ROLE_PERMISSION",
    Base.metadata,
    Column("ROLE_ID", Integer, ForeignKey("CODE.ID"), primary_key=True),
    Column("PERMISSION_ID", Integer, ForeignKey("ACCESS_PERMISSION.ID"), primary_key=True),
    UniqueConstraint("ROLE_ID", "PERMISSION_ID"),
)


class AccessPermission(Base):
    __tablename__ = "ACCESS_PERMISSION"

    id = Column("ID", Integer, primary_key=True, index=True)
    key = Column("KEY", String(96), nullable=False, unique=True)
    name_default = Column("NAME_DEFAULT", String(128), nullable=False, default="")

    roles = relationship("Code", secondary=role_permission_table, back_populates="permissions")
