# Experiment

Reproduce the ISC evaluation from the paper. The three modes differ in how much context the model gets.

## Three evaluation modes

**TVD Chatbot** (`K=1, N=−`): One prompt holds the task script, validator, data file, and validation traceback. The LLM answers once.

**TVD ICL** (`K=1, N=1,5,10,20`): The same single prompt starts with `N` completed examples of the TVD task. This measures how in-context examples change the result.

**TVD Agent** (`K=∞, N=−`): The LLM has filesystem access and code execution. It reads project files and fixes validation errors over multiple turns.

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
| TVD Chatbot | [`tvd_chatbot/`](tvd_chatbot/) |
| TVD ICL | [`tvd_icl/`](tvd_icl/) |
| TVD Agent | [`tvd_agent/`](tvd_agent/) |
| Automated red teaming (refusal gate) | [`automated-red-teaming-refusal/`](automated-red-teaming-refusal/) |
| Automated red teaming + Qwen3Guard | [`automated-red-teaming-qwen-guard/`](automated-red-teaming-qwen-guard/) |

You need Python 3.11+, [uv](https://docs.astral.sh/uv/), and `OPENROUTER_API_KEY` in `.env` at the project root. **TVD Agent** and **automated red teaming** both use Docker by default.

## Harmful data generator

Five domain notebooks from §3 of the paper. They show TVD-style generation of harmful or policy-violating content under a task-validator-data framing. See [`harmful_data_generator/`](harmful_data_generator/).
