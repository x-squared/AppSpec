import { useCallback, useEffect, useMemo, useState } from 'react';
import { api, type AppUser, type DevRequest } from '../../api';
import { toUserErrorMessage } from '../../api/error';
import { useI18n } from '../../i18n/i18n';
import { DEV_FORUM_CAPTURE_CREATED_EVENT } from '../../views/layout/devForumEvents';
import { openDevForumContextWithHighlight } from '../../views/layout/devForumHighlight';
import { getCurrentCaptureContext, withSelectedComponent } from './devForumCaptureUtils';
import DevForumReadOnlyDialog from './DevForumReadOnlyDialog';
import { useDevForumComponentPicker } from './hooks/useDevForumComponentPicker';
import type { CapturedContextPayload, DevForumTabKey } from './types';
import CapturingTab from './tabs/CapturingTab';
import DevelopmentTab from './tabs/DevelopmentTab';
import ReviewTab from './tabs/ReviewTab';
import './DevForumSurface.css';

interface DevForumSurfaceProps {
  title: string;
  includeCapturing: boolean;
  includeClaimedByOtherDevelopers: boolean;
  enableDeveloperFilter: boolean;
  hasDevRole: boolean;
  compact?: boolean;
}

function asPrettyJson(raw: string): string {
  try {
    const parsed = JSON.parse(raw);
    return JSON.stringify(parsed, null, 2);
  } catch {
    return raw;
  }
}

function escapeHtml(value: string): string {
  return value
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#39;');
}

function htmlToPlainText(html: string): string {
  const element = document.createElement('div');
  element.innerHTML = html || '';
  return (element.textContent || '').trim();
}

function buildCursorPromptHtmlFromRequest(item: DevRequest): string {
  const rawRequestHtml = (item.request_text || '').trim();
  const requestHtml = rawRequestHtml
    ? `<div>${rawRequestHtml}</div>`
    : `<div><p>${escapeHtml('(empty)')}</p></div>`;
  const captureState = asPrettyJson(item.capture_state_json);
  return [
    requestHtml,
    `<p><strong>Context information:</strong></p>`,
    `<ul>`,
    `<li><strong>Request ID:</strong> ${escapeHtml(String(item.id))}</li>`,
    `<li><strong>Status:</strong> ${escapeHtml(item.status)}</li>`,
    `<li><strong>Submitter:</strong> ${escapeHtml(item.submitter_user?.name ?? '-')}</li>`,
    `<li><strong>Claimed by:</strong> ${escapeHtml(item.claimed_by_user?.name ?? '-')}</li>`,
    `<li><strong>GUI part:</strong> ${escapeHtml(item.capture_gui_part || '-')}</li>`,
    `<li><strong>Capture URL:</strong> ${escapeHtml(item.capture_url || '-')}</li>`,
    `</ul>`,
    `<p><strong>Captured state JSON:</strong></p>`,
    `<pre>${escapeHtml(captureState)}</pre>`,
  ].join('');
}

function htmlToMarkdown(html: string): string {
  const root = document.createElement('div');
  root.innerHTML = html || '';

  const walk = (node: Node): string => {
    if (node.nodeType === Node.TEXT_NODE) {
      return (node.textContent || '').replace(/\s+/g, ' ');
    }
    if (node.nodeType !== Node.ELEMENT_NODE) {
      return '';
    }
    const element = node as HTMLElement;
    const tag = element.tagName.toLowerCase();
    const children = Array.from(element.childNodes).map(walk).join('');
    if (tag === 'br') return '\n';
    if (tag === 'strong' || tag === 'b') return `**${children.trim()}**`;
    if (tag === 'em' || tag === 'i') return `*${children.trim()}*`;
    if (tag === 'h1' || tag === 'h2' || tag === 'h3') return `${children.trim()}\n\n`;
    if (tag === 'code') return `\`${children.trim()}\``;
    if (tag === 'pre') return `\n\`\`\`\n${element.textContent || ''}\n\`\`\`\n\n`;
    if (tag === 'li') return `- ${children.trim()}\n`;
    if (tag === 'ul' || tag === 'ol') return `\n${children}\n`;
    if (tag === 'p' || tag === 'div') return `${children.trim()}\n\n`;
    if (tag === 'a') {
      const href = element.getAttribute('href') || '';
      return href ? `[${children.trim()}](${href})` : children;
    }
    return children;
  };

  return Array.from(root.childNodes)
    .map(walk)
    .join('')
    .replace(/\n{3,}/g, '\n\n')
    .trim();
}

