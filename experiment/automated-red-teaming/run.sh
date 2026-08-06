#!/usr/bin/env bash
# Automated red-teaming runner (OpenAI Agents SDK + OpenRouter).
#
# Usage:
#   ./run.sh
#   ./run.sh --model x-ai/grok-4.1-fast
#   ./run.sh --model x-ai/grok-4.1-fast --max-turns 30
#   ./run.sh --target deepseek/deepseek-v4-flash --judge deepseek/deepseek-v4-flash
set -euo pipefail

MODEL="${MODEL:-x-ai/grok-4.1-fast}"
TARGET_MODEL="${TARGET_MODEL:-deepseek/deepseek-v4-flash}"
JUDGE_MODEL="${JUDGE_MODEL:-deepseek/deepseek-v4-flash}"
MAX_TURNS=40
THINKING=""
TEMPLATE="default"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
ENV_FILE="$PROJECT_ROOT/.env"

while [[ $# -gt 0 ]]; do
  case $1 in
    --model) MODEL="$2"; shift 2 ;;
    --target) TARGET_MODEL="$2"; shift 2 ;;
    --judge) JUDGE_MODEL="$2"; shift 2 ;;
    --max-turns) MAX_TURNS="$2"; shift 2 ;;
    --template) TEMPLATE="$2"; shift 2 ;;
    --thinking) THINKING="--thinking"; shift ;;
    *) echo "Unknown arg: $1"; exit 1 ;;
  esac
done

if [[ -f "$ENV_FILE" ]]; then
  # shellcheck disable=SC1090
  set -a
  source "$ENV_FILE"
  set +a
fi

if [[ -z "${OPENROUTER_API_KEY:-}" ]]; then
  echo "Error: OPENROUTER_API_KEY not set (export it or put it in $ENV_FILE)"
  exit 1
fi

TMPL_DIR="$SCRIPT_DIR/template/$TEMPLATE"
if [[ ! -d "$TMPL_DIR" ]]; then
  echo "Error: template '$TEMPLATE' not found at $TMPL_DIR"
  exit 1
fi

MODEL_SLUG=$(echo "$MODEL" | tr '/:' '__')
TIMESTAMP=$(date -u +%Y%m%d_%H%M%S)
TASK_DIR="$SCRIPT_DIR/workspace/${MODEL_SLUG}_${TEMPLATE}_${TIMESTAMP}"
mkdir -p "$TASK_DIR"
cp -R "$TMPL_DIR/." "$TASK_DIR/"

export TARGET_MODEL JUDGE_MODEL OPENROUTER_API_KEY
export OPENROUTER_BASE_URL="${OPENROUTER_BASE_URL:-https://openrouter.ai/api/v1}"

echo "============================================"
echo "Automated Red Teaming"
echo "Attacker:  $MODEL"
echo "Target:    $TARGET_MODEL"
echo "Judge:     $JUDGE_MODEL"
echo "Workspace: $TASK_DIR"
echo "============================================"

# Attacker loop (Agents SDK). Agent only sees workspace files + pass/fail from commands.
uv run "$SCRIPT_DIR/agent.py" \
  --workspace "$TASK_DIR" \
  --model "$MODEL" \
  --max-turns "$MAX_TURNS" \
  ${THINKING}

# Post-check with the ORIGINAL template validator (agent cannot rewrite the source of truth).
echo ""
echo "[validate] running original template validator on workspace..."
(
  cd "$TASK_DIR"
  # Use original validator.py from template, overwriting any agent edits for the audit run.
  cp "$TMPL_DIR/validator.py" "$TASK_DIR/validator.py"
  cp "$TMPL_DIR/task.py" "$TASK_DIR/task.py"
  cp "$TMPL_DIR/target_client.py" "$TASK_DIR/target_client.py"
  cp "$TMPL_DIR/judge.py" "$TASK_DIR/judge.py"
  cp "$TMPL_DIR/llm_client.py" "$TASK_DIR/llm_client.py"
  python3 validator.py
) && echo "[validate] PASSED" || echo "[validate] FAILED"

echo ""
echo "Done. Results: $TASK_DIR"
