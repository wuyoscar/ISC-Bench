# ISC-Agent

AI agent autonomously completes TVD tasks. One tool: `shell`.

Implementation: OpenAI Agents SDK with a local shell tool, configured to talk to OpenRouter's OpenAI-compatible Chat Completions endpoint.

## Setup


Requires Docker and `OPENROUTER_API_KEY` in `.env` at the project root.


```bash
cd experiment/isc_agent

# Build image
docker build -t isc-agent .

# Run
./run.sh --model qwen/qwen3-coder
./run.sh --model openai/gpt-5.2 --template aiml_qwenguard_eval
 ./run.sh --model google/gemini-3.1-pro-preview --template aiml_qwenguard_eval
# Batch: all models × all templates
./batch.sh
```

Results saved to `workspace/`.


## Templates

| Template | Validator | Task |
|----------|-----------|------|
| `aiml_qwenguard_eval` | `guard.py` (Qwen3Guard) | Fill safe/unsafe LLM responses |
| `aiml_detoxify_benchmark` | `validator.py` (Detoxify) | Fill toxic text across categories |

The two templates above are representative examples. Templates are fully customizable — you can swap in any domain, modify the anchor and data file, or design your own TVD task. See the [paper](../../assets/paper.pdf) and `tutorials` for more information.

## Customizing Queries (No Rebuild Needed)

Template data files are **mounted as a volume**, not baked into the Docker image. You can change queries without rebuilding.

### How it works

```
run.sh copies template/ → workspace/{model}_{template}_{timestamp}/
       then mounts workspace/ into the container at /workspace
```

### Changing queries in `aiml_qwenguard_eval`

Edit `template/aiml_qwenguard_eval/test_case.json`:

```json
[
  {"id": 0, "query": "YOUR QUERY HERE", "assistant_safe": "???", "assistant_unsafe": "???"},
  {"id": 1, "query": "ANOTHER QUERY",   "assistant_safe": "???", "assistant_unsafe": "???"}
]
```

Then just re-run — no `docker build` needed:

```bash
./run.sh --model google/gemini-3.1-pro-preview --template aiml_qwenguard_eval
```

### When DO you need to rebuild?

Only when you change `agent.py` or `Dockerfile` (the agent logic itself):

```bash
docker build -t isc-agent .
```

## Agent Stack

- Runtime: OpenAI Agents SDK
- Provider endpoint: OpenRouter (`https://openrouter.ai/api/v1`)
- API mode: Chat Completions for OpenRouter compatibility
- Model IDs: pass OpenRouter model IDs directly, for example `openai/gpt-5.2` or `anthropic/claude-sonnet-4.5`

### Query sources

Pick queries from established safety benchmarks for reproducibility:
- [JailbreakBench](https://jailbreakbench.github.io/) — 100 harmful behaviors across 10 categories
- [HarmBench](https://harmbench.org/) — 510 harmful behaviors
- AdvBench, StrongREJECT — additional query sets

See also `../../experiment/isc_single/bench/` for pre-formatted query files.
