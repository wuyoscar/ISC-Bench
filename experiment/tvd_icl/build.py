#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
Rebuild ICL experiment data with a different benchmark.

Takes existing ICL demo data (which contains pre-filled demonstrations)
and swaps the target query (last item, assistant_safe/unsafe = ???)
with queries from a different benchmark dataset.

Usage:
    uv run build.py --bench harmbench
    uv run build.py --bench strongreject
    uv run build.py --bench advbench
    uv run build.py --bench jbb          # (default, already built)

The demo context (messages[0:-1] and filler items in the JSON) stays
identical — only the final query is replaced.
"""
import json
import re
import sys
from pathlib import Path

BENCH_DIR = Path(__file__).parent.parent / "tvd_chatbot" / "bench"
DATA_DIR = Path(__file__).parent / "data"
OUT_DIR = Path(__file__).parent / "data"


def load_bench(name: str) -> list[dict]:
    """Load benchmark queries: list of {query, category}."""
    path = BENCH_DIR / f"{name}.json"
    if not path.exists():
        available = [f.stem for f in BENCH_DIR.glob("*.json")]
        print(f"Bench '{name}' not found. Available: {available}")
        sys.exit(1)
    return json.loads(path.read_text())


def replace_target_query(last_msg_content: str, new_query: str) -> str:
    """Replace the target query (last JSON item with ???) in the last user message."""
    match = re.search(r'```json\s*\n(.*?)\n```', last_msg_content, re.DOTALL)
    if not match:
        raise ValueError("No JSON block found in last message")

    items = json.loads(match.group(1))
    # Target is the last item (assistant_safe/unsafe == ???)
    target = items[-1]
    assert target["assistant_safe"] == "???", f"Expected ??? in last item, got {target['assistant_safe']}"
    target["query"] = new_query

    new_json = json.dumps(items, indent=2, ensure_ascii=False)
    return last_msg_content[:match.start(1)] + new_json + last_msg_content[match.end(1):]


def rebuild(bench_name: str) -> None:
    bench_queries = load_bench(bench_name)
    model_dirs = [d for d in DATA_DIR.iterdir() if d.is_dir()]

    if not model_dirs:
        print("No model directories found in data/")
        sys.exit(1)

    for model_dir in sorted(model_dirs):
        for demo_file in sorted(model_dir.glob("demo*.json")):
            data = json.loads(demo_file.read_text())
            config, results = data["config"], data["results"]

            new_results = []
            for i, query_item in enumerate(bench_queries):
                if i >= len(results):
                    # Use the last result as template if bench has more queries
                    template = results[-1]
                else:
                    template = results[i]

                new_item = {
                    "id": i,
                    "index": i,
                    "query": query_item["query"],
                    "category": query_item.get("category", ""),
                    "n_demos": template["n_demos"],
                    "demo_indices": template["demo_indices"],
                    "messages": [*template["messages"][:-1]],  # keep demos
                }
                # Replace query in last message
                last_msg = dict(template["messages"][-1])
                last_msg["content"] = replace_target_query(
                    last_msg["content"], query_item["query"]
                )
                new_item["messages"].append(last_msg)
                new_results.append(new_item)

            # Save to bench-specific subdirectory
            out_dir = OUT_DIR / f"{bench_name}" / model_dir.name
            out_dir.mkdir(parents=True, exist_ok=True)
            out_file = out_dir / demo_file.name

            new_config = {**config, "bench": bench_name, "n_queries": len(new_results)}
            out_file.write_text(json.dumps(
                {"config": new_config, "results": new_results},
                indent=2, ensure_ascii=False,
            ))
            print(f"  {out_file.relative_to(OUT_DIR)} ({len(new_results)} queries)")

    print(f"\nDone. Built {bench_name} ICL data for {len(model_dirs)} models.")


def main() -> None:
    import argparse
    parser = argparse.ArgumentParser(description="Rebuild ICL data with a different benchmark")
    parser.add_argument("-b", "--bench", required=True,
                        help="Benchmark name (jbb, harmbench, strongreject, advbench)")
    args = parser.parse_args()
    rebuild(args.bench)


if __name__ == "__main__":
    main()
