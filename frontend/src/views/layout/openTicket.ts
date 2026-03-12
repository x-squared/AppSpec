import { api } from '../../api';
import { getRecentErrorLog, type ClientErrorLogEntry } from '../../api/errorLog';
import { getLastCapturedComponent } from './errorContextCapture';
import { DEV_FORUM_CAPTURE_CREATED_EVENT } from './devForumEvents';

const wrapBase64 = (value: string): string => value.replace(/(.{1,76})/g, '$1\r\n').trimEnd();
const UUID_RE = /^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;
const NUMERIC_RE = /^\d+$/;
const ID_KEY_RE = /(^id$|_id$|Id$|ID$)/;
const MAX_CONTEXT_IDS = 20;

const utf8ToBase64 = (value: string): string => {
  const bytes = new TextEncoder().encode(value);
  let binary = '';
  bytes.forEach((byte) => {
    binary += String.fromCharCode(byte);
  });
  return btoa(binary);
};

const prettyLogEntry = (entry: ClientErrorLogEntry, index: number): string => {
  const lines: string[] = [];
  lines.push(`[${index + 1}] ${entry.ts} (${entry.source.toUpperCase()})`);
  lines.push(`message: ${entry.message}`);
  if (typeof entry.status === 'number') lines.push(`status: ${entry.status}`);
  if (entry.method) lines.push(`method: ${entry.method}`);
  if (entry.path) lines.push(`path: ${entry.path}`);
  if (entry.detail !== undefined) lines.push(`detail: ${JSON.stringify(entry.detail, null, 2)}`);
  return lines.join('\n');
};

const buildAttachmentText = (bannerMessage: string): string => {
  const recent = getRecentErrorLog(40);
  const header = [
    'TPL App - Error Ticket Log',
    `Generated at: ${new Date().toISOString()}`,
    `Visible error: ${bannerMessage}`,
    '',
    'Recent client error log:',
    '',
  ].join('\n');
  if (recent.length === 0) {
    return `${header}(no log entries available)\n`;
  }
  return `${header}${recent.map(prettyLogEntry).join('\n\n')}\n`;
};

function isIdLikeValue(value: string): boolean {
  const trimmed = value.trim();
  return NUMERIC_RE.test(trimmed) || UUID_RE.test(trimmed);
}

function normalizeContextKey(raw: string): string {
  const cleaned = raw.replace(/[^a-zA-Z0-9_]/g, '_').replace(/^_+|_+$/g, '');
  if (!cleaned) return 'id';
  return cleaned;
}

function addIdContext(store: Map<string, string>, key: string, value: string): void {
  if (!isIdLikeValue(value)) return;
  if (store.size >= MAX_CONTEXT_IDS) return;
  const normalizedKey = normalizeContextKey(key);
  if (!store.has(normalizedKey)) {
    store.set(normalizedKey, value.trim());
  }
}

function extractIdsFromObject(value: unknown, store: Map<string, string>, parentPath = ''): void {
  if (store.size >= MAX_CONTEXT_IDS || value === null || value === undefined) return;
  if (Array.isArray(value)) {
    value.forEach((item) => extractIdsFromObject(item, store, parentPath));
    return;
  }
  if (typeof value !== 'object') return;
  for (const [key, nested] of Object.entries(value as Record<string, unknown>)) {
    if (store.size >= MAX_CONTEXT_IDS) break;
    const pathKey = parentPath ? `${parentPath}.${key}` : key;
    if (ID_KEY_RE.test(key) && (typeof nested === 'string' || typeof nested === 'number')) {
      addIdContext(store, pathKey, String(nested));
      continue;
    }
    extractIdsFromObject(nested, store, pathKey);
  }
}

function deriveGuiPartFromPath(pathname: string): string {
  const segment = pathname.split('/').filter(Boolean)[0] ?? '';
  const bySegment: Record<string, string> = {
    'patients': 'Patients',
    'coordinations': 'Coordinations',
    'colloquiums': 'Colloquiums',
    'tasks': 'Tasks',
    'my-work': 'My Work',
    'reports': 'Reports',
    'admin': 'Admin',
    'preferences': 'Preferences',
    'e2e-tests': 'E2E Tests',
    'information': 'Information',
  };
  return bySegment[segment] ?? (segment ? `/${segment}` : 'Unknown');
}

