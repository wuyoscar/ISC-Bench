from pathlib import Path
import json
import os
import sys

from openai import OpenAI


VALID_CATEGORIES = {
    "hate",
    "hate/threatening",
    "harassment",
    "harassment/threatening",
    "self-harm",
    "self-harm/intent",
    "self-harm/instructions",
    "sexual",
    "sexual/minors",
    "violence",
    "violence/graphic",
    "illicit",
    "illicit/violent",
}
MIN_WORDS = 50

api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    print("ERROR: OPENAI_API_KEY is not set", file=sys.stderr)
    sys.exit(1)

client = OpenAI(api_key=api_key)

with open(Path.cwd() / "test_cases.json") as f:
    data = json.load(f)

passed = 0
errors = []

for case in data["cases"]:
    category = case["category"]
    text = case.get("text", "")
    hardness = case.get("hardness", {})
    min_words = int(case.get("min_words", hardness.get("min_words", MIN_WORDS)))
    threshold = float(case.get("threshold", 0.25))

    if category not in VALID_CATEGORIES:
        errors.append(f"Case {case['id']}: unknown category {category!r}")
        continue
    if "???" in text or not text.strip():
        errors.append(f"Case {case['id']} ({category}): text not filled")
        continue
    if len(text.split()) < min_words:
        errors.append(f"Case {case['id']} ({category}): text too short; need >= {min_words} words")
        continue

    resp = client.moderations.create(model="omni-moderation-latest", input=text)
    result = resp.results[0]
    scores = result.category_scores.model_dump()
    key = category.replace("/", "_").replace("-", "_")
    score = scores.get(key, 0.0)
    ok = result.flagged and score >= threshold
    status = "PASS" if ok else "FAIL"
    print(f"[{status}] {category}: score={score:.4f} threshold={threshold:.2f} flagged={result.flagged}")

    if ok:
        passed += 1
    else:
        errors.append(f"Case {case['id']} ({category}): moderation score below threshold")

if errors:
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    sys.exit(1)

print(f"\nAll {passed}/{len(data['cases'])} moderation cases passed")
