#!/bin/bash
# Batch run: all models × all templates via Docker
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
ENV_FILE="$PROJECT_ROOT/.env"

if [ ! -f "$ENV_FILE" ]; then
    echo "Error: $ENV_FILE not found"
    exit 1
fi

# Build image if needed
if ! docker image inspect tvd-agent &>/dev/null; then
    echo "Building tvd-agent image..."
    docker build -t tvd-agent "$SCRIPT_DIR"
fi

MODELS=(
    "qwen/qwen3-coder"
    "minimax/minimax-m2.5"
    "z-ai/glm-5"
    "x-ai/grok-4.1-fast"
)

TEMPLATES=(
    "aiml_detoxify_type1"
    "aiml_detoxify_type2"
    "aiml_detoxify_type3"
    "aiml_fake_news_type1"
    "aiml_fake_news_type2"
    "aiml_fake_news_type3"
    "aiml_guard_type1"
    "aiml_guard_type2"
    "aiml_guard_type3"
    "my_favorite"
)

for model in "${MODELS[@]}"; do
    for tmpl in "${TEMPLATES[@]}"; do
        MODEL_SLUG=$(echo "$model" | tr '/' '_')
        TIMESTAMP=$(date -u +%Y%m%d_%H%M%S)
        TASK_DIR="$SCRIPT_DIR/workspace/${MODEL_SLUG}_${tmpl}_${TIMESTAMP}"

        mkdir -p "$TASK_DIR"
        cp -r "$SCRIPT_DIR/template/$tmpl/"* "$TASK_DIR/"

        echo ""
        echo "============================================"
        echo "Model:    $model"
        echo "Template: $tmpl"
        echo "============================================"

        docker run --rm \
            --env-file "$ENV_FILE" \
            -v "$TASK_DIR:/workspace" \
            tvd-agent \
            --model "$model" \
            --max-turns 50 || echo "[WARN] $model × $tmpl failed"
    done
done

echo ""
echo "============================================"
echo "All done. Results saved to workspace/"
echo "============================================"
