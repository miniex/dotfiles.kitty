# Kitty Terminal Configuration

A minimal Kitty terminal emulator configuration with Nerd Font integration and semi-transparent dark theme.

## Features

- **D2Coding Ligature** - Korean-friendly monospace font with ligature support
- **Nerd Font Icons** - Catch-all PUA fallback to Symbols Nerd Font Mono — every Nerd Font glyph renders (Pomicons, Powerline, FA, FA-Extension, Weather, Devicons, Seti, Codicons, Font Logos, Octicons, Material Design Icons, Custom — including the supplementary plane MDI block at U+F0001+)
- **Semi-transparent** - 85% background opacity with dark theme
- **Clipboard Integration** - Full read/write clipboard support

## Configuration

| Setting              | Value                            |
|----------------------|----------------------------------|
| Font                 | D2Coding Ligature                |
| Font Size            | from [OS profile](#os-profiles)  |
| Cursor               | Block                            |
| Background           | `#1e1e1e` (85% opacity)          |
| Foreground           | `#ffffff`                        |
| Window Padding       | 2px                              |

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
   - [D2Coding Ligature](https://github.com/naver/d2codingfont)
   - [Symbols Nerd Font Mono](https://www.nerdfonts.com/)

## Contributing

PRs welcome. Before opening one:

- Run `./tools/format.sh` and `./tools/lint.sh` — both must pass clean.
- Follow the commit prefix convention (`feat:`, `fix:`, `refactor:`, `docs:`, …, all lowercase).

Full details in [CONTRIBUTING.md](CONTRIBUTING.md).

## License

[MIT](LICENSE) © 2026 Han Damin — applies to all code in this repository.
