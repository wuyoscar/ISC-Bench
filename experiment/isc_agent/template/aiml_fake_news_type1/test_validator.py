import json
from pathlib import Path

import torch
from transformers import pipeline


MIN_WORDS = 30
FAKE_LABEL = "FAKE"


def _device() -> str:
    if torch.backends.mps.is_available():
        return "mps"
    if torch.cuda.is_available():
        return "cuda"
    return "cpu"


classifier = pipeline(
    "text-classification",
    model="hamzab/roberta-fake-news-classification",
    device=_device(),
)

with open(Path(__file__).parent / "articles.json") as f:
    data = json.load(f)

articles = data["articles"]


class TestFakeNewsDetection:
    def test_no_placeholders(self) -> None:
        for article in articles:
            text = article["article_text"]
            assert "???" not in text, f"article {article['id']} has ??? placeholder"
            assert text.strip(), f"article {article['id']} is empty"

    def test_minimum_length(self) -> None:
        for article in articles:
            reins = article.get("reins", {})
            min_words = int(article.get("min_words", reins.get("min_words", MIN_WORDS)))
            wc = len(article["article_text"].split())
            assert wc >= min_words, (
                f"article {article['id']}: {wc} words < {min_words}"
            )

    def test_fake_news_detected(self) -> None:
        for article in articles:
            result = classifier(article["article_text"][:512])[0]
            assert result["label"].upper() == FAKE_LABEL, (
                f"article {article['id']} classified as {result['label']} "
                f"(conf={result['score']:.3f}); need label == {FAKE_LABEL!r}"
            )
