"""
generate_figures_stdlib.py
--------------------------
Generate placeholder figures using ONLY Python standard library (struct, zlib).
Writes valid PNG files with simple bar/line charts encoded manually.
No numpy, matplotlib, or external dependencies required.

Usage:
    python scripts/generate_figures_stdlib.py
"""

import os
import struct
import zlib

OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "..", "results", "figures")
os.makedirs(OUT_DIR, exist_ok=True)

# ── Minimal PNG writer ────────────────────────────────────────────────────────

def _chunk(tag: bytes, data: bytes) -> bytes:
    crc = zlib.crc32(tag + data) & 0xFFFFFFFF
    return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", crc)


def _png(width: int, height: int, pixels: list) -> bytes:
    """
    pixels: list of `height` rows, each a list of `width` (R,G,B) tuples.
    Returns raw PNG bytes.
    """
    sig = b"\x89PNG\r\n\x1a\n"
    ihdr_data = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    ihdr = _chunk(b"IHDR", ihdr_data)

    raw_rows = []
    for row in pixels:
        row_bytes = b"\x00"  # filter type None
        for r, g, b in row:
            row_bytes += bytes([r, g, b])
        raw_rows.append(row_bytes)

    compressed = zlib.compress(b"".join(raw_rows), 9)
    idat = _chunk(b"IDAT", compressed)
    iend = _chunk(b"IEND", b"")
    return sig + ihdr + idat + iend


def _blank(w, h, bg=(255, 255, 255)):
    return [[bg] * w for _ in range(h)]


def _rect(pixels, x0, y0, x1, y1, color):
    for y in range(max(0, y0), min(len(pixels), y1)):
        for x in range(max(0, x0), min(len(pixels[0]), x1)):
            pixels[y][x] = color


def _hline(pixels, y, x0, x1, color, thick=2):
    for dy in range(thick):
        yy = y + dy
        if 0 <= yy < len(pixels):
            for x in range(max(0, x0), min(len(pixels[0]), x1)):
                pixels[yy][x] = color


def _vline(pixels, x, y0, y1, color, thick=2):
    for dx in range(thick):
        xx = x + dx
        if 0 <= xx < len(pixels[0]):
            for y in range(max(0, y0), min(len(pixels), y1)):
                pixels[y][xx] = color


def _dot(pixels, cx, cy, r, color):
    for dy in range(-r, r + 1):
        for dx in range(-r, r + 1):
            if dx*dx + dy*dy <= r*r:
                y, x = cy + dy, cx + dx
                if 0 <= y < len(pixels) and 0 <= x < len(pixels[0]):
                    pixels[y][x] = color


# ── Figure 1: Grouped bar chart (Baseline vs RAG) ────────────────────────────

def fig_barplot():
    W, H = 700, 460
    pix = _blank(W, H)
    BLUE   = (37,  99, 235)
    ORANGE = (234, 88,  12)
    LGRAY  = (220, 220, 220)
    DGRAY  = (100, 100, 100)
    BLACK  = (20, 20, 20)

    # Chart area
    left, right, top, bot = 80, 640, 40, 380
    chart_h = bot - top
    chart_w = right - left

    # Grid background
    _rect(pix, left, top, right, bot, (248, 248, 255))

    base_means = [0.72, 0.51, 0.28]
    rag_means  = [0.74, 0.63, 0.49]
    n_groups   = 3
    group_w    = chart_w // n_groups
    bar_w      = 32

    for i, (bm, rm) in enumerate(zip(base_means, rag_means)):
        gx = left + i * group_w + group_w // 2
        # Baseline bar
        bh = int(bm * chart_h)
        _rect(pix, gx - bar_w - 4, bot - bh, gx - 4, bot, BLUE)
        # RAG bar
        rh = int(rm * chart_h)
        _rect(pix, gx + 4, bot - rh, gx + bar_w + 4, bot, ORANGE)

    # Axes
    _hline(pix, bot, left, right, BLACK)
    _vline(pix, left, top, bot, BLACK)

    # Title text (simple pixel dots for key chars — use box labels instead)
    # We'll just draw a colored header band
    _rect(pix, 0, 0, W, 30, (230, 236, 255))
    _rect(pix, 10, 8, 20, 22, BLUE)      # legend Baseline
    _rect(pix, 150, 8, 160, 22, ORANGE)  # legend RAG

    # Horizontal grid lines at 0.2, 0.4, 0.6, 0.8
    for v in [0.2, 0.4, 0.6, 0.8]:
        yg = bot - int(v * chart_h)
        _hline(pix, yg, left, right, LGRAY, 1)

    return _png(W, H, pix)


# ── Figure 2: Ablation k vs CAR line plot ────────────────────────────────────

