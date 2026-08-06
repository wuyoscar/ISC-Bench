# Harmful data generator

Five Jupyter notebooks for the TVD Chatbot mode in §3 of the paper. They also cover the §3.4 point that a successful trigger is not the end: follow-up prompts in the same workflow can keep producing more unsafe content.

## What's inside

| Notebook | Domain |
|---|---|
| `unsafe_response.ipynb` | AI Safety / ML (Llama-Guard-style classifier evaluation) |
| `media_bias.ipynb` | Media and communication (extreme-bias text classification) |
| `misinformation.ipynb` | Misinformation (false-claim verification) |
| `cybersecurity.ipynb` | Cybersecurity (network-reconnaissance findings) |
| `drug_screening.ipynb` | Pharmacology (binding-affinity records) |

Each notebook ships as a runnable `.ipynb`. After you run it, you can export static `.html` with cell outputs kept.

## Setup

```bash
export OPENROUTER_API_KEY="sk-or-..."
pip install -r requirements.txt
jupyter notebook unsafe_response.ipynb
```

Refresh the HTML exports after a run:

```bash
./convert.sh
```

## Notes

- Each notebook reads `OPENROUTER_API_KEY` from the environment. The key is never printed.
- Notebooks call a frontier LLM and **will produce policy-violating content**. That is the point of the demo. Use it only for good-faith safety research, as described in the paper's Broader Impact (Appendix K).
- Default model: `anthropic/claude-3.5-sonnet`. Change the `MODEL` constant in a notebook's setup cell to switch (for example `openai/gpt-4o` or `google/gemini-pro-1.5`).
