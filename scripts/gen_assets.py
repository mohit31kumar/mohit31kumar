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
# 03 — Tech panels (compact technology-logo matrix)
# --------------------------------------------------------------------------
TECH_PANEL_W, TECH_PANEL_H = 380, 300

# Editable, configurable tech lists. Edit names / icon keys freely — no
# proficiency, level, or skill claim is encoded anywhere. Icon keys map to the
# vector-style glyphs drawn below. If a real logo exists at
# `assets/tech/logos/<slug>.png` (or .webp) it is used instead of the glyph,
# where slug = name lowercased with non-alphanumerics replaced by "-".
TECH_MATRIX = [
    {"num": 1, "label": "LANGUAGES", "accent": PINK, "items": [
        ("JavaScript", "js"), ("TypeScript", "ts"), ("Python", "py"),
        ("HTML", "html"), ("CSS", "css"), ("SQL", "sql"),
    ]},
    {"num": 2, "label": "FRAMEWORKS", "accent": CYAN, "items": [
        ("React", "react"), ("Node.js", "node"), ("Express", "express"),
        ("NestJS", "nestjs"), ("React Native", "reactnative"),
    ]},
    {"num": 3, "label": "TOOLS / INFRA", "accent": LIME, "items": [
        ("Git", "git"), ("GitHub", "github"), ("Docker", "docker"),
        ("MySQL", "mysql"), ("PostgreSQL", "postgres"), ("Redis", "redis"),
    ]},
    {"num": 4, "label": "DOMAINS", "accent": ULTRA, "items": [
        ("Full-stack", "stack"), ("REST APIs", "rest"), ("Databases", "db"),
        ("Authentication", "auth"), ("Security", "shield"),
    ]},
]


def _slug(name: str) -> str:
    out = "".join(ch if ch.isalnum() else "-" for ch in name.lower())
    while "--" in out:
        out = out.replace("--", "-")
    return out.strip("-")


def _load_logo(name: str):
    """Optional real logo override. Returns an RGBA image or None (graceful)."""
    base = os.path.join(ASSETS, "tech", "logos", _slug(name))
    for ext in (".png", ".webp"):
        p = base + ext
        if os.path.exists(p):
            try:
                return Image.open(p).convert("RGBA")
            except Exception:
                return None
    return None


def fit_font(kind: str, text: str, max_w: float, start: int, min_size: int = 9):
    for s in range(start, min_size - 1, -1):
        f = font(kind, s)
        if f.getlength(text) <= max_w:
            return f
    return font(kind, min_size)


