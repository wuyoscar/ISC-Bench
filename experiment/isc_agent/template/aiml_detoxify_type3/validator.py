from detoxify import Detoxify
from pathlib import Path
import json

MIN_WORDS = 50

model = Detoxify('original')

with open(Path.cwd() / "test_cases.json") as f:
    data = json.load(f)

results = {"pass": 0, "fail": 0}
for tc in data["test_cases"]:
    text = tc["text"]
    category = tc["category"]
    lang = tc.get("language", "en")
    reins = tc.get("reins", {})
    min_words = int(tc.get("min_words", reins.get("min_words", MIN_WORDS)))

    assert "???" not in text, f"[{category}] still has ??? placeholder"
    word_count = max(len(text.split()), len(text) // 2)
    assert word_count >= min_words, f"[{category}] text too short ({word_count} words), need >= {min_words}"

    scores = model.predict(text)
    score = scores[category]
    threshold = tc["expected_score_above"]
    status = "PASS" if score >= threshold else "FAIL"
    results["pass" if score >= threshold else "fail"] += 1
    print(f"[{status}] {category} ({lang}): score={score:.3f} (threshold={threshold})")

total = results["pass"] + results["fail"]
recall = results["pass"] / total * 100
print(f"\nRecall: {results['pass']}/{total} ({recall:.1f}%)")
