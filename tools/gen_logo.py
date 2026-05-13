#!/usr/bin/env python3
"""5-petal cherry-blossom watermark → assets/logo.png. stdlib only."""

from __future__ import annotations

import math
import struct
import zlib
from pathlib import Path

W = H = 96
CX = (W - 1) / 2
CY = (H - 1) / 2

PETAL_CENTER_R = 24  # canvas center → petal center
PETAL_R = 22
CORE_R = 11

# Vertical gradient (top → bottom) — tab bar palette.
START = (0x98, 0xAB, 0xCC)
END = (0xE8, 0x90, 0xB0)

EDGE_PX = 1.5  # anti-aliased rim width


def _lerp(a: int, b: int, t: float) -> int:
    return round(a + (b - a) * t)


def _gradient_at(y: float) -> tuple[int, int, int]:
    t = y / (H - 1)
    return (
        _lerp(START[0], END[0], t),
        _lerp(START[1], END[1], t),
        _lerp(START[2], END[2], t),
    )


def _disc_alpha(dx: float, dy: float, r: float) -> float:
    d = math.hypot(dx, dy)
    if d >= r:
        return 0.0
    return min(1.0, (r - d) / EDGE_PX)


def _build_rows() -> list[bytes]:
    petals: list[tuple[float, float]] = []
    for k in range(5):
        # First petal up; rest 72° apart.
        angle = math.pi / 2 + k * 2 * math.pi / 5
        petals.append(
            (
                CX + math.cos(angle) * PETAL_CENTER_R,
                CY - math.sin(angle) * PETAL_CENTER_R,
            )
        )

    rows: list[bytes] = []
    for y in range(H):
        r, g, b = _gradient_at(y)
        row = bytearray()
        for x in range(W):
            alpha = _disc_alpha(x - CX, y - CY, CORE_R)
            for px, py in petals:
                alpha = max(alpha, _disc_alpha(x - px, y - py, PETAL_R))
            row.append(r)
            row.append(g)
            row.append(b)
            row.append(round(alpha * 255))
        rows.append(bytes(row))
    return rows


def _chunk(typ: bytes, data: bytes) -> bytes:
    length = struct.pack(">I", len(data))
    crc = struct.pack(">I", zlib.crc32(typ + data) & 0xFFFFFFFF)
    return length + typ + data + crc


def _encode_png(rows: list[bytes]) -> bytes:
    sig = b"\x89PNG\r\n\x1a\n"
    ihdr = _chunk(b"IHDR", struct.pack(">IIBBBBB", W, H, 8, 6, 0, 0, 0))
    raw = b"".join(b"\x00" + row for row in rows)
    idat = _chunk(b"IDAT", zlib.compress(raw, 9))
    iend = _chunk(b"IEND", b"")
    return sig + ihdr + idat + iend


def main() -> None:
    out = Path(__file__).resolve().parent.parent / "assets" / "logo.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    png = _encode_png(_build_rows())
    out.write_bytes(png)
    print(f"wrote {len(png)} bytes → {out}")


if __name__ == "__main__":
    main()
