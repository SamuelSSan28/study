# Engineering Principles

## General

- Start with the simplest system that exposes the problem.
- Let architecture evolve in response to an observed constraint.
- Measure before optimizing; state the metric and baseline.
- Prefer explicit state, ownership, contracts, and failure behavior.
- Avoid premature abstractions and speculative infrastructure.
- Design for partial failure when a system crosses process or network boundaries.

## Frontend

- Identify whether state belongs to a component, shared client state, the URL, or a server cache.
- Trace rendering from the state change through its subscription boundary.
- Treat referential equality and immutable updates as observable behavior, not trivia.
- Separate server-state lifecycles from client-state coordination.

## Backend

- Make transaction boundaries and invariants explicit.
- Test concurrency and failure handling, not only successful requests.
- Keep transport delivery guarantees separate from business guarantees.
- Prefer enforceable constraints over check-then-act assumptions.

## Distributed systems

- Assume messages can be delayed, duplicated, reordered, or lost according to the transport contract.
- Decide how retries, idempotency, ordering, backpressure, and recovery work.
- Do not claim exactly-once business behavior solely from a delivery setting.

## Databases

- Model invariants in the database when it is the authority capable of enforcing them.
- Inspect query plans and measurements before adding indexes.
- Include contention, isolation, and migration costs in design decisions.
