#!/usr/bin/env python3
"""Generate assets/stats-dark.svg from the GitHub GraphQL API.

Requires GITHUB_TOKEN in the environment. Stdlib only.
"""
import datetime as dt
import json
import os
import sys
import urllib.request

USER = "Rolazo"
API = "https://api.github.com/graphql"
OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "stats-dark.svg")


def gql(query, variables=None):
    body = json.dumps({"query": query, "variables": variables or {}}).encode()
    req = urllib.request.Request(
        API,
        data=body,
        headers={
            "Authorization": f"bearer {os.environ['GITHUB_TOKEN']}",
            "Content-Type": "application/json",
        },
    )
    with urllib.request.urlopen(req) as r:
        data = json.load(r)
    if "errors" in data:
        raise RuntimeError(data["errors"])
    return data["data"]


def main():
    created = gql(
        "query($u:String!){user(login:$u){createdAt}}", {"u": USER}
    )["user"]["createdAt"]
    first_year = int(created[:4])
    now = dt.datetime.now(dt.timezone.utc)

    total_contribs = 0
    year_contribs = 0
    days = []  # (date, count) across all years, for streak
    for year in range(first_year, now.year + 1):
        start = f"{year}-01-01T00:00:00Z"
        end = f"{year}-12-31T23:59:59Z"
        cc = gql(
            """
            query($u:String!,$from:DateTime!,$to:DateTime!){
              user(login:$u){
                contributionsCollection(from:$from,to:$to){
                  contributionCalendar{
                    totalContributions
                    weeks{contributionDays{date contributionCount}}
                  }
                }
              }
            }
            """,
            {"u": USER, "from": start, "to": end},
        )["user"]["contributionsCollection"]
        year_total = cc["contributionCalendar"]["totalContributions"]
        total_contribs += year_total
        if year == now.year:
            year_contribs = year_total
        for w in cc["contributionCalendar"]["weeks"]:
            for d in w["contributionDays"]:
                days.append((d["date"], d["contributionCount"]))

    counts = dict(days)
    today = now.date()
    streak = 0
    # A streak is alive if today or yesterday has contributions.
    cursor = today if counts.get(str(today), 0) > 0 else today - dt.timedelta(days=1)
    while counts.get(str(cursor), 0) > 0:
        streak += 1
        cursor -= dt.timedelta(days=1)

    rows = [
        ("contributions (all time)", f"{total_contribs:,}"),
        (f"contributions ({now.year})", f"{year_contribs:,}"),
        ("current streak", f"{streak} day" + ("" if streak == 1 else "s")),
    ]
    updated = today.strftime("%b %d, %Y")

    row_svg = ""
    y = 118
    for label, value in rows:
        row_svg += (
            f'  <text x="32" y="{y}" font-size="15" fill="#8b949e">{label}</text>\n'
            f'  <text x="470" y="{y}" font-size="15" font-weight="600" '
            f'fill="#58a6ff">{value}</text>\n'
        )
        y += 32

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 230" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" role="img" aria-label="GitHub stats: {total_contribs:,} contributions all time, {year_contribs:,} this year, {streak}-day streak">
  <rect x="1" y="1" width="798" height="228" rx="10" fill="#0d1117" stroke="#30363d" stroke-width="1.5"/>
  <line x1="1" y1="40" x2="799" y2="40" stroke="#30363d" stroke-width="1"/>
  <circle cx="26" cy="20.5" r="6" fill="#30363d"/>
  <circle cx="46" cy="20.5" r="6" fill="#30363d"/>
  <circle cx="66" cy="20.5" r="6" fill="#30363d"/>
  <text x="400" y="25" text-anchor="middle" font-size="13" fill="#8b949e">nicolas@baena-labs: ~</text>
  <text x="32" y="78" font-size="15">
    <tspan fill="#58a6ff">$</tspan>
    <tspan fill="#8b949e" dx="8">gh stats</tspan>
  </text>
{row_svg}  <text x="768" y="210" text-anchor="end" font-size="11" fill="#484f58">updated {updated}</text>
</svg>
"""
    with open(OUT, "w") as f:
        f.write(svg)
    print(f"wrote {os.path.normpath(OUT)}: {total_contribs:,} contribs all time, "
          f"{year_contribs:,} this year, {streak}-day streak")


if __name__ == "__main__":
    sys.exit(main())
