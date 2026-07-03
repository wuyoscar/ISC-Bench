#!/bin/bash
# ISC-Bench Agent Runner
# Usage:
#   ./run.sh                                              # all templates, default model
#   ./run.sh --model openai/gpt-5.2                       # all templates, specific model
#   ./run.sh --template aiml_guard_type1                       # one template
#   ./run.sh --template aiml_guard_type1 --model qwen/qwen3-coder
set -e

MODEL="${MODEL:-qwen/qwen3-coder}"
TEMPLATE=""
MAX_TURNS=50
THINKING=""
PROVIDER="openrouter"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
ENV_FILE="$PROJECT_ROOT/.env"

# Parse args
while [[ $# -gt 0 ]]; do
    case $1 in
        --model) MODEL="$2"; shift 2 ;;
        --template) TEMPLATE="$2"; shift 2 ;;
        --max-turns) MAX_TURNS="$2"; shift 2 ;;
        --thinking) THINKING="--thinking"; shift ;;
        --provider) PROVIDER="$2"; shift 2 ;;
        *) echo "Unknown arg: $1"; exit 1 ;;
    esac
done

# Check env
if [ ! -f "$ENV_FILE" ]; then
    echo "Error: $ENV_FILE not found. Copy .env.example and add your API key."
    exit 1
fi

# Build image if needed
if ! docker image inspect isc-agent &>/dev/null; then
    echo "Building isc-agent image..."
    docker build -t isc-agent "$SCRIPT_DIR"
fi

# Determine which templates to run
if [ -n "$TEMPLATE" ]; then
    TEMPLATES=("$TEMPLATE")
else
    TEMPLATES=()
    for dir in "$SCRIPT_DIR"/template/*/; do
        TEMPLATES+=("$(basename "$dir")")
    done
fi

MODEL_SLUG=$(echo "$MODEL" | tr '/' '_')

echo "============================================"
echo "ISC-Bench Agent Runner"
echo "Model:     $MODEL"
echo "Templates: ${TEMPLATES[*]}"
echo "============================================"

for tmpl in "${TEMPLATES[@]}"; do
    TMPL_DIR="$SCRIPT_DIR/template/$tmpl"
    if [ ! -d "$TMPL_DIR" ]; then
        echo "Error: template '$tmpl' not found"
        exit 1
    fi

    # Each run: workspace/{model}_{template}_{timestamp}/
    TIMESTAMP=$(date -u +%Y%m%d_%H%M%S)
    TASK_DIR="$SCRIPT_DIR/workspace/${MODEL_SLUG}_${tmpl}_${TIMESTAMP}"
    mkdir -p "$TASK_DIR"
    cp -r "$TMPL_DIR/"* "$TASK_DIR/"

    echo ""
    echo "--- Running: $tmpl ---"

    docker run --rm \
        --env-file "$ENV_FILE" \
        -v "$TASK_DIR:/workspace" \
        isc-agent \
        --model "$MODEL" \
        ${THINKING} \
        --provider "$PROVIDER" \
        --max-turns "$MAX_TURNS"

    # ── Post-agent validation ──────────────────────────────────────────
    # Run the ORIGINAL validator from the template dir (read-only mount)
    # so the agent cannot cheat by overwriting it inside the workspace.
    VALIDATOR=$(find "$TMPL_DIR" -maxdepth 1 -name "*.py" | grep -v "test_" | head -1)
    if [ -n "$VALIDATOR" ]; then
        echo "  [validate] running original $(basename $VALIDATOR) on workspace..."
        # Create HF model cache volume on first use to avoid re-downloading
        docker volume create hf-cache &>/dev/null || true
        docker run --rm \
            --entrypoint python3 \
            --env-file "$ENV_FILE" \
            -v "$TASK_DIR:/workspace" \
            -v "$VALIDATOR:/validator.py:ro" \
            -v "hf-cache:/root/.cache/huggingface" \
            -w /workspace \
            isc-agent \
            /validator.py \
            && echo "  [validate] PASSED" \
            || echo "  [validate] FAILED (content did not pass validator)"
    fi

    echo "--- Done: $tmpl ---"
done

echo ""
echo "============================================"
echo "Done. Results saved to workspace/"
echo "============================================"
