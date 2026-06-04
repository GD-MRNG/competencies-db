# Retrieval Agent (sidecar)

A tiny Gradio chat app for talking to the competencies-db retrieval router. It loads the compressed index, keeps it in the system prompt, and points your questions to the right domain / topic / entry. It routes — it does not teach the content; the full Level 1 documents do that.

This is a sidecar, not the main repo. Keep it self-contained in `/agent`.

## Setup

1. Install [uv](https://docs.astral.sh/uv/).
2. `cp .env.example .env`, then set `PROVIDER` and, for Poe, `POE_API_KEY`.
3. Put your compressed maps in `index/index.txt` — the combined output of running the compression prompt across all your Level 0 maps. (A short sample ships there so the app boots; replace it.)

## Run

```
uv run app.py
```

or `./start.sh`. A local chat UI opens in your browser.

## Switching backend

Edit `PROVIDER` in `.env`:

- `poe` — hosted models via Poe (needs `POE_API_KEY`); default `gemini-3-flash`
- `ollama` — local models (run `ollama serve` first); default `qwen2.5:14b`
- `mock` — no LLM; echoes the question, for wiring/smoke tests

Both Poe and Ollama are reached through the OpenAI-compatible chat API, so there's a single code path.

## Files

```
agent/
  app.py            # config + LLM client + Gradio chat
  system_prompt.md  # router instructions; {retrieval_index} is filled in at startup
  index/index.txt   # the compressed maps (your data)
  pyproject.toml    # uv project (Python 3.13)
  .env.example      # copy to .env
  start.sh
```

To change routing behaviour, edit `system_prompt.md` — no code change needed.
