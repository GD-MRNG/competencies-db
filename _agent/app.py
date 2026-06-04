"""
Competencies-DB retrieval agent (sidecar).

Loads the compressed retrieval index from index/index.txt, holds it in the
system prompt, and lets a person chat with a router that points them to the
right domain / topic / entry in the knowledge base. It routes; it does not
teach the content.

Run:      uv run app.py
Provider: set PROVIDER in .env to poe | ollama | mock
"""

from __future__ import annotations

import logging
import os
import re
import time
from abc import ABC, abstractmethod
from pathlib import Path

import gradio as gr
import openai
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")
logger = logging.getLogger("agent")

load_dotenv()

HERE = Path(__file__).parent
INDEX_FILE = HERE / "index" / "index.txt"
SYSTEM_PROMPT_FILE = HERE / "system_prompt.md"

# --- Config (edit .env to change) ---------------------------------------
PROVIDER = os.getenv("PROVIDER", "poe").lower()
TEMPERATURE = float(os.getenv("TEMPERATURE", "0"))
MAX_ATTEMPTS = int(os.getenv("MAX_ATTEMPTS", "3"))  # env key kept for backwards compat; default raised to 3 (1 original + 2 retries)
BASE_DELAY = float(os.getenv("RETRY_DELAY", "2"))

# Both Poe and Ollama speak the OpenAI chat API, so one code path serves both.
PROVIDERS = {
    "poe": {
        "base_url": "https://api.poe.com/v1",
        "api_key": os.getenv("POE_API_KEY", ""),
        "model": os.getenv("POE_MODEL", "gemini-3-flash"),
    },
    "ollama": {
        "base_url": os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1"),
        "api_key": "ollama",  # Ollama ignores it, but the SDK requires a value
        "model": os.getenv("OLLAMA_MODEL", "qwen2.5:14b"),
    },
}

# Strip reasoning scaffolding some local models emit.
_BLOCK_PATTERNS = [r"<think>.*?</think>", r"<thought>.*?</thought>"]


def _clean(text: str) -> str:
    text = text or ""
    for pattern in _BLOCK_PATTERNS:
        text = re.sub(pattern, "", text, flags=re.DOTALL | re.IGNORECASE)
    return text.strip()


# --- Prompt assembly ----------------------------------------------------
def build_system_prompt() -> str:
    if not INDEX_FILE.exists() or not INDEX_FILE.read_text(encoding="utf-8").strip():
        raise SystemExit(
            f"\nNo index found at {INDEX_FILE}\n"
            "Compress your level-0 maps, save the combined result there, "
            "then start the agent again.\n"
        )
    index_text = INDEX_FILE.read_text(encoding="utf-8")
    template = SYSTEM_PROMPT_FILE.read_text(encoding="utf-8")
    return template.replace("{retrieval_index}", index_text)


# --- LLM client ---------------------------------------------------------
class BaseLLMClient(ABC):
    @abstractmethod
    def chat(self, messages: list[dict]) -> str: ...


class MockLLMClient(BaseLLMClient):
    """No network. Echoes the question — for wiring/smoke tests."""

    def chat(self, messages: list[dict]) -> str:
        question = messages[-1]["content"]
        return f"[mock] would route this against the index:\n\n> {question}"


class ProductionLLMClient(BaseLLMClient):
    def __init__(self, provider: str):
        if provider not in PROVIDERS:
            raise ValueError(f"Unknown provider: {provider!r} (use poe, ollama, or mock)")
        cfg = PROVIDERS[provider]
        self.model = cfg["model"]
        if provider == "poe" and not cfg["api_key"]:
            logger.warning("POE_API_KEY is not set — Poe calls will fail.")
        self.client = openai.OpenAI(api_key=cfg["api_key"] or "none", base_url=cfg["base_url"])

    def chat(self, messages: list[dict]) -> str:
        last_exc = None
        for attempt in range(1, MAX_ATTEMPTS + 1):
            try:
                resp = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=TEMPERATURE,
                )
                return _clean(resp.choices[0].message.content)
            except Exception as e:  # noqa: BLE001 - surface any provider error, then retry
                last_exc = e
                logger.warning(f"Attempt {attempt}/{MAX_ATTEMPTS} failed: {e}")
                if attempt < MAX_ATTEMPTS:
                    time.sleep(BASE_DELAY * (2 ** (attempt - 1)))
        raise last_exc


def get_client() -> BaseLLMClient:
    if PROVIDER == "mock":
        return MockLLMClient()
    return ProductionLLMClient(PROVIDER)


# --- Chat ---------------------------------------------------------------
SYSTEM_PROMPT = build_system_prompt()
client = get_client()


def respond(message: str, history: list[dict]) -> str:
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for turn in history:  # history is already in {"role","content"} form
        messages.append({"role": turn["role"], "content": turn["content"]})
    messages.append({"role": "user", "content": message})
    return client.chat(messages)


demo = gr.ChatInterface(
    fn=respond,
    title="Competencies Retrieval Agent",
    description="Ask a messy question. I'll point you to the right map, topic, and entry — I don't teach the content, I tell you where it lives.",
)

if __name__ == "__main__":
    model = PROVIDERS.get(PROVIDER, {}).get("model", "mock")
    logger.info(f"provider={PROVIDER}  model={model}")
    demo.launch()
