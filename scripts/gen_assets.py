#!/usr/bin/env python3
"""
Code-generated asset builder for the mohit31kumar profile README.

Design system: Experimental Brutalism x Hacker Terminal.
Everything is generated from the palette + font stack below so the whole
profile shares one coherent visual language.

Run:  python3 scripts/gen_assets.py
Outputs into assets/{hero,separators,terminal,tech,projects,activity,footer}
"""

from __future__ import annotations

import math
import os
import random

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "assets")

# --------------------------------------------------------------------------
# Design tokens
# --------------------------------------------------------------------------
VOID = (11, 11, 18)
PINK = (255, 46, 136)
LIME = (182, 255, 0)
CYAN = (0, 229, 255)
ULTRA = (168, 85, 247)
ORANGE = (255, 107, 53)
GHOST = (244, 240, 255)
YELLOW = (255, 228, 94)
PANEL = (14, 14, 24)
GRID = (26, 26, 40)

NEON = [PINK, LIME, CYAN, ULTRA, ORANGE, YELLOW]

FONT_DIRS = {
    "display": [
        "/usr/share/fonts/truetype/noto/NotoSansDisplay-CondensedBlack.ttf",
        "/usr/share/fonts/truetype/noto/NotoSansDisplay-ExtraCondensedBlack.ttf",
        "/usr/share/fonts/truetype/lato/Lato-Black.ttf",
    ],
    "display_xb": [
        "/usr/share/fonts/truetype/noto/NotoSansDisplay-CondensedExtraBold.ttf",
        "/usr/share/fonts/truetype/noto/NotoSansDisplay-ExtraCondensedExtraBold.ttf",
    ],
    "mono": [
        "/usr/share/fonts/truetype/firacode/FiraCode-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    ],
    "mono_reg": [
        "/usr/share/fonts/truetype/firacode/FiraCode-Regular.ttf",
        "/usr/share/fonts/truetype/noto/NotoSansMono-Regular.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    ],
}

_font_cache: dict[tuple[str, int], ImageFont.FreeTypeFont] = {}


def font(kind: str, size: int) -> ImageFont.FreeTypeFont:
    key = (kind, size)
    if key in _font_cache:
        return _font_cache[key]
    for path in FONT_DIRS[kind]:
        if os.path.exists(path):
            f = ImageFont.truetype(path, size)
            _font_cache[key] = f
            return f
    f = ImageFont.load_default()
    _font_cache[key] = f
    return f


def ensure(*parts: str) -> str:
    p = os.path.join(ASSETS, *parts)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    return p


# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------
def add_noise(img: Image.Image, amount: int = 18, seed: int = 0) -> Image.Image:
    rng = np.random.default_rng(seed)
    arr = np.asarray(img).astype(np.int16)
    noise = rng.integers(-amount, amount + 1, arr.shape, dtype=np.int16)
    arr = np.clip(arr + noise, 0, 255).astype(np.uint8)
    return Image.fromarray(arr, img.mode)


def scanlines(size, step=4, alpha=42, color=(0, 0, 0)):
    w, h = size
    layer = Image.new("RGBA", size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for y in range(0, h, step):
        d.line([(0, y), (w, y)], fill=(*color, alpha))
    return layer


def grid_overlay(size, step=40, color=GRID, alpha=90):
    w, h = size
    layer = Image.new("RGBA", size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for x in range(0, w, step):
        d.line([(x, 0), (x, h)], fill=(*color, alpha))
    for y in range(0, h, step):
        d.line([(0, y), (w, y)], fill=(*color, alpha))
    return layer


def text_size(draw, text, f):
    box = draw.textbbox((0, 0), text, font=f)
    return box[2] - box[0], box[3] - box[1]


def draw_glitch_text(draw, xy, text, f, base, alt, offset=4):
    x, y = xy
    draw.text((x - offset, y), text, font=f, fill=alt)
    draw.text((x + offset, y), text, font=f, fill=alt)
    draw.text((x, y), text, font=f, fill=base)


def paste_rgba(base, layer, xy=(0, 0)):
    base.alpha_composite(layer, xy)


def quantize_frames(frames, colors=32):
    """Quantize a list of RGB frames to ONE shared palette so GIF LZW compresses well."""
    sample = Image.new("RGB", (sum(f.width for f in frames[:4]), max(f.height for f in frames[:4])))
    x = 0
    for f in frames[:4]:
        sample.paste(f, (x, 0))
        x += f.width
    palette_img = sample.quantize(colors=colors, method=Image.MEDIANCUT)
    out = []
    for f in frames:
        q = f.quantize(palette=palette_img, dither=Image.Dither.NONE)
        out.append(q)
    return out


def save_gif(path, frames, duration, colors=32, loop=0):
    pal = quantize_frames([f.convert("RGB") for f in frames], colors=colors)
    pal[0].save(path, save_all=True, append_images=pal[1:], duration=duration, loop=loop, disposal=2, optimize=True)
    return path


# --------------------------------------------------------------------------
# 01 — Dividers
# --------------------------------------------------------------------------
def divider(name: str, base_color, accent, frames=16, height=10, seed=1):
    w = 1280
    imgs = []
    rng = random.Random(seed)
    for fi in range(frames):
        img = Image.new("RGBA", (w, height), (*VOID, 255))
        d = ImageDraw.Draw(img)
        d.line([(0, height // 2), (w, height // 2)], fill=(*base_color, 255), width=2)
        # animated neon chase
        chase = (fi / frames) * w
        for k in range(6):
            cx = int((chase + k * 90) % w)
            cw = 60
            d.rectangle([cx, 1, cx + cw, height - 1], fill=(*accent, 255))
        # glitch tears
        for _ in range(3):
            gx = rng.randint(0, w - 80)
            gw = rng.randint(20, 80)
            gy = rng.randint(0, height - 3)
            d.rectangle([gx, gy, gx + gw, gy + 1], fill=(*GHOST, 220))
        # edge caps
        d.rectangle([0, 0, 60, height - 1], fill=(*base_color, 255))
        d.rectangle([w - 60, 0, w - 1, height - 1], fill=(*accent, 255))
        imgs.append(img.convert("P", palette=Image.ADAPTIVE, colors=64))
    out = ensure("separators", name)
    imgs[0].save(out, save_all=True, append_images=imgs[1:], duration=70, loop=0, disposal=2)
    return out


# --------------------------------------------------------------------------
# 01b — Section header banners (image typography)
# --------------------------------------------------------------------------
SECTION_HEADERS = [
    ("02", "SIGNAL FRAGMENT", PINK),
    ("03", "TERMINAL", CYAN),
    ("04", "TECH MATRIX", LIME),
    ("05", "PROJECT DIMENSION", ULTRA),
    ("06", "ACTIVITY FIELD", ORANGE),
    ("//", "END OF TRANSMISSION", YELLOW),
]


def section_header(num, title, accent):
    w, h = 1280, 72
    img = Image.new("RGBA", (w, h), (*VOID, 255))
    d = ImageDraw.Draw(img)
    paste_rgba(img, grid_overlay((w, h), 32, GRID, 70))

    # left number block
    d.rectangle([0, 0, 92, h], fill=(*accent, 255))
    fnum = font("display", 46)
    nw = d.textlength(num, font=fnum)
    d.text(((92 - nw) / 2, 8), num, font=fnum, fill=VOID)

    # top + bottom rules
    d.line([(92, 6), (w, 6)], fill=(*accent, 255), width=2)
    d.line([(92, h - 6), (w, h - 6)], fill=(*GHOST, 120), width=1)

    ft = font("display", 44)
    tw = d.textlength(title, font=ft)
    d.text((120, 10), title, font=ft, fill=GHOST)

    # trailing slashes / ticks
    x0 = 120 + tw + 26
    for i in range(6):
        c = accent if i % 2 == 0 else ULTRA
        d.rectangle([x0 + i * 18, 30, x0 + i * 18 + 10, 42], fill=(*c, 255))
    # right meta
    fm = font("mono", 15)
    meta = "/// STREAM : ACTIVE"
    mw = d.textlength(meta, font=fm)
    d.text((w - mw - 20, 29), meta, font=fm, fill=accent)

    img.convert("RGB").save(ensure("separators", f"header-{num.replace('//','end').strip()}.png"), optimize=True)
    return f"header-{num}"


# --------------------------------------------------------------------------
# 02 — Terminal session
# --------------------------------------------------------------------------
TERMINAL_LINES = [
    ("prompt", "who are you"),
    ("out", "MOHIT KUMAR"),
    ("out", "Developer  •  Terminal Dweller  •  Cybersecurity Enthusiast"),
    ("out", "Building tools that live in the command line."),
    ("blank", ""),
    ("prompt", "ls projects"),
    ("out", "ufosay               flying-saucer terminal animation      [python]"),
    ("out", "face-unlock          PAM facial auth for linux            [python]"),
    ("out", "apnadabba            full-stack delivery app               [typescript]"),
    ("out", "db-manager           database management interface         [ejs]"),
    ("out", "render               rendering engine experiments          [typescript]"),
    ("out", "anti_theft           anti-theft security tool              [html]"),
    ("out", "library-management   library management system             [python]"),
    ("blank", ""),
    ("prompt", "cat status"),
    ("out", "7 projects  •  5 languages  •  status: ONLINE"),
]


def terminal_frame(width, height, visible_lines, cursor_on, frame_i=0):
    img = Image.new("RGBA", (width, height), (*PANEL, 255))
    d = ImageDraw.Draw(img)
    paste_rgba(img, grid_overlay((width, height), 36, GRID, 70))

    # title bar
    d.rectangle([0, 0, width, 44], fill=(*VOID, 255))
    d.line([(0, 44), (width, 44)], fill=(*PINK, 255), width=2)
    for i, c in enumerate([PINK, YELLOW, LIME]):
        cx = 22 + i * 26
        d.ellipse([cx, 16, cx + 14, 30], fill=(*c, 255))
    t = font("mono", 18)
    title = "mohit31kumar@void: ~  —  zsh"
    tw = d.textlength(title, font=t)
    d.text(((width - tw) / 2, 14), title, font=t, fill=GHOST)

    mono = font("mono_reg", 18)
    mono_b = font("mono", 18)
    x = 26
    y = 72
    lh = 27
    last_end = (x, y)
    for kind, text in visible_lines:
        if kind == "blank":
            y += lh
            continue
        if kind == "prompt":
            p1 = "┌──["
            d.text((x, y), p1, font=mono, fill=PINK)
            px = x + d.textlength(p1, font=mono)
            host = "mohit31kumar@void"
            d.text((px, y), host, font=mono_b, fill=LIME)
            px += d.textlength(host, font=mono_b)
            d.text((px, y), "]", font=mono, fill=PINK)
            y += lh
            lead = "└─$ "
            d.text((x, y), "└─$", font=mono, fill=PINK)
            cx0 = x + d.textlength(lead, font=mono)
            d.text((cx0, y), text, font=mono_b, fill=CYAN)
            last_end = (cx0 + d.textlength(text, font=mono_b), y)
        else:
            d.text((x + 24, y), text, font=mono, fill=LIME)
            last_end = (x + 24 + d.textlength(text, font=mono), y)
        y += lh

    if cursor_on:
        cx, cy = last_end
        d.rectangle([cx + 3, cy + 4, cx + 15, cy + 23], fill=LIME)

    # scanlines
    paste_rgba(img, scanlines((width, height), 4, 46))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, width, 3], fill=(*CYAN, 180))
    d.rectangle([0, height - 3, width, height], fill=(*ULTRA, 180))
    return img


def terminal_animation():
    width, height = 900, 620
    total = len(TERMINAL_LINES)
    frames = []
    for s in range(total + 1):
        frames.append(terminal_frame(width, height, TERMINAL_LINES[:s], cursor_on=True, frame_i=s))
    # blink hold
    for b in range(4):
        frames.append(terminal_frame(width, height, TERMINAL_LINES, cursor_on=(b % 2 == 0), frame_i=99 + b))
    out = ensure("terminal", "terminal.gif")
    save_gif(out, frames, duration=420, colors=24)
    return out


def terminal_panel_bg():
    width, height = 900, 620
    img = Image.new("RGBA", (width, height), (*PANEL, 255))
    paste_rgba(img, grid_overlay((width, height), 36, GRID, 70))
    img.save(ensure("terminal", "panel-bg.png"))
    return "panel-bg"


def terminal_scanlines():
    width, height = 900, 620
    layer = scanlines((width, height), 3, 70)
    layer.save(ensure("terminal", "scanlines.png"))
    return "scanlines"


def cursor_gif():
    w, h = 12, 24
    on = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(on).rectangle([0, 0, w - 1, h - 1], fill=(*LIME, 255))
    off = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    out = ensure("terminal", "cursor.gif")
    on.convert("P").save(out, save_all=True, append_images=[off.convert("P")], duration=380, loop=0, disposal=2)
    return "cursor"


# --------------------------------------------------------------------------
# 03 — Tech panels
# --------------------------------------------------------------------------
def tech_panel(idx, label, accent):
    w, h = 380, 180
    img = Image.new("RGBA", (w, h), (*PANEL, 255))
    d = ImageDraw.Draw(img)
    paste_rgba(img, grid_overlay((w, h), 30, GRID, 80))
    # brutalist frame
    d.rectangle([0, 0, w - 1, h - 1], outline=(*GHOST, 255), width=3)
    d.rectangle([0, 0, w - 1, 52], fill=(*VOID, 255))
    d.rectangle([0, 0, w - 1, 52], outline=(*accent, 255), width=3)
    # corner brackets
    for (cx, cy, sx, sy) in [(0, 0, 1, 1), (w - 1, 0, -1, 1), (0, h - 1, 1, -1), (w - 1, h - 1, -1, -1)]:
        d.line([(cx, cy), (cx + sx * 26, cy)], fill=(*accent, 255), width=4)
        d.line([(cx, cy), (cx, cy + sy * 26)], fill=(*accent, 255), width=4)
    fnum = font("mono", 16)
    flab = font("display", 34)
    d.text((16, 16), f"0{idx}", font=fnum, fill=accent)
    lw, _ = text_size(d, label, flab)
    d.text(((w - lw) / 2, 92), label, font=flab, fill=GHOST)
    # accent underline
    d.rectangle([(w - lw) / 2, 136, (w + lw) / 2, 141], fill=(*accent, 255))
    img.save(ensure("tech", f"tech-panel-0{idx}.png"))
    return f"tech-panel-0{idx}"


# --------------------------------------------------------------------------
# 04 — Project thumbnails
# --------------------------------------------------------------------------
PROJECTS = [
    ("ufosay", "UFOSAY", "PYTHON", PINK, "saucer"),
    ("face-unlock", "FACE-UNLOCK", "PYTHON", CYAN, "face"),
    ("apnadabba", "APNADABBA", "TYPESCRIPT", LIME, "box"),
    ("db-manager", "DB-MANAGER", "EJS", ULTRA, "db"),
    ("render", "RENDER", "TYPESCRIPT", ORANGE, "cube"),
    ("anti_theft", "ANTI_THEFT", "HTML/JS", YELLOW, "shield"),
    ("library-management", "LIBRARY-MGMT", "PYTHON", PINK, "book"),
]


def project_thumb(slug, title, lang, accent, motif):
    w, h = 320, 180
    img = Image.new("RGBA", (w, h), (*VOID, 255))
    d = ImageDraw.Draw(img)
    paste_rgba(img, grid_overlay((w, h), 20, GRID, 90))
    # diagonal band
    d.polygon([(0, h), (w, 0), (w, 60), (0, h - 60 + 0)], fill=(*accent, 40))
    # motif wireframe
    cx, cy = w // 2, h // 2 - 6
    if motif == "saucer":
        d.ellipse([cx - 46, cy - 10, cx + 46, cy + 10], outline=(*accent, 255), width=3)
        d.ellipse([cx - 20, cy - 30, cx + 20, cy - 4], outline=(*GHOST, 220), width=3)
    elif motif == "face":
        d.rectangle([cx - 30, cy - 34, cx + 30, cy + 34], outline=(*accent, 255), width=3)
        d.line([(cx - 16, cy - 10), (cx - 4, cy - 10)], fill=(*GHOST, 230), width=3)
        d.line([(cx + 4, cy - 10), (cx + 16, cy - 10)], fill=(*GHOST, 230), width=3)
        d.line([(cx - 14, cy + 16), (cx + 14, cy + 16)], fill=(*GHOST, 230), width=3)
    elif motif == "box":
        d.polygon([(cx, cy - 34), (cx + 34, cy - 16), (cx + 34, cy + 16), (cx, cy + 34), (cx - 34, cy + 16), (cx - 34, cy - 16)], outline=(*accent, 255), width=3)
    elif motif == "db":
        d.ellipse([cx - 32, cy - 34, cx + 32, cy - 14], outline=(*accent, 255), width=3)
        d.line([(cx - 32, cy - 24), (cx - 32, cy + 24)], fill=(*accent, 255), width=3)
        d.line([(cx + 32, cy - 24), (cx + 32, cy + 24)], fill=(*accent, 255), width=3)
        d.arc([cx - 32, cy + 8, cx + 32, cy + 40], 0, 180, fill=(*accent, 255), width=3)
    elif motif == "cube":
        d.polygon([(cx, cy - 30), (cx + 30, cy - 12), (cx + 30, cy + 14), (cx, cy + 32), (cx - 30, cy + 14), (cx - 30, cy - 12)], outline=(*accent, 255), width=3)
        d.line([(cx, cy - 30), (cx, cy + 0)], fill=(*GHOST, 200), width=2)
        d.line([(cx - 30, cy - 12), (cx, cy + 0)], fill=(*GHOST, 200), width=2)
        d.line([(cx + 30, cy - 12), (cx, cy + 0)], fill=(*GHOST, 200), width=2)
    elif motif == "shield":
        d.polygon([(cx, cy - 36), (cx + 30, cy - 22), (cx + 30, cy + 6), (cx, cy + 36), (cx - 30, cy + 6), (cx - 30, cy - 22)], outline=(*accent, 255), width=3)
        d.line([(cx - 12, cy + 0), (cx - 2, cy + 12)], fill=(*GHOST, 230), width=3)
        d.line([(cx - 2, cy + 12), (cx + 16, cy - 12)], fill=(*GHOST, 230), width=3)
    elif motif == "book":
        d.rectangle([cx - 30, cy - 30, cx + 30, cy + 30], outline=(*accent, 255), width=3)
        d.line([(cx, cy - 30), (cx, cy + 30)], fill=(*accent, 255), width=2)
        for k in range(4):
            yy = cy - 18 + k * 12
            d.line([(cx - 22, yy), (cx - 6, yy)], fill=(*GHOST, 200), width=2)
            d.line([(cx + 6, yy), (cx + 22, yy)], fill=(*GHOST, 200), width=2)

    # bottom label bar
    d.rectangle([0, h - 42, w, h], fill=(*VOID, 235))
    d.line([(0, h - 42), (w, h - 42)], fill=(*accent, 255), width=3)
    ft = font("display_xb", 22)
    fl = font("mono", 14)
    d.text((12, h - 34), title, font=ft, fill=GHOST)
    lw, _ = text_size(d, lang, fl)
    d.text((w - lw - 12, h - 28), lang, font=fl, fill=accent)
    img = add_noise(img, 4, seed=abs(hash(slug)) % 1000)
    img.convert("RGB").save(ensure("projects", f"thumb-{slug}.png"), optimize=True)
    return f"thumb-{slug}"


# --------------------------------------------------------------------------
# 05 — Code fallback hero / footer
# --------------------------------------------------------------------------
def hero_static():
    w, h = 1280, 400
    img = Image.new("RGBA", (w, h), (*VOID, 255))
    d = ImageDraw.Draw(img)
    paste_rgba(img, grid_overlay((w, h), 40, GRID, 80))
    # accent shards
    d.polygon([(0, 0), (420, 0), (0, 300)], fill=(*PINK, 60))
    d.polygon([(w, h), (w - 460, h), (w, h - 260)], fill=(*ULTRA, 60))
    d.polygon([(w, 0), (w - 260, 0), (w, 180)], fill=(*CYAN, 45))
    # frame
    d.rectangle([16, 16, w - 16, h - 16], outline=(*GHOST, 255), width=3)
    d.rectangle([16, 16, w - 16, 66], fill=(*VOID, 255), outline=(*PINK, 255), width=3)
    fm = font("mono", 18)
    d.text((34, 32), "/// SECTION 01", font=fm, fill=PINK)
    d.text((w - 300, 32), "TRANSMISSION: LIVE", font=fm, fill=LIME)

    fbig = font("display", 150)
    fsub = font("mono", 24)
    title = "MOHIT KUMAR"
    tw, _ = text_size(d, title, fbig)
    draw_glitch_text(d, ((w - tw) / 2, 118), title, fbig, GHOST, CYAN, offset=5)
    sub = "// TERMINAL DWELLER // CYBERSEC"
    sw, _ = text_size(d, sub, fsub)
    d.text(((w - sw) / 2, 292), sub, font=fsub, fill=LIME)
    # status ticks
    for i in range(12):
        col = LIME if i % 3 else PINK
        d.rectangle([60 + i * 30, h - 52, 74 + i * 30, h - 40], fill=(*col, 255))
    d.text((w - 250, h - 52), "1280 x 400 // RENDER OK", font=font("mono", 15), fill=GHOST)
    paste_rgba(img, scanlines((w, h), 4, 40))
    img.convert("RGB").save(ensure("hero", "hero-static.png"))
    return "hero-static"


def hero_animated():
    w, h = 1280, 400
    frames = []
    fbig = font("display", 150)
    fsub = font("mono", 24)
    fm = font("mono", 18)
    title = "MOHIT KUMAR"
    for fi in range(20):
        img = Image.new("RGBA", (w, h), (*VOID, 255))
        d = ImageDraw.Draw(img)
        paste_rgba(img, grid_overlay((w, h), 40, GRID, 80))
        d.polygon([(0, 0), (420, 0), (0, 300)], fill=(*PINK, 60))
        d.polygon([(w, h), (w - 460, h), (w, h - 260)], fill=(*ULTRA, 60))
        d.polygon([(w, 0), (w - 260, 0), (w, 180)], fill=(*CYAN, 45))
        d.rectangle([16, 16, w - 16, h - 16], outline=(*GHOST, 255), width=3)
        d.rectangle([16, 16, w - 16, 66], fill=(*VOID, 255), outline=(*PINK, 255), width=3)
        d.text((34, 32), "/// SECTION 01", font=fm, fill=PINK)
        dash = "-" * (fi % 4 + 1)
        d.text((w - 320, 32), f"TRANSMISSION: LIVE {dash}", font=fm, fill=LIME)
        tw, _ = text_size(d, title, fbig)
        gx = (w - tw) / 2
        glitch = (fi % 5 == 0)
        if glitch:
            shift = random.randint(-8, 8)
            d.text((gx + shift - 6, 118), title, font=fbig, fill=PINK)
            d.text((gx - shift + 6, 118), title, font=fbig, fill=CYAN)
        draw_glitch_text(d, (gx, 118), title, fbig, GHOST, CYAN, offset=5 if glitch else 3)
        sub = "// TERMINAL DWELLER // CYBERSEC"
        sw, _ = text_size(d, sub, fsub)
        d.text(((w - sw) / 2, 292), sub, font=fsub, fill=LIME)
        # moving scan highlight
        sy = int((fi / 20) * h)
        d.rectangle([17, sy, w - 17, sy + 3], fill=(*GHOST, 90))
        for i in range(12):
            on = (i + fi) % 3 != 0
            col = LIME if on else PINK
            d.rectangle([60 + i * 30, h - 52, 74 + i * 30, h - 40], fill=(*col, 255))
        d.text((w - 250, h - 52), "1280 x 400 // RENDER OK", font=font("mono", 15), fill=GHOST)
        paste_rgba(img, scanlines((w, h), 4, 40))
        frames.append(img)
    out = ensure("hero", "hero.gif")
    save_gif(out, frames, duration=110, colors=48)
    return "hero.gif"


def footer_static():
    w, h = 1280, 180
    img = Image.new("RGBA", (w, h), (*VOID, 255))
    d = ImageDraw.Draw(img)
    paste_rgba(img, grid_overlay((w, h), 36, GRID, 70))
    d.rectangle([12, 12, w - 12, h - 12], outline=(*ULTRA, 255), width=3)
    fbig = font("display", 62)
    fm = font("mono", 18)
    title = "END OF TRANSMISSION"
    tw, _ = text_size(d, title, fbig)
    draw_glitch_text(d, ((w - tw) / 2, 34), title, fbig, GHOST, PINK, offset=4)
    sub = "// SIGNAL LOST // MOHIT KUMAR // 2024 — NOW"
    sw, _ = text_size(d, sub, fm)
    d.text(((w - sw) / 2, 118), sub, font=fm, fill=CYAN)
    paste_rgba(img, scanlines((w, h), 4, 44))
    img.convert("RGB").save(ensure("footer", "footer-static.png"))
    return "footer-static"


def footer_animated():
    w, h = 1280, 180
    frames = []
    fbig = font("display", 62)
    fm = font("mono", 18)
    title = "END OF TRANSMISSION"
    for fi in range(18):
        img = Image.new("RGBA", (w, h), (*VOID, 255))
        d = ImageDraw.Draw(img)
        paste_rgba(img, grid_overlay((w, h), 36, GRID, 70))
        d.rectangle([12, 12, w - 12, h - 12], outline=(*ULTRA, 255), width=3)
        tw, _ = text_size(d, title, fbig)
        glitch = (fi % 4 == 0)
        if glitch:
            sh = random.randint(-7, 7)
            d.text(((w - tw) / 2 + sh, 34), title, font=fbig, fill=PINK)
            d.text(((w - tw) / 2 - sh, 34), title, font=fbig, fill=CYAN)
        draw_glitch_text(d, ((w - tw) / 2, 34), title, fbig, GHOST, PINK, offset=3 if glitch else 2)
        sub = "// SIGNAL LOST // MOHIT KUMAR // 2024 — NOW"
        sw, _ = text_size(d, sub, fm)
        d.text(((w - sw) / 2, 118), sub, font=fm, fill=CYAN)
        # falling blocks
        for k in range(20):
            bx = (k * 64 + fi * 9) % w
            by = (fi * 11 + k * 23) % h
            col = NEON[k % len(NEON)]
            d.rectangle([bx, by, bx + 4, by + 18], fill=(*col, 120))
        paste_rgba(img, scanlines((w, h), 4, 44))
        frames.append(img)
    out = ensure("footer", "footer.gif")
    save_gif(out, frames, duration=120, colors=40)
    return "footer.gif"


# --------------------------------------------------------------------------
# 06 — Activity fallback (isometric contribution field)
# --------------------------------------------------------------------------
def contrib_static():
    w, h = 800, 400
    img = Image.new("RGBA", (w, h), (*VOID, 255))
    d = ImageDraw.Draw(img)
    paste_rgba(img, grid_overlay((w, h), 40, GRID, 60))
    cols, rows = 30, 7
    cw, ch = 20, 20
    ox, oy = 120, 150
    rng = random.Random(42)
    for r in range(rows):
        for c in range(cols):
            level = rng.choice([0, 0, 1, 1, 2, 3])
            if level == 0:
                continue
            iso_x = ox + (c - r) * (cw * 0.9) + 300
            iso_y = oy + (c + r) * (ch * 0.5)
            bh = level * 16
            col = [LIME, CYAN, PINK, ULTRA][min(level, 3) % 4]
            top = [(iso_x, iso_y), (iso_x + cw, iso_y - ch * 0.5), (iso_x + 2 * cw, iso_y), (iso_x + cw, iso_y + ch * 0.5)]
            # left face
            d.polygon([(iso_x, iso_y), (iso_x + cw, iso_y + ch * 0.5), (iso_x + cw, iso_y + ch * 0.5 - bh), (iso_x, iso_y - bh)], fill=tuple(int(v * 0.6) for v in col))
            # right face
            d.polygon([(iso_x + cw, iso_y + ch * 0.5), (iso_x + 2 * cw, iso_y), (iso_x + 2 * cw, iso_y - bh), (iso_x + cw, iso_y + ch * 0.5 - bh)], fill=tuple(int(v * 0.4) for v in col))
            # top
            d.polygon([(t[0], t[1] - bh) for t in top], fill=col)
    d.text((28, 26), "// CONTRIBUTION FIELD // ISOMETRIC", font=font("mono", 18), fill=CYAN)
    paste_rgba(img, scanlines((w, h), 4, 40))
    img.convert("RGB").save(ensure("activity", "contrib-3d-static.png"))
    return "contrib-3d-static"


def contrib_animated():
    w, h = 800, 400
    cols, rows = 30, 7
    cw, ch = 20, 20
    ox, oy = 120, 150
    rng = random.Random(42)
    field = [[rng.choice([0, 0, 1, 1, 2, 3]) for _ in range(cols)] for _ in range(rows)]
    frames = []
    for fi in range(20):
        img = Image.new("RGBA", (w, h), (*VOID, 255))
        d = ImageDraw.Draw(img)
        paste_rgba(img, grid_overlay((w, h), 40, GRID, 60))
        for r in range(rows):
            for c in range(cols):
                level = field[r][c]
                if level == 0:
                    continue
                grow = min(1.0, max(0.0, (fi - (c + r) * 0.4) / 8.0))
                if grow <= 0:
                    continue
                iso_x = ox + (c - r) * (cw * 0.9) + 300
                iso_y = oy + (c + r) * (ch * 0.5)
                bh = level * 16 * grow
                col = [LIME, CYAN, PINK, ULTRA][min(level, 3) % 4]
                top = [(iso_x, iso_y), (iso_x + cw, iso_y - ch * 0.5), (iso_x + 2 * cw, iso_y), (iso_x + cw, iso_y + ch * 0.5)]
                d.polygon([(iso_x, iso_y), (iso_x + cw, iso_y + ch * 0.5), (iso_x + cw, iso_y + ch * 0.5 - bh), (iso_x, iso_y - bh)], fill=tuple(int(v * 0.6) for v in col))
                d.polygon([(iso_x + cw, iso_y + ch * 0.5), (iso_x + 2 * cw, iso_y), (iso_x + 2 * cw, iso_y - bh), (iso_x + cw, iso_y + ch * 0.5 - bh)], fill=tuple(int(v * 0.4) for v in col))
                d.polygon([(t[0], t[1] - bh) for t in top], fill=col)
        d.text((28, 26), "// CONTRIBUTION FIELD // ISOMETRIC", font=font("mono", 18), fill=CYAN)
        paste_rgba(img, scanlines((w, h), 4, 40))
        frames.append(img)
    for _ in range(6):
        frames.append(frames[-1])
    out = ensure("activity", "contrib-3d.gif")
    save_gif(out, frames, duration=140, colors=40)
    return "contrib-3d"


# --------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------
def main():
    done = []
    done.append(divider("divider-01.gif", PINK, CYAN, seed=1))
    done.append(divider("divider-02.gif", ULTRA, LIME, seed=7))
    for num, title, accent in SECTION_HEADERS:
        done.append(section_header(num, title, accent))
    done.append(terminal_animation())
    done.append(terminal_panel_bg())
    done.append(terminal_scanlines())
    done.append(cursor_gif())
    for i, (label, accent) in enumerate([
        ("LANGUAGES", PINK),
        ("FRAMEWORKS", CYAN),
        ("TOOLS / INFRA", LIME),
        ("DOMAINS", ULTRA),
    ], start=1):
        done.append(tech_panel(i, label, accent))
    for slug, title, lang, accent, motif in PROJECTS:
        done.append(project_thumb(slug, title, lang, accent, motif))
    done.append(hero_static())
    done.append(hero_animated())
    done.append(footer_static())
    done.append(footer_animated())
    done.append(contrib_static())
    done.append(contrib_animated())
    print(f"generated {len(done)} assets:")
    for d in done:
        print("  -", d)


if __name__ == "__main__":
    main()
