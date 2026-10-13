# ASSET MANIFEST

All artwork lives under `assets/`. Every file below is committed to the repo.
Regenerate the code-made assets at any time with:

```bash
python3 scripts/gen_assets.py
```

Requires: `python3`, `Pillow`, `numpy`.

---

## Design tokens (shared by all assets)
| Token | Hex |
|-------|-----|
| Void black | `#0B0B12` |
| Hot pink | `#FF2E88` |
| Acid lime | `#B6FF00` |
| Laser cyan | `#00E5FF` |
| Ultraviolet | `#A855F7` |
| Toxic orange | `#FF6B35` |
| Ghost white | `#F4F0FF` |
| Signal yellow | `#FFE45E` |

Fonts: **Noto Sans Display Condensed/ExtraCondensed Black** (display),
**Fira Code** (terminal/mono), fallback DejaVu/Liberation.

---

## Asset table

| Asset | Path | Format | Dimensions | Source | Fallback |
|-------|------|--------|------------|--------|----------|
| Hero (animated) | `assets/hero/hero.gif` | GIF | 1280×400, 20f | code → replace with AI | `hero-static.png` |
| Hero (static) | `assets/hero/hero-static.png` | PNG | 1280×400 | code | — |
| Divider 01 | `assets/separators/divider-01.gif` | GIF | 1280×10, 16f | code | frame 1 |
| Divider 02 | `assets/separators/divider-02.gif` | GIF | 1280×10, 16f | code | frame 1 |
| Section headers ×6 | `assets/separators/header-02|03|04|05|06|end.png` | PNG | 1280×72 | code | — |
| Terminal session | `assets/terminal/terminal.gif` | GIF | 900×620, 18f | code | static frame |
| Terminal panel bg | `assets/terminal/panel-bg.png` | PNG | 900×620 | code | — |
| Scanlines overlay | `assets/terminal/scanlines.png` | PNG | 900×620 | code | — |
| Cursor | `assets/terminal/cursor.gif` | GIF | 12×24, 2f | code | — |
| Tech panel 01 | `assets/tech/tech-panel-01.png` | PNG | 380×180 | code | — |
| Tech panel 02 | `assets/tech/tech-panel-02.png` | PNG | 380×180 | code | — |
| Tech panel 03 | `assets/tech/tech-panel-03.png` | PNG | 380×180 | code | — |
| Tech panel 04 | `assets/tech/tech-panel-04.png` | PNG | 380×180 | code | — |
| Project thumb ×7 | `assets/projects/thumb-<slug>.png` | PNG | 320×180 | code | — |
| Activity (animated) | `assets/activity/contrib-3d.gif` | GIF | 800×400, 26f | code → replace with AI | `contrib-3d-static.png` |
| Activity (static) | `assets/activity/contrib-3d-static.png` | PNG | 800×400 | code | — |
| Footer (animated) | `assets/footer/footer.gif` | GIF | 1280×180, 18f | code → replace with AI | `footer-static.png` |
| Footer (static) | `assets/footer/footer-static.png` | PNG | 1280×180 | code | — |

Project slugs: `ufosay`, `face-unlock`, `apnadabba`, `db-manager`, `render`,
`anti_theft`, `library-management`.

---

## File-size budget
| Target | Limit | Current worst |
|--------|-------|---------------|
| Animated GIF | ≤ 2 MB | hero.gif ≈ 0.6 MB |
| Static PNG | ≤ 300 KB | project thumb ≈ 0.09 MB |

Total `assets/` payload: well under 3 MB.

---

## External services (not stored locally)
| Service | Purpose | URL pattern |
|---------|---------|-------------|
| Shields.io | tech badges | `https://img.shields.io/badge/...` |
| github-readme-stats | stats + top-langs | `https://github-readme-stats.vercel.app/api?...` |

Widgets are rendered by GitHub's camo proxy; if a service is down the README
still shows alt text + the static fallbacks.

---

## AI-generated targets
See `prompt.txt` for the three assets we recommend replacing with AI renders
(hero.gif, footer.gif, contrib-3d.gif). Code stand-ins already sit at those exact
paths, so the README never breaks.
