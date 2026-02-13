# Kitty Terminal Configuration

A minimal Kitty terminal emulator configuration with Nerd Font integration and semi-transparent dark theme.

## Features

- **D2Coding Ligature** - Korean-friendly monospace font with ligature support
- **Nerd Font Icons** - Full symbol mapping via Symbols Nerd Font Mono
- **Semi-transparent** - 85% background opacity with dark theme
- **Clipboard Integration** - Full read/write clipboard support

## Configuration

| Setting              | Value                    |
|----------------------|--------------------------|
| Font                 | D2Coding Ligature 12pt   |
| Cursor               | Block                    |
| Background           | `#1e1e1e` (85% opacity)  |
| Foreground           | `#ffffff`                |
| Window Padding       | 2px                      |

## Key Bindings

| Key              | Description        |
|------------------|--------------------|
| `Ctrl+Shift+J`   | Move tab forward   |
| `Ctrl+Shift+K`   | Move tab backward  |

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
