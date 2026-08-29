import { act, render, screen } from '@testing-library/react'
import { useCallback } from 'react'
import { describe, expect, it, vi } from 'vitest'
import { createStore } from './createStore'
import { useStore } from './useStore'

describe('useStore', () => {
  it('rerenders only when the selected slice changes', () => {
    const store = createStore({ search: '', selectedId: null as number | null })
    const renders = vi.fn()
    function Search() {
      renders()
      const search = useStore(store, useCallback((state) => state.search, []))
      return <span>{search || 'empty'}</span>
    }

    render(<Search />)
    act(() => store.setState({ selectedId: 3 }))
    expect(renders).toHaveBeenCalledTimes(1)
    act(() => store.setState({ search: 'cache' }))
    expect(screen.getByText('cache')).toBeInTheDocument()
    expect(renders).toHaveBeenCalledTimes(2)
  })
})