function buildCursorCopyPayload(markdown: string): string {
  const normalized = markdown.trim();
  if (!normalized) {
    return [
      'MODE: IMPLEMENT TICKET ONLY',
      '',
      'TICKET:',
      '(empty)',
      '',
      'SCOPE:',
      '- Allowed files/areas: (not specified in ticket)',
      '- Do not touch: (not specified in ticket)',
      '',
      'DONE WHEN:',
      '- Requested change is implemented and visible in UI/behavior.',
      '- Existing behavior outside ticket scope remains unchanged.',
      '',
      'OUT OF SCOPE:',
      '- Unrelated refactors and behavior changes.',
      '',
      'CONTEXT:',
      '(none)',
      '',
      'REQUIREMENT: First restate the ticket in 3 bullets and wait for my OK before coding.',
    ].join('\n');
  }
  if (/^\s*MODE:\s*IMPLEMENT TICKET ONLY\b/i.test(normalized)) {
    return normalized;
  }
  const [ticketBlock, ...restBlocks] = normalized.split(/\n\s*\n/);
  const ticket = ticketBlock.replace(/\s+/g, ' ').trim() || '(empty)';
  const context = restBlocks.join('\n\n').trim();
  return [
    'MODE: IMPLEMENT TICKET ONLY',
    '',
    'TICKET:',
    ticket,
    '',
    'SCOPE:',
    '- Allowed files/areas: (not specified in ticket)',
    '- Do not touch: (not specified in ticket)',
    '',
    'DONE WHEN:',
    '- Requested behavior is implemented exactly as described.',
    '- Add/adjust error handling and user-facing message if failure is possible.',
    '- Build/typecheck for touched frontend/backend parts passes.',
    '',
    'OUT OF SCOPE:',
    '- Additional UX or architecture changes not required by this ticket.',
    '',
    `CONTEXT:\n${context || '(none)'}`,
    '',
    'REQUIREMENT: First restate the ticket in 3 bullets and wait for my OK before coding.',
  ].join('\n');
}

async function copyTextToClipboard(text: string): Promise<boolean> {
  if (navigator.clipboard?.writeText) {
    try {
      await navigator.clipboard.writeText(text);
      return true;
    } catch {
      // fallback below
    }
  }
  const textarea = document.createElement('textarea');
  textarea.value = text;
  textarea.setAttribute('readonly', 'true');
  textarea.style.position = 'fixed';
  textarea.style.opacity = '0';
  document.body.appendChild(textarea);
  textarea.focus();
  textarea.select();
  let copied = false;
  try {
    copied = document.execCommand('copy');
  } catch {
    copied = false;
  }
  document.body.removeChild(textarea);
  return copied;
}

