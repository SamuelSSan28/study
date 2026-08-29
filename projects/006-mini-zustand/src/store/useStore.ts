import { useCallback, useRef, useSyncExternalStore } from 'react'
import type { Store } from './createStore'

export function useStore<State, Selection>(
  store: Store<State>,
  selector: (state: State) => Selection,
  equalityFn: (left: Selection, right: Selection) => boolean = Object.is,
): Selection {
  const cache = useRef<{
    state: State
    selection: Selection
    selector: (state: State) => Selection
    equalityFn: (left: Selection, right: Selection) => boolean
  } | null>(null)

  const getSnapshot = useCallback(() => {
    const state = store.getState()
    const previous = cache.current

    const sameSelector = previous?.selector === selector && previous.equalityFn === equalityFn
    if (previous && sameSelector && Object.is(previous.state, state)) return previous.selection

    const selection = selector(state)
    if (previous && sameSelector && equalityFn(previous.selection, selection)) {
      cache.current = { state, selection: previous.selection, selector, equalityFn }
      return previous.selection
    }

    cache.current = { state, selection, selector, equalityFn }
    return selection
  }, [store, selector, equalityFn])

  return useSyncExternalStore(store.subscribe, getSnapshot, getSnapshot)
}
