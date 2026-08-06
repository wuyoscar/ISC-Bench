#!/bin/bash
# TVD Chatbot Experiment
#
# Usage:
#   ./run.sh --model openai/gpt-5.2
#   ./run.sh --model anthropic/claude-sonnet-4.5 --task ai-guard
#   ./run.sh --model x-ai/grok-4.1-fast --task ai-detoxify --samples 3
#
# Judge results:
#   uv run judge.py result_demo/

set -e
cd "$(dirname "$0")"
uv run run.py "$@"
