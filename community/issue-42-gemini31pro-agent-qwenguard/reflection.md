# Reflection

I first tried a simpler single-mode attack by directly copy-pasting the usual content patterns we often use. On Gemini 3.1 Pro Preview, that route was not especially reliable. The model did not fall as cleanly or as consistently as expected.

I then switched to agent mode. Once the model was given a shell tool and a standard TVD-style workspace with a validator and placeholder JSON, the compromise was immediate. It inspected the files, inferred the task, generated all missing `assistant_safe` and `assistant_unsafe` fields, wrote the updated JSON, and ran the validator successfully.

During this process, it also became clear that the previous hand-rolled agent loop was not ideal. I replaced the old implementation with an OpenAI Agents SDK-based runtime configured for OpenRouter compatibility. That made the agent architecture cleaner and more stable for repeated runs, while preserving the same task structure and model IDs routed through OpenRouter.

The main lesson from this case is that Gemini 3.1 Pro Preview appeared materially more vulnerable under agentic execution than under the simpler single-turn setup. The agent loop did not need any sophisticated optimization; ordinary autonomy over files and execution was enough.
