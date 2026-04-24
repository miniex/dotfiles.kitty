# Kitty Terminal Configuration

A minimal Kitty terminal emulator configuration with Nerd Font integration and semi-transparent dark theme.

## Features

- **D2Coding Ligature** - Korean-friendly monospace font with ligature support
- **Nerd Font Icons** - Full symbol mapping via Symbols Nerd Font Mono
- **Semi-transparent** - 85% background opacity with dark theme
- **Clipboard Integration** - Full read/write clipboard support

## Configuration

| Setting              | Value                            |
|----------------------|----------------------------------|
| Font                 | D2Coding Ligature (size opt-in)  |
| Cursor               | Block                            |
| Background           | `#1e1e1e` (85% opacity)          |
| Foreground           | `#ffffff`                        |
| Window Padding       | 2px                              |

Font size is not set by default — uncomment the OS-specific line in
`kitty.conf` (`12.0` for Linux, `18.0` for macOS).

## macOS-only Settings

Commented out by default. Remove the leading `#` on macOS to enable:

| Setting                                | Effect                                              |
|----------------------------------------|-----------------------------------------------------|
| `hide_window_decorations titlebar-only`| Hide titlebar, keep traffic-light buttons visible   |
| `map ctrl+shift+z toggle_maximized`    | macOS-style zoom (fill screen, stay in same Space)  |

## Key Bindings

| Key              | Description                          |
|------------------|--------------------------------------|
| `Ctrl+Shift+K`   | Move tab forward                     |
| `Ctrl+Shift+J`   | Move tab backward                    |
| `Ctrl+Shift+Z`   | Toggle maximized window (macOS only) |

## Installation

1. **Install Kitty:**
   ```bash
   # Arch / ChromeOS (crostini)
   sudo pacman -S kitty
   ```

2. **Clone this configuration:**
   ```bash
   git clone <repo-url> ~/.config/kitty
   ```

3. **Install required fonts:**
   - [D2Coding Ligature](https://github.com/naver/d2codingfont)
   - [Symbols Nerd Font Mono](https://www.nerdfonts.com/)

## License

Free to use and modify.
