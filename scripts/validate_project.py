#!/usr/bin/env python3
"""Validate configuration, persistent state, and the publishable static site."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parents[1]
PUBLIC_ROOTS = [ROOT / "site", ROOT / "sources", ROOT / "reports", ROOT / "config"]
JSON_FILES = [
    ROOT / "config/watchlist.json",
    ROOT / "config/source_feeds.json",
    ROOT / "config/search_queries.json",
    ROOT / "config/exclusions.json",
    ROOT / "state/source_health.json",
    ROOT / "state/watchlist_candidates.json",
]
JSONL_FILES = [ROOT / "state/seen_items.jsonl", ROOT / "state/run_log.jsonl"]
REQUIRED_FILES = [
    ROOT / "AGENTS.md",
    ROOT / "README.md",
    ROOT / "automation_prompt.md",
    ROOT / ".github/workflows/deploy-pages.yml",
    ROOT / "site/index.html",
    ROOT / "site/editions/index.html",
    ROOT / "site/watchlist/index.html",
    ROOT / "site/assets/style.css",
]


def load_json(path: Path, errors: list[str]):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"{path.relative_to(ROOT)}: {exc}")
        return None


def validate_jsonl(path: Path, errors: list[str]) -> int:
    count = 0
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        errors.append(f"{path.relative_to(ROOT)}: {exc}")
        return 0
    for line_number, line in enumerate(lines, 1):
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"{path.relative_to(ROOT)}:{line_number}: {exc}")
            continue
        if not isinstance(value, dict):
            errors.append(f"{path.relative_to(ROOT)}:{line_number}: expected an object")
        count += 1
    return count


def iter_public_files():
    for root in PUBLIC_ROOTS:
        if root.exists():
            yield from (path for path in root.rglob("*") if path.is_file())


def main() -> int:
    errors: list[str] = []
    for path in REQUIRED_FILES:
        if not path.is_file():
            errors.append(f"missing required file: {path.relative_to(ROOT)}")

    loaded = {path.name: load_json(path, errors) for path in JSON_FILES}
    watchlist = loaded.get("watchlist.json")
    names: list[str] = []
    source_count = 0
    if isinstance(watchlist, dict):
        people = watchlist.get("people")
        if not isinstance(people, list) or len(people) < 30:
            errors.append("config/watchlist.json: expected at least 30 people")
        else:
            for index, person in enumerate(people):
                if not isinstance(person, dict):
                    errors.append(f"config/watchlist.json: person {index} is not an object")
                    continue
                name = person.get("name")
                if not isinstance(name, str) or not name.strip():
                    errors.append(f"config/watchlist.json: person {index} has no name")
                    continue
                names.append(name.casefold())
                sources = person.get("sources")
                if not isinstance(sources, list) or not sources:
                    errors.append(f"config/watchlist.json: {name} has no sources")
                    continue
                for source in sources:
                    url = source.get("url") if isinstance(source, dict) else None
                    parts = urlsplit(url) if isinstance(url, str) else None
                    if not parts or parts.scheme != "https" or not parts.netloc:
                        errors.append(f"config/watchlist.json: invalid source URL for {name}")
                    source_count += 1
            if len(names) != len(set(names)):
                errors.append("config/watchlist.json: duplicate person names")

    exclusions = loaded.get("exclusions.json")
    if isinstance(exclusions, dict):
        blocked = exclusions.get("known_do_not_track_from_seed_research", [])
        for name in blocked:
            if isinstance(name, str) and name.casefold() in names:
                errors.append(f"excluded person appears in watchlist: {name}")

    for path in JSONL_FILES:
        validate_jsonl(path, errors)

    index_path = ROOT / "site/index.html"
    if index_path.is_file():
        index_text = index_path.read_text(encoding="utf-8")
        if "RWE-Signal" not in index_text:
            errors.append("site/index.html: missing publication name")
        if "All editions" not in index_text:
            errors.append("site/index.html: missing editions navigation")

    editions_index = ROOT / "site/editions/index.html"
    if editions_index.is_file():
        text = editions_index.read_text(encoding="utf-8")
        slugs = re.findall(r'href="(?:\./)?([^"/]+)/?"', text)
        for slug in slugs:
            if re.fullmatch(r"\d{4}-\d{2}-\d{2}(?:-\d+)?", slug):
                target = ROOT / "site/editions" / slug / "index.html"
                if not target.is_file():
                    errors.append(f"site/editions/index.html: missing edition {slug}")

    forbidden_patterns = {
        "Windows user path": re.compile(r"[A-Za-z]:\\Users\\", re.IGNORECASE),
        "local file URL": re.compile(r"file:///", re.IGNORECASE),
        "email address": re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"),
        "GitHub token": re.compile(r"(?:github_pat_|gh[pousr]_)[A-Za-z0-9_]+"),
        "private key": re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    }
    for path in iter_public_files():
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for label, pattern in forbidden_patterns.items():
            if pattern.search(text):
                errors.append(f"{path.relative_to(ROOT)}: contains {label}")

    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Validation passed: {len(names)} people and {source_count} person-source links.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