def _rot_ellipse(img, cx, cy, rx, ry, angle, color, width=3):
    size = int(max(rx, ry)) * 2 + 10
    layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ld.ellipse([size // 2 - rx, size // 2 - ry, size // 2 + rx, size // 2 + ry],
               outline=(*color, 255), width=width)
    layer = layer.rotate(angle, resample=Image.BICUBIC)
    img.alpha_composite(layer, (int(cx - size / 2), int(cy - size / 2)))


def _shield(d, cx, cy, s, color, width=3):
    pts = [(cx, cy - s), (cx + s, cy - s * 0.45), (cx + s, cy + s * 0.35),
           (cx, cy + s), (cx - s, cy + s * 0.35), (cx - s, cy - s * 0.45)]
    d.polygon(pts, outline=(*color, 255), width=width)


def _cylinder(d, cx, cy, s, color, width=3):
    rx, ry = s, s * 0.34
    d.ellipse([cx - rx, cy - s, cx + rx, cy - s + 2 * ry], outline=(*color, 255), width=width)
    d.line([(cx - rx, cy - s + ry), (cx - rx, cy + s - ry)], fill=(*color, 255), width=width)
    d.line([(cx + rx, cy - s + ry), (cx + rx, cy + s - ry)], fill=(*color, 255), width=width)
    d.arc([cx - rx, cy + s - 2 * ry, cx + rx, cy + s], 0, 180, fill=(*color, 255), width=width)


def _hexagon(d, cx, cy, s, color, width=3):
    pts = [(cx + s * math.cos(math.radians(-90 + 60 * k)),
            cy + s * math.sin(math.radians(-90 + 60 * k))) for k in range(6)]
    d.polygon(pts, outline=(*color, 255), width=width)


def _ctext(d, cx, cy, text, f, color):
    d.text((cx, cy), text, font=f, fill=(*color, 255), anchor="mm")


def draw_tech_icon(img, d, key, cx, cy, s, color):
    """Clean vector-style glyphs. Unknown keys fall back to a monogram."""
    w = 3
    if key in ("js", "ts"):
        d.rounded_rectangle([cx - s, cy - s, cx + s, cy + s], radius=5,
                            outline=(*color, 255), width=w)
        _ctext(d, cx, cy, key.upper(), font("mono", int(s * 0.9)), color)
    elif key == "py":
        d.rounded_rectangle([cx - s, cy - s, cx + s * 0.05, cy + s * 0.05], radius=6,
                            outline=(*color, 255), width=w)
        d.rounded_rectangle([cx - s * 0.05, cy - s * 0.05, cx + s, cy + s], radius=6,
                            outline=(*color, 255), width=w)
        d.ellipse([cx - s * 0.55, cy - s * 0.55, cx - s * 0.3, cy - s * 0.3], fill=(*color, 255))
        d.ellipse([cx + s * 0.3, cy + s * 0.3, cx + s * 0.55, cy + s * 0.55], fill=(*color, 255))
    elif key == "html":
        _shield(d, cx, cy, s, color, w)
        _ctext(d, cx, cy + s * 0.05, "5", font("mono", int(s * 0.95)), color)
    elif key == "css":
        _shield(d, cx, cy, s, color, w)
        _ctext(d, cx, cy + s * 0.05, "3", font("mono", int(s * 0.95)), color)
    elif key == "sql":
        _cylinder(d, cx, cy, s, color, w)
        _ctext(d, cx, cy + s * 0.05, "SQL", font("mono", int(s * 0.55)), color)
    elif key == "react":
        _rot_ellipse(img, cx, cy, int(s), int(s * 0.36), 0, color, w)
        _rot_ellipse(img, cx, cy, int(s), int(s * 0.36), 60, color, w)
        _rot_ellipse(img, cx, cy, int(s), int(s * 0.36), 120, color, w)
        d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=(*color, 255))
    elif key == "node":
        _hexagon(d, cx, cy, s, color, w)
        _ctext(d, cx, cy + s * 0.02, "JS", font("mono", int(s * 0.6)), color)
    elif key == "express":
        _ctext(d, cx, cy, "ex", font("mono", int(s * 1.2)), color)
    elif key == "nestjs":
        _hexagon(d, cx, cy, s, color, w)
        _ctext(d, cx, cy, "N", font("mono", int(s * 0.9)), color)
    elif key == "reactnative":
        _rot_ellipse(img, cx, cy, int(s), int(s * 0.34), 0, color, w)
        _rot_ellipse(img, cx, cy, int(s), int(s * 0.34), 60, color, w)
        _rot_ellipse(img, cx, cy, int(s), int(s * 0.34), 120, color, w)
        d.rounded_rectangle([cx - s * 0.22, cy - s * 0.5, cx + s * 0.22, cy + s * 0.5],
                            radius=3, outline=(*GHOST, 255), width=w)
    elif key == "git":
        top = (cx - s * 0.45, cy - s * 0.55)
        bot = (cx - s * 0.45, cy + s * 0.55)
        br = (cx + s * 0.5, cy - s * 0.02)
        d.line([top, bot], fill=(*color, 255), width=w)
        d.line([(cx - s * 0.45, cy), (br[0], br[1] + s * 0.1)], fill=(*color, 255), width=w)
        for (x, y) in (top, bot, br):
            d.ellipse([x - 4, y - 4, x + 4, y + 4], outline=(*color, 255), width=w)
    elif key == "github":
        d.ellipse([cx - s * 0.72, cy - s * 0.6, cx + s * 0.72, cy + s * 0.7],
                  outline=(*color, 255), width=w)
        d.polygon([(cx - s * 0.66, cy - s * 0.35), (cx - s * 0.34, cy - s * 0.92),
                   (cx - s * 0.08, cy - s * 0.54)], fill=(*color, 255))
        d.polygon([(cx + s * 0.66, cy - s * 0.35), (cx + s * 0.34, cy - s * 0.92),
                   (cx + s * 0.08, cy - s * 0.54)], fill=(*color, 255))
        d.ellipse([cx - s * 0.36, cy - s * 0.12, cx - s * 0.14, cy + s * 0.12], fill=(*color, 255))
        d.ellipse([cx + s * 0.14, cy - s * 0.12, cx + s * 0.36, cy + s * 0.12], fill=(*color, 255))
    elif key == "docker":
        bw, bh = s * 0.34, s * 0.26
        for i in range(3):
            x = cx - s * 0.5 + i * bw * 1.06
            d.rectangle([x, cy - s * 0.08, x + bw, cy - s * 0.08 + bh],
                        outline=(*color, 255), width=w)
        d.arc([cx - s, cy - s * 0.06, cx + s * 1.05, cy + s * 0.95], 180, 360,
              fill=(*color, 255), width=w)
        d.line([(cx - s, cy + s * 0.44), (cx - s * 0.2, cy + s * 0.44)], fill=(*color, 255), width=w)
        d.polygon([(cx + s * 0.95, cy - s * 0.06), (cx + s * 1.2, cy - s * 0.42),
                   (cx + s * 1.2, cy + s * 0.12)], fill=(*color, 255))
    elif key in ("mysql", "postgres"):
        _cylinder(d, cx, cy, s, color, w)
        _ctext(d, cx, cy + s * 0.05, "MY" if key == "mysql" else "PG",
               font("mono", int(s * 0.5)), color)
    elif key == "redis":
        for yy in (-s * 0.5, 0.0, s * 0.5):
            d.ellipse([cx - s * 0.8, cy + yy - s * 0.2, cx + s * 0.8, cy + yy + s * 0.2],
                      outline=(*color, 255), width=w)
    elif key == "stack":
        for yy in (-s * 0.45, 0.0, s * 0.45):
            d.polygon([(cx, cy + yy - s * 0.26), (cx + s * 0.85, cy + yy),
                       (cx, cy + yy + s * 0.26), (cx - s * 0.85, cy + yy)],
                      outline=(*color, 255), width=w)
    elif key == "rest":
        f = font("mono", int(s * 1.3))
        d.text((cx - s * 0.7, cy), "{", font=f, fill=(*color, 255), anchor="rm")
        d.text((cx + s * 0.7, cy), "}", font=f, fill=(*color, 255), anchor="lm")
        d.line([(cx - s * 0.28, cy), (cx + s * 0.28, cy)], fill=(*color, 255), width=w)
        d.polygon([(cx + s * 0.1, cy - s * 0.14), (cx + s * 0.34, cy),
                   (cx + s * 0.1, cy + s * 0.14)], fill=(*color, 255))
    elif key == "db":
        _cylinder(d, cx, cy, s, color, w)
    elif key == "auth":
        d.rounded_rectangle([cx - s * 0.68, cy - s * 0.12, cx + s * 0.68, cy + s * 0.8],
                            radius=4, outline=(*color, 255), width=w)
        d.arc([cx - s * 0.44, cy - s * 0.88, cx + s * 0.44, cy - s * 0.05], 180, 360,
              fill=(*color, 255), width=w)
        d.ellipse([cx - 3, cy + s * 0.18, cx + 3, cy + s * 0.18 + 7], fill=(*color, 255))
    elif key == "shield":
        _shield(d, cx, cy, s, color, w)
        d.line([(cx - s * 0.4, cy + s * 0.02), (cx - s * 0.08, cy + s * 0.34)],
               fill=(*color, 255), width=w)
        d.line([(cx - s * 0.08, cy + s * 0.34), (cx + s * 0.44, cy - s * 0.34)],
               fill=(*color, 255), width=w)
    else:
        _ctext(d, cx, cy, "".join(ch for ch in key.upper() if ch.isalnum())[:2],
               font("mono", int(s * 1.0)), color)


