from __future__ import annotations

from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from ..config import get_config
from ..integration import IntegrationPrincipal
from ..models import GuiSpecImplLink, GuiSpecNote, GuiSpecRegion, GuiSpecView
from ..schemas import (
    GuiSpecImplLinkUpsert,
    GuiSpecNoteUpdate,
    GuiSpecRegionCreate,
    GuiSpecRegionStatusUpdate,
    GuiSpecViewCreate,
    GuiSpecViewListItemResponse,
)


_DEV_ROLE_KEYS = {"DEV", "DEVELOPER"}
_SPEC_USER_ROLE_KEYS = {"SPECIFICATION_USER", "SPEC_USER", "SPEC_EDITOR"}
_DONE_STATUS = "DONE"


def _require_developer_role(principal: IntegrationPrincipal) -> None:
    if not principal.has_any_role(_DEV_ROLE_KEYS):
        raise HTTPException(status_code=403, detail="Developer role required")


def _require_spec_access(principal: IntegrationPrincipal) -> None:
    """Allow either developer or specification-user integration roles."""
    if principal.has_any_role(_DEV_ROLE_KEYS):
        return
    if principal.has_any_role(_SPEC_USER_ROLE_KEYS):
        return
    raise HTTPException(status_code=403, detail="Specification role required")


def _require_dev_mode_enabled() -> None:
    env = get_config().env.strip().upper()
    if env not in {"DEV", "TEST"}:
        raise HTTPException(status_code=403, detail="GUI specs are only available in DEV/TEST mode")


def list_gui_spec_views(*, db: Session, principal: IntegrationPrincipal) -> list[GuiSpecViewListItemResponse]:
    """List GUI spec views visible to spec-capable users."""
    _require_dev_mode_enabled()
    _require_spec_access(principal)
    views = db.query(GuiSpecView).order_by(GuiSpecView.updated_at.desc().nullslast(), GuiSpecView.id.desc()).all()
    items: list[GuiSpecViewListItemResponse] = []
    for view in views:
        done_count = (
            db.query(func.count(GuiSpecRegion.id))
            .filter(GuiSpecRegion.view_id == view.id, GuiSpecRegion.status == _DONE_STATUS)
            .scalar()
            or 0
        )
        open_count = (
            db.query(func.count(GuiSpecRegion.id))
            .filter(GuiSpecRegion.view_id == view.id, GuiSpecRegion.status != _DONE_STATUS)
            .scalar()
            or 0
        )
        items.append(
            GuiSpecViewListItemResponse(
                id=view.id,
                name=view.name,
                view_type=str(view.view_type),
                open_regions_count=int(open_count),
                done_regions_count=int(done_count),
                created_at=view.created_at,
                updated_at=view.updated_at,
            )
        )
    return items


