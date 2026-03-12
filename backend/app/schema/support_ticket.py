from pydantic import BaseModel


class SupportTicketConfigResponse(BaseModel):
    support_email: str


class SupportTicketDevForumCaptureRequest(BaseModel):
    capture_url: str
    capture_gui_part: str
    capture_state_json: str
    request_text: str


class SupportTicketDevForumCaptureResponse(BaseModel):
    request_id: int
