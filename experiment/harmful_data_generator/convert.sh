#!/usr/bin/env bash
# Re-run after executing notebooks to refresh HTML exports with the latest cell outputs.
set -e
cd "$(dirname "$0")"
for f in *.ipynb; do
    uv run --with nbconvert --with jupyter --with ipykernel \
        python -m nbconvert --to html "$f"
done
