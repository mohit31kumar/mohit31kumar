# MOHIT.OS Editable Content

- Update the operator introduction and prose in `README.md`.
- Update public project descriptions, stacks and URLs in `data/projects.json`.
- Update technology inventory in `data/skills.json`.
- Update theme tokens in `config/theme.json`.
- Do not manually edit `data/profile.json` or `assets/activity/contributions.json`; these are generated from GitHub APIs.

Run:
`python -m pip install -r requirements.txt`
`GITHUB_TOKEN=YOUR_TOKEN python scripts/update_profile_metrics.py`
`python scripts/mohit_os.py --render --validate`

GitHub profile READMEs cannot execute arbitrary JavaScript or host a continuously interactive 3D scene. MOHIT.OS uses pre-rendered SVG, PNG and GIF assets with static fallbacks.
