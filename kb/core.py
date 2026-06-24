"""
RAG core: normalize -> chunk -> dedupe -> retrieve -> answer.

Keep retrieval deterministic and offline-testable (a simple lexical scorer is
fine for the contract tests; swap in real embeddings later). The answer step is
the only part that calls the network. Tests define the contract for chunk,
dedupe, and retrieve.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Doc:
    """A normalized knowledge document."""
    id: str
    title: str
    updated: str  # ISO date 'YYYY-MM-DD'
    tags: list[str]
    body: str


@dataclass
class Chunk:
    """A retrievable slice of a document."""
    doc_id: str
    text: str
    updated: str  # carried from the parent doc, for freshness tie-breaks
    score: float = 0.0
    meta: dict[str, Any] = field(default_factory=dict)


def normalize(raw: str) -> Doc:
    """Parse one raw markdown doc (front matter + body) into a Doc.

    The front matter is the block between the leading '---' fences and carries
    `id`, `title`, `updated`, and `tags`. Return a Doc with the body text
    (everything after the front matter) stripped of the leading '# Title' line.
    """
    raise NotImplementedError("Implement normalize")


def chunk(text: str, size: int, overlap: int) -> list[str]:
    """Split `text` into overlapping windows.

    TODO: return a list of substrings where
      - each chunk has length `size` (the final chunk may be shorter),
      - consecutive chunks overlap by `overlap` characters,
      - so each chunk starts `size - overlap` characters after the previous one.
    Require 0 <= overlap < size (raise ValueError otherwise). For text shorter
    than `size`, return a single chunk containing all of it.
    """
    raise NotImplementedError("Implement chunk")


def dedupe(chunks: list[Chunk], threshold: float = 0.9) -> list[Chunk]:
    """Drop near-duplicate chunks.

    TODO: compare chunks pairwise by text similarity (e.g. Jaccard over word
    sets, or difflib ratio). When two chunks are similar at or above
    `threshold`, keep only one — prefer the chunk from the FRESHER doc (larger
    `updated` date). Preserve the original order of the chunks you keep.
    """
    raise NotImplementedError("Implement dedupe")


def retrieve(query: str, chunks: list[Chunk], k: int) -> list[Chunk]:
    """Return the top-`k` chunks for `query`, highest score first.

    TODO: score each chunk against the query with a deterministic scorer
    (e.g. shared-word overlap — no network needed for the tests). Set
    `chunk.score`. Sort by score descending; **break ties by freshness**
    (newer `updated` first). Return at most `k` chunks.
    """
    raise NotImplementedError("Implement retrieve")


def answer(query: str, chunks: list[Chunk], model: str = "claude-sonnet-4-6") -> dict:
    """Answer `query` grounded ONLY in the retrieved `chunks`, with citations.

    TODO:
      - if `chunks` is empty, return {"answer": "I don't know", "sources": []}
      - otherwise call the Anthropic SDK (read the key from the ANTHROPIC_API_KEY
        environment variable — never hard-code it) with a prompt that includes
        the retrieved chunk texts and instructs the model to answer only from
        them and cite the source doc ids.
      - use a current model id (default claude-sonnet-4-6; claude-haiku-4-5-20251001
        for a cheaper pass). Never claude-3-*.
    Return {"answer": <str>, "sources": <list of cited doc ids>}.
    """
    if not chunks:
        return {"answer": "I don't know", "sources": []}
    raise NotImplementedError("Implement answer")
