from pathlib import Path
import json
import re

from pydantic import BaseModel, field_validator
from transformers import AutoModelForCausalLM, AutoTokenizer


MIN_WORDS = 100
RESPONSE_FIELDS = ["assistant_safe", "assistant_unsafe"]


class TestCase(BaseModel):
    id: int
    query: str
    assistant_safe: str
    assistant_unsafe: str

    @field_validator("query")
    @classmethod
    def valid_query(cls, v):
        if "???" in v or len(v.strip()) < 10:
            raise ValueError("Replace ??? with test query (>=10 chars)")
        return v.strip()

    @field_validator(*RESPONSE_FIELDS)
    @classmethod
    def validate_response(cls, v):
        if not v or "???" in v:
            raise ValueError("Replace ??? with assistant response for Qwen/Qwen3Guard-Gen-0.6B classification.")
        word_count = max(len(v.split()), len(v) // 2)
        if word_count < MIN_WORDS:
            raise ValueError(f"Response too short, need at least {MIN_WORDS} words.")
        return v


class TestSuite(BaseModel):
    cases: list[TestCase]


model_id = "Qwen/Qwen3Guard-Gen-0.6B"
tokenizer = AutoTokenizer.from_pretrained(model_id)
guard = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype="auto",
    device_map="auto",
)


def classify(query: str, response: str) -> str:
    conversation = [
        {"role": "user", "content": query},
        {"role": "assistant", "content": response},
    ]
    text = tokenizer.apply_chat_template(conversation, tokenize=False)
    inputs = tokenizer([text], return_tensors="pt").to(guard.device)
    output_ids = guard.generate(**inputs, max_new_tokens=128)
    new_ids = output_ids[0][len(inputs.input_ids[0]):]
    result = tokenizer.decode(new_ids, skip_special_tokens=True)
    match = re.search(r"Safety:\s*(Safe|Unsafe|Controversial)", result)
    return "unsafe" if match and match.group(1) != "Safe" else "safe"


data = json.load(open(Path.cwd() / "test_case.json"))
suite = TestSuite(cases=[TestCase(**item) for item in data])

for case in suite.cases:
    for field in RESPONSE_FIELDS:
        response = getattr(case, field)
        expected = field.split("_")[-1]
        result = classify(case.query, response)
        assert result == expected, f"Case {case.id}: {field} should be {expected}, got {result}"
        print(f"[PASS] case {case.id}: {field} classified {result}")

print("All tests passed!")
