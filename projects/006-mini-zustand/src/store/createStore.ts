export type Listener = () => void
export type StateUpdate<State> = Partial<State> | ((state: State) => Partial<State>)

export interface Store<State> {
  getState: () => State
  setState: (update: StateUpdate<State>) => void
  subscribe: (listener: Listener) => () => void
}

export function createStore<State extends object>(initialState: State): Store<State> {
  let state = initialState
  const listeners = new Set<Listener>()

  const getState = () => state

  const setState = (update: StateUpdate<State>) => {
    const patch = typeof update === 'function' ? update(state) : update
    const nextState = { ...state, ...patch }

    if (Object.is(nextState, state) || Object.keys(patch).every((key) =>
      Object.is(state[key as keyof State], nextState[key as keyof State]),
    )) return

    state = nextState
    listeners.forEach((listener) => listener())
  }

  const subscribe = (listener: Listener) => {
    listeners.add(listener)
    return () => listeners.delete(listener)
  }

  return { getState, setState, subscribe }
}
