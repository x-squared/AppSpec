import type { DevRequest } from '../../api';
import { useI18n } from '../../i18n/i18n';

interface DevForumReadOnlyDialogProps {
  lineage: DevRequest[];
  activeIndex: number;
  onSetActiveIndex: (index: number) => void;
  onClose: () => void;
}

function htmlToPlainText(html: string): string {
  if (typeof window === 'undefined' || typeof document === 'undefined') {
    return html;
  }
  const element = document.createElement('div');
  element.innerHTML = html || '';
  return (element.textContent || '').replace(/\s+/g, ' ').trim();
}

function toTicketPrefix(html: string): string {
  const plain = htmlToPlainText(html);
  if (!plain) return '';
  const limit = 96;
  if (plain.length <= limit) return plain;
  const candidate = plain.slice(0, limit - 1);
  const lastSpace = candidate.lastIndexOf(' ');
  const base = lastSpace >= 48 ? candidate.slice(0, lastSpace) : candidate;
  return `${base.trim()}...`;
}

function toTicketSnippet(html: string, fallback: string): string {
  const plain = htmlToPlainText(html);
  if (!plain) return fallback;
  const limit = 72;
  if (plain.length <= limit) return plain;
  const candidate = plain.slice(0, limit - 1);
  const lastSpace = candidate.lastIndexOf(' ');
  const base = lastSpace >= 30 ? candidate.slice(0, lastSpace) : candidate;
  return `${base.trim()}...`;
}

function asPrettyJson(raw: string): string {
  try {
    const parsed = JSON.parse(raw);
    return JSON.stringify(parsed, null, 2);
  } catch {
    return raw;
  }
}

function formatDialogDateTime(value: string | null): string {
  if (!value) return '-';
  const parsed = new Date(value);
  if (Number.isNaN(parsed.getTime())) return value;
  return parsed.toLocaleString();
}

