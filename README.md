# Kitty Terminal Configuration

A minimal Kitty terminal emulator configuration with Nerd Font integration and semi-transparent dark theme.

## Features

- **D2Coding** - Korean-friendly monospace font
- **Nerd Font Icons** - Catch-all PUA fallback to Symbols Nerd Font Mono — every Nerd Font glyph renders (Pomicons, Powerline, FA, FA-Extension, Weather, Devicons, Seti, Codicons, Font Logos, Octicons, Material Design Icons, Custom — including the supplementary plane MDI block at U+F0001+)
- **Semi-transparent** - 85% background opacity with dark theme
- **Clipboard Integration** - Full read/write clipboard support
- **Kawaii Tab Bar** - Custom Python tab renderer (`tab_bar.py`):
  - Each tab is a rounded pill (Powerline-Extra caps `` U+E0B6 / `` U+E0B4) framed by an MDI flower `󰴈` (U+F0D08) on the left and a `♥` (U+2665) on the right, so every tab carries the same decoration and the layout never shifts when activation changes.
  - Pill colors are interpolated along a `#98ABCC` → `#E890B0` gradient and adjacent caps borrow the next tab's color, so the strip reads as one continuous ribbon.
  - Active title + flower + heart render in white & bold; inactive ones use an HSL-muted version of the tab's own color (sat ×0.3, lum ×0.55) so they sit quietly tone-on-tone.
  - On tab switch the title fg fades muted ↔ white over 300 ms with a smoothstep curve, driven by an `add_timer` ~60 fps repaint loop in the renderer. The previously-active tab holds its bold weight through the fade-out window so weight doesn't snap off while the color is still drifting back to muted.
  - Per-tab pill color and its HSL-muted variant are memoized (`functools.lru_cache`), so the ~60 fps repaint loop re-uses cached values instead of re-running the gradient math and RGB↔HLS round-trip every frame.
  - Titles truncate with `…` to fit kitty's per-tab budget; when the budget falls below the decoration size, the pill collapses to a compact `…`-only form so tabs keep shrinking instead of overflowing and getting dropped by kitty's tab-bar layout.
  - `kitty.conf` re-pins `U+E0A0–U+E0D4` to Symbols Nerd Font Mono so D2Coding's own (rectangular) Powerline placeholders don't win for the tab caps.

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