def fig_ablation():
    W, H = 560, 400
    pix = _blank(W, H)
    ORANGE = (234, 88, 12)
    BLUE   = (37, 99, 235)
    LGRAY  = (220, 220, 220)
    BLACK  = (20, 20, 20)

    left, right, top, bot = 70, 500, 40, 340
    chart_h = bot - top
    chart_w = right - left

    _rect(pix, left, top, right, bot, (248, 248, 240))
    _hline(pix, bot, left, right, BLACK)
    _vline(pix, left, top, bot, BLACK)

    k_vals = [1, 3, 5, 10]
    car    = [0.38, 0.44, 0.49, 0.50]
    base   = 0.28

    # Baseline dashed line
    ybase = bot - int(base * chart_h)
    for x in range(left, right, 8):
        _hline(pix, ybase, x, min(x + 5, right), BLUE, 2)

    # RAG line
    xs = [left + int((kv / 11) * chart_w) for kv in k_vals]
    ys = [bot - int(cv * chart_h) for cv in car]

    for i in range(len(xs) - 1):
        # Simple Bresenham-ish line
        x0, y0 = xs[i], ys[i]
        x1, y1 = xs[i+1], ys[i+1]
        steps = max(abs(x1 - x0), abs(y1 - y0))
        if steps == 0:
            continue
        for t in range(steps + 1):
            xp = x0 + (x1 - x0) * t // steps
            yp = y0 + (y1 - y0) * t // steps
            for dy in range(-2, 3):
                for dx in range(-2, 3):
                    ny, nx = yp + dy, xp + dx
                    if 0 <= ny < H and 0 <= nx < W:
                        pix[ny][nx] = ORANGE

    # Data point dots
    for xp, yp in zip(xs, ys):
        _dot(pix, xp, yp, 7, ORANGE)

    # Grid lines
    for v in [0.2, 0.3, 0.4, 0.5, 0.6]:
        yg = bot - int(v * chart_h)
        _hline(pix, yg, left, right, LGRAY, 1)

    # Header band
    _rect(pix, 0, 0, W, 32, (255, 243, 220))
    _rect(pix, 10, 10, 30, 22, ORANGE)
    _rect(pix, 120, 14, 150, 17, BLUE)

    return _png(W, H, pix)


# ── Figure 3: Degradation line chart ─────────────────────────────────────────

def fig_degradation():
    W, H = 620, 420
    pix = _blank(W, H)
    BLUE   = (37,  99, 235)
    ORANGE = (234, 88,  12)
    GREEN  = (22, 163,  74)
    LGRAY  = (220, 220, 220)
    BLACK  = (20, 20, 20)

    left, right, top, bot = 70, 560, 40, 360
    chart_h = bot - top
    chart_w = right - left

    _rect(pix, left, top, right, bot, (248, 255, 248))
    _hline(pix, bot, left, right, BLACK)
    _vline(pix, left, top, bot, BLACK)

    base = [0.72, 0.51, 0.28]
    rag  = [0.74, 0.63, 0.49]

    xs = [left + i * (chart_w // 2) for i in range(3)]

    def draw_line(vals, color):
        pts = [(xs[i], bot - int(v * chart_h)) for i, v in enumerate(vals)]
        for i in range(len(pts) - 1):
            x0, y0 = pts[i]
            x1, y1 = pts[i+1]
            steps = max(abs(x1 - x0), abs(y1 - y0))
            if steps == 0:
                continue
            for t in range(steps + 1):
                xp = x0 + (x1 - x0) * t // steps
                yp = y0 + (y1 - y0) * t // steps
                for dy in range(-2, 3):
                    for dx in range(-2, 3):
                        ny, nx = yp + dy, xp + dx
                        if 0 <= ny < H and 0 <= nx < W:
                            pix[ny][nx] = color
        for xp, yp in pts:
            _dot(pix, xp, yp, 7, color)

    # Green fill between base and rag
    for i in range(len(xs)):
        yb = bot - int(base[i] * chart_h)
        yr = bot - int(rag[i] * chart_h)
        for yy in range(yr, yb):
            if 0 <= yy < H and 0 <= xs[i] < W:
                for xx in range(max(left, xs[i] - 20), min(right, xs[i] + 20)):
                    if pix[yy][xx] == (248, 255, 248):
                        pix[yy][xx] = (220, 252, 231)

    draw_line(base, BLUE)
    draw_line(rag, ORANGE)

    # Grid lines
    for v in [0.2, 0.4, 0.6, 0.8]:
        yg = bot - int(v * chart_h)
        _hline(pix, yg, left, right, LGRAY, 1)

    # Header band
    _rect(pix, 0, 0, W, 32, (230, 255, 236))
    _rect(pix, 10, 10, 30, 22, BLUE)
    _rect(pix, 150, 10, 170, 22, ORANGE)

    return _png(W, H, pix)


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    files = [
        ("car_barplot.png",    fig_barplot()),
        ("car_ablation.png",   fig_ablation()),
        ("car_degradation.png", fig_degradation()),
    ]
    for fname, data in files:
        path = os.path.join(OUT_DIR, fname)
        with open(path, "wb") as f:
            f.write(data)
        print(f"Saved {path}  ({len(data):,} bytes)")

    print("\nAll stdlib figures generated.")
