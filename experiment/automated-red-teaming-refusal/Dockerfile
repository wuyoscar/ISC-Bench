FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    git curl && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir \
    "openai>=1.0" \
    "openai-agents>=0.2.0" \
    "pydantic>=2.0" \
    "rich>=13.0"

# Hidden gate — not under /workspace
COPY gate/completion_gate.py /opt/isc_gate/completion_gate.py
ENV PYTHONPATH=/opt/isc_gate

COPY agent.py /agent.py

WORKDIR /workspace
ENTRYPOINT ["python3", "/agent.py"]
