"""Target completion wrapper. The model id is injected by the harness via env."""
from __future__ import annotations

import os

from llm_client import chat

DEFAULT_TARGET = "deepseek/deepseek-v4-flash"


def target_model() -> str:
    return os.environ.get("TARGET_MODEL", DEFAULT_TARGET)


def complete(prompt: str) -> str:
    """Send `prompt` to the target completion service and return the answer text."""
    return chat(
        target_model(),
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=2048,
    )
