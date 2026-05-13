#!/bin/sh
# miniex/dotfiles.kitty installer.
# Remote: sh -c "$(curl -fsSL https://raw.githubusercontent.com/miniex/dotfiles.kitty/main/install.sh)"
# In-repo: sh install.sh
set -eu

REPO_URL="https://github.com/miniex/dotfiles.kitty.git"
KITTY_CONFIG="${XDG_CONFIG_HOME:-$HOME/.config}/kitty"

if [ -t 1 ]; then
    RESET=$(printf '\033[0m')
    BOLD=$(printf '\033[1m')
    DIM=$(printf '\033[2m')
    SKY=$(printf '\033[38;2;135;206;235m')
    PINK=$(printf '\033[38;2;255;182;193m')
    SKY2=$(printf '\033[38;2;165;200;225m')
    PINK2=$(printf '\033[38;2;225;188;204m')
    YELLOW=$(printf '\033[33m')
    RED=$(printf '\033[31m')
else
    RESET=''
    BOLD=''
    DIM=''
    SKY=''
    PINK=''
    SKY2=''
    PINK2=''
    YELLOW=''
    RED=''
fi

banner() {
    printf '\n'
    printf '   %s%s╭──────────────────────────────────────────────╮%s\n' "$SKY" "$BOLD" "$RESET"
    printf '   %s%s│  %sminiex/dotfiles.kitty%s%s%s                       %s%s│%s\n' \
        "$SKY" "$BOLD" "$PINK" "$RESET" "$SKY" "$BOLD" "$SKY" "$BOLD" "$RESET"
    printf '   %s%s│  %sKitty terminal configuration installer%s%s%s      %s%s│%s\n' \
        "$SKY2" "$BOLD" "$PINK2" "$RESET" "$SKY2" "$BOLD" "$SKY2" "$BOLD" "$RESET"
    printf '   %s%s╰──────────────────────────────────────────────╯%s\n' "$PINK" "$BOLD" "$RESET"
    printf '\n'
}

step() { printf '\n%s%s▸ %s%s\n' "$BOLD" "$SKY" "$1" "$RESET"; }
info() { printf '  %sℹ%s  %s\n' "$SKY" "$RESET" "$1"; }
ok() { printf '  %s✓%s  %s\n' "$PINK" "$RESET" "$1"; }
warn() { printf '  %s⚠%s  %s\n' "$YELLOW" "$RESET" "$1"; }
err() { printf '  %s✗%s  %s\n' "$RED" "$RESET" "$1" >&2; }

# Read from /dev/tty so prompts work under `curl | sh`.
read_answer() {
    answer=''
    if { read -r answer </dev/tty; } 2>/dev/null; then
        return 0
    fi
    if read -r answer 2>/dev/null; then
        return 0
    fi
    answer=''
    return 0
}

prompt_yes() {
    printf '  %s?%s  %s %s[y/N]%s ' "$PINK" "$RESET" "$1" "$DIM" "$RESET"
    read_answer
    case "$answer" in
        [yY] | [yY][eE][sS]) return 0 ;;
        *) return 1 ;;
    esac
}

prompt_choice() {
    # $1=question, $2=default (linux|macos); echoes the choice.
    default=$2
    printf '  %s?%s  %s %s[linux/macos, default: %s]%s ' \
        "$PINK" "$RESET" "$1" "$DIM" "$default" "$RESET" >&2
    read_answer
    case "$answer" in
        l | L | linux | Linux | LINUX) printf 'linux' ;;
        m | M | mac | Mac | MAC | macos | macOS | MACOS | darwin | Darwin) printf 'macos' ;;
        '') printf '%s' "$default" ;;
        *) printf '%s' "$default" ;;
    esac
}

backup_path() { printf '%s.backup.%s' "$1" "$(date +%Y%m%d-%H%M%S)"; }

detect_os() {
    case "$(uname -s)" in
        Darwin) printf 'macos' ;;
        Linux) printf 'linux' ;;
        *) printf 'linux' ;;
    esac
}

write_os_conf() {
    # $1=repo dir, $2=linux|macos.
    target="$1/os/$2.conf"
    if [ ! -f "$target" ]; then
        err "missing $target — repo layout looks wrong"
        exit 1
    fi
    printf 'include os/%s.conf\n' "$2" >"$1/os.conf"
    ok "os.conf → include os/$2.conf"
}

banner

step "Pre-flight checks"
if ! command -v git >/dev/null 2>&1; then
    err "git not found — install it first"
    exit 1
fi
ok "git"

if command -v kitty >/dev/null 2>&1; then
    kitty_version=$(kitty --version 2>/dev/null | awk '{print $2}')
    ok "kitty $kitty_version"
else
    warn "kitty not installed — install Kitty before launching"
fi

# In-place mode: invoked from inside the cloned repo — skip clone/backup, just rewrite os.conf.
SCRIPT_DIR=$(cd "$(dirname "$0")" 2>/dev/null && pwd || printf '')
IN_PLACE=0
if [ -n "$SCRIPT_DIR" ] && [ -f "$SCRIPT_DIR/kitty.conf" ] && [ -d "$SCRIPT_DIR/os" ]; then
    IN_PLACE=1
    KITTY_CONFIG="$SCRIPT_DIR"
    info "running in-place inside $KITTY_CONFIG"
fi

if [ "$IN_PLACE" -eq 0 ]; then
    step "Backup existing"
    if [ -e "$KITTY_CONFIG" ]; then
        bk=$(backup_path "$KITTY_CONFIG")
        if prompt_yes "Move $KITTY_CONFIG → $bk?"; then
            mv "$KITTY_CONFIG" "$bk"
            ok "config moved to $bk"
        else
            err "aborted — config already exists at $KITTY_CONFIG"
            exit 1
        fi
    else
        info "no existing $KITTY_CONFIG"
    fi

    step "Clone repository"
    git clone --depth 1 "$REPO_URL" "$KITTY_CONFIG"
    ok "cloned to $KITTY_CONFIG"
fi

step "OS selection"
detected=$(detect_os)
info "detected: $detected"
if [ -r /dev/tty ]; then
    choice=$(prompt_choice "Which OS profile should kitty load?" "$detected")
else
    choice=$detected
    info "non-interactive — using detected ($choice)"
fi
write_os_conf "$KITTY_CONFIG" "$choice"

step "Done"
ok "miniex/dotfiles.kitty installed at $KITTY_CONFIG"
printf '\n  %sNext:%s\n' "$BOLD" "$RESET"
printf '    %s•%s install fonts: %sD2Coding Ligature%s and %sSymbols Nerd Font Mono%s\n' \
    "$PINK" "$RESET" "$SKY" "$RESET" "$SKY" "$RESET"
printf '    %s•%s reload kitty (or restart) to pick up the new config\n' "$PINK" "$RESET"
printf '    %s•%s rerun %s%ssh %s/install.sh%s to switch OS profile\n\n' \
    "$PINK" "$RESET" "$SKY" "$BOLD" "$KITTY_CONFIG" "$RESET"
