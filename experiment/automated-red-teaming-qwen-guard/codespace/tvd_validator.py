#!/usr/bin/env python3
"""TVD validator — iterate until this exits 0.

Only data.json is meant to be edited. This file and task.py are fixed.
Each run appends one entry to rounds.json (all attempted prompts across the loop).
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from pydantic import BaseModel, field_validator

from task import evaluate_sample

ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "data.json"
ROUNDS_PATH = ROOT / "rounds.json"
RESULTS_PATH = ROOT / "results.json"
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


def _load_rounds() -> list[dict]:
    if not ROUNDS_PATH.is_file():
        return []
    try:
        data = json.loads(ROUNDS_PATH.read_text())
        if isinstance(data, list):
            return data
        if isinstance(data, dict) and isinstance(data.get("rounds"), list):
            return data["rounds"]
    except json.JSONDecodeError:
        pass
    return []


def _save_rounds(rounds: list[dict]) -> None:
    ROUNDS_PATH.write_text(
        json.dumps({"rounds": rounds}, indent=2, ensure_ascii=False) + "\n"
    )


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
    # Structural failures (e.g. ???) — still log the attempt.
    rounds = _load_rounds()
    round_idx = len(rounds) + 1
    ts = datetime.now(timezone.utc).isoformat()

    try:
        samples = [Sample(**item) for item in items]
    except Exception as exc:
        rounds.append(
            {
                "round": round_idx,
                "timestamp": ts,
                "passed": False,
                "error": str(exc),
                "prompts": [
                    {"id": it.get("id"), "prompt": it.get("prompt")}
                    for it in items
                    if isinstance(it, dict)
                ],
            }
        )
        _save_rounds(rounds)
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if not samples:
        rounds.append(
            {
                "round": round_idx,
                "timestamp": ts,
                "passed": False,
                "error": "no samples in data.json",
                "prompts": [],
            }
        )
        _save_rounds(rounds)
        print("ERROR: no samples in data.json", file=sys.stderr)
        return 1

    rows = []
    all_ok = True
    for sample in samples:
        ok, detail, payload = evaluate_sample(sample.prompt)
        row = {
            "id": sample.id,
            "prompt": sample.prompt,
            "detail": detail,
            "moderation_flagged": payload.get("moderation_flagged"),
            "target_model": payload.get("target_model"),
            "target_response": payload.get("target_response"),
            "target_response_len": payload.get("target_response_len"),
            "target_response_preview": (payload.get("target_response") or "")[:500]
            or None,
            "guard_label": payload.get("guard_label"),
            "guard_categories": payload.get("guard_categories"),
            "guard_refusal": payload.get("guard_refusal"),
            "guard_raw": payload.get("guard_raw"),
        }
        rows.append(row)
        if not ok:
            all_ok = False
            print(f"ERROR: sample {sample.id}: {detail}", file=sys.stderr)

    # One rounds entry per validator invocation (all prompts this attempt).
    rounds.append(
        {
            "round": round_idx,
            "timestamp": ts,
            "passed": all_ok,
            "prompts": [{"id": s.id, "prompt": s.prompt} for s in samples],
            "details": [
                {
                    "id": r["id"],
                    "detail": r["detail"],
                    "moderation_flagged": r["moderation_flagged"],
                    "target_response_len": r["target_response_len"],
                    "guard_label": r["guard_label"],
                    "guard_categories": r["guard_categories"],
                }
                for r in rows
            ],
        }
    )
    _save_rounds(rounds)
    print(f"[rounds] logged round {round_idx} (total {len(rounds)})")

    out_payload = {
        "passed": all_ok,
        "results": rows,
        "rounds": rounds,
        "n_rounds": len(rounds),
    }
    RESULTS_PATH.write_text(
        json.dumps(out_payload, indent=2, ensure_ascii=False) + "\n"
    )

    if not all_ok:
        return 1

    print(f"OK: {len(samples)} sample(s) passed after {len(rounds)} round(s)")
    print(f"wrote {RESULTS_PATH.name} and {ROUNDS_PATH.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
