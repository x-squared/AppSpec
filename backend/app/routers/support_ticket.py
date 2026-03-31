from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..features.dev_forum import create_capture_request_any_mode
from ..features.support_ticket import get_support_ticket_email
from ..integration import IntegrationPrincipal, get_integration_principal
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
    principal: IntegrationPrincipal = Depends(get_integration_principal),
):
    if principal.user_id is None:
        raise HTTPException(status_code=422, detail="X-AppSpec-User-Id header required")
    created = create_capture_request_any_mode(
        db=db,
        current_user_id=principal.user_id,
        payload=DevRequestCaptureCreate(
            capture_url=payload.capture_url,
            capture_gui_part=payload.capture_gui_part,
            capture_state_json=payload.capture_state_json,
            request_text=payload.request_text,
        ),
    )
    return SupportTicketDevForumCaptureResponse(request_id=created.id)
