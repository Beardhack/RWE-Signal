#!/usr/bin/env python3
"""Render the public follow list from config/watchlist.json."""

from __future__ import annotations

import html
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config/watchlist.json"
OUTPUT = ROOT / "site/watchlist/index.html"


def person_card(person: dict) -> str:
    topics = "".join(f'<span class="tag">{html.escape(topic)}</span>' for topic in person.get("topics", [])[:3])
    links = "".join(
        f'<a href="{html.escape(source["url"], quote=True)}">{html.escape(source["label"])}</a>'
        for source in person.get("sources", [])
    )
    follow = '<span class="label">Follow</span>' if person.get("follow_manually") else '<span class="label secondary">Monitor</span>'
    return f'''<article class="person-card">
      {follow}
      <h3>{html.escape(person["name"])}</h3>
      <p><strong>{html.escape(person["lane"])}</strong></p>
      <p>{topics}</p>
      <p class="links">{links}</p>
    </article>'''


def main() -> int:
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    people = config["people"]
    groups = {
        1: ("Follow first", "The active manual follow list and the first people searched each day."),
        2: ("Monitor closely", "Lower-frequency feeds and implementation authors that often surface important primary work."),
        3: ("Publication watch", "Exact-name searches for foundational evaluation authors and key conference coauthors."),
    }
    sections = []
    for priority, (title, description) in groups.items():
        cards = "\n".join(person_card(person) for person in people if person["priority"] == priority)
        sections.append(f'''<section class="section">
          <div class="tier-heading"><span class="score">Tier {priority}</span><h2>{title}</h2></div>
          <p>{description}</p>
          <div class="card-grid">{cards}</div>
        </section>''')

    document = f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="People and public sources monitored by External RWE Signal Watch.">
  <title>Who to follow — External RWE Signal Watch</title>
  <link rel="stylesheet" href="../assets/style.css">
</head>
<body>
  <main class="shell">
    <header class="masthead">
      <a class="brand" href="../">External RWE Signal Watch</a>
      <nav class="nav" aria-label="Publication navigation"><a href="../">Latest</a><a href="../editions/">Editions</a></nav>
    </header>
    <header class="hero">
      <p class="eyebrow">Curated public watchlist · {len(people)} people</p>
      <h1>Who to follow</h1>
      <p class="dek">Outside-Datavant experts spanning regulation, agentic evidence generation, causal methods, de-identification, privacy engineering, and patient-level linkage.</p>
      <p class="meta">Follow actions are manual. Automated research stays read-only.</p>
    </header>
    <div class="content">
      <div class="callout"><p><strong>Coverage note:</strong> public search cannot guarantee complete LinkedIn coverage. The ledger pairs social profiles with institutional pages, journals, conference records, and publication searches wherever possible.</p></div>
      {''.join(sections)}
    </div>
    <footer class="footer"><p>Datavant employees and Datavant-authored sources are excluded.</p><p><a href="../">Latest edition</a></p></footer>
  </main>
</body>
</html>
'''
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(document, encoding="utf-8", newline="\n")
    print(f"Rendered {len(people)} people to {OUTPUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
