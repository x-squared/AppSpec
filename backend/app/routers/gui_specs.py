from fastapi import APIRouter, Depends, Query
from fastapi import Response
from sqlalchemy.orm import Session

from ..database import get_db
from ..features.gui_specs import (
    create_gui_spec_region,
    create_gui_spec_view,
    get_gui_spec_region_with_details,
    get_gui_spec_view,
    list_gui_spec_regions,
    list_gui_spec_views,
    set_gui_spec_region_impl_link,
    set_gui_spec_region_note,
    set_gui_spec_region_status,
    delete_gui_spec_region,
)
from ..integration import IntegrationPrincipal, get_gui_specs_principal
from ..schemas import (
    GuiSpecImplLinkResponse,
    GuiSpecImplLinkUpsert,
    GuiSpecNoteResponse,
    GuiSpecNoteUpdate,
    GuiSpecRegionCreate,
    GuiSpecRegionResponse,
    GuiSpecRegionStatusUpdate,
    GuiSpecViewCreate,
    GuiSpecViewListItemResponse,
    GuiSpecViewResponse,
)

router = APIRouter(prefix="/gui-specs", tags=["gui-specs"])


@router.get("/views", response_model=list[GuiSpecViewListItemResponse])
def list_views(
    include_done: bool = Query(False),
    db: Session = Depends(get_db),
    principal: IntegrationPrincipal = Depends(get_gui_specs_principal),
):
    _ = include_done
    return list_gui_spec_views(db=db, principal=principal)


@router.post("/views", response_model=GuiSpecViewResponse, status_code=201)
def create_view(
    payload: GuiSpecViewCreate,
    db: Session = Depends(get_db),
    principal: IntegrationPrincipal = Depends(get_gui_specs_principal),
):
    return create_gui_spec_view(db=db, principal=principal, payload=payload)


@router.get("/views/{view_id}", response_model=GuiSpecViewResponse)
def get_view(
    view_id: int,
    db: Session = Depends(get_db),
    principal: IntegrationPrincipal = Depends(get_gui_specs_principal),
):
    return get_gui_spec_view(db=db, principal=principal, view_id=view_id)


@router.get("/views/{view_id}/regions", response_model=list[GuiSpecRegionResponse])
def list_regions(
    view_id: int,
    include_done: bool = Query(False),
    db: Session = Depends(get_db),
    principal: IntegrationPrincipal = Depends(get_gui_specs_principal),
):
    return list_gui_spec_regions(db=db, principal=principal, view_id=view_id, include_done=include_done)


@router.post("/views/{view_id}/regions", response_model=GuiSpecRegionResponse, status_code=201)
def create_region(
    view_id: int,
    payload: GuiSpecRegionCreate,
    db: Session = Depends(get_db),
    principal: IntegrationPrincipal = Depends(get_gui_specs_principal),
):
    return create_gui_spec_region(db=db, principal=principal, payload=payload.model_copy(update={"view_id": view_id}))


@router.get("/regions/{region_id}", response_model=GuiSpecRegionResponse)
def get_region(
    region_id: int,
    db: Session = Depends(get_db),
    principal: IntegrationPrincipal = Depends(get_gui_specs_principal),
):
    return get_gui_spec_region_with_details(db=db, principal=principal, region_id=region_id)


@router.patch("/regions/{region_id}/note", response_model=GuiSpecNoteResponse)
def set_region_note(
    region_id: int,
    payload: GuiSpecNoteUpdate,
    db: Session = Depends(get_db),
    principal: IntegrationPrincipal = Depends(get_gui_specs_principal),
):
    return set_gui_spec_region_note(db=db, principal=principal, region_id=region_id, payload=payload)


@router.patch("/regions/{region_id}/status", response_model=GuiSpecRegionResponse)
def set_region_status(
    region_id: int,
    payload: GuiSpecRegionStatusUpdate,
    db: Session = Depends(get_db),
    principal: IntegrationPrincipal = Depends(get_gui_specs_principal),
):
    updated = set_gui_spec_region_status(db=db, principal=principal, region_id=region_id, payload=payload)
    return get_gui_spec_region_with_details(db=db, principal=principal, region_id=updated.id)


@router.put("/regions/{region_id}/impl-link", response_model=GuiSpecImplLinkResponse)
def upsert_impl_link(
    region_id: int,
    payload: GuiSpecImplLinkUpsert,
    db: Session = Depends(get_db),
    principal: IntegrationPrincipal = Depends(get_gui_specs_principal),
):
    return set_gui_spec_region_impl_link(db=db, principal=principal, region_id=region_id, payload=payload)


@router.delete("/regions/{region_id}", status_code=204, response_class=Response)
def delete_region(
    region_id: int,
    db: Session = Depends(get_db),
    principal: IntegrationPrincipal = Depends(get_gui_specs_principal),
):
    delete_gui_spec_region(db=db, principal=principal, region_id=region_id)
    return Response(status_code=204)

