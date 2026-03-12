import { useI18n } from '../../../i18n/i18n';
import RichTextEditor from '../../../views/layout/RichTextEditor';
import type { CapturedContextPayload, SelectedComponentDescriptor } from '../types';

interface CapturingTabProps {
  saving: boolean;
  captureDraft: string;
  capturedContext: CapturedContextPayload | null;
  selectedComponent: SelectedComponentDescriptor | null;
  pickingComponent: boolean;
  onCaptureContext: () => void;
  onStartPicking: () => void;
  onCaptureDraftChange: (next: string) => void;
  onSubmitCapture: () => Promise<void>;
  onCancelCapture: () => void;
}

export default function CapturingTab({
  saving,
  captureDraft,
  capturedContext,
  selectedComponent,
  pickingComponent,
  onCaptureContext,
  onStartPicking,
  onCaptureDraftChange,
  onSubmitCapture,
  onCancelCapture,
}: CapturingTabProps) {
  const { t } = useI18n();

  return (
    <div className="ui-panel-section dev-forum-panel">
      <div className="dev-forum-capture-actions">
        {!capturedContext ? (
          <button type="button" className="patients-add-btn" onClick={onCaptureContext} disabled={saving}>
            {t('devForum.capture.captureContext', 'Open ticket')}
          </button>
        ) : null}
        {capturedContext ? (
          <button
            type="button"
            className="patients-add-btn"
            onClick={onStartPicking}
            disabled={saving || pickingComponent}
          >
            {t('devForum.capture.pickComponent', 'Pick component')}
          </button>
        ) : null}
      </div>
      {pickingComponent ? (
        <p className="dev-forum-meta">{t('devForum.capture.pickHint', 'Move mouse over the app and press Enter to store the highlighted component. Esc cancels.')}</p>
      ) : null}
      {selectedComponent ? (
        <p className="dev-forum-meta">
          {t('devForum.capture.pickedComponent', 'Selected component')}: {selectedComponent.selector}
        </p>
      ) : null}
      {capturedContext ? (
        <>
          <p className="dev-forum-meta">
            {t('devForum.capture.capturedMeta', 'Captured context')}: {capturedContext.capture_gui_part} - {capturedContext.capture_url}
          </p>
          <RichTextEditor
            value={captureDraft}
            onChange={onCaptureDraftChange}
            ariaLabel={t('devForum.capture.requestEditorAria', 'Request editor')}
            boldTitle={t('devForum.editor.bold', 'Bold')}
            italicTitle={t('devForum.editor.italic', 'Italic')}
            underlineTitle={t('devForum.editor.underline', 'Underline')}
          />
          <div className="dev-forum-actions-row">
            <button type="button" className="patients-save-btn" onClick={() => void onSubmitCapture()} disabled={saving || !captureDraft.trim()}>
              {t('devForum.capture.submit', 'Send request')}
            </button>
            <button type="button" className="patients-cancel-btn" onClick={onCancelCapture} disabled={saving}>
              {t('devForum.capture.cancel', 'Cancel')}
            </button>
          </div>
        </>
      ) : (
        <p className="dev-forum-meta">{t('devForum.capture.hint', 'Capture context first, then write your request.')}</p>
      )}
    </div>
  );
}
