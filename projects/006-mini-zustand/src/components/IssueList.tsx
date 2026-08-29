import { useCallback, useMemo } from 'react'
import { issueStore } from '../store/issueStore'
import { useStore } from '../store/useStore'
import { RenderBadge } from './RenderBadge'

export function IssueList() {
  const issues = useStore(issueStore, useCallback((state) => state.issues, []))
  const search = useStore(issueStore, useCallback((state) => state.search, []))
  const status = useStore(issueStore, useCallback((state) => state.statusFilter, []))
  const selectedId = useStore(issueStore, useCallback((state) => state.selectedIssueId, []))

  const visibleIssues = useMemo(() => issues.filter((issue) => {
    const matchesSearch = issue.title.toLowerCase().includes(search.toLowerCase())
    return matchesSearch && (status === 'all' || issue.status === status)
  }), [issues, search, status])

  return (
    <section className="issues" aria-labelledby="issues-title">
      <div className="section-heading">
        <div><p className="eyebrow">Live result</p><h2 id="issues-title">Issues <span>{visibleIssues.length}</span></h2></div>
        <RenderBadge />
      </div>
      <div className="issue-list">
        {visibleIssues.map((issue) => (
          <button
            className={`issue-row ${selectedId === issue.id ? 'selected' : ''}`}
            key={issue.id}
            onClick={() => issueStore.setState({ selectedIssueId: issue.id })}
          >
            <span className="issue-number">#{issue.id}</span>
            <span className="issue-copy"><strong>{issue.title}</strong><small>{issue.description}</small></span>
            <span className={`status ${issue.status}`}>{issue.status}</span>
          </button>
        ))}
        {visibleIssues.length === 0 && <p className="empty">No issues match these filters.</p>}
      </div>
    </section>
  )
}
