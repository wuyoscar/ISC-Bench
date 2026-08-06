FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    git curl && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir \
    "openai>=1.0" \
    "openai-agents>=0.2.0" \
    "pydantic>=2.0" \
    "rich>=13.0"

COPY agent.py /agent.py
COPY template/default/samples.json /template/samples.json
COPY template/default/check.py /template/check.py

WORKDIR /workspace
ENTRYPOINT ["python3", "/agent.py"]
