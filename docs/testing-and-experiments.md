# Testing and Experiments

Every project needs at least one reproducible experiment that exposes the behavior being studied. Automated tests protect contracts; experiments build understanding. They are related but not interchangeable.

## Experiment template

Document:

1. **Question** — the behavior or failure being investigated.
2. **Setup** — versions, data, configuration, and tools.
3. **Procedure** — exact commands or interactions.
4. **Expected result** — the falsifiable hypothesis.
5. **Observed result** — evidence collected when the experiment is run.
6. **Explanation** — the path through the implementation that produced it.

## Useful failure dimensions

Do not test only the happy path. When relevant, introduce:

- concurrent operations;
- process crashes or interrupted work;
- latency and unavailable dependencies;
- duplicate or out-of-order operations;
- overload and backpressure;
- unstable identities or unnecessary renders.

## Examples

| Topic | Experiment |
| --- | --- |
| Idempotency | Send the same event 100 times concurrently. |
| Job queue | Stop a worker while a job is being processed. |
| Redis | Add 100 ms latency and observe timeouts. |
| React state | Change an unrelated slice and inspect commits in React Profiler. |
| Database | Compare `EXPLAIN ANALYZE` before and after an index. |
| Messaging | Deliver duplicate and out-of-order messages intentionally. |

## Test placement

- Test pure domain or store contracts without a UI framework.
- Test integration boundaries where notifications, serialization, or rendering occurs.
- Use end-to-end tests only for behavior that smaller tests cannot prove.
- Prefer deterministic assertions; use profilers and benchmarks to investigate performance rather than as brittle pass/fail gates.
