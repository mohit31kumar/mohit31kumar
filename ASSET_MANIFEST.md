# ASSET MANIFEST

All artwork lives under `assets/`. Every file below is committed to the repo.
Regenerate the code-made assets at any time with:

```bash
python3 scripts/gen_assets.py
```

Requires: `python3`, `Pillow`, `numpy`.

Live activity is refreshed by `.github/workflows/update-profile-activity.yml` daily
and on manual dispatch. `scripts/update_profile_metrics.py` fetches the last 365 days
of contribution data and repository language/stat data; `scripts/render_contribution_nebula.py`
regenerates only the 3D Contribution Nebula GIF/PNG so other artwork is never overwritten.
Run the nebula renderer directly with `python3 scripts/render_contribution_nebula.py`.
The workflow uses the built-in `GITHUB_TOKEN` for public data. Add an optional repository
Actions secret named `PROFILE_TOKEN` with `read:user` scope to include private/internal
contribution counts when your GitHub profile is configured to show them.

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
| Tech panel 01 | `assets/tech/tech-panel-01.png` | PNG | 380×300 | code | — |
| Tech panel 02 | `assets/tech/tech-panel-02.png` | PNG | 380×300 | code | — |
| Tech panel 03 | `assets/tech/tech-panel-03.png` | PNG | 380×300 | code | — |
| Tech panel 04 | `assets/tech/tech-panel-04.png` | PNG | 380×300 | code | — |
| Project thumb ×7 | `assets/projects/thumb-<slug>.png` | PNG | 640×360 | code / real src | — |
| Contribution Nebula (animated) | `assets/activity/contrib-3d.gif` | GIF | 1000×420, 24f | contribution data + 3D particle renderer | `contrib-3d-static.png` |
| Contribution Nebula (static) | `assets/activity/contrib-3d-static.png` | PNG | 1000×420 | live contribution data + 3D particle renderer | — |
| GitHub stats | `assets/activity/github-stats.svg` | SVG | 900×230 | GitHub API | — |
| Top languages | `assets/activity/top-languages.svg` | SVG | 900×230 | GitHub repository language API | — |
| Contribution source | `assets/activity/contributions.json` | JSON | 53×7 levels | GitHub GraphQL API | — |
| Footer (animated) | `assets/footer/footer.gif` | GIF | 1280×180, 18f | code → replace with AI | `footer-static.png` |
| Footer (static) | `assets/footer/footer-static.png` | PNG | 1280×180 | code | — |

Project slugs: `ufosay`, `face-unlock`, `apnadabba`, `db-manager`, `render`,
`anti_theft`, `library-management`.

Real project images: drop screenshots at `assets/projects/src/<slug>.{png,jpg,jpeg,webp}`.
On the next `python3 scripts/gen_assets.py` run each is letterboxed (contain, no
crop) onto the canonical 640×360 canvas and written to `thumb-<slug>.png`.
Slugs with no source file fall back to the generated placeholder. This keeps
real art from being overwritten by a rerun.

---

## File-size budget
| Target | Limit | Current worst |
|--------|-------|---------------|
| Animated GIF | ≤ 2 MB | hero.gif ≈ 0.6 MB |
| Static PNG | ≤ 300 KB | project thumb ≈ 0.07 MB |

Total `assets/` payload: keep under 3 MB; the animated Contribution Nebula is one of the largest assets.

---

## External services (not stored locally)
| Service | Purpose | URL pattern |
|---------|---------|-------------|
| Shields.io | tech badges | `https://img.shields.io/badge/...` |
| Local GitHub API cards | stats + top-langs | `assets/activity/github-stats.svg`, `assets/activity/top-languages.svg` |

Widgets are rendered by GitHub's camo proxy; if a service is down the README
still shows alt text + the static fallbacks.

---

## AI-generated targets
See `prompt.txt` for optional AI-rendered hero and footer artwork. The Contribution
Nebula is generated from real contribution data by `scripts/render_contribution_nebula.py`;
it is no longer an AI-image placeholder.
