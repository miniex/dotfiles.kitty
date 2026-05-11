# Kitty Terminal Configuration

A minimal Kitty terminal emulator configuration with Nerd Font integration and semi-transparent dark theme.

## Features

- **D2Coding** - Korean-friendly monospace font
- **Nerd Font Icons** - All Nerd Font glyph families via PUA catch-all to Symbols Nerd Font Mono (Powerline, FA, MDI incl. supplementary-plane block at `U+F0001+`, Devicons, Codicons, etc.)
- **Semi-transparent** - 85% opacity dark theme
- **Clipboard Integration** - Full read/write clipboard support
- **Kawaii Tab Bar** - Custom Python tab renderer (`tab_bar.py`):
  - Cell-level gradient `#98ABCC` → `#E890B0` across the whole bar. Tab N owns the slice `(N-1)/total → N/total` so tabs are content-sized with no color step at boundaries.
  - Rounded Powerline-Extra caps (`` / ``) only on the first tab's left and last tab's right.
  - Per-tab decoration: layout glyph (`▌▐▦═║◫▣`), `✿` (swaps to `‼` on `needs_attention`), title, `❥` (swaps to superscript digit when `num_window_groups > 1`).
  - Tab switch fades title fg muted ↔ white over 300 ms (smoothstep). Bold persists through fade-out so weight doesn't snap.
  - `kitty.conf` re-pins `U+E0A0–U+E0D4` to Symbols Nerd Font Mono so D2Coding's rectangular Powerline placeholders don't win for the caps.

## Configuration

| Setting              | Value                            |
|----------------------|----------------------------------|
| Font                 | D2Coding                         |
| Font Size            | from [OS profile](#os-profiles)  |
| Cursor               | Block                            |
| Background           | `#1e1e1e` (85% opacity)          |
| Foreground           | `#ffffff`                        |
| Window Border        | `#E890B0`                        |
| Window Padding       | 2px                              |
| Tab Bar Style        | `custom` (see `tab_bar.py`)      |
| Tab Bar Gradient     | `#98ABCC` → `#E890B0`            |
| Tab Bar Edge         | bottom                           |

OS-specific settings (font size, window decorations, etc.) live in
`os/linux.conf` and `os/macos.conf`. The active profile is selected by
`install.sh`, which writes a one-line `os.conf` that `kitty.conf`
loads via `globinclude`.

## OS Profiles

| File              | Settings                                                           |
|-------------------|--------------------------------------------------------------------|
| `os/linux.conf`   | `font_size 12.0`                                                   |
| `os/macos.conf`   | `font_size 18.0`, `hide_window_decorations titlebar-only`, `map ctrl+shift+z toggle_maximized` |

Switch profiles anytime by re-running `sh ~/.config/kitty/install.sh`,
or edit `os.conf` by hand to point at a different file.

## Key Bindings

| Key              | Description                          |
|------------------|--------------------------------------|
| `Ctrl+Shift+K`   | Move tab forward                     |
| `Ctrl+Shift+J`   | Move tab backward                    |
| `Ctrl+Shift+Z`   | Toggle maximized window (macOS only) |

## Installation

**One-liner (curl):**
```bash
sh -c "$(curl -fsSL https://raw.githubusercontent.com/miniex/dotfiles.kitty/main/install.sh)"
```

The installer clones the repo to `~/.config/kitty`, auto-detects your OS
(Linux / macOS), and writes the matching `os.conf`.

**Manual:**
1. Install Kitty (`sudo pacman -S kitty`, `brew install --cask kitty`, etc.)
2. Clone the repo:
   ```bash
   git clone https://github.com/miniex/dotfiles.kitty.git ~/.config/kitty
   ```
3. Run the installer in-place to pick the OS profile:
   ```bash
   sh ~/.config/kitty/install.sh
   ```
4. Install the required fonts:
   - [D2Coding](https://github.com/naver/d2codingfont)
   - [Symbols Nerd Font Mono](https://www.nerdfonts.com/)

## Contributing

PRs welcome. Before opening one:

- Install the toolchain: `shfmt`, `shellcheck`, `ruff`.
- Run `./tools/format.sh` and `./tools/lint.sh` — both must pass clean.
- Follow the commit prefix convention (`feat:`, `fix:`, `refactor:`, `docs:`, …, all lowercase).

Full details in [CONTRIBUTING.md](CONTRIBUTING.md).

## License

[MIT](LICENSE) © 2026 Han Damin — applies to all code in this repository.
