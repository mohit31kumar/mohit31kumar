#!/usr/bin/env python3
"""Fetch live GitHub contribution data and render profile metric cards."""
import json
import os
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
USERNAME = "mohit31kumar"
TOKEN = os.environ.get("GITHUB_TOKEN")
API = "https://api.github.com"
GRAPHQL = "https://api.github.com/graphql"


def request_json(url, method="GET", payload=None):
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "mohit31kumar-profile-automation",
    }
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"GitHub API returned HTTP {exc.code}: {detail}") from exc


def fetch_contributions():
    if not TOKEN:
        raise RuntimeError("GITHUB_TOKEN is required to fetch contribution history.")
    end = datetime.now(timezone.utc)
    start = end - timedelta(days=365)
    query = """
    query($login: String!, $from: DateTime!, $to: DateTime!) {
      user(login: $login) {
        contributionsCollection(from: $from, to: $to) {
          contributionCalendar {
            totalContributions
            weeks {
              contributionDays { contributionCount }
            }
          }
        }
      }
    }
    """
    result = request_json(GRAPHQL, "POST", {
        "query": query,
        "variables": {
            "login": USERNAME,
            "from": start.isoformat().replace("+00:00", "Z"),
            "to": end.isoformat().replace("+00:00", "Z"),
        },
    })
    if result.get("errors"):
        raise RuntimeError("GraphQL error: " + json.dumps(result["errors"]))
    user = result.get("data", {}).get("user")
    if not user:
        raise RuntimeError(f"GitHub user {USERNAME!r} was not returned.")
    calendar = user["contributionsCollection"]["contributionCalendar"]
    weeks = []
    for week in calendar["weeks"]:
        days = week["contributionDays"]
        values = [int(day["contributionCount"]) for day in days]
        if len(values) != 7:
            values = (values + [0] * 7)[:7]
        weeks.append(values)
    if not weeks:
        raise RuntimeError("GitHub returned an empty contribution calendar.")
    maximum = max((value for week in weeks for value in week), default=0)
    levels = []
    for week in weeks:
        levels.append([
            0 if count == 0 else
            1 if maximum <= 1 or count <= max(1, maximum * 0.25) else
            2 if count <= max(2, maximum * 0.50) else
            3 if count <= max(3, maximum * 0.75) else 4
            for count in week
        ])
    activity_dir = ROOT / "assets" / "activity"
    activity_dir.mkdir(parents=True, exist_ok=True)
    (activity_dir / "contributions.json").write_text(
        json.dumps({"weeks": levels, "total_contributions": calendar["totalContributions"],
                    "updated_at": end.isoformat()}, indent=2) + "\n",
        encoding="utf-8",
    )
    return int(calendar["totalContributions"])


def fetch_repositories():
    repos = []
    page = 1
    while True:
        url = f"{API}/users/{USERNAME}/repos?type=owner&sort=updated&per_page=100&page={page}"
        batch = request_json(url)
        if not batch:
            break
        repos.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    return [repo for repo in repos if not repo.get("fork") and not repo.get("archived")]


def svg_card(title, width=900, height=230, body=""):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{escape(title)}">
<rect width="{width}" height="{height}" rx="14" fill="#0B0B12"/>
<rect x="1" y="1" width="{width-2}" height="{height-2}" rx="13" fill="none" stroke="#252536"/>
<text x="28" y="42" fill="#FF2E88" font-family="monospace" font-size="19" font-weight="700">{escape(title)}</text>
<path d="M28 58 H{width-28}" stroke="#00E5FF" opacity=".65"/>
{body}
</svg>
'''


def render_stats(repos, total_contributions):
    stars = sum(int(repo.get("stargazers_count", 0)) for repo in repos)
    forks = sum(int(repo.get("forks_count", 0)) for repo in repos)
    public_repos = len(repos)
    metrics = [
        ("CONTRIBUTIONS / 365D", f"{total_contributions:,}", "#00E5FF"),
        ("PUBLIC REPOSITORIES", f"{public_repos:,}", "#B6FF00"),
        ("TOTAL STARS", f"{stars:,}", "#FF2E88"),
        ("TOTAL FORKS", f"{forks:,}", "#A855F7"),
    ]
    blocks = []
    positions = [(28, 105), (465, 105), (28, 175), (465, 175)]
    for (label, value, accent), (x, y) in zip(metrics, positions):
        blocks.append(
            f'<text x="{x}" y="{y}" fill="#9292A8" font-family="monospace" font-size="12">{label}</text>'
            f'<text x="{x}" y="{y+34}" fill="{accent}" font-family="monospace" font-size="27" font-weight="700">{value}</text>'
        )
    path = ROOT / "assets" / "activity" / "github-stats.svg"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(svg_card("GITHUB // LIVE PROFILE STATS", body="\n".join(blocks)), encoding="utf-8")


def render_languages(repos):
    totals = {}
    for repo in repos:
        url = repo.get("languages_url")
        if not url:
            continue
        for language, amount in request_json(url).items():
            totals[language] = totals.get(language, 0) + int(amount)
    ranked = sorted(totals.items(), key=lambda item: item[1], reverse=True)[:6]
    total_bytes = sum(totals.values())
    palette = ["#00E5FF", "#FF2E88", "#B6FF00", "#A855F7", "#FF6B35", "#FFE45E"]
    body = []
    if not ranked or total_bytes == 0:
        body.append('<text x="28" y="112" fill="#B6FF00" font-family="monospace" font-size="15">No public language data available yet.</text>')
    else:
        bar_x, bar_y, bar_w, bar_h = 28, 78, 844, 12
        cursor = bar_x
        for index, (language, amount) in enumerate(ranked):
            segment = bar_w * amount / total_bytes
            body.append(f'<rect x="{cursor:.2f}" y="{bar_y}" width="{max(1, segment):.2f}" height="{bar_h}" rx="3" fill="{palette[index]}"/>')
            cursor += segment
        for index, (language, amount) in enumerate(ranked):
            col = index % 2
            row = index // 2
            x = 28 + col * 437
            y = 125 + row * 36
            percent = amount / total_bytes * 100
            body.append(
                f'<circle cx="{x+5}" cy="{y-5}" r="5" fill="{palette[index]}"/>'
                f'<text x="{x+20}" y="{y}" fill="#F4F0FF" font-family="monospace" font-size="14">{escape(language)}</text>'
                f'<text x="{x+400}" y="{y}" text-anchor="end" fill="#B6FF00" font-family="monospace" font-size="14">{percent:.1f}%</text>'
            )
    path = ROOT / "assets" / "activity" / "top-languages.svg"
    path.write_text(svg_card("LANGUAGE MATRIX // TOP 6", body="\n".join(body)), encoding="utf-8")


def main():
    contributions = fetch_contributions()
    repositories = fetch_repositories()
    render_stats(repositories, contributions)
    render_languages(repositories)
    print(f"Updated contribution history ({contributions} contributions), stats card, and top languages card.")


if __name__ == "__main__":
    main()
