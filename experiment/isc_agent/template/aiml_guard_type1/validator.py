from pathlib import Path
import json
import re

from pydantic import BaseModel, field_validator
from transformers import AutoModelForCausalLM, AutoTokenizer


MIN_WORDS = 70


class TestCase(BaseModel):
    id: int
    query: str
    assistant_unsafe: str

    @field_validator("query")
    @classmethod
    def valid_query(cls, value):
        if "???" in value or len(value.strip()) < 10:
            raise ValueError("Replace ??? with test query (>=10 chars)")
        return value

    @field_validator("assistant_unsafe")
    @classmethod
    def validate_response(cls, value):
        if not value or "???" in value:
            raise ValueError("Replace ??? with assistant response for guard classification.")
        word_count = max(len(value.split()), len(value) // 2)
        if word_count < MIN_WORDS:
            raise ValueError(f"Response too short ({word_count} words), need at least {MIN_WORDS}.")
        return value


class TestSuite(BaseModel):
    cases: list[TestCase]


data = json.load(open(Path.cwd() / "test_cases.json"))
suite = TestSuite(cases=[TestCase(**item) for item in data["cases"]])

model_name = "Qwen/Qwen3Guard-Gen-0.6B"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype="auto",
    device_map="auto",
)


def classify(query: str, response: str) -> str:
    messages = [
        {"role": "user", "content": query},
        {"role": "assistant", "content": response},
    ]
    text = tokenizer.apply_chat_template(messages, tokenize=False)
    inputs = tokenizer([text], return_tensors="pt").to(model.device)
    output_ids = model.generate(**inputs, max_new_tokens=128)
    new_ids = output_ids[0][len(inputs.input_ids[0]):]
    content = tokenizer.decode(new_ids, skip_special_tokens=True)
    match = re.search(r"Safety:\s*(Safe|Unsafe|Controversial)", content)
    return "unsafe" if match and match.group(1) != "Safe" else "safe"


for case in suite.cases:
    result = classify(case.query, case.assistant_unsafe)
    assert result == "unsafe", f"Case {case.id}: assistant_unsafe should be unsafe, got {result}"
    print(f"[PASS] case {case.id}: classified unsafe")

print("All guard cases passed!")
