# TVD ICL

In-context learning evaluation. A multi-turn conversation starts with `N` completed examples, then the target query.

Use [OpenRouter](https://openrouter.ai/models) model IDs. Scripts use [PEP 723](https://peps.python.org/pep-0723/) metadata, so `uv run` installs dependencies. Set `OPENROUTER_API_KEY` in `.env` at the project root.

## Run

```bash
cd experiment/tvd_icl

# Default (JBB queries)
uv run run.py --model <model-id> --demos 5

# Switch benchmark: build first, then run
uv run build.py --bench harmbench
uv run run.py --model <model-id> --bench harmbench --demos 5
```

| Flag | Description |
|------|-------------|
| `--model` | OpenRouter model ID |
| `--demos` | Number of completed demonstrations (1, 5, 10, 20) |
| `--bench` | Benchmark name (`harmbench`, `strongreject`, `advbench`; omit for default JBB) |

**Benchmarks**: `jbb` (100 queries, default), `harmbench` (400), `strongreject` (313), and `advbench` (520). Query data is shared with TVD Chatbot (`../tvd_chatbot/bench/`).

**Output**: `results/{model}/icl_{N}demo.json`

## How it works

Each query becomes a multi-turn conversation:

```
[system]     Agent persona
[user]       Demo query 1 (TVD prompt with ???)
[assistant]  Completed response 1 (actual LLM output from a prior run)
[user]       Demo query 2
[assistant]  Completed response 2
...
[user]       Target query (the one the LLM must answer)
```

The `N` completed pairs show the model earlier task completions. Demo data is stored by model in `data/`. If a model has no demos of its own, the script reuses demos from another available model.

## Extract and judge

Use the same tools as TVD Chatbot:

```bash
cd ../tvd_chatbot
uv run extract.py <result-file>.json
uv run judge.py <result-file>.json
```
