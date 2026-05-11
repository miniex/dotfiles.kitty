# Contributing

Thanks for sending changes. The bar is small but firm: every commit and PR must pass `tools/format.sh` and `tools/lint.sh` cleanly.

## Required tools

Install on your `$PATH` before working on this repo:

- [`shfmt`](https://github.com/mvdan/sh) — shell script formatter
- [`shellcheck`](https://www.shellcheck.net/) — shell script linter
- [`ruff`](https://github.com/astral-sh/ruff) — Python formatter/linter (for `tab_bar.py`)

Examples:

```bash
# macOS
brew install shfmt shellcheck ruff

# Arch
sudo pacman -S shfmt shellcheck ruff
```

## Workflow

Before every commit:

```bash
./tools/format.sh   # shfmt on shell scripts; ruff format + autofix on tab_bar.py
./tools/lint.sh     # shfmt --diff + shellcheck + ruff format --check + ruff check
```

`lint.sh` exits non-zero on any formatting drift or shellcheck finding. CI / reviewers expect a clean run.

Smoke-test the kitty config end-to-end after touching `kitty.conf` or `os/*.conf`:

```bash
sh install.sh                                                                                 # regenerate os.conf in-place
kitty +runpy 'from kitty.config import load_config; print(load_config("kitty.conf"))'         # confirm it parses
```

## PR expectations

- Keep changes scoped — one concern per PR.
- Update `README.md` when behavior, keymaps, or the OS-profile layout changes.
- Match the existing layout: base settings in `kitty.conf`, OS-specific overrides in `os/<name>.conf`, `os.conf` stays gitignored.
- `install.sh` must remain POSIX-compatible (`#!/bin/sh`, no bashisms) and survive being piped from `curl`.
- Don't add OS-conditional logic to `kitty.conf` directly — push it down into `os/<name>.conf`.

## Commit messages

Follow the prefixes already in `git log`. Shape: `prefix(scope?): description`.

Common prefixes: `feat`, `fix`, `refactor`, `perf`, `docs`, `chore`, `tools`.

Rules:

- **Prefix is always lowercase** — `feat:` not `Feat:`.
- **First word after the prefix is always lowercase** — `fix: handle missing os.conf`, not `fix: Handle missing os.conf`.
- The rest of the description follows no strict case rule, but prefer lowercase. Reserve uppercase for proper nouns, acronyms, or genuine emphasis.

Examples:

```
feat: add install.sh with per-OS profile selection
feat: swap tab movement keybindings to match vim-style navigation
refactor: collapse symbol_map ranges into a PUA catch-all
docs: add README.md
```

Single-line, imperative mood. No trailing period.
