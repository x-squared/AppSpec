from __future__ import annotations

from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload

from ..models import DevRequest, User
from ..schemas import DevRequestCaptureCreate, DevRequestDecisionUpdate

_DEVELOPMENT_VISIBLE_STATUSES = {"PENDING", "IN_DEVELOPMENT"}
_REVIEW_VISIBLE_STATUSES = {"REJECTED_REVIEW", "IMPLEMENTED_REVIEW"}


def _user_has_dev_role(user: User) -> bool:
    role_keys = set()
    if user.role is not None and user.role.type == "ROLE":
        role_keys.add(user.role.key)
    for role in user.roles or []:
        if role is not None and role.type == "ROLE":
            role_keys.add(role.key)
    return "DEV" in role_keys


def _require_dev_role(user: User) -> None:
    if not _user_has_dev_role(user):
        raise HTTPException(status_code=403, detail="DEV role required")


def list_review_requests(*, db: Session, current_user_id: int) -> list[DevRequest]:
    return (
        db.query(DevRequest)
        .options(
            joinedload(DevRequest.submitter_user),
            joinedload(DevRequest.claimed_by_user),
            joinedload(DevRequest.decided_by_user),
        )
        .filter(
            DevRequest.submitter_user_id == current_user_id,
            DevRequest.status.in_(_REVIEW_VISIBLE_STATUSES),
        )
        .order_by(DevRequest.created_at.desc(), DevRequest.id.desc())
        .all()
    )


def get_request_for_view(*, db: Session, current_user: User, request_id: int) -> DevRequest:
    item = (
        db.query(DevRequest)
        .options(
            joinedload(DevRequest.submitter_user),
            joinedload(DevRequest.claimed_by_user),
            joinedload(DevRequest.decided_by_user),
        )
        .filter(DevRequest.id == request_id)
        .first()
    )
    if item is None:
        raise HTTPException(status_code=404, detail="Dev request not found")

    is_participant = (
        item.submitter_user_id == current_user.id
        or item.claimed_by_user_id == current_user.id
        or item.decided_by_user_id == current_user.id
    )
    if not is_participant and not _user_has_dev_role(current_user):
        raise HTTPException(status_code=403, detail="Not allowed to view this dev request")
    return item


def list_request_lineage(*, db: Session, current_user: User, request_id: int) -> list[DevRequest]:
    item = get_request_for_view(db=db, current_user=current_user, request_id=request_id)

    root_id = item.id
    cursor = item
    while cursor.parent_request_id is not None:
        parent = db.query(DevRequest).filter(DevRequest.id == cursor.parent_request_id).first()
        if parent is None:
            break
        root_id = parent.id
        cursor = parent

    all_rows = db.query(DevRequest).all()
    by_parent: dict[int, list[int]] = {}
    for row in all_rows:
        if row.parent_request_id is not None:
            by_parent.setdefault(row.parent_request_id, []).append(row.id)

    lineage_ids: set[int] = set()
    queue: list[int] = [root_id]
    while queue:
        current_id = queue.pop(0)
        if current_id in lineage_ids:
            continue
        lineage_ids.add(current_id)
        for child_id in by_parent.get(current_id, []):
            queue.append(child_id)

    return (
        db.query(DevRequest)
        .options(
            joinedload(DevRequest.submitter_user),
            joinedload(DevRequest.claimed_by_user),
            joinedload(DevRequest.decided_by_user),
        )
        .filter(DevRequest.id.in_(lineage_ids))
        .order_by(DevRequest.created_at.asc(), DevRequest.id.asc())
        .all()
    )


def list_development_requests(
    *,
    db: Session,
    current_user: User,
    include_claimed_by_other_developers: bool,
    filter_claimed_by_user_id: int | None,
) -> list[DevRequest]:
    _require_dev_role(current_user)

    query = (
        db.query(DevRequest)
        .options(
            joinedload(DevRequest.submitter_user),
            joinedload(DevRequest.claimed_by_user),
            joinedload(DevRequest.decided_by_user),
        )
        .filter(DevRequest.status.in_(_DEVELOPMENT_VISIBLE_STATUSES))
    )

    if filter_claimed_by_user_id is not None:
        query = query.filter(DevRequest.claimed_by_user_id == filter_claimed_by_user_id)
    elif not include_claimed_by_other_developers:
        query = query.filter((DevRequest.claimed_by_user_id.is_(None)) | (DevRequest.claimed_by_user_id == current_user.id))

    return query.order_by(DevRequest.created_at.asc(), DevRequest.id.asc()).all()


