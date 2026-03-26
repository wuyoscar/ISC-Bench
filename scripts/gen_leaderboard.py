#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
Generate ISC Leaderboard table from arena_cache.json + isc_cases.json.
Replaces the leaderboard section in README.md between markers.

Usage:
    uv run scripts/gen_leaderboard.py
    uv run scripts/gen_leaderboard.py --top 100  # show top N in main table
"""
import json
import re
import sys
from pathlib import Path
from datetime import date

ROOT = Path(__file__).parent.parent
ARENA = ROOT / "assets" / "arena_cache.json"
ISC = ROOT / "assets" / "isc_cases.json"
README = ROOT / "README.md"

# Model name slug → display name overrides
DISPLAY_NAMES: dict[str, str] = {
    "claude-opus-4-6-thinking": "Claude Opus 4.6 Thinking",
    "claude-opus-4-6": "Claude Opus 4.6",
    "gemini-3.1-pro-preview": "Gemini 3.1 Pro Preview",
    "grok-4.20-beta1": "Grok 4.20 Beta",
    "gemini-3-pro": "Gemini 3 Pro",
    "gpt-5.4-high": "GPT-5.4 High",
    "gpt-5.2-chat-latest-20260210": "GPT-5.2 Chat",
    "grok-4.20-beta-0309-reasoning": "Grok 4.20 Reasoning",
    "gemini-3-flash": "Gemini 3 Flash",
    "claude-opus-4-5-20251101-thinking-32k": "Claude Opus 4.5 Thinking",
    "grok-4.1-thinking": "Grok 4.1 Thinking",
    "claude-opus-4-5-20251101": "Claude Opus 4.5",
    "claude-sonnet-4-6": "Claude Sonnet 4.6",
    "qwen3.5-max-preview": "Qwen 3.5 Max Preview",
    "gpt-5.3-chat-latest": "GPT-5.3 Chat",
    "gemini-3-flash (thinking-minimal)": "Gemini 3 Flash Thinking",
    "gpt-5.4": "GPT-5.4",
    "dola-seed-2.0-preview": "Dola Seed 2.0 Preview",
    "grok-4.1": "Grok 4.1",
    "gpt-5.1-high": "GPT-5.1 High",
    "glm-5": "GLM-5",
    "kimi-k2.5-thinking": "Kimi K2.5 Thinking",
    "claude-sonnet-4-5-20250929": "Claude Sonnet 4.5",
    "claude-sonnet-4-5-20250929-thinking-32k": "Claude Sonnet 4.5 Thinking",
    "ernie-5.0-0110": "ERNIE 5.0",
    "qwen3.5-397b-a17b": "Qwen 3.5 397B",
    "ernie-5.0-preview-1203": "ERNIE 5.0 Preview",
    "claude-opus-4-1-20250805-thinking-16k": "Claude Opus 4.1 Thinking",
    "gemini-2.5-pro": "Gemini 2.5 Pro",
    "claude-opus-4-1-20250805": "Claude Opus 4.1",
    "mimo-v2-pro": "Mimo V2 Pro",
    "gpt-4.5-preview-2025-02-27": "GPT-4.5 Preview",
    "chatgpt-4o-latest-20250326": "ChatGPT 4o Latest",
    "glm-4.7": "GLM-4.7",
    "gpt-5.2-high": "GPT-5.2 High",
    "gpt-5.2": "GPT-5.2",
    "gpt-5.1": "GPT-5.1",
    "gemini-3.1-flash-lite-preview": "Gemini 3.1 Flash Lite Preview",
    "qwen3-max-preview": "Qwen 3 Max Preview",
    "gpt-5-high": "GPT-5 High",
    "kimi-k2.5-instant": "Kimi K2.5 Instant",
    "o3-2025-04-16": "o3",
    "grok-4-1-fast-reasoning": "Grok 4.1 Fast Reasoning",
    "kimi-k2-thinking-turbo": "Kimi K2 Thinking Turbo",
    "amazon-nova-experimental-chat-26-02-10": "Amazon Nova Experimental",
    "gpt-5-chat": "GPT-5 Chat",
    "glm-4.6": "GLM-4.6",
    "deepseek-v3.2-exp-thinking": "DeepSeek V3.2 Thinking",
    "deepseek-v3.2": "DeepSeek V3.2",
    "qwen3-max-2025-09-23": "Qwen 3 Max 2025-09-23",
}

# ISC case name matching (isc_cases.json uses display names)
ISC_NAME_MAP: dict[str, str] = {
    "claude-opus-4-6": "Claude Opus 4.6",
    "claude-opus-4-5-20251101": "Claude Opus 4.5",
    "claude-sonnet-4-6": "Claude Sonnet 4.6",
    "gemini-3-pro": "Gemini 3 Pro",
    "gpt-5.2-chat-latest-20260210": "GPT-5.2 Chat",
    "o3-2025-04-16": "o3",
    "grok-4.1": "Grok 4.1",
    "kimi-k2.5-thinking": "Kimi K2.5 Thinking",
    "qwen3-max-preview": "Qwen 3 Max Preview",
    "deepseek-v3.2": "DeepSeek V3.2",
    "glm-5": "GLM-5",
    "qwen3.5-397b-a17b": "Qwen 3.5 397B",
}


def slug_to_display(slug: str) -> str:
    """Convert API slug to display name."""
    if slug in DISPLAY_NAMES:
        return DISPLAY_NAMES[slug]
    # Auto-generate: replace hyphens, capitalize
    name = slug.replace("-", " ").title()
    # Fix common patterns
    name = re.sub(r"(\d) (\d)", r"\1.\2", name)  # "3 5" → "3.5"
    return name


def fav(domain: str) -> str:
    if not domain:
        return ""
    return f'<img src="https://www.google.com/s2/favicons?domain={domain}&sz=32" width="14">'


def gen_row(model: dict, isc_cases: dict) -> str:
    display = slug_to_display(model["name"])
    icon = fav(model["domain"])
    rank = model["rank"]
    score = model["score"]

    # Check ISC case
    isc = isc_cases.get(display)
    if isc:
        demos = isc["demos"]
        if len(demos) == 1:
            demo_str = f'[🔗]({demos[0]["link"]})'
            by_str = f'[@{demos[0]["by"]}](https://github.com/{demos[0]["by"]})'
        else:
            demo_str = " ".join(f'[🔗₁]({d["link"]})' if i == 0 else f'[🔗₂]({d["link"]})' for i, d in enumerate(demos))
            by_str = " ".join(f'[@{d["by"]}](https://github.com/{d["by"]})' for d in demos)
        status = "🔴"
    else:
        demo_str = ""
        by_str = ""
        status = "🟢"

    return f"| {rank} | {icon} {display} | {score} | {status} | {demo_str} | {by_str} |"


def main() -> None:
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--top", type=int, default=50, help="Models in main table")
    args = parser.parse_args()

    arena = json.loads(ARENA.read_text())
    isc_cases = json.loads(ISC.read_text())

    confirmed = sum(1 for m in arena if slug_to_display(m["name"]) in isc_cases)
    total = len(arena)
    today = date.today().isoformat()

    # No header/rules — kept minimal, handled in README manually

    table_header = "| Rank | Model | Arena Score | Jailbroken | Link | By |\n|:----:|-------|:-----:|:------:|:----:|:--:|"

    # Main table (top N)
    main_rows = [gen_row(m, isc_cases) for m in arena[:args.top]]

    # Extended table (rest)
    ext_rows = [gen_row(m, isc_cases) for m in arena[args.top:]]

    chart = (
        '<p align="center">\n'
        '  <img src="assets/leaderboard_progress.svg" width="80%">\n'
        '</p>'
    )

    lines = [
        "## 🏆 JailbreakArena",
        "",
        chart,
        "",
        table_header,
    ]
    lines.extend(main_rows)

    if ext_rows:
        lines.append("")
        lines.append("<details>")
        lines.append(f"<summary><b>Show all models ({args.top + 1}–{total})</b></summary>")
        lines.append("")
        lines.append(table_header)
        lines.extend(ext_rows)
        lines.append("")
        lines.append("</details>")

    section = "\n".join(lines)

    # Replace in README — only replace table, preserve History section
    readme = README.read_text()
    start = readme.index("## 🏆 JailbreakArena")
    # End boundary: either History <details> or the next --- section
    history_marker = readme.find("<details>\n<summary><b>📜 JailbreakArena History</b>", start)
    fallback_marker = re.search(r'\n---\n\n## ⚡', readme[start:])
    if history_marker > start:
        end = history_marker
    elif fallback_marker:
        end = start + fallback_marker.start()
    else:
        print("ERROR: Could not find section end marker")
        sys.exit(1)

    new_readme = readme[:start] + section + "\n\n" + readme[end:]
    README.write_text(new_readme)

    print(f"Updated README: {confirmed}/{total} ISC cases, {len(main_rows)} main + {len(ext_rows)} extended")


if __name__ == "__main__":
    main()
