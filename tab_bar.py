from kitty.boss import get_boss
from kitty.fast_data_types import Screen
from kitty.tab_bar import (
    DrawData,
    ExtraData,
    TabBarData,
    as_rgb,
    draw_title,
)

START = (0x98, 0xAB, 0xCC)  # #98ABCC
END = (0xE8, 0x90, 0xB0)  # #E890B0


def _lerp(a: int, b: int, t: float) -> int:
    return round(a + (b - a) * t)


def _gradient(t: float) -> int:
    r = _lerp(START[0], END[0], t)
    g = _lerp(START[1], END[1], t)
    b = _lerp(START[2], END[2], t)
    return (r << 16) | (g << 8) | b


def _pick_fg(rgb: int) -> int:
    r = (rgb >> 16) & 0xFF
    g = (rgb >> 8) & 0xFF
    b = rgb & 0xFF
    luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
    return 0x1E1E1E if luminance > 0.55 else 0xFFFFFF


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
    t = 0.0 if total <= 1 else (index - 1) / (total - 1)

    bg = _gradient(t)
    fg = _pick_fg(bg)

    if not tab.is_active:
        # Dim inactive tabs by blending toward background
        r = (bg >> 16) & 0xFF
        g = (bg >> 8) & 0xFF
        b = bg & 0xFF
        r = round(r * 0.55 + 0x1E * 0.45)
        g = round(g * 0.55 + 0x1E * 0.45)
        b = round(b * 0.55 + 0x1E * 0.45)
        bg = (r << 16) | (g << 8) | b
        fg = _pick_fg(bg)

    screen.cursor.bg = as_rgb(bg)
    screen.cursor.fg = as_rgb(fg)
    screen.draw(" ")

    draw_title(draw_data, screen, tab, index)

    screen.cursor.bg = as_rgb(bg)
    screen.cursor.fg = as_rgb(fg)
    screen.draw(" ")

    end = screen.cursor.x
    screen.cursor.bg = 0
    screen.cursor.fg = 0
    if not is_last:
        screen.draw(" ")
    return end
