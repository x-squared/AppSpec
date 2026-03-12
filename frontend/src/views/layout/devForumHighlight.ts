import { DEV_FORUM_OPEN_CONTEXT_EVENT, type DevForumOpenContextDetail } from './devForumEvents';

const DEV_FORUM_HIGHLIGHT_STORAGE_PREFIX = 'dev_forum_highlight_payload:';
const DEV_FORUM_HIGHLIGHT_QUERY_KEY = 'dev_forum_highlight_key';

interface CapturedSelectedComponent {
  selector?: string;
  tag?: string;
  id?: string;
  class_name?: string;
  text_sample?: string;
}

function parseSelectedComponent(captureStateJson: string): CapturedSelectedComponent | null {
  try {
    const parsed = JSON.parse(captureStateJson);
    if (typeof parsed !== 'object' || parsed === null || Array.isArray(parsed)) return null;
    const selected = (parsed as Record<string, unknown>).selected_component;
    if (typeof selected !== 'object' || selected === null || Array.isArray(selected)) return null;
    return selected as CapturedSelectedComponent;
  } catch {
    return null;
  }
}

function resolveElement(selected: CapturedSelectedComponent): HTMLElement | null {
  if (selected.selector) {
    const bySelector = document.querySelector(selected.selector);
    if (bySelector instanceof HTMLElement) return bySelector;
  }
  if (selected.id) {
    const byId = document.getElementById(selected.id);
    if (byId) return byId;
  }
  return null;
}

export function openDevForumContextWithHighlight(
  captureUrl: string,
  captureStateJson: string,
  captureGuiPart?: string | null,
): void {
  const payloadKey = `k${Date.now()}_${Math.random().toString(36).slice(2, 10)}`;
  sessionStorage.setItem(`${DEV_FORUM_HIGHLIGHT_STORAGE_PREFIX}${payloadKey}`, captureStateJson);
  const url = new URL(captureUrl || '/', window.location.origin);
  url.searchParams.set(DEV_FORUM_HIGHLIGHT_QUERY_KEY, payloadKey);
  window.history.pushState(null, '', `${url.pathname}${url.search}${url.hash}`);
  const eventDetail: DevForumOpenContextDetail = {
    capture_url: `${url.pathname}${url.search}${url.hash}`,
    capture_state_json: captureStateJson,
    capture_gui_part: captureGuiPart ?? null,
  };
  window.dispatchEvent(new CustomEvent<DevForumOpenContextDetail>(DEV_FORUM_OPEN_CONTEXT_EVENT, { detail: eventDetail }));
  applyDevForumHighlightFromLocation();
}

export function applyDevForumHighlightFromLocation(): void {
  const params = new URLSearchParams(window.location.search);
  const payloadKey = params.get(DEV_FORUM_HIGHLIGHT_QUERY_KEY);
  if (!payloadKey) return;

  const storageKey = `${DEV_FORUM_HIGHLIGHT_STORAGE_PREFIX}${payloadKey}`;
  const payload = sessionStorage.getItem(storageKey);
  sessionStorage.removeItem(storageKey);

  params.delete(DEV_FORUM_HIGHLIGHT_QUERY_KEY);
  const remainingQuery = params.toString();
  const nextUrl = `${window.location.pathname}${remainingQuery ? `?${remainingQuery}` : ''}${window.location.hash}`;
  window.history.replaceState(null, '', nextUrl);

  if (!payload) return;
  const selected = parseSelectedComponent(payload);
  if (!selected) return;

  let attempts = 0;
  let activeElement: HTMLElement | null = null;
  let cleanedUp = false;
  let timeoutId: number | null = null;

  const cleanup = () => {
    if (cleanedUp) return;
    cleanedUp = true;
    if (activeElement) {
      activeElement.classList.remove('dev-forum-focus-highlight');
    }
    if (timeoutId !== null) {
      window.clearTimeout(timeoutId);
      timeoutId = null;
    }
    window.removeEventListener('pointerdown', cleanup, true);
    window.removeEventListener('keydown', cleanup, true);
    window.removeEventListener('wheel', cleanup, true);
  };

  const tryApply = () => {
    if (cleanedUp) return;
    const target = resolveElement(selected);
    if (target) {
      activeElement = target;
      target.classList.add('dev-forum-focus-highlight');
      target.scrollIntoView({ block: 'center', inline: 'nearest', behavior: 'smooth' });
      timeoutId = window.setTimeout(cleanup, 8000);
      window.addEventListener('pointerdown', cleanup, true);
      window.addEventListener('keydown', cleanup, true);
      window.addEventListener('wheel', cleanup, true);
      return;
    }
    attempts += 1;
    if (attempts < 40) {
      window.requestAnimationFrame(tryApply);
    }
  };

  window.requestAnimationFrame(tryApply);
}
