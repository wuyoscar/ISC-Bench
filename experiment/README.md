# Experiment

Reproduce the ISC evaluation from the paper. The three modes differ in how much context the model gets.

## Three evaluation modes

**TVD-Chatbot** (`K=1, N=−`): One prompt holds the task script, validator, data file, and validation traceback. The LLM answers once.

**TVD-ICL** (`K=1, N=1,5,10,20`): The same single prompt starts with `N` completed examples of the TVD task. This measures how in-context examples change the result.

**TVD-Agentic** (`K=∞, N=−`): The LLM has filesystem access and code execution. It reads project files and fixes validation errors over multiple turns.

## Results

### Table 3. Safety failure rates (%) under TVD across evaluation modes and frontier LLMs

<p align="center">
  <img src="tab3_tvd_results.png" width="100%">
</p>

### Table 4. Comparison with jailbreak baselines on JailbreakBench

<p align="center">
  <img src="tab4_baseline_comparison.png" width="100%">
</p>

## How to run

Each mode has its own README:

| Mode | Directory |
|------|-----------|
| TVD-Chatbot | [`isc_chatbot/`](isc_chatbot/) |
| TVD-ICL | [`isc_icl/`](isc_icl/) |
| TVD-Agentic | [`isc_agent/`](isc_agent/) |
| Automated red teaming (v0) | [`automated-red-teaming/`](automated-red-teaming/) |

You need Python 3.11+, [uv](https://docs.astral.sh/uv/), and `OPENROUTER_API_KEY` in `.env` at the project root. TVD-Agentic also needs Docker. Automated red teaming runs locally via the OpenAI Agents SDK (no Docker in v0).

## Harmful data generator

Five domain notebooks from §3 of the paper. They show TVD-style generation of harmful or policy-violating content under a task-validator-data framing. See [`harmful_data_generator/`](harmful_data_generator/).
