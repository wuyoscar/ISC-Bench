#!/bin/bash
# ISC In-Context Learning Experiment
#
# Usage:
#   ./run.sh --model openai/gpt-5.2
#   ./run.sh --model openai/gpt-5.2 --demos 5
#   ./run.sh --model anthropic/claude-sonnet-4.5 --demos 10

set -e
cd "$(dirname "$0")"
uv run run.py "$@"
