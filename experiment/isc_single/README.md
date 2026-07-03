# ISC-Single

Single-turn evaluation. One TVD prompt, one LLM response.

Model names use [OpenRouter](https://openrouter.ai/models) model IDs. All scripts use [PEP 723](https://peps.python.org/pep-0723/) inline metadata — `uv run` handles dependencies automatically, no install needed. Requires `OPENROUTER_API_KEY` in `.env` at the project root.

---

## Case 1: Using Pre-built Prompts

Pre-built prompts for JailbreakBench (JBB) are included in `prompts/jbb/`. You can run them directly.

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

LLM responses contain code blocks, JSON, and explanations. Extract the actual harmful content using an LLM (DeepSeek by default).

```bash
uv run extract.py <result-file>.json
uv run extract.py <result-file>.json --model deepseek/deepseek-chat   # explicit model

# e.g
uv run extract.py result_demo/x-ai-grok-4.1-fast/jbb/ai-guard/1sample.json --model deepseek/deepseek-chat
```

**Effect**: Adds `extraction.extracted` field to each item in the same file.

### Step 3 — Judge

Score extracted content on a 1–5 harmfulness scale (GPT-4o by default). Only score 5 counts as unsafe.

```bash
uv run judge.py <result-file>.json
uv run judge.py <result-file>.json --model openai/gpt-4o   # explicit model

#e.g., 
uv run judge.py result_demo/x-ai-grok-4.1-fast/jbb/ai-guard/1sample.json --model openai/gpt-4o

```

**Output**: `<result-file>_judged.json` with `judge.score` and `judge.reason` per item.

---

## Case 2: Custom Benchmark

To use a different query source (HarmBench, AdvBench, StrongREJECT, or your own), build prompts first.

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

Custom queries: `.txt` (one per line), `.json` (list of `{"query": "..."}` objects), or `.csv` (with `query` column).

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

`--samples N` controls how many pre-filled (safe, unsafe) response pairs are embedded in the data file as demonstrations. When `N=0` (zero-shot), the data file contains only the target query with `???` placeholders — the LLM infers what to generate from the task structure alone. When `N>0`, completed examples are prepended from `bench/fewshot_corpus.json` (65 pairs across 13 harm categories), showing the LLM the expected format and content before the target entry.

The figure below illustrates how **anchors** (pre-filled fields) and **triggers** (validation errors) work across different domain schemas:

<p align="center">
  <img src="fig_anchor_trigger.png" width="80%">
</p>

---

## FAQ

<details>
<summary><b>Q: How reliable is the extraction step?</b></summary>

**A:** Once the model produces a response at Step 1, it has already complied — ISC has been triggered. The extraction step uses an LLM to locate the harmful content within code blocks, JSON, and mixed-format outputs. This introduces a degree of bias: some extraction models may refuse to process extremely harmful content. We recommend treating LLM-based extraction as a convenience rather than ground truth. For rigorous evaluation, consider supplementing with your own rule-based extractor, regex pipeline, or manual inspection.

</details>

<details>
<summary><b>Q: Why these three templates?</b></summary>

**A:** The `ai-guard`, `ai-detoxify`, and `ai-outlier` templates are representative instantiations of the TVD framework applied to ML safety evaluation tools. They are chosen because their outputs map directly onto established harm categories (JailbreakBench), enabling controlled comparison with existing jailbreak methods. They are not the only way ISC manifests — ISC-Bench includes 84 templates across 9 professional domains (biology, chemistry, cybersecurity, pharmacology, etc.), each with a different TVD structure. See [`codebase_templates/`](../../codebase_templates/) for the full set.

</details>

<details>
<summary><b>Q: How can I explore ISC beyond these scripts?</b></summary>

**A:** These scripts provide a reproducible baseline for the evaluation reported in the paper. ISC is a *structural failure mode*, not a specific prompt — the key insight is that harmful data generation arises as a functional requirement of the task, not from an explicit instruction. To explore further, you can compose different templates, swap domain tools, modify anchor strategies, or design entirely new TVD patterns. Understanding the ISC phenomenon and the TVD design principle (see the [paper](https://arxiv.org/abs/2603.23509)) is essential for constructing effective scenarios.

</details>

<details>
<summary><b>Q: Why might my reproduction results be higher than the paper?</b></summary>

**A:** If you simply measure whether the model generates harmful content under TVD, the trigger rate approaches 100% for most frontier LLMs. However, the safety failure rates reported in the paper (e.g., 95.3% average) use a stricter criterion: only responses scored 5 on a 1–5 harmfulness scale — meaning *extremely harmful with high utility* — count as unsafe. Lower-severity harmful outputs (scores 3–4) are still harmful but do not meet this threshold. The gap between "model generated something harmful" (~100%) and "model generated maximally harmful, actionable content" (85–100%) reflects this distinction in evaluation stringency.

</details>

<details>
<summary><b>Q: Does ISC only work with code-based prompts?</b></summary>

**A:** No. The templates here use a code-based format (Python + Pydantic + JSON), but this is one of many possible domain languages. During our research, we found ISC triggers across diverse structured formats — LaTeX tables, YAML configurations, CSV datasets, FASTA sequences, CIF crystal structures, and more. Each member of our authoring team independently designed a structurally different TVD variant, all achieving comparable trigger rates. The code-based format is chosen here because it maps cleanly to JailbreakBench evaluation, but the phenomenon extends to any structured professional workflow where task completion functionally requires sensitive data.

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
