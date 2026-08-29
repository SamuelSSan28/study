# Architectural decisions

## PostgreSQL is both durable store and queue

- **Decision:** Claim jobs directly from a PostgreSQL table.
- **Context:** The lesson is transactional claiming, leases, and retries rather than broker APIs.
- **Why:** It makes state and locking observable and avoids a second service.
- **Trade-offs:** Polling adds latency and database load; PostgreSQL lacks broker-native routing and streaming retention.
- **When to reconsider:** Measured claim contention, throughput, retention, or routing requirements exceed the database's acceptable budget.

## Short ownership transaction with a lease

- **Decision:** Commit immediately after assigning `worker_id`; do not hold a transaction while generating a report.
- **Context:** Work is deliberately slow and workers may be killed.
- **Why:** Other consumers can progress without long transactions, while expired `locked_at` values permit recovery.
- **Trade-offs:** Expiry can duplicate work. A task longer than its lease needs renewal, and clocks are evaluated by PostgreSQL to avoid worker-clock disagreement.
- **When to reconsider:** Add heartbeats when legitimate processing can approach the lease duration.

## At-least-once processing with guarded completion

- **Decision:** Treat handlers as potentially duplicated and accept completion only from the recorded owner.
- **Context:** A worker can finish an external action and crash before marking the row complete.
- **Why:** No queue claim can make unrelated business effects exactly once.
- **Trade-offs:** Handlers must supply idempotency; owner checks prevent stale state writes but not duplicate external effects.
- **When to reconsider:** Use an atomic business transaction or outbox/inbox design when the effect shares a transactional database.

## Full-jitter exponential retry

- **Decision:** Retry under random delays capped at 5, 10, then 20 seconds; fail on attempt four.
- **Context:** Immediate simultaneous retries can amplify an outage.
- **Why:** Exponential caps reduce pressure and jitter prevents a synchronized retry wave.
- **Trade-offs:** Recovery latency is nondeterministic and the short caps are demonstration values.
- **When to reconsider:** Tune from service recovery objectives and downstream rate limits.
