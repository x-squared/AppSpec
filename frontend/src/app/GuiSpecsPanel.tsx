import GuiSpecsSurface from '../features/gui-specs/GuiSpecsSurface';
import { useI18n } from '../i18n/i18n';

declare const React: unknown;

interface GuiSpecsPanelProps {
  hasDevRole: boolean;
}

export default function GuiSpecsPanel({ hasDevRole }: GuiSpecsPanelProps) {
  const { t } = useI18n();
  return (
    <div className="dev-forum-right-panel">
      <GuiSpecsSurface title={t('guiSpecs.panel.title', 'GUI Specs Builder')} hasDevRole={hasDevRole} />
    </div>
  );
}

