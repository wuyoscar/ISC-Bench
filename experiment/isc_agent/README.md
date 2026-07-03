# ISC Agent

Run executable ISC templates with a local shell-enabled agent.

Implementation: OpenAI Agents SDK with a local shell tool, configured to talk to OpenRouter's OpenAI-compatible Chat Completions endpoint.

## Setup

Requires Docker and `OPENROUTER_API_KEY` in `.env` at the project root.

```bash
cd experiment/isc_agent

# Build image (one-time)
docker build -t isc-agent .

# Run a single template
./run.sh --model qwen/qwen3-coder --template aiml_detoxify_type1
./run.sh --model qwen/qwen3-coder --template aiml_detoxify_type2
./run.sh --model qwen/qwen3-coder --template aiml_detoxify_type3
./run.sh --model qwen/qwen3-coder --template aiml_fake_news_type1
./run.sh --model qwen/qwen3-coder --template aiml_guard_type1

# Run all templates against one model
./run.sh --model openai/gpt-5.2

# Batch: all configured models × all configured templates
./batch.sh
```

Results saved to `workspace/{model}_{template}_{timestamp}/`.

## Templates

Template variants are flat runnable directories under `template/`. Do not nest
`type1`, `type2`, or `type3` inside a template folder, because `run.sh` copies
`template/{name}/` directly into the Docker workspace.

For each template family, use this convention:

- `*_type1` — no `query`; untargeted generation.
- `*_type2` — has `query`; targeted generation.
- `*_type3` — has `query` plus `reins`; targeted generation with quality/style constraints and few-shot guidance.

| Template | Validator | Shape | Model Download |
|----------|-----------|------|:-:|
| `aiml_detoxify_type1` | Detoxify classifier | Type 1: untargeted generation, no query | ~500MB |
| `aiml_detoxify_type2` | Detoxify classifier | Type 2: targeted generation with query | ~500MB |
| `aiml_detoxify_type3` | Detoxify classifier | Type 3: targeted generation with query, reins, and few-shot guidance | ~500MB |
| `aiml_fake_news_type1` | Fake news detector | Type 1: untargeted article generation, no query | ~300MB |
| `aiml_fake_news_type2` | Fake news detector | Type 2: targeted article generation with query | ~300MB |
| `aiml_fake_news_type3` | Fake news detector | Type 3: targeted article generation with query, reins, and few-shot guidance | ~300MB |
| `aiml_guard_type1` | Qwen3Guard-Gen-0.6B | Type 1: guard validation, zero-shot | ~16GB |
| `aiml_guard_type2` | Qwen3Guard-Gen-0.6B | Type 2: guard validation with examples | ~16GB |
| `aiml_guard_type3` | OpenAI Moderation API | Type 3: moderation validation with reins | None |

For a quick smoke test, start with a template that does not require a large
model download, such as `aiml_guard_type3`.

## How It Works

```
1. run.sh copies template/{name}/ → workspace/{model}_{name}_{timestamp}/
2. Docker mounts workspace/ at /workspace
3. Agent receives a workspace-local task instruction.
4. Agent updates the template data files and runs the local validator.
5. Results: agent_log.json + filled data files in workspace/
```

## Adding Your Own Codebase Templates

Each agent codebase template is a self-contained directory with:

```
template/your_template/
├── validator.py        # Runnable Python script — exits 0 on success, 1 on failure
├── data_file.json      # Data with ??? placeholders
└── (optional) test_validator.py  # pytest-style additional checks
```

**To adapt another template:**

1. Create `validator.py` — the script that loads the data file and validates it.
2. Create the data file (JSON/YAML/CSV) with `???` placeholders.
3. Add an optional `test_validator.py` for pytest checks.
4. Place both in `template/{name}/`
5. Test: `./run.sh --model qwen/qwen3-coder --template {name}`

Templates are executable code, not prompt-only examples. The validator must run
inside the Docker container.

## Customizing Queries (No Rebuild Needed)

Codebase template data files are **mounted as a volume**, not baked into the Docker image. You can change queries without rebuilding.

Edit the data file in `template/{name}/`, then re-run — no `docker build` needed:

```bash
./run.sh --model google/gemini-2.5-flash --template aiml_guard_type1
```

Only rebuild when you change `agent.py` or `Dockerfile`:

```bash
docker build -t isc-agent .
```

## Docker Environment

The Docker container provides:
- Python 3.11 + pip
- Common ML libraries (transformers, torch, detoxify, etc.)
- Shell access for the agent
- Network access for OpenRouter API calls + HuggingFace model downloads

**First run per codebase template may be slow** — the agent downloads the validator's HuggingFace model inside the container. Subsequent runs reuse the cached model if the container layer persists.

## Agent Stack

- Runtime: OpenAI Agents SDK
- Provider endpoint: OpenRouter (`https://openrouter.ai/api/v1`)
- API mode: Chat Completions for OpenRouter compatibility
- Model IDs: pass OpenRouter model IDs directly, for example `openai/gpt-5.2` or `anthropic/claude-sonnet-4.5`
