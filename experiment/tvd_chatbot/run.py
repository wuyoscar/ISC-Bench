#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["openai>=1.0", "python-dotenv", "tqdm"]
# ///
"""
TVD Chatbot Experiment Runner.

Sends pre-built TVD prompts to a target LLM and saves responses.

Usage:
    uv run run.py --model openai/gpt-5.2
    uv run run.py --model openai/gpt-5.2 --bench jbb --task ai-guard
    uv run run.py --model openai/gpt-5.2 --bench jbb --task ai-detoxify --samples 3
    uv run run.py --model openai/gpt-5.2 --bench harmbench --task ai-guard

Bench: jbb (default), harmbench, strongreject, or any custom name
Tasks: ai-guard (Llama-Guard), ai-detoxify (Detoxify), ai-outlier (PyOD)
Samples: 0-5 (number of pre-filled examples in the data file)
"""
import asyncio
import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from openai import AsyncOpenAI, APIError, RateLimitError
from tqdm.asyncio import tqdm_asyncio

load_dotenv(Path(__file__).parent.parent.parent / ".env")

BASE_URL = "https://openrouter.ai/api/v1"
DATA_DIR = Path(__file__).parent / "prompts"
OUTPUT_DIR = Path(__file__).parent / "result_demo"


async def call_llm(client: AsyncOpenAI, model: str, messages: list,
                   max_tokens: int = 4096) -> str:
    try:
        resp = await client.chat.completions.create(
            model=model, messages=messages,
            max_tokens=max_tokens, temperature=0.0,
            extra_body={"reasoning": {"effort": "none"}},
        )
        content = resp.choices[0].message.content
        return content.strip() if content else f"[EMPTY] finish_reason={resp.choices[0].finish_reason}"
    except RateLimitError:
        await asyncio.sleep(5)
        return await call_llm(client, model, messages, max_tokens)
    except APIError as e:
        return f"[ERROR] {e}"


async def run(model: str, task: str, samples: int, bench: str = "jbb", concurrent: int = 10) -> None:
    # Find input file: data/{bench}/{task}/{samples}sample.json
    task_dir = DATA_DIR / bench / task
    input_file = task_dir / f"{samples}sample.json"
    if not input_file.exists():
        if not task_dir.exists():
            available_benchs = [d.name for d in DATA_DIR.iterdir() if d.is_dir()]
            print(f"Benchmark '{bench}' not found. Available: {available_benchs}")
            print(f"Build custom data first: uv run build.py --queries your_queries.txt --bench {bench} --task {task}")
        else:
            available = [f.name for f in task_dir.glob("*.json")]
            print(f"No {samples}sample.json in {bench}/{task}/. Available: {available}")
        sys.exit(1)
    data = json.loads(input_file.read_text())
    config, items = data["config"], data["results"]

    print(f"Model:   {model}")
    print(f"Bench:   {bench}")
    print(f"Task:    {task}")
    print(f"Samples: {samples}")
    print(f"Queries: {len(items)}")

    client = AsyncOpenAI(base_url=BASE_URL, api_key=os.environ["OPENROUTER_API_KEY"])
    sem = asyncio.Semaphore(concurrent)

    async def process(item: dict) -> dict:
        async with sem:
            response = await call_llm(client, model, item["messages"])
            return {**item, "response": response}

    results = await tqdm_asyncio.gather(*[process(item) for item in items])

    # Save
    model_slug = model.replace("/", "-")
    out_dir = OUTPUT_DIR / model_slug / bench / task
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"{samples}sample.json"
    out_file.write_text(json.dumps(
        {"config": {**config, "target_model": model}, "results": results},
        indent=2, ensure_ascii=False
    ))
    print(f"Saved: {out_file}")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="TVD Chatbot Experiment")
    parser.add_argument("-m", "--model", required=True, help="OpenRouter model ID")
    parser.add_argument("-b", "--bench", default="jbb", help="Benchmark name (jbb, harmbench, advbench, strongreject)")
    parser.add_argument("-t", "--task", default="ai-guard", choices=["ai-guard", "ai-detoxify", "ai-outlier"])
    parser.add_argument("-s", "--samples", type=int, default=0, choices=[0, 1, 2, 3, 4, 5],
                        help="Number of pre-filled examples (0=zero-shot)")
    parser.add_argument("-c", "--concurrent", type=int, default=10)
    args = parser.parse_args()
    asyncio.run(run(args.model, args.task, args.samples, args.bench, args.concurrent))


if __name__ == "__main__":
    main()
