#!/bin/sh
# Format shell (shfmt) + Python (ruff).
set -e

cd "$(dirname "$0")/.."

missing=
for tool in shfmt ruff; do
    if ! command -v "$tool" >/dev/null 2>&1; then
        missing="$missing $tool"
    fi
done

if [ -n "$missing" ]; then
    echo "missing required tool(s):$missing" >&2
    exit 1
fi

shfmt -w -i 4 -ci -bn -s install.sh tools/format.sh tools/lint.sh
ruff format tab_bar.py
ruff check --fix-only tab_bar.py
