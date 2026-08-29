# Architectural Decisions

## Use Vite instead of Next.js

**Decision:** Build a client-only React application with Vite.

**Context:** The lesson concerns hooks, subscriptions, snapshots, and browser rendering. It has no routing, SSR, RSC, SEO, or backend requirement.

**Why:** Vite provides the smallest environment needed to observe the React behavior without introducing unrelated server/client boundaries.

**Trade-offs:** The project does not demonstrate SSR hydration or `getServerSnapshot` with real server output.

**When to reconsider:** Add an SSR-specific experiment about external-store hydration.

## Implement the store instead of installing Zustand

**Decision:** Keep the store and React bridge in project source.

**Context:** A ready-made store would hide the listener set, snapshot caching, and selector comparison that the project exists to study.

**Why:** The notification-to-render path stays short enough to trace line by line.

**Trade-offs:** This implementation omits production features such as middleware composition, devtools integration, persistence, and established edge-case coverage.

**When to reconsider:** After completing the experiment, use Zustand only as a comparison target or add one feature at a time for a stated lesson.

## Shallow-merge partial updates

**Decision:** `setState` accepts a partial object or updater and shallow-merges it into a new root state.

**Context:** The dashboard updates independent top-level slices and needs stable references for unchanged slices.

**Why:** It makes immutable root snapshots and selector identity easy to observe.

**Trade-offs:** Nested updates must be copied explicitly, and shallow merging is not suitable for every state model.

**When to reconsider:** Introduce replace semantics or a reducer when studying transactions across fields or nested update ergonomics.

## Cache selected snapshots with optional equality

**Decision:** `useStore` returns the previous selected reference when its equality function considers the next selection equal.

**Context:** `useSyncExternalStore` expects cached snapshots, while selectors can create values whose identities differ from the root store snapshot.

**Why:** It allows narrow subscriptions and a direct experiment with referential versus shallow equality.

**Trade-offs:** The hook is more complex than a primitive-only version, equality functions add runtime work, and incorrect equality can hide real changes.

**When to reconsider:** If production correctness or concurrency coverage becomes the objective, compare with the maintained `use-sync-external-store/with-selector` implementation.
