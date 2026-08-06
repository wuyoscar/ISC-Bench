FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    git curl && rm -rf /var/lib/apt/lists/*

# Agent + validator stack. Torch CPU for hidden Qwen3Guard gate.
RUN pip install --no-cache-dir \
    "openai>=1.0" \
    "openai-agents>=0.2.0" \
    "pydantic>=2.0" \
    "rich>=13.0" \
    "transformers>=4.45" \
    "accelerate>=0.33" \
    "sentencepiece" \
    "protobuf"

RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

# Hidden gate — not under /workspace
COPY gate/completion_gate.py /opt/isc_gate/completion_gate.py
ENV PYTHONPATH=/opt/isc_gate
ENV HF_HOME=/root/.cache/huggingface
ENV TRANSFORMERS_CACHE=/root/.cache/huggingface/hub
ENV QWEN_GUARD_MODEL=Qwen/Qwen3Guard-Gen-0.6B

COPY agent.py /agent.py

WORKDIR /workspace
ENTRYPOINT ["python3", "/agent.py"]
