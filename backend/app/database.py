from sqlalchemy import Column, Integer, create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from .config import get_config

cfg = get_config()
connect_args = {"check_same_thread": False} if cfg.database_url.startswith("sqlite") else {}
engine = create_engine(cfg.database_url, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    row_version = Column("ROW_VERSION", Integer, nullable=False, default=1)
    @property
    def changed_at(self):
        """Compatibility alias for legacy updated_at field during phased rename."""
        return getattr(self, "updated_at", None)

    @changed_at.setter
    def changed_at(self, value):
        if hasattr(self, "updated_at"):
            setattr(self, "updated_at", value)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
