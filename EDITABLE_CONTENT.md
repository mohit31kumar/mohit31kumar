# EDITABLE CONTENT — REVIEW & APPROVE

Everything on this page is a **placeholder awaiting your approval**.
Nothing here is invented biography. Verified facts are marked `[VERIFIED]`.
Anything inferred or drafted is marked `[DRAFT — APPROVE OR EDIT]`.

When you approve/change an item, also update the matching string in `README.md`
(and, for terminal text, `scripts/gen_assets.py` → `TERMINAL_LINES`, then re-run
`python3 scripts/gen_assets.py`).

---

## 1. HERO TAGLINE  [DRAFT — APPROVE OR EDIT]
Baked into `assets/hero/hero.gif` + `hero-static.png`.

```
MOHIT KUMAR
// TERMINAL DWELLER // CYBERSEC
```

- Big line: display name (`[VERIFIED]` = your GitHub name "Mohit Kumar").
- Sub line: role tagline. Change the words in `gen_assets.py` → `hero_static()` /
  `hero_animated()` (search `TERMINAL DWELLER`).

---

## 2. SIGNAL FRAGMENT (hero-adjacent bio)  [DRAFT — APPROVE OR EDIT]
Shown directly under the hero. Currently:

> Building tools that live in the command line. Cybersecurity, systems, and
> the occasional flying saucer.

Keep it to 1-2 sentences. Replace freely in `README.md`.

---

## 3. TERMINAL SESSION TEXT  [DRAFT — APPROVE OR EDIT]
Rendered into `assets/terminal/terminal.gif`.

Commands simulated (static image — **not** actually interactive):

```text
$ who are you
MOHIT KUMAR
Developer  •  Terminal Dweller  •  Cybersecurity Enthusiast
Building tools that live in the command line.

$ ls projects
ufosay               flying-saucer terminal animation      [python]
face-unlock          PAM facial auth for linux            [python]
apnadabba            full-stack delivery app               [typescript]
db-manager           database management interface         [ejs]
render               rendering engine experiments          [typescript]
anti_theft           anti-theft security tool              [html]
library-management   library management system             [python]

$ cat status
7 projects  •  5 languages  •  status: ONLINE
```

> Note on the old interactive request: GitHub READMEs cannot run JavaScript,
> accept input, or execute commands. This is a rendered image of a session.
> The **clickable** project links live as real Markdown link-chips directly
> below the terminal image, so navigation still works.

---

## 4. TECH MATRIX  [DRAFT — APPROVE OR EDIT]
Four brutalist panels. Badges use [Shields.io](https://shields.io). Groups:

| Panel | Label | Badges shown (all `[VERIFIED]` from your repo languages) |
|-------|-------|----------------------------------------------------------|
| 01 | LANGUAGES | Python, TypeScript, JavaScript, Dart, HTML5, CSS/SCSS |
| 02 | FRAMEWORKS | Node.js, Express, EJS, Flutter, React *(⚠ only if accurate)* |
| 03 | TOOLS / INFRA | Git, Linux, Docker *(⚠)*, Vercel, Render, Bash |
| 04 | DOMAINS | Cybersecurity, Terminal Tooling, Web Apps, Auth Systems |

> ⚠ Items in the FRAMEWORKS / TOOLS panels are **not yet verified** from your
> repos. Confirm each one before publishing, or delete badges that don't apply.
> Badge list lives in `README.md` under `SECTION 04`.

---

## 5. PROJECT DIMENSION  [DRAFT — APPROVE OR EDIT]
Seven repos, thumbnails generated from repo names. Links `[VERIFIED]`.

| # | Repo | Description (status) | Live demo |
|---|------|----------------------|-----------|
| 1 | `ufosay` | "A flying saucer terminal animation tool" `[VERIFIED]` | https://ufosay.vercel.app |
| 2 | `face-unlock` | "PAM-based facial authentication for Linux" `[VERIFIED]` | — |
| 3 | `ApnaDabba` | `[DRAFT]` full-stack delivery app | https://apna-dabba-kappa.vercel.app |
| 4 | `DB-MANAGER` | `[DRAFT]` database management interface | https://db-manager-4n4m.onrender.com |
| 5 | `render` | `[DRAFT]` rendering engine experiments | — |
| 6 | `anti_theft` | `[DRAFT]` anti-theft security tool | — |
| 7 | `library-management` | `[DRAFT]` library management system | — |

Descriptions marked `[DRAFT]` were inferred from the repo name only — **edit or
confirm these.** Repo link base: `https://github.com/mohit31kumar/<repo>`.

---

## 6. ACTIVITY FIELD  [VERIFIED WIDGETS]
- Isometric contribution GIF: `assets/activity/contrib-3d.gif`
  → ⚠ currently a **decorative generated field**, NOT your real contribution data.
  Treat as art. If you want real data, use the live widget shown below it.
- Live stats widgets (measure real data):
  - `github-readme-stats.vercel.app` — stars/commits/PRs/issues (self-reported by service)
  - `github-readme-stats.vercel.app/api/top-langs` — most-used languages by bytes
- Static fallbacks: `contrib-3d-static.png` + plain-text stat note in README.

---

## 7. CLOSING / FOOTER  [DRAFT — APPROVE OR EDIT]
Rendered into `assets/footer/footer.gif`.
- Wordmark: `END OF TRANSMISSION`
- Sub: `// SIGNAL LOST // MOHIT KUMAR // 2024 — NOW` (`2024` = account creation `[VERIFIED]`)

---

## 8. SOCIAL LINKS  [PLACEHOLDERS — REPLACE BEFORE PUBLISHING]
These are **obvious fakes** so nothing is misrepresented:

| Label | Placeholder URL | Status |
|-------|-----------------|--------|
| GITHUB | https://github.com/mohit31kumar | `[VERIFIED]` |
| TWITTER / X | https://twitter.com/mohit31kumar | **FAKE — replace or remove** |
| LINKEDIN | https://linkedin.com/in/mohit31kumar | **FAKE — replace or remove** |
| EMAIL | mailto:mohit31kumar@example.com | **FAKE — replace or remove** |

> Remove any line you don't have a real account for. Do not publish fake socials.
