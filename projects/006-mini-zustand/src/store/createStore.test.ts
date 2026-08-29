import { describe, expect, it, vi } from 'vitest'
import { createStore } from './createStore'

describe('createStore', () => {
  it('reads, merges, and functionally updates state', () => {
    const store = createStore({ count: 0, label: 'ready' })
    store.setState({ count: 1 })
    store.setState((state) => ({ count: state.count + 1 }))
    expect(store.getState()).toEqual({ count: 2, label: 'ready' })
  })

  it('notifies subscribers only for actual changes and supports unsubscribe', () => {
    const store = createStore({ count: 0 })
    const listener = vi.fn()
    const unsubscribe = store.subscribe(listener)
    store.setState({ count: 0 })
    store.setState({ count: 1 })
    unsubscribe()
    store.setState({ count: 2 })
    expect(listener).toHaveBeenCalledTimes(1)
  })
})
