#!/bin/sh
# Lint shell (shfmt --diff + shellcheck) + Python (ruff). All tools must be on PATH.
set -e

cd "$(dirname "$0")/.."

missing=
for tool in shfmt shellcheck ruff; do
    if ! command -v "$tool" >/dev/null 2>&1; then
        missing="$missing $tool"
    fi
done

if [ -n "$missing" ]; then
    echo "missing required tool(s):$missing" >&2
    echo "install via your package manager (brew/apt/cargo/etc.)" >&2
    exit 1
fi

shfmt -d -i 4 -ci -bn -s install.sh tools/format.sh tools/lint.sh
shellcheck install.sh tools/format.sh tools/lint.sh
ruff format --check tab_bar.py tools/gen_logo.py
ruff check tab_bar.py tools/gen_logo.py
