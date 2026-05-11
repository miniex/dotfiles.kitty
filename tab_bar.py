import colorsys
import time
from functools import lru_cache

from kitty.boss import get_boss
from kitty.fast_data_types import Screen, add_timer, remove_timer
from kitty.tab_bar import (
    DrawData,
    ExtraData,
    TabBarData,
    as_rgb,
    draw_title,
)

START = (0x98, 0xAB, 0xCC)  # #98ABCC
END = (0xE8, 0x90, 0xB0)  # #E890B0
BAR_BG = 0x1E1E1E
WHITE = 0xFFFFFF
# Inactive tab title is rendered as a hue-preserving, lower-saturation,
# dimmer version of the pill color. Numbers are tuned so the transition
# to/from white isn't a harsh jump — softer span keeps the fade gentle.
INACTIVE_TEXT_SAT = 0.3
INACTIVE_TEXT_LUM = 0.55

# Glyphs via escape sequences — PUA literals can be mangled by tooling.
LEFT_CAP = ""
RIGHT_CAP = ""
FLOWER = "✿"  # ✿ left-side decoration on every tab
HEART = "❥"  # ❥ kawaii right-side decoration on every tab

# Active-switch fade animation. Kitty's tab bar is cell-based, so we can't
# slide pixels — but we can repaint at ~60 fps for ANIM_DURATION seconds
# and interpolate the title fg between muted and white during that window.
# Longer duration + smoothstep easing makes the change land softly.
ANIM_DURATION = 0.30
ANIM_TICK = 0.016

# Per-tab decoration cells (spaces + flower + heart + right cap); first tab adds a left cap.
DECO_CELLS = 7
FIRST_TAB_EXTRA = 1

_anim = {
    "start": 0.0,
    "active_id": None,
    "prev_active_id": None,
    "timer_id": None,
}


def _now() -> float:
    return time.monotonic()


def _ease(t: float) -> float:
    # smoothstep — symmetric S-curve, slow at both ends, no harsh edges.
    return t * t * (3.0 - 2.0 * t)


def _progress() -> float:
    elapsed = _now() - _anim["start"]
    if elapsed <= 0.0:
        return 0.0
    if elapsed >= ANIM_DURATION:
        return 1.0
    return _ease(elapsed / ANIM_DURATION)


def _tick(timer_id: int) -> None:
    if _now() - _anim["start"] >= ANIM_DURATION:
        remove_timer(timer_id)
        _anim["timer_id"] = None
        _anim["prev_active_id"] = None
        return
    tm = get_boss().active_tab_manager
    if tm is not None:
        tm.mark_tab_bar_dirty()


def _start_anim(new_active_id: int) -> None:
    if _anim["active_id"] == new_active_id:
        return
    _anim["prev_active_id"] = _anim["active_id"]
    _anim["active_id"] = new_active_id
    _anim["start"] = _now()
    if _anim["timer_id"] is None:
        _anim["timer_id"] = add_timer(_tick, ANIM_TICK, True)


def _lerp(a: int, b: int, t: float) -> int:
    return round(a + (b - a) * t)


def _gradient(t: float) -> int:
    return (
        (_lerp(START[0], END[0], t) << 16)
        | (_lerp(START[1], END[1], t) << 8)
        | _lerp(START[2], END[2], t)
    )


def _lerp_color(a: int, b: int, t: float) -> int:
    return (
        (_lerp((a >> 16) & 0xFF, (b >> 16) & 0xFF, t) << 16)
        | (_lerp((a >> 8) & 0xFF, (b >> 8) & 0xFF, t) << 8)
        | _lerp(a & 0xFF, b & 0xFF, t)
    )


@lru_cache(maxsize=64)
def _muted(rgb: int) -> int:
    r = ((rgb >> 16) & 0xFF) / 255
    g = ((rgb >> 8) & 0xFF) / 255
    b = (rgb & 0xFF) / 255
    h, lum, sat = colorsys.rgb_to_hls(r, g, b)
    r, g, b = colorsys.hls_to_rgb(h, lum * INACTIVE_TEXT_LUM, sat * INACTIVE_TEXT_SAT)
    return (round(r * 255) << 16) | (round(g * 255) << 8) | round(b * 255)


@lru_cache(maxsize=64)
def _bg_for(idx: int, total: int) -> int:
    t = 0.0 if total <= 1 else (idx - 1) / (total - 1)
    return _gradient(t)


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
    tm = get_boss().active_tab_manager
    total = len(tm.tabs) if tm is not None else 1

    if tab.is_active:
        _start_anim(tab.tab_id)

    bg = _bg_for(index, total)
    muted = _muted(bg)
    progress = _progress()
    fading_out = tab.tab_id == _anim["prev_active_id"] and progress < 1.0

    if tab.is_active:
        fg = _lerp_color(muted, WHITE, progress)
    elif fading_out:
        fg = _lerp_color(WHITE, muted, progress)
    else:
        fg = muted

    bar = as_rgb(BAR_BG)
    pill = as_rgb(bg)
    text = as_rgb(fg)
    is_first = extra_data.prev_tab is None
    deco = DECO_CELLS + (FIRST_TAB_EXTRA if is_first else 0)

    def _right_cap_bg() -> int:
        if extra_data.next_tab is not None:
            return as_rgb(_bg_for(index + 1, total))
        return bar

    # Budget too tight for full pill — draw a compact "…" pill so kitty doesn't
    # bail out and drop the rest of the tabs.
    if max_title_length < deco + 1:
        if is_first:
            screen.cursor.fg = pill
            screen.cursor.bg = bar
            screen.draw(LEFT_CAP)
        screen.cursor.fg = text
        screen.cursor.bg = pill
        body = max(0, max_title_length - (2 if is_first else 1))
        if body > 0:
            screen.draw("…" + " " * (body - 1))
        screen.cursor.bg = _right_cap_bg()
        screen.cursor.fg = pill
        screen.draw(RIGHT_CAP)
        end = screen.cursor.x
        screen.cursor.bg = 0
        screen.cursor.fg = 0
        return end

    if is_first:
        screen.cursor.fg = pill
        screen.cursor.bg = bar
        screen.draw(LEFT_CAP)

    # Flower on the left and a small heart on the right are drawn on every
    # tab so the layout stays stable on activation; their colors fade with
    # the title so the active tab glows white while inactive tabs sit quietly
    # in the muted hue.
    screen.cursor.fg = text
    screen.cursor.bg = pill
    # Hold bold through the fade-out window so weight doesn't snap off while
    # the color is still drifting back to muted — keeps the transition smooth.
    screen.cursor.bold = tab.is_active or fading_out
    screen.draw(" ")
    screen.draw(FLOWER)
    screen.draw(" ")
    title_budget = max(1, max_title_length - deco)
    draw_title(draw_data, screen, tab, index, title_budget)
    # Title can still overshoot (wide glyphs, template extras) — back up and
    # drop in an ellipsis so the trailing decoration fits within budget.
    trailing = 4  # " ", heart, " ", right cap
    target_x = before + max_title_length - trailing
    overflow = screen.cursor.x - target_x
    if overflow > 0:
        screen.cursor.x -= overflow + 1
        screen.draw("…")
    screen.draw(" ")
    screen.draw(HEART)
    screen.draw(" ")
    screen.cursor.bold = False

    screen.cursor.bg = _right_cap_bg()
    screen.cursor.fg = pill
    screen.draw(RIGHT_CAP)

    end = screen.cursor.x
    screen.cursor.bg = 0
    screen.cursor.fg = 0
    return end
