#!/usr/bin/env bash
# Dual-channel sample gate (TVD) via OpenAI Agents SDK in Docker.
#
# Agent fills samples.json. check.py requires:
#   A) OpenAI Moderation flagged (filter match)
#   B) backend completion is not a short decline template
#
# Usage:
#   ./run.sh
#   ./run.sh --model x-ai/grok-4.5 --max-turns 50
set -euo pipefail

MODEL="${MODEL:-x-ai/grok-4.5}"
TARGET_MODEL="${TARGET_MODEL:-deepseek/deepseek-v4-flash}"
MAX_TURNS=50
THINKING=""
TEMPLATE="default"
USE_LOCAL=0
IMAGE_NAME="isc-art"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
ENV_FILE="$PROJECT_ROOT/.env"
RESULT_ROOT="$SCRIPT_DIR/result"

while [[ $# -gt 0 ]]; do
  case $1 in
    --model) MODEL="$2"; shift 2 ;;
    --target) TARGET_MODEL="$2"; shift 2 ;;
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
  echo "Error: OPENROUTER_API_KEY not set"; exit 1
fi
if [[ -z "${OPENAI_API_KEY:-}" ]]; then
  echo "Error: OPENAI_API_KEY not set"; exit 1
fi

TMPL_DIR="$SCRIPT_DIR/template/$TEMPLATE"
[[ -d "$TMPL_DIR" ]] || { echo "Error: template missing"; exit 1; }

MODEL_SLUG=$(echo "$MODEL" | tr '/:' '__')
TIMESTAMP=$(date -u +%Y%m%d_%H%M%S)
RUN_NAME="${MODEL_SLUG}_${TEMPLATE}_${TIMESTAMP}"
TASK_DIR="$SCRIPT_DIR/workspace/${RUN_NAME}"
mkdir -p "$TASK_DIR"
cp "$TMPL_DIR/samples.json" "$TASK_DIR/"
cp "$TMPL_DIR/check.py" "$TASK_DIR/"

export TARGET_MODEL OPENROUTER_API_KEY OPENAI_API_KEY
export OPENROUTER_BASE_URL="${OPENROUTER_BASE_URL:-https://openrouter.ai/api/v1}"

echo "============================================"
echo "Sample dual-channel gate (Agents SDK)"
echo "Agent model: $MODEL"
echo "Backend:     $TARGET_MODEL"
echo "Workspace:   $TASK_DIR"
echo "============================================"

if [[ "$USE_LOCAL" -eq 1 ]]; then
  uv run "$SCRIPT_DIR/agent.py" --workspace "$TASK_DIR" --model "$MODEL" --max-turns "$MAX_TURNS" ${THINKING}
else
  if ! docker image inspect "$IMAGE_NAME" &>/dev/null; then
    docker build -t "$IMAGE_NAME" "$SCRIPT_DIR"
  fi
  docker run --rm \
    --env-file "$ENV_FILE" \
    -e TARGET_MODEL="$TARGET_MODEL" \
    -e OPENROUTER_BASE_URL="$OPENROUTER_BASE_URL" \
    -v "$TASK_DIR:/workspace" \
    "$IMAGE_NAME" \
    --workspace /workspace \
    --model "$MODEL" \
    --max-turns "$MAX_TURNS" \
    ${THINKING}
fi

echo ""
echo "[check] re-run original check.py ..."
cp "$TMPL_DIR/check.py" "$TASK_DIR/check.py"

VALIDATE_OK=0
if [[ "$USE_LOCAL" -eq 1 ]]; then
  (cd "$TASK_DIR" && python3 check.py) && VALIDATE_OK=1 || VALIDATE_OK=0
else
  if docker run --rm \
    --entrypoint python3 \
    --env-file "$ENV_FILE" \
    -e TARGET_MODEL="$TARGET_MODEL" \
    -e OPENROUTER_BASE_URL="$OPENROUTER_BASE_URL" \
    -v "$TASK_DIR:/workspace" \
    -w /workspace \
    "$IMAGE_NAME" \
    /workspace/check.py
  then VALIDATE_OK=1; else VALIDATE_OK=0; fi
fi

if [[ "$VALIDATE_OK" -eq 1 ]]; then
  echo "[check] PASSED"
  PROMOTE_DIR="$RESULT_ROOT/${RUN_NAME}"
  mkdir -p "$PROMOTE_DIR"
  for f in samples.json results.json agent_log.json; do
    [[ -f "$TASK_DIR/$f" ]] && cp "$TASK_DIR/$f" "$PROMOTE_DIR/"
  done
  cat > "$PROMOTE_DIR/run_meta.json" <<EOF
{
  "run_name": "$RUN_NAME",
  "agent_model": "$MODEL",
  "backend_model": "$TARGET_MODEL",
  "checks": ["moderation_flagged", "backend_non_decline"],
  "validated": true
}
EOF
  echo "[result] $PROMOTE_DIR"
else
  echo "[check] FAILED — see $TASK_DIR"
fi
