import { useEffect, useState } from 'react';
import { toUserErrorMessage } from '../../api/error';
import { useI18n } from '../../i18n/i18n';
import { openTicketDraft } from './openTicket';

interface ErrorBannerProps {
  message: string;
  className?: string;
}

export default function ErrorBanner({ message, className = '' }: ErrorBannerProps) {
  const { t } = useI18n();
  const [openingTicket, setOpeningTicket] = useState(false);
  const [ticketError, setTicketError] = useState('');
  const [dismissed, setDismissed] = useState(false);

  useEffect(() => {
    setDismissed(false);
    setTicketError('');
  }, [message]);

  if (!message || dismissed) return null;
  const merged = ['ui-error-banner', className].filter(Boolean).join(' ');
  return (
    <div className={merged}>
      <button
        type="button"
        className="ui-error-close-btn"
        onClick={() => setDismissed(true)}
        aria-label={t('errorBanner.closeMessage', 'Close error message')}
        title={t('actions.close', 'Close')}
      >
        ×
      </button>
      <div className="ui-error-banner-main">
        <span>{message}</span>
        <div className="ui-error-actions">
          <button
            type="button"
            className="ui-error-ticket-btn"
            disabled={openingTicket}
            onClick={() => {
              setOpeningTicket(true);
              setTicketError('');
              void openTicketDraft(message)
                .then((result) => {
                  if (!result.dev_forum_capture_created) {
                    setTicketError(t('errorBanner.devForumCaptureFailed', 'Ticket email was created, but adding to Dev-Forum failed.'));
                  }
                })
                .catch((error) => {
                  setTicketError(toUserErrorMessage(error, t('errorBanner.ticketCreateFailed', 'Could not create support ticket draft.')));
                })
                .finally(() => {
                  setOpeningTicket(false);
                });
            }}
          >
            {openingTicket ? t('errorBanner.preparing', 'Preparing...') : t('errorBanner.openTicket', 'Open Ticket')}
          </button>
        </div>
      </div>
      {ticketError && <p className="ui-error-ticket-note">{ticketError}</p>}
    </div>
  );
}
