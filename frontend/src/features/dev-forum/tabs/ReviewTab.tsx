import { useState } from 'react';
import { useI18n } from '../../../i18n/i18n';
import type { DevRequest } from '../../../api';
import RichTextEditor from '../../../views/layout/RichTextEditor';

interface ReviewTabProps {
  reviewItems: DevRequest[];
  saving: boolean;
  reviewRejectDraft: Record<number, string>;
  onSetReviewRejectDraft: (requestId: number, next: string) => void;
  onReviewAccept: (requestId: number) => Promise<void>;
  onReviewReject: (requestId: number) => Promise<void>;
  onOpenContext: (item: DevRequest) => void;
  onOpenPreviousRequest: (requestId: number) => void;
}

export default function ReviewTab({
  reviewItems,
  saving,
  reviewRejectDraft,
  onSetReviewRejectDraft,
  onReviewAccept,
  onReviewReject,
  onOpenContext,
  onOpenPreviousRequest,
}: ReviewTabProps) {
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
      {reviewItems.length === 0 ? <p className="status">{t('devForum.review.empty', 'No review items right now.')}</p> : null}
      {reviewItems.map((item) => {
        const parentRequestId = item.parent_request_id;
        const isExpanded = expandedRequestId === item.id;
        return (
        <article key={item.id} className="ui-panel-section dev-forum-item">
          <h3 className="detail-section-heading">
            {t('devForum.request.title', 'Request')} #{item.id}
          </h3>
          <p className="dev-forum-meta">{t('devForum.request.status', 'Status')}: {item.status}</p>
          <p className="dev-forum-meta">{t('devForum.request.guiPart', 'GUI part')}: {item.capture_gui_part || '-'}</p>
          <p className="dev-forum-meta">{t('devForum.readOnlyDialog.createdAt', 'Created at')}: {formatDate(item.created_at)}</p>
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
            <button type="button" className="patients-save-btn" onClick={() => void onReviewAccept(item.id)} disabled={saving}>
              {t('devForum.review.accept', 'Accept')}
            </button>
          </div>
          {isExpanded ? (
            <>
              <div className="dev-forum-request-box">
                <p className="dev-forum-text" dangerouslySetInnerHTML={{ __html: item.request_text }} />
              </div>
              {item.developer_response_text ? (
                <>
                  <h4 className="detail-section-heading">{t('devForum.review.developerReply', 'Developer reply')}</h4>
                  <p className="dev-forum-text" dangerouslySetInnerHTML={{ __html: item.developer_response_text }} />
                </>
              ) : null}
              <h4 className="detail-section-heading">{t('devForum.review.notAccepted', 'Not accepted')}</h4>
              <RichTextEditor
                value={reviewRejectDraft[item.id] ?? ''}
                onChange={(next) => onSetReviewRejectDraft(item.id, next)}
                ariaLabel={t('devForum.review.rejectEditorAria', 'Review reject editor')}
                boldTitle={t('devForum.editor.bold', 'Bold')}
                italicTitle={t('devForum.editor.italic', 'Italic')}
                underlineTitle={t('devForum.editor.underline', 'Underline')}
              />
              <div className="dev-forum-actions-row">
                <button type="button" className="patients-cancel-btn" onClick={() => void onReviewReject(item.id)} disabled={saving || !(reviewRejectDraft[item.id] ?? '').trim()}>
                  {t('devForum.review.sendRejection', 'Send rejection and reopen')}
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
