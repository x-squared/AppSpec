import { useEffect, useMemo, useState } from 'react';
import GuiSpecsSurface from '../features/gui-specs/GuiSpecsSurface';
import { api } from '../api';
import { useI18n } from '../i18n/i18n';

export default function GuiSpecsView() {
  const { t } = useI18n();
  const [hasDevRole, setHasDevRole] = useState(false);

  useEffect(() => {
    let disposed = false;
    api.getMe()
      .then((me) => {
        if (disposed) return;
        const roleKeys = new Set<string>(
          [me.role?.key ?? '', ...(me.roles ?? []).map((role) => role.key)]
            .map((value) => String(value).trim().toUpperCase())
            .filter((value) => value.length > 0),
        );
        setHasDevRole(roleKeys.has('DEVELOPER'));
      })
      .catch(() => {
        if (disposed) return;
        setHasDevRole(false);
      });
    return () => {
      disposed = true;
    };
  }, []);

  const title = useMemo(() => t('guiSpecs.page.title', 'GUI Specs Builder'), [t]);
  return <GuiSpecsSurface title={title} hasDevRole={hasDevRole} />;
}

