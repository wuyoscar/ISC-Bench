#!/usr/bin/env bash
# Automated red-teaming runner — Docker + OpenAI Agents SDK + OpenRouter.
#
# Usage:
#   ./run.sh
#   ./run.sh --model x-ai/grok-4.3
#   ./run.sh --model x-ai/grok-4.5 --max-turns 50
#   ./run.sh --target deepseek/deepseek-v4-flash --judge deepseek/deepseek-v4-flash
#   ./run.sh --local   # optional: uv on host instead of Docker
set -euo pipefail

MODEL="${MODEL:-x-ai/grok-4.3}"
TARGET_MODEL="${TARGET_MODEL:-deepseek/deepseek-v4-flash}"
JUDGE_MODEL="${JUDGE_MODEL:-deepseek/deepseek-v4-flash}"
MAX_TURNS=40
THINKING=""
TEMPLATE="default"
USE_LOCAL=0
IMAGE_NAME="isc-art"

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
    --local) USE_LOCAL=1; shift ;;
    *) echo "Unknown arg: $1"; exit 1 ;;
  esac
done

if [[ -f "$ENV_FILE" ]]; then
  set -a
  # shellcheck disable=SC1090
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
echo "Runtime:   $([ "$USE_LOCAL" -eq 1 ] && echo local-uv || echo docker/$IMAGE_NAME)"
echo "============================================"

if [[ "$USE_LOCAL" -eq 1 ]]; then
  uv run "$SCRIPT_DIR/agent.py" \
    --workspace "$TASK_DIR" \
    --model "$MODEL" \
    --max-turns "$MAX_TURNS" \
    ${THINKING}
else
  if ! docker image inspect "$IMAGE_NAME" &>/dev/null; then
    echo "Building $IMAGE_NAME image..."
    docker build -t "$IMAGE_NAME" "$SCRIPT_DIR"
  fi

  docker run --rm \
    --env-file "$ENV_FILE" \
    -e TARGET_MODEL="$TARGET_MODEL" \
    -e JUDGE_MODEL="$JUDGE_MODEL" \
    -e OPENROUTER_BASE_URL="$OPENROUTER_BASE_URL" \
    -v "$TASK_DIR:/workspace" \
    "$IMAGE_NAME" \
    --workspace /workspace \
    --model "$MODEL" \
    --max-turns "$MAX_TURNS" \
    ${THINKING}
fi

# Post-check with ORIGINAL template files (agent cannot cheat by rewriting them).
echo ""
echo "[validate] running original template validator on workspace..."
if [[ "$USE_LOCAL" -eq 1 ]]; then
  (
    cd "$TASK_DIR"
    cp "$TMPL_DIR/validator.py" "$TASK_DIR/validator.py"
    cp "$TMPL_DIR/task.py" "$TASK_DIR/task.py"
    cp "$TMPL_DIR/target_client.py" "$TASK_DIR/target_client.py"
    cp "$TMPL_DIR/judge.py" "$TASK_DIR/judge.py"
    cp "$TMPL_DIR/llm_client.py" "$TASK_DIR/llm_client.py"
    python3 validator.py
  ) && echo "[validate] PASSED" || echo "[validate] FAILED"
else
  # Restore pristine pipeline scripts then re-run inside the same image.
  cp "$TMPL_DIR/validator.py" "$TASK_DIR/validator.py"
  cp "$TMPL_DIR/task.py" "$TASK_DIR/task.py"
  cp "$TMPL_DIR/target_client.py" "$TASK_DIR/target_client.py"
  cp "$TMPL_DIR/judge.py" "$TASK_DIR/judge.py"
  cp "$TMPL_DIR/llm_client.py" "$TASK_DIR/llm_client.py"
  docker run --rm \
    --entrypoint python3 \
    --env-file "$ENV_FILE" \
    -e TARGET_MODEL="$TARGET_MODEL" \
    -e JUDGE_MODEL="$JUDGE_MODEL" \
    -e OPENROUTER_BASE_URL="$OPENROUTER_BASE_URL" \
    -v "$TASK_DIR:/workspace" \
    -w /workspace \
    "$IMAGE_NAME" \
    /workspace/validator.py \
    && echo "[validate] PASSED" \
    || echo "[validate] FAILED"
fi

echo ""
echo "Done. Results: $TASK_DIR"
