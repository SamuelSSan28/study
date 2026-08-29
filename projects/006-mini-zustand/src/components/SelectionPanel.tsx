import { useCallback } from 'react'
import { issueStore } from '../store/issueStore'
import { useStore } from '../store/useStore'
import { RenderBadge } from './RenderBadge'

export function SelectionPanel() {
  const selectedId = useStore(issueStore, useCallback((state) => state.selectedIssueId, []))

  return (
    <aside className="selection-panel">
      <div><p className="eyebrow">Selected slice</p><strong>{selectedId ? `Issue #${selectedId}` : 'Nothing selected'}</strong></div>
      <RenderBadge />
    </aside>
  )
}
