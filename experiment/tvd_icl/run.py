#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["openai>=1.0", "python-dotenv", "tqdm"]
# ///
"""
ISC In-Context Learning Experiment Runner.

Sends multi-turn TVD prompts (with completed demos) to a target LLM.

Usage:
    uv run run.py --model openai/gpt-5.2
    uv run run.py --model openai/gpt-5.2 --demos 5
    uv run run.py --model openai/gpt-5.2 --bench harmbench --demos 1

Demos: 1, 5, 10, 20 (number of completed examples shown before target)
Bench: default (JBB), or harmbench/strongreject/advbench (run build.py first)
"""
import asyncio
import json
import os
import random
import sys
from pathlib import Path

from dotenv import load_dotenv
from openai import AsyncOpenAI, APIError, RateLimitError
from tqdm.asyncio import tqdm_asyncio

load_dotenv(Path(__file__).parent.parent.parent / ".env")

BASE_URL = "https://openrouter.ai/api/v1"
DATA_DIR = Path(__file__).parent / "data"
OUTPUT_DIR = Path(__file__).parent / "results"


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


def find_input(model: str, demos: int, bench: str | None = None) -> Path:
    """Find ICL input file. Model-specific if available, otherwise random fallback."""
    model_slug = model.replace("/", "-")
    base = DATA_DIR / bench if bench else DATA_DIR
    model_dir = base / model_slug

    # Try model-specific data first
    if model_dir.exists():
        candidates = list(model_dir.glob(f"demo{demos}_*.json"))
        if candidates:
            print(f"Using model-specific demos from {model_slug}/")
            return candidates[0]

    # Fallback: randomly pick from available models
    if not base.exists():
        print(f"No ICL demo data found in {base}.")
        sys.exit(1)
    available = [d for d in base.iterdir() if d.is_dir()]
    if not available:
        print("No ICL demo data found.")
        sys.exit(1)

    random.shuffle(available)
    for d in available:
        candidates = list(d.glob(f"demo{demos}_*.json"))
        if candidates:
            print(f"No demos for {model_slug}, using fallback from {d.name}/")
            return candidates[0]

    print(f"No input for {demos} demos in any model directory.")
    print(f"Available demo counts: {set(f.name.split('_')[0] for d in available for f in d.glob('demo*.json'))}")
    sys.exit(1)


async def run(model: str, demos: int, bench: str | None = None,
              concurrent: int = 10) -> None:
    model_slug = model.replace("/", "-")
    input_file = find_input(model, demos, bench)
    data = json.loads(input_file.read_text())
    config, items = data["config"], data["results"]

    print(f"Model:   {model}")
    print(f"Demos:   {demos}")
    print(f"Source:  {input_file.parent.name}/{input_file.name}")
    print(f"Queries: {len(items)}")

    client = AsyncOpenAI(base_url=BASE_URL, api_key=os.environ["OPENROUTER_API_KEY"])
    sem = asyncio.Semaphore(concurrent)

    async def process(item: dict) -> dict:
        async with sem:
            response = await call_llm(client, model, item["messages"])
            return {**item, "response": response}

    results = await tqdm_asyncio.gather(*[process(item) for item in items])

    # Save
    out_dir = OUTPUT_DIR / model_slug
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"icl_{demos}demo.json"
    out_file.write_text(json.dumps(
        {"config": {**config, "target_model": model}, "results": results},
        indent=2, ensure_ascii=False
    ))
    print(f"Saved: {out_file}")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="ISC ICL Experiment")
    parser.add_argument("-m", "--model", required=True, help="OpenRouter model ID")
    parser.add_argument("-d", "--demos", type=int, default=1, choices=[1, 5, 10, 20])
    parser.add_argument("-b", "--bench", default=None,
                        help="Benchmark name (default: use base data/; or harmbench, strongreject, advbench after build.py)")
    parser.add_argument("-c", "--concurrent", type=int, default=10)
    args = parser.parse_args()
    asyncio.run(run(args.model, args.demos, args.bench, args.concurrent))


if __name__ == "__main__":
    main()
