CREATE TABLE IF NOT EXISTS jobs (
    id text PRIMARY KEY,
    type text NOT NULL,
    payload jsonb NOT NULL,
    status text NOT NULL CHECK (status IN ('queued', 'processing', 'completed', 'failed')),
    attempts integer NOT NULL DEFAULT 0 CHECK (attempts >= 0),
    available_at timestamptz NOT NULL DEFAULT now(),
    locked_at timestamptz,
    worker_id text,
    result jsonb,
    error text,
    created_at timestamptz NOT NULL DEFAULT now(),
    completed_at timestamptz,
    CHECK ((status = 'processing') = (locked_at IS NOT NULL AND worker_id IS NOT NULL))
);

CREATE INDEX IF NOT EXISTS jobs_claim_idx
    ON jobs (available_at, created_at)
    WHERE status IN ('queued', 'processing');
