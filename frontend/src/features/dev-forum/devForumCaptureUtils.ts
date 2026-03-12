import type { SelectedComponentDescriptor } from './types';

export function parseCaptureState(raw: string): Record<string, unknown> {
  try {
    const parsed = JSON.parse(raw);
    if (typeof parsed === 'object' && parsed !== null && !Array.isArray(parsed)) {
      return parsed as Record<string, unknown>;
    }
  } catch {
    // keep empty state for invalid payloads
  }
  return {};
}

export function getCurrentCaptureContext() {
  const path = window.location.pathname;
  const query = window.location.search;
  const hash = window.location.hash;
  const body = typeof document !== 'undefined' ? document.body : null;
  const currentPage = body?.dataset.tplCurrentPage?.trim() || '';
  const patientId = body?.dataset.tplCurrentPatientId ? Number(body.dataset.tplCurrentPatientId) : null;
  const coordinationId = body?.dataset.tplCurrentCoordinationId ? Number(body.dataset.tplCurrentCoordinationId) : null;
  const colloquiumId = body?.dataset.tplCurrentColloquiumId ? Number(body.dataset.tplCurrentColloquiumId) : null;
  const pathIds = Array.from(path.matchAll(/\/(\d+)(?=\/|$)/g)).map((match) => Number(match[1]));
  const ids = [
    ...(Number.isFinite(patientId as number) ? [{ key: 'patient_id', value: Number(patientId) }] : []),
    ...(Number.isFinite(coordinationId as number) ? [{ key: 'coordination_id', value: Number(coordinationId) }] : []),
    ...(Number.isFinite(colloquiumId as number) ? [{ key: 'colloquium_id', value: Number(colloquiumId) }] : []),
    ...pathIds.map((value) => ({ key: 'path_id', value })),
  ];
  const guiPart = currentPage || path.split('/').filter(Boolean)[0] || 'app';
  return {
    capture_url: `${path}${query}${hash}`,
    capture_gui_part: guiPart,
    capture_state_json: JSON.stringify({
      page: currentPage || null,
      path,
      query,
      hash,
      gui_part: guiPart,
      ids,
      captured_at: new Date().toISOString(),
    }),
  };
}

export function withSelectedComponent(captureStateJson: string, selected: SelectedComponentDescriptor | null): string {
  let payload: Record<string, unknown> = {};
  try {
    const parsed = JSON.parse(captureStateJson);
    if (typeof parsed === 'object' && parsed !== null && !Array.isArray(parsed)) {
      payload = parsed as Record<string, unknown>;
    }
  } catch {
    payload = {};
  }
  payload.selected_component = selected;
  return JSON.stringify(payload);
}
