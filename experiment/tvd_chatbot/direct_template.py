#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["openai>=1.0", "python-dotenv"]
# ///
"""Direct single-turn template runner.

Feed a `codebase_templates/<name>/exp0.txt` straight to a model (one call) and save the
raw simulated output. No agent loop, no validator — just input -> output, to
check whether a model fills the TVD scenario.

Providers (OpenRouter is the default; the others are direct vendor APIs for
models OpenRouter can't serve on this account):
    --provider openrouter   OPENROUTER_API_KEY   https://openrouter.ai/api/v1
    --provider openai        OPENAI_API_KEY        https://api.openai.com/v1
    --provider anthropic     ANTHROPIC_API_KEY     https://api.anthropic.com/v1/

Usage:
    uv run direct_template.py --model moonshotai/kimi-k2 --template aiml_detoxify
    uv run direct_template.py --provider openai --model gpt-5 --template aiml_propaganda
"""
import argparse
import json
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

ROOT = Path(__file__).resolve().parents[2]
TEMPLATES = ROOT / "codebase_templates"
OUT = Path(__file__).parent / "result_direct"
load_dotenv(ROOT / ".env", override=True)  # .env wins over empty/stale shell vars

PROVIDERS = {
    "openrouter": ("https://openrouter.ai/api/v1", "OPENROUTER_API_KEY"),
    "openai": ("https://api.openai.com/v1", "OPENAI_API_KEY"),
    "anthropic": ("https://api.anthropic.com/v1/", "ANTHROPIC_API_KEY"),
}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("-m", "--model", required=True, help="model id for the chosen provider")
    ap.add_argument("-t", "--template", required=True, help="template dir under codebase_templates/")
    ap.add_argument("--provider", default="openrouter", choices=list(PROVIDERS))
    ap.add_argument("--variant", default="exp0.txt")
    ap.add_argument("--max-tokens", type=int, default=16000)
    args = ap.parse_args()

    prompt = (TEMPLATES / args.template / args.variant).read_text()
    base_url, key_env = PROVIDERS[args.provider]
    client = OpenAI(base_url=base_url, api_key=os.environ[key_env])

    kwargs = {"model": args.model, "messages": [{"role": "user", "content": prompt}]}
    # Reasoning models on OpenAI use max_completion_tokens and reject temperature;
    # everything else uses max_tokens. Keep it simple and provider-correct.
    if args.provider == "openai":
        kwargs["max_completion_tokens"] = args.max_tokens
    else:
        kwargs["max_tokens"] = args.max_tokens

    resp = client.chat.completions.create(**kwargs)
    output = resp.choices[0].message.content or ""

    out_dir = OUT / f"{args.provider}_{args.model.replace('/', '-')}"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"{args.template}.json"
    out_file.write_text(json.dumps(
        {"model": args.model, "provider": args.provider, "template": args.template,
         "variant": args.variant, "prompt": prompt, "output": output},
        ensure_ascii=False, indent=2,
    ))
    print(f"== {args.provider}:{args.model} / {args.template} == chars={len(output)}")
    print(output[:600])
    print(f"saved: {out_file}")


if __name__ == "__main__":
    main()
