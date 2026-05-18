# Contributing

Every commit and PR must pass `tools/format.sh` and `tools/lint.sh` cleanly.

## Required tools

On `$PATH`: [`shfmt`](https://github.com/mvdan/sh), [`shellcheck`](https://www.shellcheck.net/), [`ruff`](https://github.com/astral-sh/ruff). `brew install shfmt shellcheck ruff` (macOS) / `pacman -S shfmt shellcheck ruff` (Arch).

## Workflow

```bash
./tools/format.sh   # shfmt + ruff format/autofix
./tools/lint.sh     # shfmt --diff + shellcheck + ruff check
```

Smoke-test after touching `kitty.conf`, `themes/*.conf`, or `os/*.conf`:

```bash
sh install.sh
kitty +runpy 'from kitty.config import load_config; load_config("kitty.conf")'
```

## PR expectations

- One concern per PR. Update `README.md` when behavior, keymaps, themes, or OS profiles change.
- Layout: base in `kitty.conf`, colors in `themes/<name>.conf`, OS overrides in `os/<name>.conf` (`os.conf` is gitignored).
- `themes/*.conf` is **colors only** (opacity, fg/bg, borders, `tab_bar_background`).
- `install.sh` stays POSIX (`#!/bin/sh`, no bashisms, survives `curl | sh`).
- No OS-conditional logic in `kitty.conf` — push it into `os/<name>.conf`.

## Comment style

One line, terse, explains the _why_ when it isn't obvious from the code.

- Section dividers: single-line `# Section name`, no ASCII boxes.
- Collapse multi-line explanations to one sentence (em dash for cause/effect).
- Drop comments that restate the code.
- Shell function docs: `$1=…, $2=…`.

## Commit messages

`prefix: description`. Common prefixes: `feat`, `fix`, `refactor`, `perf`, `docs`, `chore`, `tools`. Prefix and first word lowercase. Single-line, imperative, no trailing period.

```
feat: add install.sh with per-OS profile selection
refactor: collapse symbol_map ranges into a PUA catch-all
```
