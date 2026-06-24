"""Contract tests — fail against the starter stubs; make them pass.

All three run offline: chunking and dedupe are pure, and retrieve uses a
deterministic scorer. No network and no Anthropic key required.
"""
from kb import chunk, dedupe, retrieve
from kb.core import Chunk


def test_chunk_size_and_overlap():
    # 100 chars, size=40, overlap=10 -> stride 30 -> starts at 0, 30, 60, 90.
    text = "".join(str(i % 10) for i in range(100))
    pieces = chunk(text, size=40, overlap=10)
    assert pieces[0] == text[0:40]            # first chunk is exactly `size`
    assert pieces[1] == text[30:70]           # next starts at size - overlap
    assert pieces[1][:10] == pieces[0][-10:]  # they overlap by `overlap`
    assert "".join(dict.fromkeys("".join(pieces))) != ""  # something came back
    assert all(len(p) <= 40 for p in pieces)  # no chunk exceeds `size`


def test_dedupe_removes_near_duplicate_keeps_fresher():
    # Two near-identical refund chunks; the 2026 one is fresher and must survive.
    old = Chunk(doc_id="kb-refunds-2024", updated="2024-06-10",
                text="You may request a refund within the stated window of your charge.")
    new = Chunk(doc_id="kb-refunds-2026", updated="2026-02-20",
                text="You may request a refund within the stated window of your charge.")
    other = Chunk(doc_id="kb-sso", updated="2025-12-08",
                  text="Single sign-on is available on the Business plan via SAML.")
    kept = dedupe([old, new, other], threshold=0.9)
    kept_ids = {c.doc_id for c in kept}
    assert "kb-refunds-2026" in kept_ids        # fresher duplicate survives
    assert "kb-refunds-2024" not in kept_ids     # stale duplicate dropped
    assert "kb-sso" in kept_ids                  # the distinct chunk stays
    assert len(kept) == 2


def test_retrieve_returns_top_k_ordered_by_score():
    chunks = [
        Chunk(doc_id="a", updated="2025-01-01", text="refund policy and refund window details"),
        Chunk(doc_id="b", updated="2025-01-01", text="single sign-on setup with saml"),
        Chunk(doc_id="c", updated="2025-01-01", text="api rate limits and retry behaviour"),
    ]
    top = retrieve("how long is the refund window", chunks, k=2)
    assert len(top) == 2                         # honours k
    assert top[0].doc_id == "a"                  # most relevant first
    assert top[0].score >= top[1].score          # sorted by score descending
