import { useCallback } from 'react'
import { issueStore } from '../store/issueStore'
import { useStore } from '../store/useStore'
import { RenderBadge } from './RenderBadge'

export function SearchBox() {
  const search = useStore(issueStore, useCallback((state) => state.search, []))

  return (
    <section className="control-card">
      <div className="label-row"><label htmlFor="search">Search issues</label><RenderBadge /></div>
      <input
        id="search"
        type="search"
        placeholder="Try “authentication”"
        value={search}
        onChange={(event) => issueStore.setState({ search: event.target.value })}
      />
    </section>
  )
}
