#!/usr/bin/env python3
"""Render a contribution activity graph as a static SVG.

The upstream service this replaces (github-readme-activity-graph.vercel.app)
runs on a free Vercel instance that keeps hitting its quota. Generating the
chart here keeps the README self-contained and the palette under our control.
"""

import json
import os
import sys
import urllib.error
import urllib.request
from datetime import date, timedelta

API = "https://api.github.com/graphql"

QUERY = """
query($login: String!, $from: DateTime!, $to: DateTime!) {
  user(login: $login) {
    contributionsCollection(from: $from, to: $to) {
      contributionCalendar {
        weeks { contributionDays { date contributionCount } }
      }
    }
  }
}
"""

# Palette, kept in sync with the badges in README.md.
BACKGROUND = "#07222A"
TEXT = "#B9D6D3"
MUTED = "#7FA7A5"
LINE = "#C87A44"
POINT = "#5EEAD4"
AREA = "#0F3A42"
GRID = "#16515A"

WIDTH, HEIGHT = 860, 260
PAD_L, PAD_R, PAD_T, PAD_B = 48, 24, 56, 36


def fetch_days(login, token, days):
    end = date.today()
    start = end - timedelta(days=days - 1)
    payload = json.dumps(
        {
            "query": QUERY,
            "variables": {
                "login": login,
                "from": f"{start}T00:00:00Z",
                "to": f"{end}T23:59:59Z",
            },
        }
    ).encode()
    req = urllib.request.Request(
        API,
        data=payload,
        headers={
            "Authorization": f"bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "coaxio-activity-graph",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        body = json.load(resp)

    if "errors" in body:
        raise SystemExit(f"GraphQL error: {body['errors']}")

    weeks = body["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]
    out = [d for w in weeks for d in w["contributionDays"]]
    out.sort(key=lambda d: d["date"])
    # The calendar is week-aligned, so it can overshoot the window on both ends.
    return [d for d in out if str(start) <= d["date"] <= str(end)]


def nice_ceiling(value):
    """Round the axis maximum up to something readable."""
    if value <= 4:
        return 4
    for step in (5, 10, 20, 25, 50, 100, 200, 250, 500, 1000):
        if value <= step:
            return step
    return ((value + 999) // 1000) * 1000


def render(days, login, title):
    counts = [d["contributionCount"] for d in days]
    top = nice_ceiling(max(counts) if counts else 0)
    plot_w = WIDTH - PAD_L - PAD_R
    plot_h = HEIGHT - PAD_T - PAD_B

    span = max(len(days) - 1, 1)
    pts = []
    for i, count in enumerate(counts):
        x = PAD_L + plot_w * i / span
        y = PAD_T + plot_h * (1 - count / top)
        pts.append((x, y))

    line = " ".join(f"{'M' if i == 0 else 'L'}{x:.1f},{y:.1f}" for i, (x, y) in enumerate(pts))
    area = (
        f"M{pts[0][0]:.1f},{PAD_T + plot_h:.1f} "
        + " ".join(f"L{x:.1f},{y:.1f}" for x, y in pts)
        + f" L{pts[-1][0]:.1f},{PAD_T + plot_h:.1f} Z"
    )

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" '
        f'viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-label="{title} for {login}">',
        f'<title>{title}</title>',
        f'<rect width="{WIDTH}" height="{HEIGHT}" rx="8" fill="{BACKGROUND}"/>',
        f'<text x="{PAD_L}" y="32" fill="{LINE}" font-family="Segoe UI,Ubuntu,sans-serif" '
        f'font-size="16" font-weight="600">{title}</text>',
    ]

    # Horizontal gridlines with their value labels.
    for i in range(5):
        y = PAD_T + plot_h * i / 4
        value = int(round(top * (1 - i / 4)))
        parts.append(
            f'<line x1="{PAD_L}" y1="{y:.1f}" x2="{WIDTH - PAD_R}" y2="{y:.1f}" '
            f'stroke="{GRID}" stroke-width="1" stroke-dasharray="3 4"/>'
        )
        parts.append(
            f'<text x="{PAD_L - 10}" y="{y + 4:.1f}" fill="{MUTED}" text-anchor="end" '
            f'font-family="Segoe UI,Ubuntu,sans-serif" font-size="11">{value}</text>'
        )

    parts.append(f'<path d="{area}" fill="{AREA}" opacity="0.85"/>')
    parts.append(
        f'<path d="{line}" fill="none" stroke="{LINE}" stroke-width="2" '
        f'stroke-linejoin="round" stroke-linecap="round"/>'
    )

    # One dot per day would be noise at this width, so mark only the busy days.
    for (x, y), count in zip(pts, counts):
        if count:
            parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.5" fill="{POINT}"/>')

    # Date labels at both ends plus the midpoint.
    baseline = PAD_T + plot_h + 20
    for idx, anchor in ((0, "start"), (len(days) // 2, "middle"), (len(days) - 1, "end")):
        parts.append(
            f'<text x="{pts[idx][0]:.1f}" y="{baseline}" fill="{MUTED}" text-anchor="{anchor}" '
            f'font-family="Segoe UI,Ubuntu,sans-serif" font-size="11">{days[idx]["date"]}</text>'
        )

    total = sum(counts)
    parts.append(
        f'<text x="{WIDTH - PAD_R}" y="32" fill="{TEXT}" text-anchor="end" '
        f'font-family="Segoe UI,Ubuntu,sans-serif" font-size="12">{total} contributions</text>'
    )
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def main():
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        raise SystemExit("GITHUB_TOKEN is not set")
    login = os.environ.get("LOGIN", "Coaxio")
    days = int(os.environ.get("DAYS", "31"))
    out = os.environ.get("OUTPUT", "assets/activity.svg")
    title = os.environ.get("TITLE", f"Contributions over the last {days} days")

    try:
        calendar = fetch_days(login, token, days)
    except urllib.error.HTTPError as exc:
        raise SystemExit(f"GitHub API returned {exc.code}: {exc.read().decode()[:200]}")

    if not calendar:
        raise SystemExit("the contribution calendar came back empty")

    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    with open(out, "w") as fh:
        fh.write(render(calendar, login, title))
    print(f"wrote {out} ({len(calendar)} days, {sum(d['contributionCount'] for d in calendar)} contributions)")


if __name__ == "__main__":
    main()
