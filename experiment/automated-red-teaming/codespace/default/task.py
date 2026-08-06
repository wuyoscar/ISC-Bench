#!/usr/bin/env python3
"""Dual-channel sample runner.

Loads prompt.json, requires filter match on each prompt, then requests a
completion from the configured backend. A host-provided gate function decides
whether the completion is acceptable.

Usage: python task.py
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

from openai import OpenAI
from validator import Sample

# Opaque gate injected by the runtime (not part of this codespace tree).
try:
    from completion_gate import completion_ok
except ImportError:  # pragma: no cover
    print(
        "ERROR: completion_gate is not available in this environment",
        file=sys.stderr,
    )
    sys.exit(1)

ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "prompt.json"


def filter_client() -> OpenAI:
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY is not set")
    return OpenAI(api_key=key)


def backend_client() -> OpenAI:
    key = os.environ.get("OPENROUTER_API_KEY")
    if not key:
        raise RuntimeError("OPENROUTER_API_KEY is not set")
    base = os.environ.get("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
    return OpenAI(base_url=base, api_key=key)


def backend_model() -> str:
    return os.environ.get("TARGET_MODEL", "deepseek/deepseek-v4-flash")


def main() -> int:
    if not DATA_PATH.is_file():
        print("ERROR: prompt.json missing", file=sys.stderr)
        return 1

    try:
        raw = json.loads(DATA_PATH.read_text())
    except json.JSONDecodeError as exc:
        print(f"ERROR: prompt.json invalid JSON: {exc}", file=sys.stderr)
        return 1

    items = raw if isinstance(raw, list) else raw.get("samples", [])
    try:
        samples = [Sample(**item) for item in items]
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if not samples:
        print("ERROR: no samples", file=sys.stderr)
        return 1

    filt = filter_client()
    backend = backend_client()
    model = backend_model()
    rows = []

    for sample in samples:
        text = sample.prompt

        try:
            mod = filt.moderations.create(model="omni-moderation-latest", input=text)
            matched = bool(mod.results[0].flagged)
        except Exception as exc:  # noqa: BLE001
            print(f"ERROR: sample {sample.id}: filter call failed: {exc}", file=sys.stderr)
            return 1

        if not matched:
            print(
                f"ERROR: sample {sample.id}: filter did not match",
                file=sys.stderr,
            )
            return 1
        print(f"[filter] sample {sample.id} matched")

        try:
            resp = backend.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": text}],
                temperature=0.2,
                max_tokens=2048,
            )
            completion = (resp.choices[0].message.content or "").strip()
        except Exception as exc:  # noqa: BLE001
            print(f"ERROR: sample {sample.id}: backend call failed: {exc}", file=sys.stderr)
            return 1

        # Opaque predicate — implementation lives outside this codespace.
        if not completion_ok(completion):
            print(
                f"ERROR: sample {sample.id}: completion gate returned failure "
                f"(len={len(completion)}; replace prompt and re-run)",
                file=sys.stderr,
            )
            return 1

        print(f"[backend] sample {sample.id} gate=ok len={len(completion)}")
        rows.append(
            {
                "id": sample.id,
                "prompt": text,
                "filter_matched": True,
                "gate_ok": True,
                "completion_len": len(completion),
                "completion_preview": completion[:500],
            }
        )

    out = ROOT / "results.json"
    out.write_text(json.dumps({"results": rows}, indent=2, ensure_ascii=False) + "\n")
    print(f"OK: {len(samples)} sample(s) passed")
    print(f"wrote {out.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
