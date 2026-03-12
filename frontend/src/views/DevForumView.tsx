import DevForumSurface from '../features/dev-forum/DevForumSurface';
import { useI18n } from '../i18n/i18n';
import { api } from '../api';
import { useEffect, useState } from 'react';

function userHasDevRole(role: { key: string; type: string } | null | undefined, roles: Array<{ key: string; type: string }> | undefined): boolean {
  if (role && role.type === 'ROLE' && role.key === 'DEV') return true;
  return (roles ?? []).some((entry) => entry.type === 'ROLE' && entry.key === 'DEV');
}

export default function DevForumView() {
  const { t } = useI18n();
  const [hasDevRole, setHasDevRole] = useState(false);

  useEffect(() => {
    let disposed = false;
    api.getMe()
      .then((current) => {
        if (disposed) return;
        setHasDevRole(userHasDevRole(current.role, current.roles));
      })
      .catch(() => {
        if (disposed) return;
        setHasDevRole(false);
      });
    return () => {
      disposed = true;
    };
  }, []);

  return (
    <>
      <header className="patients-header">
        <h1>{t('navigation.dev.devForum', 'Dev-Forum')}</h1>
      </header>
      <DevForumSurface
        title={t('devForum.view.title', 'Dev-Forum')}
        includeCapturing={false}
        includeClaimedByOtherDevelopers
        enableDeveloperFilter
        hasDevRole={hasDevRole}
      />
    </>
  );
}