export default function DevForumSurface({
  title,
  includeCapturing,
  includeClaimedByOtherDevelopers,
  enableDeveloperFilter,
  hasDevRole,
  compact = false,
}: DevForumSurfaceProps) {
  const { t } = useI18n();
  const [activeTab, setActiveTab] = useState<DevForumTabKey>(includeCapturing ? 'capturing' : 'review');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [captureDraft, setCaptureDraft] = useState('');
  const [capturedContext, setCapturedContext] = useState<CapturedContextPayload | null>(null);
  const [reviewItems, setReviewItems] = useState<DevRequest[]>([]);
  const [developmentItems, setDevelopmentItems] = useState<DevRequest[]>([]);
  const [developerUsers, setDeveloperUsers] = useState<AppUser[]>([]);
  const [selectedDeveloperFilter, setSelectedDeveloperFilter] = useState<string>('all');
  const [developmentNoteDraft, setDevelopmentNoteDraft] = useState<Record<number, string>>({});
  const [developmentResponseDraft, setDevelopmentResponseDraft] = useState<Record<number, string>>({});
  const [reviewRejectDraft, setReviewRejectDraft] = useState<Record<number, string>>({});
  const [readOnlyDialogLineage, setReadOnlyDialogLineage] = useState<DevRequest[]>([]);
  const [readOnlyDialogIndex, setReadOnlyDialogIndex] = useState(0);
  const [saving, setSaving] = useState(false);
  const {
    pickingComponent,
    selectedComponent,
    startPicking,
    stopPicking,
    clearSelectedComponent,
  } = useDevForumComponentPicker();

  const refreshReview = useCallback(async () => {
    const data = await api.listReviewDevRequests();
    setReviewItems(data);
  }, []);

  const refreshDevelopment = useCallback(async () => {
    if (!hasDevRole) {
      setDevelopmentItems([]);
      return;
    }
    const filterId = selectedDeveloperFilter === 'all' ? null : Number(selectedDeveloperFilter);
    const data = await api.listDevelopmentDevRequests({
      include_claimed_by_other_developers: includeClaimedByOtherDevelopers,
      filter_claimed_by_user_id: Number.isFinite(filterId as number) ? filterId : null,
    });
    setDevelopmentItems(data);
  }, [hasDevRole, includeClaimedByOtherDevelopers, selectedDeveloperFilter]);

  const refreshAll = useCallback(async () => {
    setLoading(true);
    setError('');
    try {
      await Promise.all([
        refreshReview(),
        refreshDevelopment(),
        hasDevRole && enableDeveloperFilter ? api.listUsers('DEV').then(setDeveloperUsers) : Promise.resolve(),
      ]);
    } catch (err) {
      setError(toUserErrorMessage(err, t('devForum.errors.loadFailed', 'Could not load Dev-Forum data.')));
    } finally {
      setLoading(false);
    }
  }, [enableDeveloperFilter, hasDevRole, refreshDevelopment, refreshReview, t]);

  useEffect(() => {
    void refreshAll();
  }, [refreshAll]);

  useEffect(() => {
    const onCaptureCreated = () => {
      void refreshAll();
    };
    window.addEventListener(DEV_FORUM_CAPTURE_CREATED_EVENT, onCaptureCreated);
    return () => {
      window.removeEventListener(DEV_FORUM_CAPTURE_CREATED_EVENT, onCaptureCreated);
    };
  }, [refreshAll]);

  const visibleTabs = useMemo<DevForumTabKey[]>(() => {
    const tabs: DevForumTabKey[] = [];
    if (includeCapturing) tabs.push('capturing');
    tabs.push('review');
    if (hasDevRole) tabs.push('development');
    return tabs;
  }, [hasDevRole, includeCapturing]);

  useEffect(() => {
    if (visibleTabs.includes(activeTab)) return;
    setActiveTab(visibleTabs[0] ?? 'review');
  }, [activeTab, visibleTabs]);

  const onCaptureContext = () => {
    setCapturedContext(getCurrentCaptureContext());
  };

  const onSubmitCapture = async () => {
    if (!capturedContext) return;
    if (!captureDraft.trim()) return;
    setSaving(true);
    setError('');
    try {
      await api.createDevRequest({
        ...capturedContext,
        capture_state_json: withSelectedComponent(capturedContext.capture_state_json, selectedComponent),
        request_text: captureDraft.trim(),
      });
      setCaptureDraft('');
      setCapturedContext(null);
      clearSelectedComponent();
      await refreshAll();
    } catch (err) {
      setError(toUserErrorMessage(err, t('devForum.errors.captureFailed', 'Could not save request.')));
    } finally {
      setSaving(false);
    }
  };

  const onClaimRequest = async (requestId: number) => {
    setSaving(true);
    setError('');
    try {
      await api.claimDevRequest(requestId);
      await refreshDevelopment();
    } catch (err) {
      setError(toUserErrorMessage(err, t('devForum.errors.claimFailed', 'Could not claim request.')));
    } finally {
      setSaving(false);
    }
  };

  const onDecision = async (requestId: number, decision: 'REJECTED' | 'IMPLEMENTED') => {
    setSaving(true);
    setError('');
    try {
      await api.decideDevRequest(requestId, {
        decision,
        developer_note_text: developmentNoteDraft[requestId] ?? '',
        developer_response_text: developmentResponseDraft[requestId] ?? '',
      });
      await refreshAll();
    } catch (err) {
      setError(toUserErrorMessage(err, t('devForum.errors.decisionFailed', 'Could not save decision.')));
    } finally {
      setSaving(false);
    }
  };

  const onReviewAccept = async (requestId: number) => {
    setSaving(true);
    setError('');
    try {
      await api.acceptDevRequestReview(requestId);
      await refreshReview();
    } catch (err) {
      setError(toUserErrorMessage(err, t('devForum.errors.reviewAcceptFailed', 'Could not accept review result.')));
    } finally {
      setSaving(false);
    }
  };

  const onReviewReject = async (requestId: number) => {
    const reviewText = (reviewRejectDraft[requestId] ?? '').trim();
    if (!reviewText) return;
    setSaving(true);
    setError('');
    try {
      await api.rejectDevRequestReview(requestId, reviewText);
      setReviewRejectDraft((prev) => ({ ...prev, [requestId]: '' }));
      await refreshAll();
    } catch (err) {
      setError(toUserErrorMessage(err, t('devForum.errors.reviewRejectFailed', 'Could not reopen request.')));
    } finally {
      setSaving(false);
    }
  };

  const onOpenContext = (item: DevRequest) => {
    openDevForumContextWithHighlight(item.capture_url || '/', item.capture_state_json, item.capture_gui_part);
  };

  const onCancelCapture = () => {
    setCaptureDraft('');
    setCapturedContext(null);
    clearSelectedComponent();
    stopPicking();
  };

  const onOpenPreviousRequest = async (requestId: number) => {
    setSaving(true);
    setError('');
    try {
      const lineage = await api.listDevRequestLineage(requestId);
      const index = lineage.findIndex((entry) => entry.id === requestId);
      setReadOnlyDialogLineage(lineage);
      setReadOnlyDialogIndex(index >= 0 ? index : 0);
    } catch (err) {
      setError(toUserErrorMessage(err, t('devForum.errors.loadFailed', 'Could not load Dev-Forum data.')));
    } finally {
      setSaving(false);
    }
  };

  const readOnlyDialogRequest = readOnlyDialogLineage[readOnlyDialogIndex] ?? null;

  return (
    <section className={`dev-forum-surface ${compact ? 'compact' : ''}`}>
      <header className="dev-forum-header">
        <h2 className="detail-section-heading">{title}</h2>
        <button type="button" className="patients-add-btn" onClick={() => void refreshAll()} disabled={loading || saving}>
          {t('devForum.actions.refresh', 'Refresh')}
        </button>
      </header>

      <nav className="detail-tabs">
        {visibleTabs.map((tab) => (
          <button
            key={tab}
            type="button"
            className={`detail-tab ${activeTab === tab ? 'active' : ''}`}
            onClick={() => setActiveTab(tab)}
          >
            {tab === 'capturing' ? t('devForum.tabs.capturing', 'Capturing') : null}
            {tab === 'review' ? t('devForum.tabs.review', 'Review') : null}
            {tab === 'development' ? t('devForum.tabs.development', 'Development') : null}
          </button>
        ))}
      </nav>

      {error ? <p className="dev-forum-error">{error}</p> : null}
      {loading ? <p className="status">{t('devForum.status.loading', 'Loading Dev-Forum...')}</p> : null}

      {!loading && activeTab === 'capturing' && includeCapturing ? (
        <CapturingTab
          saving={saving}
          captureDraft={captureDraft}
          capturedContext={capturedContext}
          selectedComponent={selectedComponent}
          pickingComponent={pickingComponent}
          onCaptureContext={onCaptureContext}
          onStartPicking={startPicking}
          onCaptureDraftChange={setCaptureDraft}
          onSubmitCapture={onSubmitCapture}
          onCancelCapture={onCancelCapture}
        />
      ) : null}

      {!loading && activeTab === 'review' ? (
        <ReviewTab
          reviewItems={reviewItems}
          saving={saving}
          reviewRejectDraft={reviewRejectDraft}
          onSetReviewRejectDraft={(requestId, next) => {
            setReviewRejectDraft((prev) => ({ ...prev, [requestId]: next }));
          }}
          onReviewAccept={onReviewAccept}
          onReviewReject={onReviewReject}
          onOpenContext={onOpenContext}
          onOpenPreviousRequest={onOpenPreviousRequest}
        />
      ) : null}

      {!loading && activeTab === 'development' && hasDevRole ? (
        <DevelopmentTab
          enableDeveloperFilter={enableDeveloperFilter}
          developerUsers={developerUsers}
          selectedDeveloperFilter={selectedDeveloperFilter}
          onSetSelectedDeveloperFilter={setSelectedDeveloperFilter}
          developmentItems={developmentItems}
          saving={saving}
          developmentNoteDraft={developmentNoteDraft}
          developmentResponseDraft={developmentResponseDraft}
          onSetDevelopmentNoteDraft={(requestId, next) => {
            setDevelopmentNoteDraft((prev) => ({ ...prev, [requestId]: next }));
          }}
          onSetDevelopmentResponseDraft={(requestId, next) => {
            setDevelopmentResponseDraft((prev) => ({ ...prev, [requestId]: next }));
          }}
          onClaimRequest={onClaimRequest}
          onDecision={onDecision}
          onOpenContext={onOpenContext}
          onOpenPreviousRequest={onOpenPreviousRequest}
          onCopyRequestText={(item) => {
            void (async () => {
              const promptHtml = buildCursorPromptHtmlFromRequest(item);
              setDevelopmentNoteDraft((prev) => ({ ...prev, [item.id]: promptHtml }));
              const copied = await copyTextToClipboard(buildCursorCopyPayload(htmlToMarkdown(promptHtml)));
              if (!copied) {
                setError(t('devForum.errors.copyFailed', 'Could not copy text to clipboard.'));
              }
            })();
          }}
          onCopyNoteForCursor={(requestId) => {
            void (async () => {
              const noteHtml = developmentNoteDraft[requestId] ?? '';
              const noteMarkdown = htmlToMarkdown(noteHtml);
              const copied = await copyTextToClipboard(
                buildCursorCopyPayload(noteMarkdown || htmlToPlainText(noteHtml)),
              );
              if (!copied) {
                setError(t('devForum.errors.copyFailed', 'Could not copy text to clipboard.'));
              }
            })();
          }}
        />
      ) : null}
      {readOnlyDialogRequest ? (
        <DevForumReadOnlyDialog
          lineage={readOnlyDialogLineage}
          activeIndex={readOnlyDialogIndex}
          onSetActiveIndex={setReadOnlyDialogIndex}
          onClose={() => setReadOnlyDialogLineage([])}
        />
      ) : null}
    </section>
  );
}
