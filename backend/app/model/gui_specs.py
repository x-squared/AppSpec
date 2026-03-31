from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from ..database import Base


class GuiSpecView(Base):
    """Top-level GUI discussion container."""

    __tablename__ = "GUI_SPEC_VIEW"

    id = Column("ID", Integer, primary_key=True, index=True)
    # Host-owned user reference ids. Intentionally no FK to local USER table.
    created_by_id = Column("CREATED_BY", Integer, nullable=True, index=True)
    changed_by_id = Column("CHANGED_BY", Integer, nullable=True)
    name = Column("NAME", String(256), nullable=False, default="")
    description = Column("DESCRIPTION", String(1024), nullable=False, default="")
    view_type = Column("VIEW_TYPE", String(48), nullable=False, default="SCRATCH_VIEW", index=True)
    capture_url = Column("CAPTURE_URL", String(1024), nullable=False, default="")
    capture_gui_part = Column("CAPTURE_GUI_PART", String(256), nullable=False, default="")
    capture_state_json = Column("CAPTURE_STATE_JSON", Text, nullable=False, default="{}")
    created_at = Column("CREATED_AT", DateTime(timezone=True), server_default=func.now())
    updated_at = Column("UPDATED_AT", DateTime(timezone=True), onupdate=func.now())

    regions = relationship(
        "GuiSpecRegion",
        back_populates="view",
        cascade="all, delete-orphan",
        order_by="GuiSpecRegion.z_index.asc(), GuiSpecRegion.id.asc()",
    )


class GuiSpecRegion(Base):
    """A rectangular area inside a GUI spec view."""

    __tablename__ = "GUI_SPEC_REGION"

    id = Column("ID", Integer, primary_key=True, index=True)
    view_id = Column("VIEW_ID", Integer, ForeignKey("GUI_SPEC_VIEW.ID"), nullable=False, index=True)
    region_type = Column("REGION_TYPE", String(48), nullable=False, index=True)
    label = Column("LABEL", String(256), nullable=False, default="")
    anchor_selector = Column("ANCHOR_SELECTOR", String(512), nullable=False, default="")
    anchor_id = Column("ANCHOR_ID", String(256), nullable=False, default="")
    anchor_class_name = Column("ANCHOR_CLASS_NAME", String(256), nullable=False, default="")
    anchor_tag = Column("ANCHOR_TAG", String(64), nullable=False, default="")
    anchor_text_sample = Column("ANCHOR_TEXT_SAMPLE", String(256), nullable=False, default="")
    left_pct = Column("LEFT_PCT", Integer, nullable=False)
    top_pct = Column("TOP_PCT", Integer, nullable=False)
    width_pct = Column("WIDTH_PCT", Integer, nullable=False)
    height_pct = Column("HEIGHT_PCT", Integer, nullable=False)
    z_index = Column("Z_INDEX", Integer, nullable=False, default=0, index=True)
    status = Column("STATUS", String(48), nullable=False, default="OPEN", index=True)
    # Host-owned user reference ids. Intentionally no FK to local USER table.
    created_by_id = Column("CREATED_BY", Integer, nullable=True)
    changed_by_id = Column("CHANGED_BY", Integer, nullable=True)
    created_at = Column("CREATED_AT", DateTime(timezone=True), server_default=func.now())
    updated_at = Column("UPDATED_AT", DateTime(timezone=True), onupdate=func.now())

    view = relationship("GuiSpecView", back_populates="regions")
    note = relationship("GuiSpecNote", uselist=False, back_populates="region", cascade="all, delete-orphan")
    impl_link = relationship("GuiSpecImplLink", uselist=False, back_populates="region", cascade="all, delete-orphan")


class GuiSpecNote(Base):
    """Rich text note attached 1:1 to a GUI spec region."""

    __tablename__ = "GUI_SPEC_NOTE"

    id = Column("ID", Integer, primary_key=True, index=True)
    region_id = Column("REGION_ID", Integer, ForeignKey("GUI_SPEC_REGION.ID"), nullable=False, unique=True, index=True)
    rich_text_html = Column("RICH_TEXT_HTML", Text, nullable=False, default="")
    # Host-owned user reference ids. Intentionally no FK to local USER table.
    created_by_id = Column("CREATED_BY", Integer, nullable=True)
    changed_by_id = Column("CHANGED_BY", Integer, nullable=True)
    created_at = Column("CREATED_AT", DateTime(timezone=True), server_default=func.now())
    updated_at = Column("UPDATED_AT", DateTime(timezone=True), onupdate=func.now())

    region = relationship("GuiSpecRegion", back_populates="note")


class GuiSpecImplLink(Base):
    """Implementation reference attached 1:1 to a GUI spec region."""

    __tablename__ = "GUI_SPEC_IMPL_LINK"

    id = Column("ID", Integer, primary_key=True, index=True)
    region_id = Column("REGION_ID", Integer, ForeignKey("GUI_SPEC_REGION.ID"), nullable=False, unique=True, index=True)
    repo_key = Column("REPO_KEY", String(64), nullable=False, default="")
    module_path = Column("MODULE_PATH", String(256), nullable=False, default="")
    file_path = Column("FILE_PATH", String(512), nullable=False, default="")
    symbol = Column("SYMBOL", String(256), nullable=False, default="")
    commit_hash = Column("COMMIT_HASH", String(64), nullable=False, default="")
    note = Column("NOTE", Text, nullable=False, default="")
    # Host-owned user reference ids. Intentionally no FK to local USER table.
    created_by_id = Column("CREATED_BY", Integer, nullable=True)
    changed_by_id = Column("CHANGED_BY", Integer, nullable=True)
    created_at = Column("CREATED_AT", DateTime(timezone=True), server_default=func.now())
    updated_at = Column("UPDATED_AT", DateTime(timezone=True), onupdate=func.now())

    region = relationship("GuiSpecRegion", back_populates="impl_link")