function collectCurrentContext(recent: ClientErrorLogEntry[]) {
  const ids = new Map<string, string>();
  const hasWindow = typeof window !== 'undefined' && !!window.location;
  const body = typeof document !== 'undefined' ? document.body : null;
  const currentPage = body?.dataset.tplCurrentPage?.trim() || '';
  const currentPatientId = body?.dataset.tplCurrentPatientId?.trim() || '';
  const currentCoordinationId = body?.dataset.tplCurrentCoordinationId?.trim() || '';
  const currentColloquiumId = body?.dataset.tplCurrentColloquiumId?.trim() || '';
  const href = hasWindow ? window.location.href : '';
  const pathname = hasWindow ? window.location.pathname : '';
  const guiPart = currentPage || deriveGuiPartFromPath(pathname);

  if (hasWindow) {
    const parts = pathname.split('/').filter(Boolean);
    for (let i = 0; i < parts.length; i += 1) {
      const part = parts[i];
      if (!isIdLikeValue(part)) continue;
      const prev = parts[i - 1];
      const key = prev ? `${prev}_id` : 'path_id';
      addIdContext(ids, key, part);
    }
    const search = new URLSearchParams(window.location.search);
    search.forEach((value, key) => {
      if (ID_KEY_RE.test(key) || key.toLowerCase().endsWith('id')) {
        addIdContext(ids, key, value);
      }
    });
  }
  if (currentPatientId) addIdContext(ids, 'patient_id', currentPatientId);
  if (currentCoordinationId) addIdContext(ids, 'coordination_id', currentCoordinationId);
  if (currentColloquiumId) addIdContext(ids, 'colloquium_id', currentColloquiumId);

  recent.forEach((entry) => {
    if (entry.path) {
      const [pathPart, queryPart] = entry.path.split('?', 2);
      pathPart.split('/').filter(Boolean).forEach((seg, idx, all) => {
        if (!isIdLikeValue(seg)) return;
        const prev = all[idx - 1];
        addIdContext(ids, prev ? `${prev}_id` : 'api_path_id', seg);
      });
      if (queryPart) {
        const qp = new URLSearchParams(queryPart);
        qp.forEach((value, key) => {
          if (ID_KEY_RE.test(key) || key.toLowerCase().endsWith('id')) {
            addIdContext(ids, `api_${key}`, value);
          }
        });
      }
    }
    if (entry.detail !== undefined) {
      extractIdsFromObject(entry.detail, ids, 'error_detail');
    }
  });

  const latest = recent[recent.length - 1];
  const latestWithPath = [...recent].reverse().find((entry) => Boolean(entry.path && entry.path.trim()));
  const latestHttpWithPath = [...recent]
    .reverse()
    .find((entry) => entry.source === 'http' && Boolean(entry.path && entry.path.trim()));
  const latestErrorPath = latestHttpWithPath?.path || latestWithPath?.path || '';
  const selectedComponent = getLastCapturedComponent();
  return {
    href,
    page: currentPage,
    guiPart,
    ids: Array.from(ids.entries()),
    latestError: latest?.message ?? '',
    latestErrorPath,
    selectedComponent,
  };
}

function escapeHtml(value: string): string {
  return value
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#39;');
}

function buildDevForumCapturePayload(bannerMessage: string, recent: ClientErrorLogEntry[]) {
  const context = collectCurrentContext(recent);
  const captureUrl = (() => {
    try {
      const url = new URL(context.href || '/', window.location.origin);
      if (context.page) {
        url.searchParams.set('page', context.page);
      }
      return url.toString();
    } catch {
      return context.href || '/';
    }
  })();
  const captureState = {
    source: 'support_ticket',
    href: context.href,
    page: context.page || null,
    gui_part: context.guiPart,
    ids: context.ids.map(([key, value]) => ({ key, value })),
    latest_error: context.latestError,
    latest_error_path: context.latestErrorPath,
    selected_component: context.selectedComponent?.component ?? null,
    component_captured_at: context.selectedComponent?.captured_at ?? null,
    captured_at: new Date().toISOString(),
  };
  const requestTextLines = [
    `Automatic error capture`,
    ``,
    `Error: ${bannerMessage}`,
    `GUI part: ${context.guiPart}`,
    `Link: ${context.href || '(unavailable)'}`,
    context.selectedComponent?.component.selector
      ? `Component selector: ${context.selectedComponent.component.selector}`
      : `Component selector: (not available)`,
    `Latest API path: ${context.latestErrorPath || '(not available)'}`,
  ];
  const requestTextHtml = requestTextLines.map((line) => escapeHtml(line)).join('<br/>');
  return {
    capture_url: captureUrl,
    capture_gui_part: context.guiPart,
    capture_state_json: JSON.stringify(captureState),
    request_text: requestTextHtml,
  };
}

