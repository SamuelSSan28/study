# Study notes

## Hypothesis

A transaction using a row lock plus `SKIP LOCKED` will assign each claim to one worker without serializing all consumers. A lease will recover a job whose process disappears, at the cost of possible duplicate execution.

## Implemented evidence

- The claim query selects and updates ownership in one transaction.
- Completion and retry compare the current owner, preventing a stale worker from committing after reassignment.
- An expired lease on the final attempt moves to `failed` instead of remaining stranded in `processing`.
- API tests verify the asynchronous `202` contract independently of PostgreSQL.
- Report generation can fail through a requested attempt, making retry behavior reproducible rather than random.

## Crash experiment

The procedure is in `README.md`. It has **not been executed in this repository environment**, so its result remains a hypothesis: after killing the worker, the job remains `processing` under a dead identity until its 15-second lease expires. A replacement can then claim it as attempt 2.

The period with no live owner is intentional. Immediately resetting work on a lost client connection would confuse network uncertainty with process death. The timestamp gives other workers an objective recovery rule, although it requires the lease to exceed normal processing time (or later, lease renewal).

## Explanation

`FOR UPDATE` holds a lock until the short claim transaction commits. Without `SKIP LOCKED`, concurrent workers wait behind the same oldest row; with it, each searches for another eligible row. The lock protects assignment, not the entire report operation. Keeping that transaction open during a 10-second task would consume a connection and retain locks.

The lease closes the crash-recovery gap but changes the guarantee to at least once. A slow worker can outlive its lease. The owner predicate blocks its late database update, but cannot undo an external side effect it already performed.

## Remaining questions

- At what processing-time variance does fixed lease duration require heartbeats?
- How does claim throughput change with queue depth and many expired rows?
- Where should admission control begin for each downstream capacity limit?
