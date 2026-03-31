import { request } from './core';

export type GuiSpecViewTypeKey = 'SCRATCH_VIEW';
export type GuiSpecRegionTypeKey = 'EXISTING_PART' | 'NEW_PART';
export type GuiSpecRegionStatusKey = 'OPEN' | 'IN_PROGRESS' | 'DONE';

export interface GuiSpecViewListItem {
  id: number;
  name: string;
  view_type: GuiSpecViewTypeKey | string;
  open_regions_count: number;
  done_regions_count: number;
  created_at: string;
  updated_at: string | null;
}

export interface GuiSpecView {
  id: number;
  created_by_id: number | null;
  name: string;
  description: string;
  view_type: GuiSpecViewTypeKey | string;
  capture_url: string;
  capture_gui_part: string;
  capture_state_json: string;
  created_at: string;
  updated_at: string | null;
}

export interface GuiSpecRegionGeometry {
  left_pct: number;
  top_pct: number;
  width_pct: number;
  height_pct: number;
}

export interface GuiSpecNote {
  id: number;
  rich_text_html: string;
  created_at: string;
  updated_at: string | null;
}

export interface GuiSpecImplLink {
  id: number;
  repo_key: string;
  module_path: string;
  file_path: string;
  symbol: string;
  commit_hash: string;
  note: string;
  created_at: string;
  updated_at: string | null;
}

export interface GuiSpecRegion {
  id: number;
  view_id: number;
  region_type: GuiSpecRegionTypeKey | string;
  label: string;
  anchor_selector: string;
  anchor_id: string;
  anchor_class_name: string;
  anchor_tag: string;
  anchor_text_sample: string;
  left_pct: number;
  top_pct: number;
  width_pct: number;
  height_pct: number;
  z_index: number;
  status: GuiSpecRegionStatusKey | string;
  note: GuiSpecNote | null;
  impl_link: GuiSpecImplLink | null;
  created_at: string;
  updated_at: string | null;
}

export interface GuiSpecViewCreate {
  name: string;
  description?: string;
  view_type?: GuiSpecViewTypeKey;
  capture_url?: string;
  capture_gui_part?: string;
  capture_state_json?: string;
}

export interface GuiSpecRegionCreate {
  view_id?: number;
  region_type: GuiSpecRegionTypeKey;
  label?: string;
  anchor_selector?: string;
  anchor_id?: string;
  anchor_class_name?: string;
  anchor_tag?: string;
  anchor_text_sample?: string;
  geometry: GuiSpecRegionGeometry;
  z_index?: number | null;
  status?: GuiSpecRegionStatusKey;
}

export interface GuiSpecNoteUpdate { rich_text_html?: string; }
export interface GuiSpecRegionStatusUpdate { status: GuiSpecRegionStatusKey; }
export interface GuiSpecImplLinkUpsert { repo_key?: string; module_path?: string; file_path?: string; symbol?: string; commit_hash?: string; note?: string; }

export const guiSpecsApi = {
  listGuiSpecViews: (opts?: { include_done?: boolean }) =>
    request<GuiSpecViewListItem[]>(`/gui-specs/views?include_done=${opts?.include_done ? 'true' : 'false'}`),
  createGuiSpecView: (data: GuiSpecViewCreate) =>
    request<GuiSpecView>('/gui-specs/views', { method: 'POST', body: JSON.stringify(data) }),
  getGuiSpecView: (viewId: number) => request<GuiSpecView>(`/gui-specs/views/${viewId}`),
  listGuiSpecRegions: (viewId: number, opts?: { include_done?: boolean }) =>
    request<GuiSpecRegion[]>(`/gui-specs/views/${viewId}/regions?include_done=${opts?.include_done ? 'true' : 'false'}`),
  createGuiSpecRegion: (viewId: number, data: Omit<GuiSpecRegionCreate, 'view_id'>) =>
    request<GuiSpecRegion>(`/gui-specs/views/${viewId}/regions`, { method: 'POST', body: JSON.stringify(data) }),
  getGuiSpecRegion: (regionId: number) => request<GuiSpecRegion>(`/gui-specs/regions/${regionId}`),
  setGuiSpecRegionNote: (regionId: number, data: GuiSpecNoteUpdate) =>
    request<GuiSpecNote>(`/gui-specs/regions/${regionId}/note`, { method: 'PATCH', body: JSON.stringify(data) }),
  setGuiSpecRegionStatus: (regionId: number, data: GuiSpecRegionStatusUpdate) =>
    request<GuiSpecRegion>(`/gui-specs/regions/${regionId}/status`, { method: 'PATCH', body: JSON.stringify(data) }),
  upsertGuiSpecImplLink: (regionId: number, data: GuiSpecImplLinkUpsert) =>
    request<GuiSpecImplLink>(`/gui-specs/regions/${regionId}/impl-link`, { method: 'PUT', body: JSON.stringify(data) }),
};