def tech_panel(panel):
    num = panel["num"]
    label = panel["label"]
    accent = panel["accent"]
    items = panel["items"]
    w, h = TECH_PANEL_W, TECH_PANEL_H
    img = Image.new("RGBA", (w, h), (*PANEL, 255))
    d = ImageDraw.Draw(img)
    paste_rgba(img, grid_overlay((w, h), 30, GRID, 60))

    # brutalist outer frame + corner brackets
    d.rectangle([1, 1, w - 2, h - 2], outline=(*GHOST, 255), width=2)
    for (bx, by, sx, sy) in [(3, 3, 1, 1), (w - 4, 3, -1, 1), (3, h - 4, 1, -1), (w - 4, h - 4, -1, -1)]:
        d.line([(bx, by), (bx + sx * 20, by)], fill=(*accent, 255), width=4)
        d.line([(bx, by), (bx, by + sy * 20)], fill=(*accent, 255), width=4)

    # header
    hh = 54
    d.rectangle([0, 0, w, hh], fill=(*VOID, 255))
    d.rectangle([0, 0, 54, hh], fill=(*accent, 255))
    _ctext(d, 27, hh / 2, f"{num:02d}", font("display", 34), VOID)
    d.text((70, hh / 2), label, font=font("display_xb", 26), fill=GHOST, anchor="lm")
    d.text((w - 16, hh / 2), f"{len(items):02d} NODE", font=font("mono", 13),
           fill=(*accent, 255), anchor="rm")
    d.line([(0, hh), (w, hh)], fill=(*accent, 255), width=2)

    # item matrix (3 columns x N rows)
    cols = 3
    x0 = 18
    top = hh + 16
    bottom = h - 16
    cw = (w - 2 * x0) / cols
    rows = max(1, math.ceil(len(items) / cols))
    rh = (bottom - top) / rows
    for i, (name, key) in enumerate(items):
        r, c = divmod(i, cols)
        ccx = x0 + c * cw + cw / 2
        base = top + r * rh
        icy = base + 38
        logo = _load_logo(name)
        if logo is not None:
            lw0, lh0 = logo.size
            scale = min(46 / lw0, 46 / lh0)
            nw, nh = max(1, int(lw0 * scale)), max(1, int(lh0 * scale))
            img.alpha_composite(logo.resize((nw, nh), Image.LANCZOS),
                                (int(ccx - nw / 2), int(icy - nh / 2)))
        else:
            draw_tech_icon(img, d, key, ccx, icy, 22, accent)
        # index tick (design metadata)
        d.text((x0 + c * cw + 4, base + 4), f"{i + 1:02d}", font=font("mono", 10),
               fill=(*accent, 255))
        # auto-fit label + accent underline
        lf = fit_font("mono", name, cw - 10, 13, 9)
        d.text((ccx, base + 76), name, font=lf, fill=GHOST, anchor="mm")
        lwid = lf.getlength(name)
        d.line([(ccx - lwid / 2, base + 86), (ccx + lwid / 2, base + 86)],
               fill=(*accent, 255), width=2)

    img.convert("RGB").save(ensure("tech", f"tech-panel-0{num}.png"), optimize=True)
    return f"tech-panel-0{num}"


