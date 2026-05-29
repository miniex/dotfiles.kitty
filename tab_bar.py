import colorsys
import time
import weakref
from dataclasses import dataclass
from functools import lru_cache

from kitty.boss import get_boss
from kitty.fast_data_types import Screen, add_timer, get_options, remove_timer
from kitty.tab_bar import (
    DrawData,
    ExtraData,
    TabBarData,
    as_rgb,
)

try:
    from kitty.fast_data_types import wcswidth as _wcswidth  # type: ignore
except ImportError:
    import unicodedata

    def _wcswidth(s: str) -> int:
        return sum(2 if unicodedata.east_asian_width(c) in ("W", "F") else 1 for c in s)


def _cw(s: str) -> int:
    # wcswidth returns ≤0 for non-printable; treat as 1 cell.
    w = _wcswidth(s)
    return w if w > 0 else len(s)


START = (0x98, 0xAB, 0xCC)  # #98ABCC
END = (0xE8, 0x90, 0xB0)  # #E890B0
WHITE = 0xFFFFFF
ATTENTION = 0xF5C76A  # warm amber
INACTIVE_TEXT_SAT = 0.3
INACTIVE_TEXT_LUM = 0.55

# Powerline-Extra caps (U+E0B6/E0B4) — some editors strip them.
LEFT_CAP = ""
RIGHT_CAP = ""
SEP = "▌"  # divider between tabs
FLOWER = "✿"
BELL = "‼"
HEART = "❥"

SUPER_DIGITS = "⁰¹²³⁴⁵⁶⁷⁸⁹"
SUPER_PLUS = "⁺"

# Fixed per-tab cell width; kitty's per-tab budget shrinks it under overflow.
FIXED_TAB_WIDTH = 24

ANIM_DURATION = 0.30
ANIM_TICK = 0.016

# Quantized to memoize per-cell gradient lookups.
_GRAD_STEPS = 500


@dataclass
class AnimState:
    start: float = 0.0
    active_id: int | None = None
    prev_active_id: int | None = None
    timer_id: int | None = None


# Per-tab-manager state, keyed weakly so closed OS windows drop out.
_anim_states: "weakref.WeakKeyDictionary[object, AnimState]" = weakref.WeakKeyDictionary()


def _anim_for(tm) -> AnimState:
    st = _anim_states.get(tm)
    if st is None:
        st = AnimState()
        _anim_states[tm] = st
    return st


def _now() -> float:
    return time.monotonic()


def _ease(t: float) -> float:
    # smoothstep
    return t * t * (3.0 - 2.0 * t)


def _progress(st: AnimState) -> float:
    elapsed = _now() - st.start
    if elapsed <= 0.0:
        return 0.0
    if elapsed >= ANIM_DURATION:
        return 1.0
    return _ease(elapsed / ANIM_DURATION)


def _tick(timer_id: int) -> None:
    # Find the manager whose timer fired.
    match = next(
        ((tm, st) for tm, st in _anim_states.items() if st.timer_id == timer_id),
        None,
    )
    if match is None:
        remove_timer(timer_id)
        return
    tm, st = match
    if _now() - st.start >= ANIM_DURATION:
        remove_timer(timer_id)
        st.timer_id = None
        st.prev_active_id = None
        return
    tm.mark_tab_bar_dirty()


def _live_tab_ids(tm) -> set:
    return {getattr(t, "id", None) for t in tm.tabs}


def _start_anim(tm, new_active_id: int) -> None:
    st = _anim_for(tm)
    if st.active_id == new_active_id:
        return
    # Skip fade-out targeting a tab that's already closed.
    live = _live_tab_ids(tm)
    st.prev_active_id = st.active_id if st.active_id in live else None
    st.active_id = new_active_id
    st.start = _now()
    if st.timer_id is None:
        st.timer_id = add_timer(_tick, ANIM_TICK, True)


def _lerp(a: int, b: int, t: float) -> int:
    return round(a + (b - a) * t)


