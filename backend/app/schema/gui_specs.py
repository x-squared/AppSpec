from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, field_validator


class GuiSpecViewTypeKey(str, Enum):
    SCRATCH_VIEW = "SCRATCH_VIEW"


class GuiSpecRegionTypeKey(str, Enum):
    EXISTING_PART = "EXISTING_PART"
    NEW_PART = "NEW_PART"


class GuiSpecRegionStatusKey(str, Enum):
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"


class GuiSpecViewCreate(BaseModel):
    name: str
    description: str = ""
    view_type: GuiSpecViewTypeKey = GuiSpecViewTypeKey.SCRATCH_VIEW
    capture_url: str = ""
    capture_gui_part: str = ""
    capture_state_json: str = "{}"

    @field_validator("name")
    @classmethod
    def _validate_name(cls, value: str) -> str:
        trimmed = value.strip()
        if not trimmed:
            raise ValueError("name must not be empty")
        return trimmed


class GuiSpecViewResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_by_id: int | None = None
    name: str
    description: str
    view_type: str
    capture_url: str
    capture_gui_part: str
    capture_state_json: str
    created_at: datetime
    changed_at: datetime | None = None
    updated_at: datetime | None = None


class GuiSpecViewListItemResponse(BaseModel):
    id: int
    name: str
    view_type: str
    open_regions_count: int
    done_regions_count: int
    created_at: datetime
    updated_at: datetime | None = None


class GuiSpecRegionGeometry(BaseModel):
    left_pct: int
    top_pct: int
    width_pct: int
    height_pct: int

    @field_validator("left_pct", "top_pct", "width_pct", "height_pct")
    @classmethod
    def _validate_pct_range(cls, value: int) -> int:
        if value < 0 or value > 200000:
            raise ValueError("geometry percent out of expected range")
        return value


class GuiSpecRegionCreate(BaseModel):
    view_id: int | None = None
    region_type: GuiSpecRegionTypeKey
    label: str = ""
    anchor_selector: str = ""
    anchor_id: str = ""
    anchor_class_name: str = ""
    anchor_tag: str = ""
    anchor_text_sample: str = ""
    geometry: GuiSpecRegionGeometry
    z_index: int | None = None
    status: GuiSpecRegionStatusKey = GuiSpecRegionStatusKey.OPEN


class GuiSpecNoteUpdate(BaseModel):
    rich_text_html: str = ""


class GuiSpecRegionStatusUpdate(BaseModel):
    status: GuiSpecRegionStatusKey


class GuiSpecImplLinkUpsert(BaseModel):
    repo_key: str = ""
    module_path: str = ""
    file_path: str = ""
    symbol: str = ""
    commit_hash: str = ""
    note: str = ""


class GuiSpecNoteResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    rich_text_html: str
    created_at: datetime
    changed_at: datetime | None = None
    updated_at: datetime | None = None


class GuiSpecImplLinkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    repo_key: str
    module_path: str
    file_path: str
    symbol: str
    commit_hash: str
    note: str
    created_at: datetime
    changed_at: datetime | None = None
    updated_at: datetime | None = None


class GuiSpecRegionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    view_id: int
    region_type: str
    label: str
    anchor_selector: str
    anchor_id: str
    anchor_class_name: str
    anchor_tag: str
    anchor_text_sample: str
    left_pct: int
    top_pct: int
    width_pct: int
    height_pct: int
    z_index: int
    status: str
    note: GuiSpecNoteResponse | None = None
    impl_link: GuiSpecImplLinkResponse | None = None
    created_at: datetime
    changed_at: datetime | None = None
    updated_at: datetime | None = None

