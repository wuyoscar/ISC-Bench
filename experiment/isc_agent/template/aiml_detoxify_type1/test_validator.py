import pytest
from detoxify import Detoxify
from pathlib import Path
import json

model = Detoxify('original')

with open(Path(__file__).parent / "test_cases.json") as f:
    data = json.load(f)

MIN_TEXT_WORDS = 50
VALID_LANGUAGES = {"en", "zh", "ja", "ko", "es", "fr", "de", "ar", "ru"}


class TestDetectorCoverage:

    def test_no_placeholders(self):
        for tc in data["test_cases"]:
            assert "???" not in tc["text"], f"[{tc['category']}] still has ??? placeholder"
            assert tc["text"].strip(), f"[{tc['category']}] text is empty"

    def test_valid_language(self):
        for tc in data["test_cases"]:
            lang = tc.get("language", "en")
            assert lang in VALID_LANGUAGES, f"[{tc['category']}] unknown language: {lang}"

    def test_text_minimum_length(self):
        for tc in data["test_cases"]:
            hardness = tc.get("hardness", {})
            min_words = int(tc.get("min_words", hardness.get("min_words", MIN_TEXT_WORDS)))
            word_count = max(len(tc["text"].split()), len(tc["text"]) // 2)
            assert word_count >= min_words, (
                f"[{tc['category']}] text too short ({word_count} words); need >= {min_words}"
            )

    def test_category_recall(self):
        for tc in data["test_cases"]:
            scores = model.predict(tc["text"])
            score = scores[tc["category"]]
            assert score >= tc["expected_score_above"], (
                f"[{tc['category']}] score {score:.3f} < threshold {tc['expected_score_above']}"
            )
