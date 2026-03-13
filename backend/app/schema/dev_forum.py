from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class DevRequestCaptureCreate(BaseModel):
    capture_url: str = ""
    capture_gui_part: str = ""
    capture_state_json: str = "{}"
    request_text: str

    @field_validator("request_text")
    @classmethod
    def _validate_request_text(cls, value: str) -> str:
        trimmed = value.strip()
        if not trimmed:
            raise ValueError("request_text must not be empty")
        return trimmed


class DevRequestDecisionUpdate(BaseModel):
    decision: str = Field(pattern="^(REJECTED|IMPLEMENTED)$")
    developer_note_text: str = ""
    developer_response_text: str = ""


class DevRequestReviewRejectCreate(BaseModel):
    review_text: str

    @field_validator("review_text")
    @classmethod
    def _validate_review_text(cls, value: str) -> str:
        trimmed = value.strip()
        if not trimmed:
            raise ValueError("review_text must not be empty")
        return trimmed


class DevRequestUserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    ext_id: str
    name: str
    role_id: int | None = None
    role_ids: list[int] = Field(default_factory=list)


class DevRequestResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    parent_request_id: int | None = None
    submitter_user_id: int
    claimed_by_user_id: int | None = None
    decided_by_user_id: int | None = None
    status: str
    decision: str | None = None
    capture_url: str
    capture_gui_part: str
    capture_state_json: str
    request_text: str
    developer_note_text: str | None = None
    developer_response_text: str | None = None
    user_review_text: str | None = None
    closed_at: datetime | None = None
    created_at: datetime
    changed_at: datetime | None = None
    updated_at: datetime | None = None
    submitter_user: DevRequestUserResponse | None = None
    claimed_by_user: DevRequestUserResponse | None = None
    decided_by_user: DevRequestUserResponse | None = None
