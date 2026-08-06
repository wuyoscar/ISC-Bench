FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    git curl && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir \
    "openai>=1.0" \
    "openai-agents>=0.2.0" \
    "pydantic>=2.0" \
    "rich>=13.0"

COPY agent.py /agent.py
# Minimal TVD template baked in for image completeness; run.sh mounts a fresh copy.
COPY template/default/prompt.json /template/prompt.json
COPY template/default/validator.py /template/validator.py

WORKDIR /workspace

ENTRYPOINT ["python3", "/agent.py"]
