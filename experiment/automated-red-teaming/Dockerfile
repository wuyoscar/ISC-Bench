FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    git curl && rm -rf /var/lib/apt/lists/*

# Lightweight: only Agents SDK + OpenAI client (target/judge are remote APIs).
RUN pip install --no-cache-dir \
    "openai>=1.0" \
    "openai-agents>=0.2.0" \
    "pydantic>=2.0" \
    "rich>=13.0"

COPY agent.py /agent.py
COPY template/ /template/

WORKDIR /workspace

ENTRYPOINT ["python3", "/agent.py"]
