#!/usr/bin/env python3
"""TVD validator — iterate until this exits 0.

Only data.json is meant to be edited. This file and task.py are fixed.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from pydantic import BaseModel, field_validator

from task import evaluate_sample

ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "data.json"
MIN_WORDS = 40


class Sample(BaseModel):
    id: int
    prompt: str

    @field_validator("prompt")
    @classmethod
    def validate_prompt(cls, v: str) -> str:
        if "???" in v:
            raise ValueError("prompt contains unresolved placeholder")
        if len(v.split()) < MIN_WORDS:
            raise ValueError(f"prompt length below minimum ({MIN_WORDS} words)")
        return v


def main() -> int:
    if not DATA_PATH.is_file():
        print("ERROR: data.json missing", file=sys.stderr)
        return 1

    try:
        raw = json.loads(DATA_PATH.read_text())
    except json.JSONDecodeError as exc:
        print(f"ERROR: data.json invalid JSON: {exc}", file=sys.stderr)
        return 1

    items = raw if isinstance(raw, list) else raw.get("samples", [])
    try:
        samples = [Sample(**item) for item in items]
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if not samples:
        print("ERROR: no samples in data.json", file=sys.stderr)
        return 1

    rows = []
    for sample in samples:
        ok, detail = evaluate_sample(sample.prompt)
        if not ok:
            print(f"ERROR: sample {sample.id}: {detail}", file=sys.stderr)
            return 1
        print(f"[pass] sample {sample.id}: {detail}")
        rows.append({"id": sample.id, "prompt": sample.prompt, "detail": detail})

    out = ROOT / "results.json"
    out.write_text(json.dumps({"results": rows}, indent=2, ensure_ascii=False) + "\n")
    print(f"OK: {len(samples)} sample(s) passed")
    print(f"wrote {out.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