@lru_cache(maxsize=_GRAD_STEPS + 1)
def _gradient_bucket(bucket: int) -> int:
    t = bucket / _GRAD_STEPS
    return (
        (_lerp(START[0], END[0], t) << 16)
        | (_lerp(START[1], END[1], t) << 8)
        | _lerp(START[2], END[2], t)
    )


def _grad(t: float) -> int:
    t = max(0.0, min(1.0, t))
    return _gradient_bucket(round(t * _GRAD_STEPS))


def _lerp_color(a: int, b: int, t: float) -> int:
    return (
        (_lerp((a >> 16) & 0xFF, (b >> 16) & 0xFF, t) << 16)
        | (_lerp((a >> 8) & 0xFF, (b >> 8) & 0xFF, t) << 8)
        | _lerp(a & 0xFF, b & 0xFF, t)
    )


@lru_cache(maxsize=512)
def _muted(rgb: int) -> int:
    r = ((rgb >> 16) & 0xFF) / 255
    g = ((rgb >> 8) & 0xFF) / 255
    b = (rgb & 0xFF) / 255
    h, lum, sat = colorsys.rgb_to_hls(r, g, b)
    r, g, b = colorsys.hls_to_rgb(h, lum * INACTIVE_TEXT_LUM, sat * INACTIVE_TEXT_SAT)
    return (round(r * 255) << 16) | (round(g * 255) << 8) | round(b * 255)


def _bar_bg_int() -> int:
    # Active theme's tab_bar_background, fallback: window background.
    opts = get_options()
    c = opts.tab_bar_background or opts.background
    return (int(c.red) << 16) | (int(c.green) << 8) | int(c.blue)


def _left_glyph(tab: TabBarData) -> str:
    return BELL if tab.needs_attention else FLOWER


def _right_glyph(tab: TabBarData) -> str:
    n = tab.num_window_groups
    if n <= 1:
        return HEART
    if 2 <= n <= 9:
        return SUPER_DIGITS[n]
    return SUPER_PLUS


@lru_cache(maxsize=256)
def _render_template(
    template: str,
    index: int,
    title: str,
    layout_name: str,
    num_windows: int,
    num_window_groups: int,
) -> str:
    # Hardcoded fallback if .format() rejects unsupported fields.
    try:
        return template.format(
            index=index,
            title=title,
            layout_name=layout_name,
            num_windows=num_windows,
            num_window_groups=num_window_groups,
        )
    except (KeyError, ValueError, AttributeError):
        return f"{index}: {title}"


def _format_title(draw_data: DrawData, tab: TabBarData, index: int) -> str:
    template = getattr(draw_data, "active_title_template", None) if tab.is_active else None
    template = template or getattr(draw_data, "title_template", None) or "{index}: {title}"
    return _render_template(
        template,
        index,
        tab.title,
        tab.layout_name,
        tab.num_windows,
        tab.num_window_groups,
    )


def _truncate(s: str, max_cells: int) -> str:
    if max_cells <= 0:
        return ""
    if _cw(s) <= max_cells:
        return s
    out = ""
    used = 0
    for ch in s:
        w = _cw(ch)
        if used + w + 1 > max_cells:  # +1 for ellipsis
            break
        out += ch
        used += w
    return out + "…"


def _tm_for_tab(tab_id: int):
    # Match the drawn tab to its manager; the active manager is wrong for inactive windows.
    mgrs = list(get_boss().all_tab_managers)
    # One OS window (the common case): all tabs are its, skip the scan.
    if len(mgrs) == 1:
        return mgrs[0]
    for tm in mgrs:
        if any(getattr(t, "id", None) == tab_id for t in tm.tabs):
            return tm
    return mgrs[0] if mgrs else None


