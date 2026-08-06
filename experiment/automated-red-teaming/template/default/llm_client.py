"""Thin OpenRouter client. Model ids come from environment variables."""
from __future__ import annotations

import os
from openai import OpenAI


def _client() -> OpenAI:
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY is not set")
    base_url = os.environ.get("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
    return OpenAI(base_url=base_url, api_key=api_key)


def chat(model: str, messages: list[dict], *, temperature: float = 0.0, max_tokens: int = 2048) -> str:
    client = _client()
    resp = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    content = resp.choices[0].message.content
    return (content or "").strip()
