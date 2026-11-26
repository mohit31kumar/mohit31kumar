#!/usr/bin/env python3
"""Render a data-driven, animated 3D Contribution Nebula for the profile README."""
from __future__ import annotations

import json
import math
import random
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import gen_assets  # noqa: E402

W, H = 1000, 420
VOID = (11, 11, 18)
GHOST = (244, 240, 255)
PINK = (255, 46, 136)
LIME = (182, 255, 0)
CYAN = (0, 229, 255)
ULTRA = (168, 85, 247)
ORANGE = (255, 107, 53)
PALETTE = [CYAN, ULTRA, PINK, LIME, ORANGE]
FRAMES = 24


def load_activity():
    """Return dated contribution levels (53 weeks x 7 days) and source metadata."""
    path = ROOT / "assets" / "activity" / "contributions.json"
    if path.is_file():
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
            weeks = payload.get("weeks", [])
            clean = []
            for week in weeks[-53:]:
                values = [max(0, min(4, int(v))) for v in week[:7]]
                clean.append(values + [0] * (7 - len(values)))
            if clean and any(any(day for day in week) for week in clean):
                return clean, True, int(payload.get("total_contributions", 0))
            if clean:
                return clean, True, int(payload.get("total_contributions", 0))
        except (OSError, ValueError, TypeError, AttributeError, json.JSONDecodeError):
            pass

    # Clearly marked fallback for a fresh checkout before the first API run.
    rng = random.Random(2026)
    weeks = [[rng.choice([0, 0, 0, 0, 1, 1, 2, 3, 4]) for _ in range(7)] for _ in range(53)]
    return weeks, False, 0


def build_particles(weeks):
    """Map each active day to a spiral-arm cluster; activity intensity drives density."""
    particles = []
    rng = random.Random(713)
    count_weeks = max(1, len(weeks))
    for wi, week in enumerate(weeks):
        progress = wi / max(1, count_weeks - 1)
        for day, level in enumerate(week):
            if level <= 0:
                continue
            # The calendar advances along a gently winding arm. Week = radius,
            # weekday = angular offset; stronger days create denser/brighter clusters.
            angle = progress * math.tau * 2.15 + day * (math.tau / 7) * 0.34
            radius = 28 + progress * 178
            cx = math.cos(angle) * radius
            cy = math.sin(angle) * radius * 0.54
            cz = rng.gauss(0, 15 + level * 3)
            cluster_size = 4 + level * 5
            color = PALETTE[min(4, max(0, level - 1))]
            for _ in range(cluster_size):
                spread = 4 + level * 2.8
                particles.append((
                    cx + rng.gauss(0, spread),
                    cy + rng.gauss(0, spread * 0.58),
                    cz + rng.gauss(0, spread * 0.8),
                    rng.uniform(0.65, 1.7 + level * 0.28),
                    color,
                    rng.uniform(0.45, 1.0),
                ))

    # A faint galactic dust field gives the form depth without inventing activity:
    # its opacity is low and it is visually distinct from contribution clusters.
    for arm in range(3):
        for i in range(150):
            t = i / 150
            angle = t * math.tau * 2.0 + arm * math.tau / 3
            radius = 18 + t * 205
            jitter = rng.gauss(0, 10 + t * 7)
            particles.append((
                math.cos(angle) * (radius + jitter),
                math.sin(angle) * (radius + jitter) * 0.55,
                rng.gauss(0, 22),
                rng.uniform(0.35, 0.9),
                (54, 75, 112),
                0.20,
            ))

    # Bright core particles are structural decoration, not contribution counts.
    for _ in range(260):
        angle = rng.random() * math.tau
        radius = abs(rng.gauss(0, 34))
        particles.append((
            math.cos(angle) * radius,
            math.sin(angle) * radius * 0.52,
            rng.gauss(0, 13),
            rng.uniform(0.5, 1.45),
            rng.choice([CYAN, ULTRA, PINK, GHOST]),
            rng.uniform(0.28, 0.78),
        ))
    return particles


def project(point, rotation):
    x, y, z, size, color, intensity = point
    # Rotate the galaxy in 3D, then tilt the disk away from the camera.
    xr = x * math.cos(rotation) - z * math.sin(rotation)
    zr = x * math.sin(rotation) + z * math.cos(rotation)
    tilt = 0.48
    yr = y * math.cos(tilt) - zr * math.sin(tilt)
    depth = y * math.sin(tilt) + zr * math.cos(tilt)
    focal = 620
    perspective = focal / (focal + depth + 270)
    sx = W * 0.5 + xr * perspective * 1.48
    sy = 226 + yr * perspective * 1.48
    return sx, sy, max(0.35, size * perspective * 1.4), color, intensity, depth


