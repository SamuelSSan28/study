# Study Notes

## Initial hypothesis

An external store update notifies every subscribed listener, but a component should only rerender when the snapshot returned by its selector changes according to the equality function.

## What the implementation exposed

### A mutable global is not enough

Changing a value outside React does not schedule work. `createStore` adds the missing contract: it replaces the state snapshot and calls subscribed listeners. `useSyncExternalStore` lets React subscribe and re-read that snapshot.

### Notifications and renders are different

`setState` notifies all store listeners after an actual change. Each `useStore` call then evaluates its selected snapshot. If the selected value is equal, the hook returns the cached reference. A notification therefore does not necessarily imply a component render.

### Immutable updates make identity useful

The store shallow-merges each patch into a new root object. Unchanged nested references survive the merge, so selectors returning those references remain stable. Mutating a nested value in place would break this reasoning and can leave React with an unchanged snapshot.

### Object selectors need deliberate equality

A selector such as `state => ({ search: state.search })` allocates a new object. With `Object.is`, that result differs by reference. `useStore` accepts an equality function so this can be investigated, but primitive or stable-reference selectors remain the clearest default.

## Automated experiment

**Question:** Will changing `selectedId` rerender a component that selects only `search`?

**Procedure:** `src/store/useStore.test.tsx` renders a Search component, updates `selectedId`, checks its render count, then updates `search`.

**Expected result:** the unrelated update keeps the render count at one; the search update increments it and changes the DOM.

**Observed result:** not yet verified in this environment because package installation was blocked by the configured registry. Run `npm test` and replace this note with the result and environment details.

## Profiler experiment

**Procedure:** follow the Main experiment in `README.md` and compare a whole-state selector with a narrow search selector.

**Expected result:** issue selection commits Search with the whole-state selector, but not with the narrow selector.

**Observed result:** pending. Record React version, development/production mode, commit count, and screenshots or notes after running the Profiler.

## State ownership conclusion

- Input drafts local to one component belong in `useState`.
- Coordinated modal, cart, or notification state can belong in a client store.
- Shareable filters often belong in the URL.
- API response lifecycles belong in a server-state cache such as TanStack Query.
- Authentication/session is commonly server-owned even when a client reads it.

The decisive question is not “Where can this state fit?” but “Who owns its lifecycle?”

## Remaining questions

- How does React's concurrent rendering contract change server snapshot requirements?
- When does a shallow equality function cost more than the avoided render?
- How do real Zustand selectors behave when selector identity changes between renders?
