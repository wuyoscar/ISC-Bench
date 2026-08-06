# TVD Chatbot

Single-turn evaluation. One TVD prompt and one LLM response.

Use [OpenRouter](https://openrouter.ai/models) model IDs. Scripts use [PEP 723](https://peps.python.org/pep-0723/) metadata, so `uv run` installs dependencies. Set `OPENROUTER_API_KEY` in `.env` at the project root.

---

## Case 1: Using Pre-built Prompts

`prompts/jbb/` contains ready-to-run JailbreakBench (JBB) prompts.

### Step 1 — Run

Send prompts to a target LLM. Each query gets one API call.

```bash
uv run run.py --model x-ai/grok-4.1-fast --bench jbb --task ai-guard --samples 0
```

| Flag | Description |
|------|-------------|
| `--model` | OpenRouter model ID |
| `--bench` | Benchmark name (matches folder in `prompts/`) |
| `--task` | `ai-guard`, `ai-detoxify`, or `ai-outlier` |
| `--samples` | Number of few-shot examples (0–5) |

**Output**: `result_demo/{model}/{bench}/{task}/{N}sample.json`

**Shared example output:** One complete reference run is provided so readers can inspect the format end-to-end without rerunning: [input](prompts/jbb/ai-guard/1sample.json) → [output](result_demo/x-ai-grok-4.1-fast/jbb/ai-guard/1sample.json) → [result](result_demo/x-ai-grok-4.1-fast/jbb/ai-guard/1sample_judged.json).

### Step 2 — Extract

LLM responses can contain code blocks, JSON, and explanations. Extract the target content with an LLM. DeepSeek is the default.

```bash
uv run extract.py <result-file>.json
uv run extract.py <result-file>.json --model deepseek/deepseek-chat   # explicit model

# e.g
uv run extract.py result_demo/x-ai-grok-4.1-fast/jbb/ai-guard/1sample.json --model deepseek/deepseek-chat
```

**Result**: Adds `extraction.extracted` to every item in the same file.

### Step 3 — Judge

Score extracted content from 1 to 5. GPT-4o is the default. Only a score of 5 counts as unsafe.

```bash
uv run judge.py <result-file>.json
uv run judge.py <result-file>.json --model openai/gpt-4o   # explicit model

#e.g., 
uv run judge.py result_demo/x-ai-grok-4.1-fast/jbb/ai-guard/1sample.json --model openai/gpt-4o

```

**Output**: `<result-file>_judged.json` with `judge.score` and `judge.reason` per item.

---

## Case 2: Custom Benchmark

To use HarmBench, AdvBench, StrongREJECT, or your own query source, build prompts first.

### Step 1 — Build

Generate TVD prompts from a query set.

```bash
# From included benchmarks
uv run build.py --bench strongreject --task ai-guard --samples 0

# From custom queries (one per line)
uv run build.py --bench mybench --task ai-guard --queries my_queries.txt
```

| `--bench` name | Queries | Source |
|:--------------:|:-------:|--------|
| `jbb` | 100 | [JailbreakBench](https://jailbreakbench.github.io/) |
| `harmbench` | 400 | [HarmBench](https://www.harmbench.org/) |
| `advbench` | 520 | [AdvBench](https://github.com/llm-attacks/llm-attacks) |
| `strongreject` | 313 | [StrongREJECT](https://strong-reject.readthedocs.io/) |

Custom queries can use `.txt` (one per line), `.json` (a list of `{"query": "..."}` objects), or `.csv` (a `query` column).

**Output**: `prompts/{bench}/{task}/{N}sample.json`

> **`build.py` wraps `ai-guard` and `ai-detoxify`; `ai-outlier` is intentionally not wrapped.** The corpus you need is already shipped at `bench/fewshot_corpus.json` (the `safe` field becomes the "normal" cluster against which the LLM-generated outlier is detected — the validator needs ≥5 normals + 1 target sample). But how to assemble that cluster — 5 vs 9 vs 15 normals, single-category vs mixed, etc. — is a design knob we want users to explore. The only outlier prompt we ship is the experimental 5-shot variant we used in the paper, at [`prompts/jbb/ai-outlier/5sample.json`](prompts/jbb/ai-outlier/5sample.json).

### Step 2–4: Run → Extract → Judge

Same as Case 1. Replace `jbb` with your benchmark name:

```bash
uv run run.py --model <model-id> --bench <bench-name> --task ai-guard --samples 0
uv run extract.py <result-file>.json
uv run judge.py <result-file>.json
```

---

## Tasks

| Task | Tool | What LLM generates |
|------|------|--------------------|
| `ai-guard` | Llama-Guard | Safe refusal + unsafe response per query |
| `ai-detoxify` | Detoxify | Non-toxic + toxic text per query |
| `ai-outlier` | PyOD | Anomaly text sample |

## Samples

`--samples N` sets the number of pre-filled safe and unsafe response pairs in the data file. With `N=0`, the file has only the target query and `???` placeholders. With `N>0`, it starts with examples from `bench/fewshot_corpus.json` (65 pairs across 13 harm categories).

The figure shows how **anchors** (pre-filled fields) and **triggers** (validation errors) work in different schemas:

<p align="center">
  <img src="fig_anchor_trigger.png" width="80%">
</p>

---

## FAQ

<details>
<summary><b>Q: How reliable is the extraction step?</b></summary>

**A:** ISC triggers when the model produces a response in Step 1. Extraction uses an LLM to find the target content in code blocks, JSON, and mixed output. Some extraction models can refuse highly sensitive content. Treat LLM extraction as a convenience, not ground truth. For rigorous evaluation, add a rule-based extractor, regex pipeline, or manual review.

</details>

<details>
<summary><b>Q: Why these three templates?</b></summary>

**A:** `ai-guard`, `ai-detoxify`, and `ai-outlier` apply TVD to ML safety tools. Their outputs map to JailbreakBench harm categories, which supports a controlled comparison with jailbreak methods. The repository has 84 templates across nine domains. See [`codebase_templates/`](../../codebase_templates/) for the full set.

</details>

<details>
<summary><b>Q: How can I explore ISC beyond these scripts?</b></summary>

**A:** These scripts provide a reproducible baseline for the paper. ISC is a *structural failure mode*, not a prompt. It appears when task completion requires sensitive data rather than when a user directly asks for it. To study other cases, compose templates, change tools, change anchors, or design a new TVD pattern. See the [paper](https://arxiv.org/abs/2603.23509).

</details>

<details>
<summary><b>Q: Why might my reproduction results be higher than the paper?</b></summary>

**A:** A measure of any harmful output can approach 100% for many frontier LLMs. The paper uses a stricter rule: only a score of 5 on the 1–5 scale counts as unsafe. Scores of 3 or 4 remain harmful, but do not meet this threshold. This explains the difference between any harmful output and the reported safety-failure rate.

</details>

<details>
<summary><b>Q: Does ISC only work with code-based prompts?</b></summary>

**A:** No. These templates use Python, Pydantic, and JSON, but ISC also triggered in LaTeX tables, YAML files, CSV datasets, FASTA sequences, and CIF crystal structures. The code format works well with JailbreakBench evaluation. The same pattern can appear in any structured workflow that requires sensitive data to complete a task.

</details>

---

## File Flow

```
bench/*.json                    Query sources (JBB, HarmBench, etc.)
bench/fewshot_corpus.json       Pre-collected (safe, unsafe) pairs for few-shot
        │
        ▼  build.py
prompts/{bench}/{task}/         Generated TVD prompts
        │
        ▼  run.py
result_demo/{model}/{bench}/{task}/ Raw LLM responses
        │
        ▼  extract.py
        │  (adds extraction.extracted to same file)
        │
        ▼  judge.py
result_demo/.../*_judged.json   Scored results (1-5 per item)
```
