import { useCallback, useEffect, useMemo, useState } from 'react';
import { api, type GuiSpecImplLinkUpsert, type GuiSpecViewCreate, type GuiSpecViewListItem } from '../../api';
import { useI18n } from '../../i18n/i18n';
import { toUserErrorMessage } from '../../api/error';
import GuiSpecsOverlay from './GuiSpecsOverlay';
import { useGuiSpecsViewModel, type GuiSpecsOverlayMode } from './useGuiSpecsViewModel';
import { openDevForumContextWithHighlight } from '../../views/layout/devForumHighlight';
import './GuiSpecsSurface.css';

interface GuiSpecsSurfaceProps {
  title: string;
  hasDevRole: boolean;
}

function emptyImplLink(): GuiSpecImplLinkUpsert {
  return { repo_key: '', module_path: '', file_path: '', symbol: '', commit_hash: '', note: '' };
}

export default function GuiSpecsSurface({ title, hasDevRole }: GuiSpecsSurfaceProps) {
  const { t } = useI18n();
  const vm = useGuiSpecsViewModel({ hasDevRole });
  const [newViewMode, setNewViewMode] = useState(false);
  const [newViewName, setNewViewName] = useState('');
  const [newViewDesc, setNewViewDesc] = useState('');
  const [implLinkDraft, setImplLinkDraft] = useState<GuiSpecImplLinkUpsert>(emptyImplLink());
  const [localError, setLocalError] = useState('');
  const selectedRegion = vm.selectedRegion;

  useEffect(() => {
    if (!selectedRegion || !selectedRegion.impl_link) {
      setImplLinkDraft(emptyImplLink());
      return;
    }
    setImplLinkDraft({
      repo_key: selectedRegion.impl_link.repo_key ?? '',
      module_path: selectedRegion.impl_link.module_path ?? '',
      file_path: selectedRegion.impl_link.file_path ?? '',
      symbol: selectedRegion.impl_link.symbol ?? '',
      commit_hash: selectedRegion.impl_link.commit_hash ?? '',
      note: selectedRegion.impl_link.note ?? '',
    });
  }, [selectedRegion?.id]);

  const overlayModeHint = useMemo(() => {
    if (vm.overlayMode === 'pickingExistingPart') return t('guiSpecs.overlay.pickExistingHint', 'Click a UI element to mark it.');
    if (vm.overlayMode === 'drawingNewPart') return t('guiSpecs.overlay.drawNewHint', 'Drag on the screen to draw a new region.');
    return t('guiSpecs.overlay.idleHint', 'Select a region box or start marking.');
  }, [t, vm.overlayMode]);

  const handleSelectView = useCallback(async (view: GuiSpecViewListItem) => {
    setLocalError('');
    try {
      const detailed = await api.getGuiSpecView(view.id);
      openDevForumContextWithHighlight(detailed.capture_url, detailed.capture_state_json, detailed.capture_gui_part);
    } catch (err) {
      setLocalError(toUserErrorMessage(err, 'Could not open GUI spec view context.'));
    }
    if (vm.overlayActive) vm.exitOverlay();
    vm.setActiveViewId(view.id);
  }, [vm]);

  const handleToggleOverlay = useCallback((mode: GuiSpecsOverlayMode) => vm.startOverlay(mode), [vm]);
  const handleSaveImplLink = useCallback(async () => {
    if (!selectedRegion) return;
    await vm.upsertImplLink(selectedRegion.id, implLinkDraft);
  }, [implLinkDraft, selectedRegion, vm]);

  return (
    <div className="gui-specs-surface">
      <header className="gui-specs-header"><h2>{title}</h2></header>
      {localError ? <div className="gui-specs-error">{localError}</div> : null}
      {vm.error ? <div className="gui-specs-error">{vm.error}</div> : null}
      {!hasDevRole ? <div className="gui-specs-empty">{t('guiSpecs.noDevRole', 'Dev role required.')}</div> : (
        <>
          <section className="gui-specs-section">
            <div className="gui-specs-section-row">
              <button type="button" className="gui-specs-primary-btn" disabled={vm.loading} onClick={() => { setNewViewMode((prev) => !prev); setNewViewName(''); setNewViewDesc(''); }}>
                {t('guiSpecs.actions.newView', 'New scratch view')}
              </button>
              <label className="gui-specs-toggle">
                <input type="checkbox" checked={vm.showDoneParts} onChange={() => vm.setShowDoneParts((prev) => !prev)} />
                <span>{t('guiSpecs.actions.showDone', 'Show done parts')}</span>
              </label>
            </div>
            {newViewMode ? (
              <div className="gui-specs-new-view">
                <label><div className="gui-specs-field-label">{t('guiSpecs.fields.viewName', 'Name')}</div><input className="gui-specs-input" value={newViewName} onChange={(e) => setNewViewName(e.target.value)} /></label>
                <label><div className="gui-specs-field-label">{t('guiSpecs.fields.description', 'Description')}</div><input className="gui-specs-input" value={newViewDesc} onChange={(e) => setNewViewDesc(e.target.value)} /></label>
                <div className="gui-specs-new-view-actions">
                  <button type="button" className="gui-specs-primary-btn" disabled={vm.loading} onClick={async () => { const created = await vm.createScratchView({ name: newViewName, description: newViewDesc, view_type: 'SCRATCH_VIEW' } as GuiSpecViewCreate); if (created) setNewViewMode(false); }}>{t('common.create', 'Create')}</button>
                  <button type="button" className="gui-specs-secondary-btn" onClick={() => setNewViewMode(false)}>{t('common.cancel', 'Cancel')}</button>
                </div>
              </div>
            ) : null}
          </section>
          <section className="gui-specs-section">
            <div className="gui-specs-section-title">{t('guiSpecs.views.title', 'Discussions')}</div>
            <div className="gui-specs-view-list">
              {vm.views.map((view) => (
                <button key={view.id} type="button" className={`gui-specs-view-item ${view.id === vm.activeViewId ? 'active' : ''}`} onClick={() => void handleSelectView(view)}>
                  <div className="gui-specs-view-name">{view.name}</div>
                  <div className="gui-specs-view-counts">{view.open_regions_count} open | {view.done_regions_count} done</div>
                </button>
              ))}
              {vm.views.length === 0 ? <div className="gui-specs-muted">{t('guiSpecs.views.empty', 'No GUI specs yet.')}</div> : null}
            </div>
          </section>
          <section className="gui-specs-section">
            <div className="gui-specs-section-row">
              <div className="gui-specs-hint">{overlayModeHint}</div>
              <div className="gui-specs-actions-row">
                {vm.overlayActive ? (
                  <button type="button" className="gui-specs-secondary-btn" onClick={vm.exitOverlay}>{t('common.close', 'Close')}</button>
                ) : (
                  <>
                    <button type="button" className="gui-specs-primary-btn" disabled={!vm.activeViewId} onClick={() => handleToggleOverlay('pickingExistingPart')}>{t('guiSpecs.actions.markExisting', 'Mark existing')}</button>
                    <button type="button" className="gui-specs-secondary-btn" disabled={!vm.activeViewId} onClick={() => handleToggleOverlay('drawingNewPart')}>{t('guiSpecs.actions.drawNew', 'Draw new')}</button>
                  </>
                )}
              </div>
            </div>
          </section>
          <section className="gui-specs-section">
            <div className="gui-specs-section-title">{t('guiSpecs.regions.title', 'Regions')}</div>
            <div className="gui-specs-region-list">
              {vm.regions.map((region) => (
                <button key={region.id} type="button" className={`gui-specs-region-item ${region.id === vm.selectedRegionId ? 'selected' : ''}`} onClick={() => vm.setSelectedRegionId(region.id)}>
                  <div className="gui-specs-region-item-name">{region.label || region.region_type}</div>
                  <div className="gui-specs-region-item-meta">{region.status} | z={region.z_index}</div>
                </button>
              ))}
              {vm.regions.length === 0 ? <div className="gui-specs-muted">{t('guiSpecs.regions.empty', 'No regions for this view yet.')}</div> : null}
            </div>
          </section>
          {selectedRegion ? (
            <section className="gui-specs-section">
              <div className="gui-specs-section-title">{t('guiSpecs.implLink.title', 'Implementation link')}</div>
              <div className="gui-specs-impl-form">
                <input className="gui-specs-input" value={implLinkDraft.repo_key ?? ''} onChange={(e) => setImplLinkDraft((prev) => ({ ...prev, repo_key: e.target.value }))} placeholder={t('guiSpecs.implLink.repoKey', 'Repo key')} />
                <input className="gui-specs-input" value={implLinkDraft.module_path ?? ''} onChange={(e) => setImplLinkDraft((prev) => ({ ...prev, module_path: e.target.value }))} placeholder={t('guiSpecs.implLink.modulePath', 'Module path')} />
                <input className="gui-specs-input" value={implLinkDraft.file_path ?? ''} onChange={(e) => setImplLinkDraft((prev) => ({ ...prev, file_path: e.target.value }))} placeholder={t('guiSpecs.implLink.filePath', 'File path')} />
                <input className="gui-specs-input" value={implLinkDraft.symbol ?? ''} onChange={(e) => setImplLinkDraft((prev) => ({ ...prev, symbol: e.target.value }))} placeholder={t('guiSpecs.implLink.symbol', 'Symbol')} />
                <input className="gui-specs-input" value={implLinkDraft.commit_hash ?? ''} onChange={(e) => setImplLinkDraft((prev) => ({ ...prev, commit_hash: e.target.value }))} placeholder={t('guiSpecs.implLink.commitHash', 'Commit hash (optional)')} />
                <input className="gui-specs-input" value={implLinkDraft.note ?? ''} onChange={(e) => setImplLinkDraft((prev) => ({ ...prev, note: e.target.value }))} placeholder={t('guiSpecs.implLink.note', 'Note (optional)')} />
                <button type="button" className="gui-specs-primary-btn" onClick={handleSaveImplLink}>{t('common.save', 'Save')}</button>
              </div>
            </section>
          ) : null}
        </>
      )}
      {vm.overlayActive ? (
        <GuiSpecsOverlay
          overlayActive={vm.overlayActive}
          overlayMode={vm.overlayMode}
          setOverlayMode={vm.setOverlayMode}
          regions={vm.regions}
          selectedRegionId={vm.selectedRegionId}
          setSelectedRegionId={vm.setSelectedRegionId}
          exitOverlay={vm.exitOverlay}
          createRegion={vm.createRegion}
          setRegionNote={vm.setRegionNote}
          setRegionStatus={vm.setRegionStatus}
        />
      ) : null}
    </div>
  );
}