def draw_frame(particles, frame_index, is_real, total):
    rotation = math.tau * frame_index / FRAMES
    base = Image.new("RGBA", (W, H), (*VOID, 255))
    d = ImageDraw.Draw(base)

    # Technical frame, grid and sparse stars.
    d.rectangle((12, 12, W - 12, H - 12), outline=(42, 45, 65), width=1)
    for x in range(28, W, 40):
        d.line((x, 74, x, H - 45), fill=(17, 20, 32), width=1)
    for y in range(82, H - 40, 32):
        d.line((20, y, W - 20, y), fill=(17, 20, 32), width=1)

    star_rng = random.Random(91)
    for _ in range(125):
        sx = star_rng.randrange(22, W - 22)
        sy = star_rng.randrange(82, H - 42)
        shade = star_rng.choice([(60, 77, 112), (37, 50, 78), (95, 90, 130)])
        d.point((sx, sy), fill=(*shade, 170))

    # Header and metadata.
    mono_b = gen_assets.font("mono", 20)
    mono = gen_assets.font("mono_reg", 12)
    small = gen_assets.font("mono_reg", 11)
    d.text((28, 23), "MOHIT / ACTIVITY NEBULA", font=mono_b, fill=GHOST)
    d.text((W - 190, 29), "365D // LIVE FEED", font=mono, fill=LIME)
    d.line((28, 58, W - 28, 58), fill=(*CYAN, 170), width=1)
    d.text((28, 68), "$ visualize-contributions --mode 3d --orbit", font=mono, fill=(126, 143, 170))
    d.text((28, 68), "$", font=mono, fill=CYAN)

    # Soft radial nebula glow. Its pulse is subtle and loops seamlessly.
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    pulse = 0.92 + 0.08 * math.sin(rotation)
    gd.ellipse((275, 100, 725, 360), fill=(35, 60, 130, int(34 * pulse)))
    gd.ellipse((360, 135, 640, 315), fill=(115, 35, 150, int(26 * pulse)))
    glow = glow.filter(ImageFilter.GaussianBlur(48))
    base = Image.alpha_composite(base, glow)

    # Render far particles first for a convincing volumetric 3D disc.
    projected = [project(p, rotation) for p in particles]
    projected.sort(key=lambda item: item[5])
    haze = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hd = ImageDraw.Draw(haze)
    cores = ImageDraw.Draw(base)
    for sx, sy, radius, color, intensity, depth in projected:
        if not (-12 <= sx <= W + 12 and 72 <= sy <= H - 36):
            continue
        alpha = int(105 * intensity)
        r = max(1, radius)
        hd.ellipse((sx - r * 3.4, sy - r * 3.4, sx + r * 3.4, sy + r * 3.4),
                   fill=(*color, max(8, int(alpha * 0.34))))
        cores.ellipse((sx - r, sy - r, sx + r, sy + r),
                      fill=(*color, max(35, min(255, alpha + 40))))
    haze = haze.filter(ImageFilter.GaussianBlur(8))
    base = Image.alpha_composite(base, haze)

    # Core flare and orbit arcs.
    flare = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    fd = ImageDraw.Draw(flare)
    fd.ellipse((468, 194, 532, 258), fill=(0, 229, 255, 95))
    fd.ellipse((484, 210, 516, 242), fill=(244, 240, 255, 170))
    flare = flare.filter(ImageFilter.GaussianBlur(17))
    base = Image.alpha_composite(base, flare)
    d = ImageDraw.Draw(base)
    d.arc((285, 126, 715, 326), start=(frame_index * 5) % 360,
          end=(frame_index * 5 + 245) % 360, fill=(0, 229, 255, 85), width=1)
    d.arc((335, 145, 665, 305), start=(180 + frame_index * 4) % 360,
          end=(180 + frame_index * 4 + 190) % 360, fill=(168, 85, 247, 95), width=1)

    # Activity legend and truthful source label.
    d.line((28, H - 52, W - 28, H - 52), fill=(35, 42, 61), width=1)
    if is_real:
        d.text((28, H - 37), f"GITHUB CONTRIBUTIONS // LAST 365 DAYS // {total:,} TOTAL",
              font=small, fill=CYAN)
        d.text((W - 225, H - 37), "SOURCE: GITHUB GRAPHQL", font=small, fill=GHOST)
    else:
        d.text((28, H - 37), "PREVIEW MODE // AWAITING FIRST LIVE DATA SYNC",
              font=small, fill=(160, 165, 185))
        d.text((W - 190, H - 37), "SOURCE: LOCAL PREVIEW", font=small, fill=GHOST)

    # CRT scanlines and a restrained moving scan highlight.
    scan = gen_assets.scanlines((W, H), 4, 18)
    base.alpha_composite(scan)
    d = ImageDraw.Draw(base)
    scan_y = 82 + int((frame_index / FRAMES) * (H - 130))
    d.line((20, scan_y, W - 20, scan_y), fill=(0, 229, 255, 34), width=1)
    return base.convert("RGB")


def main():
    weeks, is_real, total = load_activity()
    particles = build_particles(weeks)
    frames = [draw_frame(particles, i, is_real, total) for i in range(FRAMES)]
    activity_dir = ROOT / "assets" / "activity"
    activity_dir.mkdir(parents=True, exist_ok=True)
    static_path = activity_dir / "contrib-3d-static.png"
    gif_path = activity_dir / "contrib-3d.gif"
    frames[0].save(static_path, optimize=True)
    gen_assets.save_gif(str(gif_path), frames, duration=105, colors=64)
    print(f"Rendered Contribution Nebula: {gif_path} ({FRAMES} frames), {static_path}")
    print(f"Source: {'GitHub contribution history' if is_real else 'illustrative preview'}; total={total}")


if __name__ == "__main__":
    main()