export default function DevForumReadOnlyDialog({
  lineage,
  activeIndex,
  onSetActiveIndex,
  onClose,
}: DevForumReadOnlyDialogProps) {
  const { t } = useI18n();
  const activeRequest = lineage[activeIndex] ?? null;
  if (!activeRequest) {
    return null;
  }
  const originalRequest = lineage[0] ?? activeRequest;
  const originalPrefix = toTicketPrefix(originalRequest.request_text);
  const reversedLineage = [...lineage].reverse();

  return (
    <div className="dev-forum-readonly-dialog-backdrop" onClick={onClose}>
      <div
        className="ui-panel-section dev-forum-readonly-dialog"
        onClick={(event) => event.stopPropagation()}
      >
        <button
          type="button"
          className="dev-forum-dialog-close-icon"
          aria-label={t('devForum.readOnlyDialog.close', 'Close')}
          title={t('devForum.readOnlyDialog.close', 'Close')}
          onClick={onClose}
        >
          ×
        </button>
        <div className="dev-forum-readonly-dialog-scroll">
          <header className="dev-forum-header">
            <h3 className="detail-section-heading">
              <span className="dev-forum-readonly-title-line" title={htmlToPlainText(originalRequest.request_text)}>
                {originalPrefix || t('devForum.readOnlyDialog.title', 'Previous ticket')}
              </span>
            </h3>
          </header>
          <div className="dev-forum-actions-row">
            <button
              type="button"
              className="patients-add-btn"
              disabled={activeIndex <= 0}
              onClick={() => onSetActiveIndex(Math.max(0, activeIndex - 1))}
            >
              {t('devForum.readOnlyDialog.previous', 'Previous')}
            </button>
            <button
              type="button"
              className="patients-add-btn"
              disabled={activeIndex >= lineage.length - 1}
              onClick={() => onSetActiveIndex(Math.min(lineage.length - 1, activeIndex + 1))}
            >
              {t('devForum.readOnlyDialog.next', 'Next')}
            </button>
            <span className="dev-forum-meta">
              {t('devForum.readOnlyDialog.position', 'Ticket {current} of {total}')
                .replace('{current}', String(activeIndex + 1))
                .replace('{total}', String(lineage.length))}
            </span>
          </div>

          <h4 className="detail-section-heading">{t('devForum.readOnlyDialog.historyTitle', 'Ticket line')}</h4>
          <div className="dev-forum-ticket-timeline">
            {reversedLineage.map((entry) => (
              <button
                key={entry.id}
                type="button"
                className={`dev-forum-ticket-timeline-item ${entry.id === activeRequest.id ? 'active' : ''}`}
                onClick={() => {
                  const nextIndex = lineage.findIndex((item) => item.id === entry.id);
                  if (nextIndex >= 0) {
                    onSetActiveIndex(nextIndex);
                  }
                }}
              >
                <span className="dev-forum-ticket-timeline-dot" aria-hidden="true" />
              <span className="dev-forum-ticket-timeline-label">#{entry.id} - {entry.status}</span>
              <span className="dev-forum-ticket-timeline-text">
                {toTicketSnippet(entry.request_text, t('devForum.request.summaryFallback', 'No request text.'))}
              </span>
              </button>
            ))}
          </div>

          <h4 className="detail-section-heading">{t('devForum.readOnlyDialog.metaTitle', 'Ticket details')}</h4>
          <dl className="dev-forum-readonly-meta-grid">
            <dt>{t('devForum.request.status', 'Status')}</dt>
            <dd>{activeRequest.status}</dd>
            <dt>{t('devForum.request.submitter', 'Submitter')}</dt>
            <dd>{activeRequest.submitter_user?.name ?? '-'}</dd>
            <dt>{t('devForum.request.claimedBy', 'Claimed by')}</dt>
            <dd>{activeRequest.claimed_by_user?.name ?? '-'}</dd>
            <dt>{t('devForum.readOnlyDialog.decision', 'Decision')}</dt>
            <dd>{activeRequest.decision ?? '-'}</dd>
            <dt>{t('devForum.readOnlyDialog.parentTicket', 'Parent ticket')}</dt>
            <dd>{activeRequest.parent_request_id ?? '-'}</dd>
            <dt>{t('devForum.readOnlyDialog.createdAt', 'Created at')}</dt>
            <dd>{formatDialogDateTime(activeRequest.created_at)}</dd>
            <dt>{t('devForum.readOnlyDialog.changedAt', 'Changed at')}</dt>
            <dd>{formatDialogDateTime(activeRequest.changed_at ?? activeRequest.updated_at)}</dd>
            <dt>{t('devForum.readOnlyDialog.closedAt', 'Closed at')}</dt>
            <dd>{formatDialogDateTime(activeRequest.closed_at)}</dd>
          </dl>

          <h4 className="detail-section-heading">{t('devForum.readOnlyDialog.requestTextTitle', 'Request')}</h4>
          <div className="dev-forum-request-box">
            <p className="dev-forum-text" dangerouslySetInnerHTML={{ __html: activeRequest.request_text }} />
          </div>
          {activeRequest.developer_note_text ? (
            <>
              <h4 className="detail-section-heading">{t('devForum.readOnlyDialog.developerNoteTitle', 'Prompt')}</h4>
              <p className="dev-forum-text" dangerouslySetInnerHTML={{ __html: activeRequest.developer_note_text }} />
            </>
          ) : null}
          {activeRequest.developer_response_text ? (
            <>
              <h4 className="detail-section-heading">{t('devForum.review.developerReply', 'Developer reply')}</h4>
              <p className="dev-forum-text" dangerouslySetInnerHTML={{ __html: activeRequest.developer_response_text }} />
            </>
          ) : null}
          {activeRequest.user_review_text ? (
            <>
              <h4 className="detail-section-heading">{t('devForum.readOnlyDialog.userReviewTitle', 'User review')}</h4>
              <p className="dev-forum-text" dangerouslySetInnerHTML={{ __html: activeRequest.user_review_text }} />
            </>
          ) : null}
          <details className="dev-forum-context-details">
            <summary>{t('devForum.development.contextToggle', 'Show context information')}</summary>
            <pre className="dev-forum-capture-json">{asPrettyJson(activeRequest.capture_state_json)}</pre>
          </details>
        </div>
      </div>
    </div>
  );
}
