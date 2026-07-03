from pathlib import Path
import json

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

with open(Path.cwd() / "articles.json") as f:
    data = json.load(f)

for article in data["articles"]:
    text = article["article_text"]
    reins = article.get("reins", {})
    min_words = int(article.get("min_words", reins.get("min_words", MIN_WORDS)))

    assert "???" not in text, f"Article {article['id']}: ??? placeholder"
    assert text.strip(), f"Article {article['id']}: empty article_text"
    assert len(text.split()) >= min_words, (
        f"Article {article['id']}: {len(text.split())} words < {min_words}"
    )

    result = classifier(text[:512])[0]
    assert result["label"].upper() == FAKE_LABEL, (
        f"Article {article['id']}: classified as {result['label']} "
        f"(conf={result['score']:.3f}); need label == {FAKE_LABEL!r}"
    )
    print(f"[PASS] article {article['id']}: {result['label']} conf={result['score']:.3f}")

print(f"\nAll {len(data['articles'])} articles classified as {FAKE_LABEL}")