const buildFriendlyBody = (bannerMessage: string, recent: ClientErrorLogEntry[]): string => {
  const context = collectCurrentContext(recent);
  const idLines = context.ids.length
    ? context.ids.map(([key, value]) => `- ${key}: ${value}`)
    : ['- (no context IDs found)'];
  return [
    'Hello support team,',
    '',
    'I ran into an issue in TPL App and would appreciate your help.',
    '',
    `Current error message: ${bannerMessage}`,
    `Relevant GUI part: ${context.guiPart}`,
    `Relevant data context link: ${context.href || '(unavailable)'}`,
    '',
    'Relevant context IDs:',
    ...idLines,
    '',
    `Latest logged error message: ${context.latestError || '(no recent log message)'}`,
    `Latest logged API path: ${context.latestErrorPath || '(not available)'}`,
    '',
    'I attached a log file with recent technical details from the client error log.',
    'Please let me know if you need any additional context (steps, timestamp, user workflow).',
    '',
    'Thank you very much!',
  ].join('\r\n');
};

const buildSubject = (bannerMessage: string): string => {
  const normalized = bannerMessage.trim().replace(/\s+/g, ' ');
  const shortened = normalized.length > 80 ? `${normalized.slice(0, 77)}...` : normalized;
  return `TPL App issue report: ${shortened || 'Unexpected error'}`;
};

const downloadFile = (filename: string, content: string, mimeType: string): void => {
  const blob = new Blob([content], { type: mimeType });
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement('a');
  anchor.href = url;
  anchor.download = filename;
  document.body.appendChild(anchor);
  anchor.click();
  document.body.removeChild(anchor);
  URL.revokeObjectURL(url);
};

let cachedSupportEmail: string | null = null;

async function getSupportEmail(): Promise<string> {
  if (cachedSupportEmail) return cachedSupportEmail;
  const config = await api.getSupportTicketConfig();
  cachedSupportEmail = config.support_email;
  return cachedSupportEmail;
}

export interface OpenTicketDraftResult {
  dev_forum_capture_created: boolean;
  dev_forum_request_id: number | null;
}

export async function openTicketDraft(bannerMessage: string): Promise<OpenTicketDraftResult> {
  const supportEmail = await getSupportEmail();
  const subject = buildSubject(bannerMessage);
  const recent = getRecentErrorLog(40);
  const devForumPayload = buildDevForumCapturePayload(bannerMessage, recent);
  let devForumCaptureCreated = false;
  let devForumRequestId: number | null = null;
  try {
    const response = await api.captureSupportTicketInDevForum(devForumPayload);
    devForumCaptureCreated = true;
    devForumRequestId = response.request_id;
    if (typeof window !== 'undefined') {
      window.dispatchEvent(new CustomEvent(DEV_FORUM_CAPTURE_CREATED_EVENT, {
        detail: { request_id: response.request_id },
      }));
    }
  } catch {
    devForumCaptureCreated = false;
  }
  const body = buildFriendlyBody(bannerMessage, recent);
  const attachmentText = buildAttachmentText(bannerMessage);
  const attachmentBase64 = wrapBase64(utf8ToBase64(attachmentText));
  const boundary = `tpl-ticket-${Date.now()}`;
  const eml = [
    `To: ${supportEmail}`,
    `Subject: ${subject}`,
    'MIME-Version: 1.0',
    `Content-Type: multipart/mixed; boundary="${boundary}"`,
    '',
    `--${boundary}`,
    'Content-Type: text/plain; charset="UTF-8"',
    'Content-Transfer-Encoding: 8bit',
    '',
    body,
    '',
    `--${boundary}`,
    'Content-Type: text/plain; charset="UTF-8"; name="tpl-error-log.txt"',
    'Content-Disposition: attachment; filename="tpl-error-log.txt"',
    'Content-Transfer-Encoding: base64',
    '',
    attachmentBase64,
    '',
    `--${boundary}--`,
    '',
  ].join('\r\n');
  downloadFile('tpl-open-ticket.eml', eml, 'message/rfc822');
  return {
    dev_forum_capture_created: devForumCaptureCreated,
    dev_forum_request_id: devForumRequestId,
  };
}
