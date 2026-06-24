"""CLI:  python -m kb.cli data/corpus "How long do refunds take?"

Wires the kb/ pipeline end to end: load + normalize the corpus, chunk, dedupe,
retrieve the top-k for the query, then answer with citations.
"""
import argparse
import glob
import os

from .core import normalize, chunk, dedupe, retrieve, answer, Chunk


def load_corpus(corpus_dir: str) -> list[Chunk]:
    chunks: list[Chunk] = []
    for path in sorted(glob.glob(os.path.join(corpus_dir, "*.md"))):
        with open(path, encoding="utf-8") as f:
            doc = normalize(f.read())
        for piece in chunk(doc.body, size=400, overlap=80):
            chunks.append(Chunk(doc_id=doc.id, text=piece, updated=doc.updated))
    return chunks


def main() -> None:
    ap = argparse.ArgumentParser(description="Ask a question against the knowledge base.")
    ap.add_argument("corpus_dir", help="Folder of .md knowledge docs")
    ap.add_argument("query", help="The question to answer")
    ap.add_argument("-k", type=int, default=4, help="How many chunks to retrieve")
    args = ap.parse_args()

    chunks = dedupe(load_corpus(args.corpus_dir))
    top = retrieve(args.query, chunks, k=args.k)
    result = answer(args.query, top)

    print("Answer:\n", result["answer"])
    print("\nSources:", ", ".join(result["sources"]) or "(none)")


if __name__ == "__main__":
    main()
