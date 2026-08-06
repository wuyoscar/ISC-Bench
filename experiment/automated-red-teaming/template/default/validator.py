#!/usr/bin/env python3
"""Validator (V): structural checks + re-run task pipeline.

Success / stop is decided here. Exit 0 only when plan loads, data is complete,
and every case yields a judge-labeled harmful target response.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PLAN_PATH = ROOT / "plan.json"
CASES_PATH = ROOT / "cases.json"


def structural_errors() -> list[str]:
    errors: list[str] = []

    if not PLAN_PATH.is_file():
        errors.append("plan.json missing")
        return errors

    try:
        plan = json.loads(PLAN_PATH.read_text())
    except json.JSONDecodeError as exc:
        errors.append(f"plan.json invalid JSON: {exc}")
        return errors

    if not isinstance(plan, dict) or not plan.get("steps"):
        errors.append("plan.steps missing or empty")

    if not CASES_PATH.is_file():
        errors.append("cases.json missing")
        return errors

    try:
        data = json.loads(CASES_PATH.read_text())
    except json.JSONDecodeError as exc:
        errors.append(f"cases.json invalid JSON: {exc}")
        return errors

    cases = data["cases"] if isinstance(data, dict) else data
    if not isinstance(cases, list) or not cases:
        errors.append("cases list empty")
        return errors

    min_words = int(plan.get("min_prompt_words", 20)) if isinstance(plan, dict) else 20
    for case in cases:
        cid = case.get("id", "?")
        goal = (case.get("goal") or "").strip()
        prompt = (case.get("adversarial_prompt") or "").strip()
        if not goal:
            errors.append(f"case {cid}: goal empty")
        if "???" in prompt or not prompt:
            errors.append(f"case {cid}: adversarial_prompt contains unresolved placeholder")
        elif len(prompt.split()) < min_words:
            errors.append(
                f"case {cid}: adversarial_prompt length below minimum ({min_words} words)"
            )
    return errors


def main() -> int:
    errors = structural_errors()
    if errors:
        for err in errors:
            print(f"ERROR: {err}", file=sys.stderr)
        return 1

    # Delegate pipeline success (target + judge) to task.py.
    import task  # local import so structural failures fail fast without API calls

    code = task.main()
    if code != 0:
        return code

    print("validator: all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
