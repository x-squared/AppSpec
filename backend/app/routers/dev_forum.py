from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ..auth import get_current_user
from ..database import get_db
from ..features.dev_forum import (
    accept_review as accept_review_service,
    claim_request as claim_request_service,
    create_capture_request as create_capture_request_service,
    decide_request as decide_request_service,
    get_request_for_view as get_request_for_view_service,
    list_request_lineage as list_request_lineage_service,
    list_development_requests as list_development_requests_service,
    list_review_requests as list_review_requests_service,
    reject_review_and_create_follow_up as reject_review_and_create_follow_up_service,
)
from ..models import User
from ..schemas import (
    DevRequestCaptureCreate,
    DevRequestDecisionUpdate,
    DevRequestResponse,
    DevRequestReviewRejectCreate,
)

router = APIRouter(prefix="/dev-forum/requests", tags=["dev-forum"])


@router.get("/review", response_model=list[DevRequestResponse])
def list_review_requests(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return list_review_requests_service(db=db, current_user_id=current_user.id)


@router.get("/development", response_model=list[DevRequestResponse])
def list_development_requests(
    include_claimed_by_other_developers: bool = Query(False),
    filter_claimed_by_user_id: int | None = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return list_development_requests_service(
        db=db,
        current_user=current_user,
        include_claimed_by_other_developers=include_claimed_by_other_developers,
        filter_claimed_by_user_id=filter_claimed_by_user_id,
    )


@router.get("/{request_id}", response_model=DevRequestResponse)
def get_request_for_view(
    request_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_request_for_view_service(db=db, current_user=current_user, request_id=request_id)


@router.get("/{request_id}/lineage", response_model=list[DevRequestResponse])
def list_request_lineage(
    request_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return list_request_lineage_service(db=db, current_user=current_user, request_id=request_id)


@router.post("/", response_model=DevRequestResponse, status_code=201)
def create_capture_request(
    payload: DevRequestCaptureCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_capture_request_service(db=db, current_user_id=current_user.id, payload=payload)


@router.post("/{request_id}/claim", response_model=DevRequestResponse)
def claim_request(
    request_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return claim_request_service(db=db, current_user=current_user, request_id=request_id)


@router.post("/{request_id}/decision", response_model=DevRequestResponse)
def decide_request(
    request_id: int,
    payload: DevRequestDecisionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return decide_request_service(db=db, current_user=current_user, request_id=request_id, payload=payload)


@router.post("/{request_id}/review-accept", response_model=DevRequestResponse)
def accept_review(
    request_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return accept_review_service(db=db, current_user_id=current_user.id, request_id=request_id)


@router.post("/{request_id}/review-reject", response_model=DevRequestResponse)
def reject_review(
    request_id: int,
    payload: DevRequestReviewRejectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return reject_review_and_create_follow_up_service(
        db=db,
        current_user_id=current_user.id,
        request_id=request_id,
        review_text=payload.review_text,
    )
