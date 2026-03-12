import DevForumSurface from '../features/dev-forum/DevForumSurface';
import { useI18n } from '../i18n/i18n';

interface DevForumPanelProps {
  hasDevRole: boolean;
}

export default function DevForumPanel({ hasDevRole }: DevForumPanelProps) {
  const { t } = useI18n();

  return (
    <div className="dev-forum-right-panel">
      <DevForumSurface
        title={t('devForum.panel.title', 'Dev-Forum')}
        includeCapturing
        includeClaimedByOtherDevelopers={false}
        enableDeveloperFilter={false}
        hasDevRole={hasDevRole}
        compact
      />
    </div>
  );
}