def create_gui_spec_view(*, db: Session, principal: IntegrationPrincipal, payload: GuiSpecViewCreate) -> GuiSpecView:
    """Create a new GUI spec view with host-supplied audit ids."""
    _require_dev_mode_enabled()
    _require_spec_access(principal)
    item = GuiSpecView(
        created_by_id=principal.user_id,
        changed_by_id=principal.user_id,
        name=payload.name.strip(),
        description=(payload.description or "").strip(),
        view_type=payload.view_type.value,
        capture_url=(payload.capture_url or "").strip(),
        capture_gui_part=(payload.capture_gui_part or "").strip(),
        capture_state_json=(payload.capture_state_json or "{}").strip() or "{}",
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def get_gui_spec_view(*, db: Session, principal: IntegrationPrincipal, view_id: int) -> GuiSpecView:
    """Get one GUI spec view by id."""
    _require_dev_mode_enabled()
    _require_spec_access(principal)
    item = db.query(GuiSpecView).filter(GuiSpecView.id == view_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="GUI spec view not found")
    return item


def list_gui_spec_regions(*, db: Session, principal: IntegrationPrincipal, view_id: int, include_done: bool) -> list[GuiSpecRegion]:
    """List regions for one view with optional DONE filtering."""
    _require_dev_mode_enabled()
    _require_spec_access(principal)
    query = (
        db.query(GuiSpecRegion)
        .options(joinedload(GuiSpecRegion.note), joinedload(GuiSpecRegion.impl_link))
        .filter(GuiSpecRegion.view_id == view_id)
    )
    if not include_done:
        query = query.filter(GuiSpecRegion.status != _DONE_STATUS)
    return query.order_by(GuiSpecRegion.z_index.asc(), GuiSpecRegion.id.asc()).all()


def create_gui_spec_region(*, db: Session, principal: IntegrationPrincipal, payload: GuiSpecRegionCreate) -> GuiSpecRegion:
    """Create one region entry under a view."""
    _require_dev_mode_enabled()
    _require_spec_access(principal)
    if payload.view_id is None:
        raise HTTPException(status_code=422, detail="view_id is required")
    view_exists = db.query(GuiSpecView).filter(GuiSpecView.id == payload.view_id).first()
    if view_exists is None:
        raise HTTPException(status_code=404, detail="GUI spec view not found")
    max_z = db.query(func.max(GuiSpecRegion.z_index)).filter(GuiSpecRegion.view_id == payload.view_id).scalar()
    next_z = int(max_z or 0) + 1
    z_index = payload.z_index if payload.z_index is not None else next_z
    geometry = payload.geometry
    item = GuiSpecRegion(
        view_id=payload.view_id,
        region_type=payload.region_type.value,
        label=(payload.label or "").strip(),
        anchor_selector=(payload.anchor_selector or "").strip(),
        anchor_id=(payload.anchor_id or "").strip(),
        anchor_class_name=(payload.anchor_class_name or "").strip(),
        anchor_tag=(payload.anchor_tag or "").strip(),
        anchor_text_sample=(payload.anchor_text_sample or "").strip(),
        left_pct=int(geometry.left_pct),
        top_pct=int(geometry.top_pct),
        width_pct=int(geometry.width_pct),
        height_pct=int(geometry.height_pct),
        z_index=int(z_index),
        status=payload.status.value,
        created_by_id=principal.user_id,
        changed_by_id=principal.user_id,
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def get_gui_spec_region_with_details(*, db: Session, principal: IntegrationPrincipal, region_id: int) -> GuiSpecRegion:
    """Load one region including note and implementation link."""
    _require_dev_mode_enabled()
    _require_spec_access(principal)
    item = (
        db.query(GuiSpecRegion)
        .options(joinedload(GuiSpecRegion.note), joinedload(GuiSpecRegion.impl_link))
        .filter(GuiSpecRegion.id == region_id)
        .first()
    )
    if item is None:
        raise HTTPException(status_code=404, detail="GUI spec region not found")
    return item


def set_gui_spec_region_note(*, db: Session, principal: IntegrationPrincipal, region_id: int, payload: GuiSpecNoteUpdate) -> GuiSpecNote:
    """Upsert the rich-text note for a region."""
    _require_dev_mode_enabled()
    _require_spec_access(principal)
    region = db.query(GuiSpecRegion).filter(GuiSpecRegion.id == region_id).first()
    if region is None:
        raise HTTPException(status_code=404, detail="GUI spec region not found")
    existing = db.query(GuiSpecNote).filter(GuiSpecNote.region_id == region_id).first()
    if existing is None:
        existing = GuiSpecNote(
            region_id=region_id,
            rich_text_html=(payload.rich_text_html or ""),
            created_by_id=principal.user_id,
            changed_by_id=principal.user_id,
        )
        db.add(existing)
    else:
        existing.rich_text_html = payload.rich_text_html or ""
        existing.changed_by_id = principal.user_id
    db.commit()
    db.refresh(existing)
    return existing


def set_gui_spec_region_status(
    *, db: Session, principal: IntegrationPrincipal, region_id: int, payload: GuiSpecRegionStatusUpdate
) -> GuiSpecRegion:
    """Update region lifecycle status.

    Kept developer-only by contract because status is used as implementation
    progress signal.
    """
    _require_dev_mode_enabled()
    _require_developer_role(principal)
    item = db.query(GuiSpecRegion).filter(GuiSpecRegion.id == region_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="GUI spec region not found")
    item.status = payload.status.value
    item.changed_by_id = principal.user_id
    db.commit()
    db.refresh(item)
    return item


def set_gui_spec_region_impl_link(
    *, db: Session, principal: IntegrationPrincipal, region_id: int, payload: GuiSpecImplLinkUpsert
) -> GuiSpecImplLink:
    """Upsert code implementation link metadata for a region."""
    _require_dev_mode_enabled()
    _require_developer_role(principal)
    region = db.query(GuiSpecRegion).filter(GuiSpecRegion.id == region_id).first()
    if region is None:
        raise HTTPException(status_code=404, detail="GUI spec region not found")
    existing = db.query(GuiSpecImplLink).filter(GuiSpecImplLink.region_id == region_id).first()
    if existing is None:
        existing = GuiSpecImplLink(region_id=region_id, created_by_id=principal.user_id, changed_by_id=principal.user_id)
        db.add(existing)
    existing.repo_key = (payload.repo_key or "").strip()
    existing.module_path = (payload.module_path or "").strip()
    existing.file_path = (payload.file_path or "").strip()
    existing.symbol = (payload.symbol or "").strip()
    existing.commit_hash = (payload.commit_hash or "").strip()
    existing.note = (payload.note or "").strip()
    existing.changed_by_id = principal.user_id
    db.commit()
    db.refresh(existing)
    return existing


def delete_gui_spec_region(*, db: Session, principal: IntegrationPrincipal, region_id: int) -> None:
    """Delete one captured region (including note/link via model cascade)."""
    _require_dev_mode_enabled()
    _require_spec_access(principal)
    item = db.query(GuiSpecRegion).filter(GuiSpecRegion.id == region_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="GUI spec region not found")
    db.delete(item)
    db.commit()

