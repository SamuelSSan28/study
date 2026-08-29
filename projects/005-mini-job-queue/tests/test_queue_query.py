from pathlib import Path


def test_claim_query_keeps_locking_and_ownership_guards_visible() -> None:
    source = Path("app/store.py").read_text(encoding="utf-8")
    assert "FOR UPDATE SKIP LOCKED" in source
    assert "status = 'processing' AND worker_id = %s" in source
    assert "locked_at < now()" in source
