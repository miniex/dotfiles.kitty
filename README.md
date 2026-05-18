# Kitty Terminal Configuration

Polished Kitty config — Nerd Font integration, custom gradient tab bar, leader keychain, dark/light theme files.

## Features

- **D2Coding** — Korean-friendly monospace.
- **Nerd Font** — PUA catch-all to Symbols Nerd Font Mono (Powerline, FA, MDI, Devicons, Codicons).
- **Themes** — `themes/dark.conf` (default) / `themes/light.conf`. Swap the `include`, or `kitten themes` for auto dark/light (kitty 0.38+).
- **Mouse-hide on type**, **long-cmd notification** (≥10s unfocused).
- **Quiet** — bell off, no update ping, inactive splits dimmed.
- **Paste guarded** — URL quote, control-code strip, confirm if large.
- **100 k scrollback** + 4 GB pager cache.
- **Leader chord** — 1.5 s timeout.
- **Neovim scrollback pager** — `q` to quit, full vim motions.
- **`kitty @` remote control** — per-PID socket at `/tmp/kitty-{kitty_pid}`.
- **Kawaii Tab Bar** (`tab_bar.py`):
    - Cell-level gradient `#98ABCC` → `#E890B0`; tab N owns slice `(N-1)/total → N/total`, continuous at boundaries.
    - Rounded Powerline-Extra caps on first/last tab.
    - Glyphs: layout (`▌▐▦═║◫▣`) · `✿` (→ `‼` on attention) · title · `❥` (→ superscript when >1 window group).
    - Active-tab fade muted ↔ white over 300 ms; bold persists.
    - Bar background follows the active theme via `get_options()`.

## Configuration

| Setting           | Value                                               |
| ----------------- | --------------------------------------------------- |
| Font              | D2Coding (size from [OS profile](#os-profiles))     |
| Color Scheme      | `themes/dark.conf`                                  |
| Tab Bar           | `custom` gradient `#98ABCC` → `#E890B0`, bottom     |
| Remote Control    | `unix:/tmp/kitty-{kitty_pid}`                       |
| Scrollback        | 100 k lines · Neovim pager · 4 GB cache             |
| Paste Safety      | Quote URLs · strip control codes · confirm if large |
| Bell              | Audio off, window alert on                          |
| Leader Timeout    | 1.5 s                                               |
| Update Check      | Disabled                                            |
| Cmd-finish Notify | `invisible` (10s threshold)                         |

## Themes

Color-scheme only — opacity, fg/bg, borders, `tab_bar_background`.

| File                | Look                                   |
| ------------------- | -------------------------------------- |
| `themes/dark.conf`  | Cherry-blossom on near-black (default) |
| `themes/light.conf` | Cherry-blossom on warm cream           |

Switch via the `include` line, or `kitten themes --reload-in=all` for system auto-switching.

## OS Profiles

| File            | Settings                                                                                            |
| --------------- | --------------------------------------------------------------------------------------------------- |
| `os/linux.conf` | `font_size 12.0`                                                                                    |
| `os/macos.conf` | `font_size 18.0`, titlebar blended into bg (`macos_titlebar_color background`), `Ctrl+Shift+Z` zoom |

Re-run `sh install.sh` to switch, or edit `os.conf` directly.

## Key Bindings

**Tab move** — `Ctrl+Shift+J/K` (back/fwd) · `Ctrl+Shift+Z` zoom (macOS).

**Hints (custom)** — `Ctrl+Shift+U` URL · `Ctrl+Shift+Y` git hash · `Ctrl+Shift+I` IP → clipboard. Defaults still cover open/insert (`Ctrl+Shift+E` opens URL, etc.).

**Leader keychain** — prefix `Ctrl+Shift+Space`, then (1.5 s window):

| Key | Action            | Key | Action           |
| --- | ----------------- | --- | ---------------- |
| `N` | New tab (cwd)     | `R` | Reload config    |
| `W` | New window (cwd)  | `T` | Themes picker    |
| `X` | Close tab         | `L` | Next layout      |
| `E` | Edit `kitty.conf` | `C` | Clear scrollback |

## Installation

```bash
sh -c "$(curl -fsSL https://raw.githubusercontent.com/miniex/dotfiles.kitty/main/install.sh)"
```

Clones to `~/.config/kitty`, auto-detects Linux/macOS, writes `os.conf`. Then install [D2Coding](https://github.com/naver/d2codingfont) and [Symbols Nerd Font Mono](https://www.nerdfonts.com/).

## Companion repos

- [btop-theme-damin](https://github.com/miniex/btop-theme-damin)
- [fish-theme-damin](https://github.com/miniex/fish-theme-damin)
- [dotfiles.tmux](https://github.com/miniex/dotfiles.tmux)
- [dotfiles.nvim](https://github.com/miniex/dotfiles.nvim)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). `./tools/format.sh` and `./tools/lint.sh` must pass clean.

## License

[MIT](LICENSE) © 2026 Han Damin.
