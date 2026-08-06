#!/usr/bin/env bash
# Codespace TVD — OpenAI Agents SDK.
# Agent may only edit data.json; repeatedly runs tvd_validator.py.
set -euo pipefail

MODEL="${MODEL:-x-ai/grok-4.5}"
TARGET_MODEL="${TARGET_MODEL:-deepseek/deepseek-v4-flash}"
MAX_TURNS=50
THINKING=""
CODESPACE="default"
USE_LOCAL=0
IMAGE_NAME="isc-art"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
ENV_FILE="$PROJECT_ROOT/.env"
RESULT_ROOT="$SCRIPT_DIR/result"
CS_DIR="$SCRIPT_DIR/codespace/$CODESPACE"

while [[ $# -gt 0 ]]; do
  case $1 in
    --model) MODEL="$2"; shift 2 ;;
    --target) TARGET_MODEL="$2"; shift 2 ;;
    --max-turns) MAX_TURNS="$2"; shift 2 ;;
    --codespace) CODESPACE="$2"; CS_DIR="$SCRIPT_DIR/codespace/$CODESPACE"; shift 2 ;;
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

[[ -n "${OPENROUTER_API_KEY:-}" ]] || { echo "Error: OPENROUTER_API_KEY not set"; exit 1; }
[[ -n "${OPENAI_API_KEY:-}" ]] || { echo "Error: OPENAI_API_KEY not set"; exit 1; }
[[ -d "$CS_DIR" ]] || { echo "Error: codespace not found: $CS_DIR"; exit 1; }

MODEL_SLUG=$(echo "$MODEL" | tr '/:' '__')
TIMESTAMP=$(date -u +%Y%m%d_%H%M%S)
RUN_NAME="${MODEL_SLUG}_${CODESPACE}_${TIMESTAMP}"
TASK_DIR="$SCRIPT_DIR/workspace/${RUN_NAME}"
mkdir -p "$TASK_DIR"

# Three agent-visible files only.
cp "$CS_DIR/data.json" "$TASK_DIR/"
cp "$CS_DIR/task.py" "$TASK_DIR/"
cp "$CS_DIR/tvd_validator.py" "$TASK_DIR/"
# Fixed files: read-only for the agent process.
chmod a-w "$TASK_DIR/task.py" "$TASK_DIR/tvd_validator.py"
chmod u+w "$TASK_DIR/data.json"

export TARGET_MODEL OPENROUTER_API_KEY OPENAI_API_KEY
export OPENROUTER_BASE_URL="${OPENROUTER_BASE_URL:-https://openrouter.ai/api/v1}"

echo "============================================"
echo "Codespace TVD (OpenAI Agents SDK)"
echo "Agent:     $MODEL"
echo "Backend:   $TARGET_MODEL"
echo "Workspace: $TASK_DIR"
echo "Writable:  data.json only"
echo "============================================"

if [[ "$USE_LOCAL" -eq 1 ]]; then
  export PYTHONPATH="$SCRIPT_DIR/gate${PYTHONPATH:+:$PYTHONPATH}"
  uv run "$SCRIPT_DIR/agent.py" --workspace "$TASK_DIR" --model "$MODEL" --max-turns "$MAX_TURNS" ${THINKING}
else
  if ! docker image inspect "$IMAGE_NAME" &>/dev/null; then
    docker build -t "$IMAGE_NAME" "$SCRIPT_DIR"
  fi
  docker run --rm \
    --env-file "$ENV_FILE" \
    -e TARGET_MODEL="$TARGET_MODEL" \
    -e OPENROUTER_BASE_URL="$OPENROUTER_BASE_URL" \
    -e PYTHONPATH=/opt/isc_gate \
    -v "$TASK_DIR:/workspace" \
    "$IMAGE_NAME" \
    --workspace /workspace \
    --model "$MODEL" \
    --max-turns "$MAX_TURNS" \
    ${THINKING}
fi

# Always restore original fixed files before operator re-check.
chmod u+w "$TASK_DIR/task.py" "$TASK_DIR/tvd_validator.py" 2>/dev/null || true
cp "$CS_DIR/task.py" "$TASK_DIR/task.py"
cp "$CS_DIR/tvd_validator.py" "$TASK_DIR/tvd_validator.py"
chmod a-w "$TASK_DIR/task.py" "$TASK_DIR/tvd_validator.py" || true

echo ""
echo "[check] python tvd_validator.py (original task+validator)..."
VALIDATE_OK=0
if [[ "$USE_LOCAL" -eq 1 ]]; then
  (cd "$TASK_DIR" && PYTHONPATH="$SCRIPT_DIR/gate" python3 tvd_validator.py) && VALIDATE_OK=1 || VALIDATE_OK=0
else
  if docker run --rm \
    --entrypoint python3 \
    --env-file "$ENV_FILE" \
    -e TARGET_MODEL="$TARGET_MODEL" \
    -e OPENROUTER_BASE_URL="$OPENROUTER_BASE_URL" \
    -e PYTHONPATH=/opt/isc_gate \
    -v "$TASK_DIR:/workspace" \
    -w /workspace \
    "$IMAGE_NAME" \
    /workspace/tvd_validator.py
  then VALIDATE_OK=1; else VALIDATE_OK=0; fi
fi

if [[ "$VALIDATE_OK" -eq 1 ]]; then
  echo "[check] PASSED"
  PROMOTE_DIR="$RESULT_ROOT/${RUN_NAME}"
  mkdir -p "$PROMOTE_DIR"
  for f in data.json results.json agent_log.json; do
    [[ -f "$TASK_DIR/$f" ]] && cp "$TASK_DIR/$f" "$PROMOTE_DIR/"
  done
  cat > "$PROMOTE_DIR/run_meta.json" <<EOF
{
  "run_name": "$RUN_NAME",
  "agent_model": "$MODEL",
  "backend_model": "$TARGET_MODEL",
  "checks": ["moderation_flagged", "completion_gate"],
  "validated": true
}
EOF
  echo "[result] $PROMOTE_DIR"
else
  echo "[check] FAILED — see $TASK_DIR"
fi
