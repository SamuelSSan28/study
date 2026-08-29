# 005 — Mini Job Queue

## Problem

An HTTP request should not wait while a report is generated. This project persists a job, returns `202 Accepted`, and lets independent workers claim it from PostgreSQL. It deliberately implements the queue mechanics rather than hiding them behind Celery or a broker.

## Learning goals

- make job lifecycle and transactional ownership explicit;
- understand why `FOR UPDATE SKIP LOCKED` permits concurrent consumers;
- recover work after a worker dies while holding a time-limited lease;
- observe at-least-once delivery, retries, backoff, and jitter;
- distinguish moving work from eliminating work.

## Architecture

```text
POST /reports ──insert──> PostgreSQL jobs <──claim── workers
GET /jobs/{id} <──read──────────┘             │
                         complete/retry <─────┘
```

`claim` selects one eligible row and updates its owner in the same transaction. A row lock prevents two transactions from selecting the same job; `SKIP LOCKED` makes losing workers continue to other rows rather than block. Attempts are incremented when work is claimed. Completion and failure updates include `worker_id`, so a stale worker cannot overwrite a job reclaimed after its lease expired.

Lifecycle: `queued → processing → completed`, or `processing → queued` on a retry, eventually `processing → failed` after four claims. Retried work uses full jitter over exponential caps of 5, 10, and 20 seconds.

## How to run

From this directory:

```bash
docker compose up --build --scale worker=3
curl -i -X POST localhost:8000/reports \
  -H 'content-type: application/json' \
  -d '{"title":"Quarterly sales"}'
curl localhost:8000/jobs/JOB_ID
```

Set `fail_until_attempt` to exercise retries: `{"title":"Retry me","fail_until_attempt":2}`.

## Main experiment: kill a worker

**Question:** Who owns a processing job after its worker dies?

**Setup:** Start exactly one worker. Defaults make processing take 10 seconds and the lease last 15 seconds.

```bash
docker compose up --build -d postgres api
docker compose up -d worker
curl -s -X POST localhost:8000/reports -H 'content-type: application/json' \
  -d '{"title":"Crash recovery"}'
docker compose logs -f worker
# After "processing" appears, within ten seconds:
docker compose kill worker
docker compose run -d --name replacement-worker worker
docker compose logs -f replacement-worker
```

**Expected result (hypothesis):** no live process owns the job immediately after the kill, but the database still records the dead worker's lease. The replacement initially finds nothing. Once `locked_at` is more than 15 seconds old, it reclaims the row, increments `attempts` to 2, and completes it. Polling `GET /jobs/{id}` exposes the transition.

**Cleanup:** `docker compose down -v --remove-orphans`.

## Tests

```bash
python -m venv .venv
.venv/bin/pip install -e '.[test]'
.venv/bin/pytest
```

The API tests use an in-memory boundary fake. The query contract test keeps the concurrency-critical SQL visible; the manual Docker experiment exercises PostgreSQL process and locking behavior.

## Reliability boundary and backpressure

This queue offers **at-least-once execution**, not exactly-once business effects. A worker can create an external effect and die before recording completion; the lease then causes a duplicate execution. Real handlers need an idempotency key or an atomic transaction with the affected database where possible.

Asynchronous processing shortens request latency and isolates transient worker failures, but adds queue delay, duplicate work, operational state, and eventual consistency. If producers sustain 1,000 jobs/s and workers finish 300 jobs/s, depth grows about 700 jobs/s. Scaling consumers is useful only until database or downstream capacity saturates; admission limits, producer rate limits, priorities, or rejecting work are then honest forms of backpressure.

## Optional extensions

- dead-letter replay endpoint;
- priorities and scheduled jobs (the schema already uses `available_at`);
- queue-depth, age, retry, and duration metrics;
- a measured 10,000-job load experiment before choosing a specialized broker.