def draw_tab(
    draw_data: DrawData,
    screen: Screen,
    tab: TabBarData,
    before: int,
    max_title_length: int,
    index: int,
    is_last: bool,
    extra_data: ExtraData,
) -> int:
    tm = _tm_for_tab(tab.tab_id) or get_boss().active_tab_manager
    total = len(tm.tabs) if tm is not None else 1

    if tab.is_active and tm is not None:
        _start_anim(tm, tab.tab_id)

    st = _anim_for(tm) if tm is not None else None
    progress: float | None
    if st is None or st.timer_id is None:
        progress = None
        fading_out = False
    else:
        progress = _progress(st)
        fading_out = tab.tab_id == st.prev_active_id and progress < 1.0

    bar = as_rgb(_bar_bg_int())
    attention_fg = as_rgb(ATTENTION)

    is_first = extra_data.prev_tab is None

    left_g = _left_glyph(tab)
    right_g = _right_glyph(tab)

    lead_left = (_cw(LEFT_CAP) + 1) if is_first else 1  # tab 1: cap + space; else a space
    cap_left = lead_left + _cw(SEP)
    cap_right = _cw(RIGHT_CAP) if is_last else 0
    # " left   right "
    inner_deco = _cw(" " + left_g + " " + " " + right_g + " ")
    deco = inner_deco + cap_left + cap_right

    # Clamp fixed width to kitty's per-tab budget so overflow still compresses.
    target_w = min(FIXED_TAB_WIDTH, max_title_length)
    in_compact = target_w < deco + 1
    if in_compact:
        title_str = ""
        title_w = 0
        pad_w = 0
        total_tab_w = target_w
    else:
        avail = target_w - deco
        title_str = _truncate(_format_title(draw_data, tab, index), avail)
        title_w = _cw(title_str)
        pad_w = max(0, avail - title_w)
        total_tab_w = target_w

    # Tab N owns gradient slice (N-1)/total → N/total — continuous at boundaries.
    t_start = (index - 1) / max(1, total)
    t_end = index / max(1, total)
    t_span = t_end - t_start
    denom = max(1, total_tab_w - 1)

    def bg_at_offset(offset: int) -> int:
        return _grad(t_start + t_span * (offset / denom))

    def fg_for(bg_rgb: int) -> int:
        m = _muted(bg_rgb)
        if progress is None:
            return WHITE if tab.is_active else m
        if tab.is_active:
            return _lerp_color(m, WHITE, progress)
        if fading_out:
            return _lerp_color(WHITE, m, progress)
        return m

    def emit(ch: str, fg_override: int | None = None) -> None:
        offset = screen.cursor.x - before
        bg_rgb = bg_at_offset(offset)
        screen.cursor.bg = as_rgb(bg_rgb)
        screen.cursor.fg = fg_override if fg_override is not None else as_rgb(fg_for(bg_rgb))
        screen.draw(ch)

    def emit_cap(ch: str) -> None:
        offset = screen.cursor.x - before
        bg_rgb = bg_at_offset(offset)
        screen.cursor.bg = bar
        screen.cursor.fg = as_rgb(bg_rgb)
        screen.draw(ch)

    # Compact fallback — kitty drops trailing tabs on overflow.
    if in_compact:
        if is_first:
            emit_cap(LEFT_CAP)
        emit(" ")
        emit(SEP)
        body = max(0, target_w - cap_left - cap_right)
        for i in range(body):
            emit("…" if i == 0 else " ")
        if is_last:
            emit_cap(RIGHT_CAP)
        end = screen.cursor.x
        screen.cursor.bg = 0
        screen.cursor.fg = 0
        return end

    if is_first:
        emit_cap(LEFT_CAP)
    emit(" ")

    # Hold bold through fade-out so weight doesn't snap mid-drift.
    screen.cursor.bold = tab.is_active or fading_out

    emit(SEP)

    emit(" ")
    if tab.needs_attention and not tab.is_active:
        emit(left_g, fg_override=attention_fg)
    else:
        emit(left_g)
    emit(" ")

    for ch in title_str:
        emit(ch)
    for _ in range(pad_w):
        emit(" ")

    emit(" ")
    emit(right_g)
    emit(" ")

    screen.cursor.bold = False

    if is_last:
        emit_cap(RIGHT_CAP)

    end = screen.cursor.x
    screen.cursor.bg = 0
    screen.cursor.fg = 0
    return end
