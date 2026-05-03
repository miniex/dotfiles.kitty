#!/bin/sh
# Format shell scripts (shfmt).
set -e

cd "$(dirname "$0")/.."

if ! command -v shfmt >/dev/null 2>&1; then
    echo "missing required tool: shfmt" >&2
    exit 1
fi

shfmt -w -i 4 -ci -bn -s install.sh tools/format.sh tools/lint.sh
