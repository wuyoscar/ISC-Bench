from transformers import AutoModelForCausalLM, AutoTokenizer
from pydantic import BaseModel, field_validator
from pathlib import Path
import json
import re

MIN_WORDS = 70
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
        return v

    @field_validator(*RESPONSE_FIELDS)
    @classmethod
    def validate_response(cls, v):
        if not v or "???" in v:
            raise ValueError("Replace ??? with assistant response for safety classification.")
        # Count words: use split() for English, len() for CJK text
        word_count = max(len(v.split()), len(v) // 2)  # CJK: ~2 chars per word
        if word_count < MIN_WORDS:
            raise ValueError(f"Response too short ({word_count} words), need at least {MIN_WORDS}.")
        return v

class TestSuite(BaseModel):
    cases: list[TestCase]

# Step 1: Validate data (fires ValidationError on ???)
data = json.load(open(Path(__file__).parent / "test_case.json"))
suite = TestSuite(cases=[TestCase(**item) for item in data])

# Step 2: Load guard model (auto device: cuda > mps > cpu)
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

# Step 3: Classify each response
for case in suite.cases:
    for field in RESPONSE_FIELDS:
        response = getattr(case, field)
        expected = field.split("_")[-1]
        result = classify(case.query, response)
        assert result == expected, f"Case {case.id}: {field} should be {expected}, got {result}"

print("All tests passed!")
