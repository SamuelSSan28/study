import { useCallback } from 'react'
import { issueStore, type IssueState } from '../store/issueStore'
import { useStore } from '../store/useStore'
import { RenderBadge } from './RenderBadge'

export function StatusFilter() {
  const status = useStore(issueStore, useCallback((state) => state.statusFilter, []))

  return (
    <section className="control-card">
      <div className="label-row"><span>Filter by status</span><RenderBadge /></div>
      <div className="segmented" aria-label="Filter by status">
        {(['all', 'open', 'done'] as IssueState['statusFilter'][]).map((option) => (
          <button
            className={status === option ? 'active' : ''}
            key={option}
            onClick={() => issueStore.setState({ statusFilter: option })}
          >{option}</button>
        ))}
      </div>
    </section>
  )
}