def create_capture_request(*, db: Session, current_user_id: int, payload: DevRequestCaptureCreate) -> DevRequest:
    item = DevRequest(
        parent_request_id=None,
        submitter_user_id=current_user_id,
        status="PENDING",
        capture_url=(payload.capture_url or "").strip(),
        capture_gui_part=(payload.capture_gui_part or "").strip(),
        capture_state_json=(payload.capture_state_json or "{}").strip() or "{}",
        request_text=payload.request_text.strip(),
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def create_capture_request_any_mode(*, db: Session, current_user_id: int, payload: DevRequestCaptureCreate) -> DevRequest:
    return create_capture_request(db=db, current_user_id=current_user_id, payload=payload)


def claim_request(*, db: Session, current_user: User, request_id: int) -> DevRequest:
    _require_dev_role(current_user)
    item = db.query(DevRequest).filter(DevRequest.id == request_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Dev request not found")
    if item.status not in _DEVELOPMENT_VISIBLE_STATUSES:
        raise HTTPException(status_code=409, detail="Dev request is no longer open for development")
    if item.claimed_by_user_id is not None and item.claimed_by_user_id != current_user.id:
        raise HTTPException(status_code=409, detail="Dev request is already claimed by another developer")

    item.claimed_by_user_id = current_user.id
    item.status = "IN_DEVELOPMENT"
    db.commit()
    db.refresh(item)
    return item


def decide_request(*, db: Session, current_user: User, request_id: int, payload: DevRequestDecisionUpdate) -> DevRequest:
    _require_dev_role(current_user)
    item = db.query(DevRequest).filter(DevRequest.id == request_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Dev request not found")
    if item.status not in _DEVELOPMENT_VISIBLE_STATUSES:
        raise HTTPException(status_code=409, detail="Dev request is no longer open for development")
    if item.claimed_by_user_id is not None and item.claimed_by_user_id != current_user.id:
        raise HTTPException(status_code=409, detail="Claim this request before deciding it")

    normalized_decision = payload.decision.strip().upper()
    item.claimed_by_user_id = current_user.id
    item.decided_by_user_id = current_user.id
    item.decision = normalized_decision
    item.developer_note_text = (payload.developer_note_text or "").strip() or None
    item.developer_response_text = (payload.developer_response_text or "").strip() or None
    item.status = "REJECTED_REVIEW" if normalized_decision == "REJECTED" else "IMPLEMENTED_REVIEW"
    item.closed_at = None
    db.commit()
    db.refresh(item)
    return item


def accept_review(*, db: Session, current_user_id: int, request_id: int) -> DevRequest:
    item = db.query(DevRequest).filter(DevRequest.id == request_id, DevRequest.submitter_user_id == current_user_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Dev request not found")
    if item.status not in _REVIEW_VISIBLE_STATUSES:
        raise HTTPException(status_code=409, detail="Dev request is not awaiting user review")

    item.status = "CLOSED_ACCEPTED"
    item.closed_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(item)
    return item


def reject_review_and_create_follow_up(
    *,
    db: Session,
    current_user_id: int,
    request_id: int,
    review_text: str,
) -> DevRequest:
    source = db.query(DevRequest).filter(DevRequest.id == request_id, DevRequest.submitter_user_id == current_user_id).first()
    if source is None:
        raise HTTPException(status_code=404, detail="Dev request not found")
    if source.status not in _REVIEW_VISIBLE_STATUSES:
        raise HTTPException(status_code=409, detail="Dev request is not awaiting user review")

    source.status = "CLOSED_REOPENED"
    source.user_review_text = review_text.strip()
    source.closed_at = datetime.now(timezone.utc)

    follow_up = DevRequest(
        parent_request_id=source.id,
        submitter_user_id=current_user_id,
        status="PENDING",
        capture_url=source.capture_url,
        capture_gui_part=source.capture_gui_part,
        capture_state_json=source.capture_state_json,
        request_text=review_text.strip(),
    )
    db.add(follow_up)
    db.commit()
    db.refresh(follow_up)
    return follow_up
