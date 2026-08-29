# Practice Project #6 — Build a Mini Zustand

A small React lab for tracing how external state causes the correct component to rerender.

## Problem

A JavaScript variable can change without React knowing:

```ts
let count = 0
count += 1 // React has no subscription to this change
```

This project builds the missing notification path instead of hiding it behind Zustand or Redux.

## Learning goals

- Implement a framework-independent store with `getState`, `setState`, and `subscribe`.
- Connect external state to React with `useSyncExternalStore`.
- Observe how selectors and referential equality affect rerenders.
- Distinguish component, shared client, URL, and server state.

## Architecture

```text
setState → immutable snapshot → listeners
                               ↓
React ← selected snapshot ← useSyncExternalStore
```

`src/store/createStore.ts` owns state and a `Set` of listeners. `src/store/useStore.ts` selects and caches a snapshot. Components subscribe to narrow slices so an unrelated update can retain the selected reference.

```text
src/
├── store/          # store contract, React bridge, seed state, tests
├── components/     # separate subscription boundaries + render counters
├── App.tsx
└── styles.css
```

## How to run

Requires Node.js 20 or newer.

```bash
cd projects/006-mini-zustand
npm install
npm run dev
```

Checks:

```bash
npm test
npm run lint
npm run build
```

## Main experiment

**Question:** Does a component rerender when an unrelated store slice changes?

1. Start the app and open React DevTools Profiler.
2. Record while selecting an issue. Search and Filter should not commit.
3. In `SearchBox.tsx`, temporarily select the entire state and then read `state.search`.
4. Record another issue selection. Search should now commit because the root snapshot changed.
5. Restore the narrow selector and repeat to validate the boundary.

Development `StrictMode` may render twice. Use Profiler commits as evidence; the visible counters are only a learning aid. Record actual results in `STUDY.md`.

## Tests

- Store tests verify merging, functional updates, no-op updates, notification, and unsubscribe.
- Hook tests verify that an unrelated slice does not cause a subscribed component to rerender.
- Manually validate filtering, empty results, keyboard focus, mobile layout, and Profiler commits.

## Optional extensions

- Add a shallow equality helper and measure object-selector commits.
- Add action metadata and a previous/next-state panel.
- Persist only filter state, then document hydration timing.
- Compare remotely fetched issues with TanStack Query and explain ownership.

## Completion check

Explain the complete path: `setState` creates a snapshot, listeners notify React, `useSyncExternalStore` reads again, the selector derives a slice, equality determines whether its identity changed, and React schedules the necessary render.

See [`STUDY.md`](./STUDY.md) for experiment notes and [`DECISIONS.md`](./DECISIONS.md) for trade-offs. Primary references: React's [`useSyncExternalStore`](https://react.dev/reference/react/useSyncExternalStore) documentation and the [Zustand documentation](https://zustand.docs.pmnd.rs/).