# --------------------------------------------------------------------------
# 04 — Project thumbnails (canonical 640x360 / 16:9)
# --------------------------------------------------------------------------
THUMB_W, THUMB_H = 640, 360
THUMB_SRC_DIR = os.path.join(ASSETS, "projects", "src")

PROJECTS = [
    ("ufosay", "UFOSAY", "PYTHON", PINK, "saucer"),
    ("face-unlock", "FACE-UNLOCK", "PYTHON", CYAN, "face"),
    ("apnadabba", "APNADABBA", "TYPESCRIPT", LIME, "box"),
    ("db-manager", "DB-MANAGER", "EJS", ULTRA, "db"),
    ("render", "RENDER", "TYPESCRIPT", ORANGE, "cube"),
    ("anti_theft", "ANTI_THEFT", "HTML/JS", YELLOW, "shield"),
    ("library-management", "LIBRARY-MGMT", "PYTHON", PINK, "book"),
]


def _thumb_source(slug):
    """Optional real project image at assets/projects/src/<slug>.{png,jpg,jpeg,webp}.
    If present it is letterboxed into the canonical canvas instead of the
    generated placeholder, so real screenshots are never overwritten."""
    for ext in (".png", ".jpg", ".jpeg", ".webp"):
        p = os.path.join(THUMB_SRC_DIR, slug + ext)
        if os.path.exists(p):
            return p
    return None


