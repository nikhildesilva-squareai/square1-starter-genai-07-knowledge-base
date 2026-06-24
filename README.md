# RAG-Powered Knowledge Base — Square 1 AI starter

**Part of [Square 1 AI](https://square1-tutor.vercel.app) · Generative AI · Project 7.**

✅ **Data included.** The dataset is committed in [`dataset/`](dataset/) and is the **same standardized dataset every learner uses** — so results are comparable. It is 100% synthetic and Square 1-owned (no third-party or personal data). You can also download it as a single file from the project page on Square 1.

To run the commands below, copy the files into `data/` (`mkdir -p data && cp -r dataset/* data/`) or point the commands straight at `dataset/`.

MIT licensed — fork it, build on it, put it in your portfolio.

---

# RAG-Powered Knowledge Base — starter

Starter for Square 1 AI **Generative AI · Project 7**. Build a RAG knowledge base: ingest docs, chunk, dedupe, retrieve with citations + freshness, answer.

## Setup
```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...                 # Windows: setx ANTHROPIC_API_KEY ...
```
The answer step reads `ANTHROPIC_API_KEY` from the environment — **never hard-code your key**.

## Get the data
Download the knowledge corpus from your project page (Resources → Dataset) into `data/corpus/` and `data/eval_queries.jsonl`.

## Your task
Three tests define the contract — they fail until you implement the stubs in `kb/core.py`:
```bash
pytest -q
python -m kb.cli data/corpus "How long do refunds take?"
```
Pipeline: `normalize` (parse front matter + body) → `chunk` (size + overlap) → `dedupe` (drop near-duplicate chunks) → `retrieve` (deterministic top-k, **freshness breaks ties**) → `answer` (Anthropic SDK, grounded + cited).

- The 3 tests run **offline** — `retrieve` uses a deterministic scorer and the LLM is mocked. Make them pass first, then wire up real embeddings (Voyage), pgvector, and the Anthropic answer call.
- Use a **current** model id: `claude-sonnet-4-6` for answers, `claude-haiku-4-5-20251001` for a cheaper pass. Never `claude-3-*`.
- Ground every answer only in retrieved chunks, cite the source `id`s, and return "I don't know" when nothing relevant is retrieved.

Full brief, rubric, and references are on your Square 1 project page. MIT licensed.
