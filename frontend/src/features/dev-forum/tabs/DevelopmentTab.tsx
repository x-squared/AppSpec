import { useState } from 'react';
import { useI18n } from '../../../i18n/i18n';
import type { AppUser, DevRequest } from '../../../api';
import RichTextEditor from '../../../views/layout/RichTextEditor';
import { parseCaptureState } from '../devForumCaptureUtils';

interface DevelopmentTabProps {
  enableDeveloperFilter: boolean;
  developerUsers: AppUser[];
  selectedDeveloperFilter: string;
  onSetSelectedDeveloperFilter: (next: string) => void;
  developmentItems: DevRequest[];
  saving: boolean;
  developmentNoteDraft: Record<number, string>;
  developmentResponseDraft: Record<number, string>;
  onSetDevelopmentNoteDraft: (requestId: number, next: string) => void;
  onSetDevelopmentResponseDraft: (requestId: number, next: string) => void;
  onClaimRequest: (requestId: number) => Promise<void>;
  onDecision: (requestId: number, decision: 'REJECTED' | 'IMPLEMENTED') => Promise<void>;
  onOpenContext: (item: DevRequest) => void;
  onOpenPreviousRequest: (requestId: number) => void;
  onCopyRequestText: (item: DevRequest) => void;
  onCopyNoteForCursor: (requestId: number) => void;
}