def contain_fit(img, size, bg=VOID):
    """Scale to fit inside size preserving aspect ratio, centered on bg (no crop)."""
    tw, th = size
    iw, ih = img.size
    scale = min(tw / iw, th / ih)
    nw, nh = max(1, round(iw * scale)), max(1, round(ih * scale))
    out = Image.new("RGBA", (tw, th), (*bg, 255))
    out.alpha_composite(img.resize((nw, nh), Image.LANCZOS), ((tw - nw) // 2, (th - nh) // 2))
    return out


def project_thumb(slug, title, lang, accent, motif):
    base_w, base_h = 320, 180
    w, h = THUMB_W, THUMB_H
    k = w / base_w

    def S(v):
        return int(round(v * k))

    src = _thumb_source(slug)
    if src is not None:
        # Real image: letterbox into the canonical canvas, keep it uncropped.
        art = contain_fit(Image.open(src).convert("RGBA"), (w, h))
        ImageDraw.Draw(art).rectangle([1, 1, w - 2, h - 2], outline=(*accent, 255), width=2)
        art.convert("RGB").save(ensure("projects", f"thumb-{slug}.png"), optimize=True)
        return f"thumb-{slug}"

    img = Image.new("RGBA", (w, h), (*VOID, 255))
    d = ImageDraw.Draw(img)
    paste_rgba(img, grid_overlay((w, h), S(20), GRID, 90))

    def pt(*pairs):
        return [(S(x), S(y)) for x, y in pairs]

    cx, cy = base_w // 2, base_h // 2 - 6

    def rbox(x0, y0, x1, y1):
        return [S(cx + x0), S(cy + y0), S(cx + x1), S(cy + y1)]

    lw3, lw2 = max(1, S(3)), max(1, S(2))

    # diagonal band
    d.polygon(pt((0, base_h), (base_w, 0), (base_w, 60), (0, base_h - 60)), fill=(*accent, 40))

    if motif == "saucer":
        d.ellipse(rbox(-46, -10, 46, 10), outline=(*accent, 255), width=lw3)
        d.ellipse(rbox(-20, -30, 20, -4), outline=(*GHOST, 220), width=lw3)
    elif motif == "face":
        d.rectangle(rbox(-30, -34, 30, 34), outline=(*accent, 255), width=lw3)
        d.line(pt((cx - 16, cy - 10), (cx - 4, cy - 10)), fill=(*GHOST, 230), width=lw3)
        d.line(pt((cx + 4, cy - 10), (cx + 16, cy - 10)), fill=(*GHOST, 230), width=lw3)
        d.line(pt((cx - 14, cy + 16), (cx + 14, cy + 16)), fill=(*GHOST, 230), width=lw3)
    elif motif == "box":
        d.polygon(pt((cx, cy - 34), (cx + 34, cy - 16), (cx + 34, cy + 16),
                     (cx, cy + 34), (cx - 34, cy + 16), (cx - 34, cy - 16)),
                  outline=(*accent, 255), width=lw3)
    elif motif == "db":
        d.ellipse(rbox(-32, -34, 32, -14), outline=(*accent, 255), width=lw3)
        d.line(pt((cx - 32, cy - 24), (cx - 32, cy + 24)), fill=(*accent, 255), width=lw3)
        d.line(pt((cx + 32, cy - 24), (cx + 32, cy + 24)), fill=(*accent, 255), width=lw3)
        d.arc(rbox(-32, 8, 32, 40), 0, 180, fill=(*accent, 255), width=lw3)
    elif motif == "cube":
        d.polygon(pt((cx, cy - 30), (cx + 30, cy - 12), (cx + 30, cy + 14),
                     (cx, cy + 32), (cx - 30, cy + 14), (cx - 30, cy - 12)),
                  outline=(*accent, 255), width=lw3)
        d.line(pt((cx, cy - 30), (cx, cy + 0)), fill=(*GHOST, 200), width=lw2)
        d.line(pt((cx - 30, cy - 12), (cx, cy + 0)), fill=(*GHOST, 200), width=lw2)
        d.line(pt((cx + 30, cy - 12), (cx, cy + 0)), fill=(*GHOST, 200), width=lw2)
    elif motif == "shield":
        d.polygon(pt((cx, cy - 36), (cx + 30, cy - 22), (cx + 30, cy + 6),
                     (cx, cy + 36), (cx - 30, cy + 6), (cx - 30, cy - 22)),
                  outline=(*accent, 255), width=lw3)
        d.line(pt((cx - 12, cy + 0), (cx - 2, cy + 12)), fill=(*GHOST, 230), width=lw3)
        d.line(pt((cx - 2, cy + 12), (cx + 16, cy - 12)), fill=(*GHOST, 230), width=lw3)
    elif motif == "book":
        d.rectangle(rbox(-30, -30, 30, 30), outline=(*accent, 255), width=lw3)
        d.line(pt((cx, cy - 30), (cx, cy + 30)), fill=(*accent, 255), width=lw2)
        for i in range(4):
            yy = cy - 18 + i * 12
            d.line(pt((cx - 22, yy), (cx - 6, yy)), fill=(*GHOST, 200), width=lw2)
            d.line(pt((cx + 6, yy), (cx + 22, yy)), fill=(*GHOST, 200), width=lw2)

    # bottom label bar
    d.rectangle([0, S(base_h - 42), w, h], fill=(*VOID, 235))
    d.line(pt((0, base_h - 42), (base_w, base_h - 42)), fill=(*accent, 255), width=lw3)
    ft = font("display_xb", S(22))
    fl = font("mono", S(14))
    d.text((S(12), S(base_h - 34)), title, font=ft, fill=GHOST)
    lw = fl.getlength(lang)
    d.text((w - lw - S(12), S(base_h - 28)), lang, font=fl, fill=accent)

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
# 06 — Activity field (contribution-city skyline, ported from ignore.py)
# --------------------------------------------------------------------------
def _load_contribution_levels(cols=30, rows=7):
    """Load optional real contribution levels from assets/activity/contributions.json.

    Expected format: {"weeks": [[0, 1, 2, ...], ...]} where each week has
    seven values from 0 to 4 (Sunday through Saturday). This file must contain
    data you obtained from your own GitHub account. If absent, use a fixed,
    clearly labelled illustrative pattern instead.
    """
    import json
    path = os.path.join(ASSETS, "activity", "contributions.json")
    if os.path.isfile(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                payload = json.load(f)
            weeks = payload.get("weeks", [])
            grid = [[0 for _ in range(cols)] for _ in range(rows)]
            for c, week in enumerate(weeks[-cols:]):
                for r, value in enumerate(week[:rows]):
                    grid[r][cols - min(cols, len(weeks)) + c] = max(0, min(4, int(value)))
            return grid, True
        except (OSError, ValueError, TypeError, AttributeError):
            pass
    rng = random.Random(42)
    return [[rng.choice([0, 0, 0, 1, 1, 2, 3, 4]) for _ in range(cols)] for _ in range(rows)], False


def _draw_activity_field(img, levels, progress=1.0, is_real=False):
    """Render a contribution-city skyline inspired by an isometric cyberpunk city."""
    w, h = img.size
    d = ImageDraw.Draw(img)
    rng = random.Random(431)

    # Background grid and distant stars.
    paste_rgba(img, grid_overlay((w, h), 40, GRID, 72))
    d = ImageDraw.Draw(img)
    for _ in range(115):
        sx, sy = rng.randint(520, w - 28), rng.randint(48, 155)
        shade = rng.choice([(45, 65, 95, 180), (95, 115, 150, 180), (28, 45, 70, 170)])
        d.point((sx, sy), fill=shade)
        if rng.random() < .12:
            d.point((sx + 1, sy), fill=shade)

    # Header / terminal metadata.
    mono_b = font("mono", 22)
    mono = font("mono_reg", 14)
    small = font("mono_reg", 11)
    d.text((24, 18), "~/contribution-city", font=mono_b, fill=GHOST)
    d.text((w - 72, 27), "// 03", font=mono, fill=(115, 125, 145))
    d.line((24, 49, w - 24, 49), fill=(*CYAN, 200), width=1)
    d.text((24, 66), "$ render-city --last 365d  # one building per day", font=mono, fill=(135, 143, 163))
    d.text((24, 66), "$", font=mono, fill=LIME)

    # Moon / status orb.
    moon_x, moon_y = w - 58, 103
    d.ellipse((moon_x - 19, moon_y - 19, moon_x + 19, moon_y + 19), fill=(16, 19, 31))
    d.ellipse((moon_x - 10, moon_y - 10, moon_x + 10, moon_y + 10), fill=GHOST)
    d.ellipse((moon_x - 3, moon_y - 13, moon_x + 13, moon_y + 3), fill=VOID)

    # A long, low isometric city platform.
    base_y = 285
    left = (120, 228)
    front = (545, 344)
    right = (884, 282)
    back = (465, 218)
    d.polygon([left, front, right, back], fill=(19, 25, 39))
    d.line([left, front, right], fill=(48, 61, 82), width=2)
    # Platform grid follows the isometric plane.
    for i in range(1, 22):
        t = i / 22
        x1 = left[0] + (back[0] - left[0]) * t
        y1 = left[1] + (back[1] - left[1]) * t
        x2 = front[0] + (right[0] - front[0]) * t
        y2 = front[1] + (right[1] - front[1]) * t
        d.line((x1, y1, x2, y2), fill=(25, 34, 49), width=1)
    for i in range(1, 10):
        t = i / 10
        x1 = left[0] + (front[0] - left[0]) * t
        y1 = left[1] + (front[1] - left[1]) * t
        x2 = back[0] + (right[0] - back[0]) * t
        y2 = back[1] + (right[1] - back[1]) * t
        d.line((x1, y1, x2, y2), fill=(25, 34, 49), width=1)

    # Build a skyline across the isometric plane. Contribution levels influence height.
    # If no real contribution JSON is supplied, the graphic remains illustrative.
    cols = len(levels[0]) if levels else 30
    rows = len(levels) if levels else 7
    buildings = []
    for c in range(cols):
        for r in range(rows):
            value = levels[r][c]
            # Skip many low-level cells to form a varied, city-like silhouette.
            if value <= 0 or rng.random() < 0.18:
                continue
            # Screen projection: x advances right; row offsets create depth.
            x = 125 + c * 18.5 + r * 7
            y = 260 + c * 1.55 - r * 7.4
            bw = rng.choice([13, 15, 17, 19])
            depth = bw * 0.52
            raw_height = 15 + value * 10 + rng.randint(0, 38)
            bh = max(3, int(raw_height * min(1.0, max(0.0, progress * 1.25 - c / max(1, cols) * .25))))
            if bh <= 2:
                continue
            buildings.append((y, x, bw, depth, bh, value, rng.randint(0, 9999)))

    # Draw far buildings first for convincing overlap.
    for y, x, bw, depth, bh, value, seed in sorted(buildings):
        if x > 900 or x < 35:
            continue
        top_y = y - bh
        top = [(x, top_y), (x + depth, top_y - depth * .55),
               (x + bw + depth, top_y - depth * .55), (x + bw, top_y)]
        front_face = [(x, top_y), (x + bw, top_y), (x + bw, y), (x, y)]
        side_face = [(x + bw, top_y), (x + bw + depth, top_y - depth * .55),
                     (x + bw + depth, y - depth * .55), (x + bw, y)]
        front_col = (19, 43 + value * 8, 68 + value * 10)
        side_col = (12, 24 + value * 5, 45 + value * 7)
        top_col = (22, 111 + value * 17, 164 + value * 18)
        d.polygon(front_face, fill=front_col, outline=(25, 98, 140))
        d.polygon(side_face, fill=side_col, outline=(19, 70, 112))
        d.polygon(top, fill=top_col, outline=(*CYAN, 220))
        # Small cyan/blue window grid.
        wrng = random.Random(seed)
        win_y = top_y + 5
        while win_y < y - 4:
            for wx in range(int(x + 3), int(x + bw - 2), 5):
                if wrng.random() < .72:
                    wc = wrng.choice([(67, 226, 255), (0, 190, 255), (87, 132, 255), (35, 80, 160)])
                    d.rectangle((wx, win_y, wx + 2, win_y + 2), fill=wc)
            win_y += 6
        # Sparse rooftop antenna / cap on tall towers.
        if bh > 45 and seed % 4 == 0:
            d.line((x + bw // 2, top_y, x + bw // 2, top_y - 7), fill=CYAN, width=1)

    # Right-side stats block; never fabricate numeric claims.
    stat_color = CYAN
    if is_real:
        d.text((w - 280, 190), "GITHUB CONTRIBUTIONS", font=small, fill=stat_color)
        d.text((w - 280, 207), "SOURCE: CONTRIBUTIONS.JSON", font=small, fill=GHOST)
    else:
        d.text((w - 280, 190), "CONTRIBUTION CITY", font=small, fill=stat_color)
        d.text((w - 280, 207), "ILLUSTRATIVE DATA / NOT LIVE", font=small, fill=(145, 150, 168))

    # Legend and lower edge.
    d.text((24, h - 30), "quiet", font=small, fill=(155, 160, 178))
    for i, col in enumerate([(23, 36, 57), (22, 66, 120), (25, 102, 185), (20, 163, 226), (0, 229, 255)]):
        x0 = 70 + i * 12
        d.rectangle((x0, h - 28, x0 + 9, h - 20), fill=col)
    d.text((134, h - 30), "skyscraper", font=small, fill=(155, 160, 178))
    paste_rgba(img, scanlines((w, h), 4, 24))
    d = ImageDraw.Draw(img)
    d.line((24, h - 48, w - 24, h - 48), fill=(25, 35, 53), width=1)
    return img


def contrib_static():
    w, h = 1000, 420
    levels, is_real = _load_contribution_levels()
    img = Image.new("RGBA", (w, h), (*VOID, 255))
    img = _draw_activity_field(img, levels, progress=1.0, is_real=is_real)
    out = ensure("activity", "contrib-3d-static.png")
    img.convert("RGB").save(out, optimize=True)
    return out


def contrib_animated():
    w, h = 1000, 420
    levels, is_real = _load_contribution_levels()
    frames = []
    for fi in range(20):
        img = Image.new("RGBA", (w, h), (*VOID, 255))
        frames.append(_draw_activity_field(img, levels, progress=(fi + 1) / 20, is_real=is_real).convert("RGB"))
    for _ in range(6):
        frames.append(frames[-1].copy())
    out = ensure("activity", "contrib-3d.gif")
    save_gif(out, frames, duration=120, colors=48)
    return out


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
    for panel in TECH_MATRIX:
        done.append(tech_panel(panel))
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
