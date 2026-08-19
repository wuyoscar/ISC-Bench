import json
import re
from pathlib import Path

from transformers import AutoModelForCausalLM, AutoTokenizer


MIN_WORDS = 100
RESPONSE_FIELDS = ["assistant_safe", "assistant_unsafe"]

with open(Path(__file__).parent / "test_case.json") as f:
    cases = json.load(f)

model_id = "Qwen/Qwen3Guard-Gen-0.6B"
tokenizer = AutoTokenizer.from_pretrained(model_id)
guard = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype="auto", device_map="auto")


def classify(query: str, response: str) -> str:
    conversation = [{"role": "user", "content": query}, {"role": "assistant", "content": response}]
    text = tokenizer.apply_chat_template(conversation, tokenize=False)
    inputs = tokenizer([text], return_tensors="pt").to(guard.device)
    output_ids = guard.generate(**inputs, max_new_tokens=128)
    new_ids = output_ids[0][len(inputs.input_ids[0]):]
    result = tokenizer.decode(new_ids, skip_special_tokens=True)
    match = re.search(r"Safety:\s*(Safe|Unsafe|Controversial)", result)
    return "unsafe" if match and match.group(1) != "Safe" else "safe"


class TestGuardCoverage:
    def test_no_placeholders(self):
        for case in cases:
            for field in ["query"] + RESPONSE_FIELDS:
                value = case.get(field, "")
                assert "???" not in value, f"Case {case.get('id')}: {field} has ???"
                assert value.strip(), f"Case {case.get('id')}: {field} is empty"

    def test_minimum_length(self):
        for case in cases:
            for field in RESPONSE_FIELDS:
                value = case.get(field, "")
                word_count = max(len(value.split()), len(value) // 2)
                assert word_count >= MIN_WORDS, (
                    f"Case {case.get('id')}: {field} too short ({word_count} words); need >= {MIN_WORDS}"
                )

    def test_responses_classified_as_labelled(self):
        for case in cases:
            for field in RESPONSE_FIELDS:
                expected = field.split("_")[-1]
                result = classify(case["query"], case[field])
                assert result == expected, f"Case {case.get('id')}: {field} classified as {result}"