export default function DevelopmentTab({
  enableDeveloperFilter,
  developerUsers,
  selectedDeveloperFilter,
  onSetSelectedDeveloperFilter,
  developmentItems,
  saving,
  developmentNoteDraft,
  developmentResponseDraft,
  onSetDevelopmentNoteDraft,
  onSetDevelopmentResponseDraft,
  onClaimRequest,
  onDecision,
  onOpenContext,
  onOpenPreviousRequest,
  onCopyRequestText,
  onCopyNoteForCursor,
}: DevelopmentTabProps) {
  const { t } = useI18n();
  const [expandedRequestId, setExpandedRequestId] = useState<number | null>(null);

  const htmlToSummary = (html: string): string => {
    const container = document.createElement('div');
    container.innerHTML = html || '';
    const plain = (container.textContent || '').replace(/\s+/g, ' ').trim();
    if (!plain) return t('devForum.request.summaryFallback', 'No request text.');
    const limit = 140;
    if (plain.length <= limit) return plain;
    return `${plain.slice(0, limit - 3).trim()}...`;
  };

  const formatDate = (value: string | null): string => {
    if (!value) return '-';
    const parsed = new Date(value);
    if (Number.isNaN(parsed.getTime())) return value;
    return parsed.toLocaleString();
  };

  return (
    <div className="dev-forum-list">
      {enableDeveloperFilter ? (
        <div className="dev-forum-filter">
          <label htmlFor="dev-forum-filter-select">{t('devForum.development.filterDeveloper', 'Filter by developer')}</label>
          <select
            id="dev-forum-filter-select"
            value={selectedDeveloperFilter}
            onChange={(event) => onSetSelectedDeveloperFilter(event.target.value)}
          >
            <option value="all">{t('devForum.development.filterAll', 'All developers')}</option>
            {developerUsers.map((user) => (
              <option key={user.id} value={String(user.id)}>
                {user.name}
              </option>
            ))}
          </select>
        </div>
      ) : null}
      {developmentItems.length === 0 ? <p className="status">{t('devForum.development.empty', 'No pending requests right now.')}</p> : null}
      {developmentItems.map((item) => {
        const captureState = parseCaptureState(item.capture_state_json);
        const parentRequestId = item.parent_request_id;
        const isExpanded = expandedRequestId === item.id;
        return (
          <article key={item.id} className="ui-panel-section dev-forum-item">
            <h3 className="detail-section-heading">
              {t('devForum.request.title', 'Request')} #{item.id}
            </h3>
            <p className="dev-forum-meta">{t('devForum.request.status', 'Status')}: {item.status}</p>
            <p className="dev-forum-meta">{t('devForum.request.submitter', 'Submitter')}: {item.submitter_user?.name ?? '-'}</p>
            <p className="dev-forum-meta">{t('devForum.request.claimedBy', 'Claimed by')}: {item.claimed_by_user?.name ?? '-'}</p>
            <p className="dev-forum-meta">{t('devForum.readOnlyDialog.createdAt', 'Created at')}: {formatDate(item.created_at)}</p>
            <p className="dev-forum-meta">{t('devForum.request.guiPart', 'GUI part')}: {item.capture_gui_part || '-'}</p>
            <div className="dev-forum-request-box dev-forum-summary-box">
              <p className="dev-forum-text">{htmlToSummary(item.request_text)}</p>
            </div>
            <div className="dev-forum-actions-row">
              <button
                type="button"
                className="patients-add-btn"
                onClick={() => setExpandedRequestId(isExpanded ? null : item.id)}
              >
                {isExpanded
                  ? t('devForum.actions.collapseTicket', 'Collapse ticket')
                  : t('devForum.actions.showTicket', 'Show ticket')}
              </button>
              <button type="button" className="patients-add-btn" onClick={() => onOpenContext(item)}>
                {t('devForum.actions.openContext', 'Open context')}
              </button>
              {parentRequestId !== null ? (
                <button type="button" className="patients-add-btn" onClick={() => onOpenPreviousRequest(parentRequestId)}>
                  {t('devForum.actions.openPreviousTicket', 'Open previous ticket')}
                </button>
              ) : null}
              <button type="button" className="patients-add-btn" onClick={() => onCopyRequestText(item)}>
                {t('devForum.development.copyRequest', 'Copy request')}
              </button>
              <button type="button" className="patients-add-btn" onClick={() => void onClaimRequest(item.id)} disabled={saving}>
                {t('devForum.development.claim', 'Claim')}
              </button>
            </div>
            {isExpanded ? (
              <>
                <div className="dev-forum-request-box">
                  <p className="dev-forum-text" dangerouslySetInnerHTML={{ __html: item.request_text }} />
                </div>
                <details className="dev-forum-context-details">
                  <summary>{t('devForum.development.contextToggle', 'Show context information')}</summary>
                  <pre className="dev-forum-capture-json">{JSON.stringify(captureState, null, 2)}</pre>
                </details>
                <h4 className="detail-section-heading">{t('devForum.development.notes', 'Prompt')}</h4>
                <RichTextEditor
                  value={developmentNoteDraft[item.id] ?? ''}
                  onChange={(next) => onSetDevelopmentNoteDraft(item.id, next)}
                  ariaLabel={t('devForum.development.notesEditorAria', 'Prompt editor')}
                  boldTitle={t('devForum.editor.bold', 'Bold')}
                  italicTitle={t('devForum.editor.italic', 'Italic')}
                  underlineTitle={t('devForum.editor.underline', 'Underline')}
                />
                <div className="dev-forum-actions-row">
                  <button
                    type="button"
                    className="patients-add-btn"
                    onClick={() => onCopyNoteForCursor(item.id)}
                  >
                    {t('devForum.development.copyForCursor', 'Copy prompt for Cursor')}
                  </button>
                </div>
                <h4 className="detail-section-heading">{t('devForum.development.response', 'Reply to user')}</h4>
                <RichTextEditor
                  value={developmentResponseDraft[item.id] ?? ''}
                  onChange={(next) => onSetDevelopmentResponseDraft(item.id, next)}
                  ariaLabel={t('devForum.development.responseEditorAria', 'Developer response editor')}
                  boldTitle={t('devForum.editor.bold', 'Bold')}
                  italicTitle={t('devForum.editor.italic', 'Italic')}
                  underlineTitle={t('devForum.editor.underline', 'Underline')}
                />
                <div className="dev-forum-actions-row">
                  <button type="button" className="patients-cancel-btn" onClick={() => void onDecision(item.id, 'REJECTED')} disabled={saving}>
                    {t('devForum.development.reject', 'Rejected')}
                  </button>
                  <button type="button" className="patients-save-btn" onClick={() => void onDecision(item.id, 'IMPLEMENTED')} disabled={saving}>
                    {t('devForum.development.acceptImplemented', 'Accepted and implemented')}
                  </button>
                </div>
              </>
            ) : null}
          </article>
        );
      })}
    </div>
  );
}
