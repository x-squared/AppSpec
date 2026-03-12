from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..auth import get_current_user
from ..database import get_db
from ..features.dev_forum import create_capture_request_any_mode
from ..features.support_ticket import get_support_ticket_email
from ..models import User
from ..schemas import (
    DevRequestCaptureCreate,
    SupportTicketConfigResponse,
    SupportTicketDevForumCaptureRequest,
    SupportTicketDevForumCaptureResponse,
)

router = APIRouter(prefix="/support-ticket", tags=["support_ticket"])


@router.get("/config", response_model=SupportTicketConfigResponse)
def get_support_ticket_config():
    return SupportTicketConfigResponse(support_email=get_support_ticket_email())


@router.post("/capture-dev-forum", response_model=SupportTicketDevForumCaptureResponse)
def capture_support_ticket_dev_forum_entry(
    payload: SupportTicketDevForumCaptureRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    created = create_capture_request_any_mode(
        db=db,
        current_user_id=current_user.id,
        payload=DevRequestCaptureCreate(
            capture_url=payload.capture_url,
            capture_gui_part=payload.capture_gui_part,
            capture_state_json=payload.capture_state_json,
            request_text=payload.request_text,
        ),
    )
    return SupportTicketDevForumCaptureResponse(request_id=created.id)
