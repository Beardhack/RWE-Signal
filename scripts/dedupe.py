#!/usr/bin/env python3
"""Canonicalize and deduplicate candidate research items.

Input is a JSON array or an object with an ``items`` array. Each item must have
``url`` and should have ``title``. Existing published items are read from the
append-only JSONL state file.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit


TRACKING_KEYS = {
    "fbclid",
    "gclid",
    "mc_cid",
    "mc_eid",
    "ref",
    "ref_src",
}


def canonicalize_url(raw_url: str) -> str:
    raw_url = raw_url.strip()
    parts = urlsplit(raw_url)
    if parts.scheme not in {"http", "https"} or not parts.netloc:
        raise ValueError(f"not an absolute HTTP(S) URL: {raw_url!r}")

    host = (parts.hostname or "").lower()
    port = parts.port
    if port and not ((parts.scheme == "https" and port == 443) or (parts.scheme == "http" and port == 80)):
        host = f"{host}:{port}"

    path = re.sub(r"/{2,}", "/", parts.path or "/")
    if path != "/":
        path = path.rstrip("/")

    query = []
    for key, value in parse_qsl(parts.query, keep_blank_values=True):
        lowered = key.lower()
        if lowered.startswith("utm_") or lowered in TRACKING_KEYS:
            continue
        query.append((key, value))
    query.sort(key=lambda pair: (pair[0].lower(), pair[1]))

    return urlunsplit((parts.scheme.lower(), host, path, urlencode(query, doseq=True), ""))


def normalize_title(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", title.casefold()).strip()


def fingerprint(url: str, title: str = "") -> str:
    payload = f"{canonicalize_url(url)}\n{normalize_title(title)}".encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def load_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    rows: list[dict] = []
    for line_number, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw_line.strip():
            continue
        try:
            value = json.loads(raw_line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}:{line_number}: {exc}") from exc
        if not isinstance(value, dict):
            raise ValueError(f"{path}:{line_number}: expected a JSON object")
        rows.append(value)
    return rows


def load_candidates(path: Path) -> list[dict]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(value, dict):
        value = value.get("items")
    if not isinstance(value, list):
        raise ValueError("candidate file must be a JSON array or an object with an items array")
    if not all(isinstance(item, dict) for item in value):
        raise ValueError("every candidate must be a JSON object")
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidates", type=Path, required=True)
    parser.add_argument("--seen", type=Path, default=Path("state/seen_items.jsonl"))
    parser.add_argument("--output", type=Path, help="Write the result JSON here; stdout is used otherwise.")
    parser.add_argument("--record", action="store_true", help="Append unique candidates to the seen JSONL file.")
    args = parser.parse_args()

    try:
        seen_rows = load_jsonl(args.seen)
        candidates = load_candidates(args.candidates)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"dedupe error: {exc}", file=sys.stderr)
        return 2

    seen_urls: set[str] = set()
    seen_fingerprints: set[str] = set()
    for row in seen_rows:
        raw_url = row.get("canonical_url") or row.get("url")
        if isinstance(raw_url, str):
            try:
                seen_urls.add(canonicalize_url(raw_url))
            except ValueError:
                pass
        if isinstance(row.get("fingerprint"), str):
            seen_fingerprints.add(row["fingerprint"])

    unique: list[dict] = []
    duplicates: list[dict] = []
    batch_urls: set[str] = set()
    batch_fingerprints: set[str] = set()

    for item in candidates:
        raw_url = item.get("url")
        if not isinstance(raw_url, str):
            duplicates.append({**item, "dedupe_reason": "missing_url"})
            continue
        try:
            canonical_url = canonicalize_url(raw_url)
        except ValueError:
            duplicates.append({**item, "dedupe_reason": "invalid_url"})
            continue
        item_fingerprint = fingerprint(canonical_url, str(item.get("title", "")))
        normalized = {**item, "canonical_url": canonical_url, "fingerprint": item_fingerprint}
        if canonical_url in seen_urls or item_fingerprint in seen_fingerprints:
            duplicates.append({**normalized, "dedupe_reason": "already_published"})
        elif canonical_url in batch_urls or item_fingerprint in batch_fingerprints:
            duplicates.append({**normalized, "dedupe_reason": "duplicate_in_batch"})
        else:
            unique.append(normalized)
            batch_urls.add(canonical_url)
            batch_fingerprints.add(item_fingerprint)

    result = {"unique": unique, "duplicates": duplicates}
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")

    if args.record and unique:
        args.seen.parent.mkdir(parents=True, exist_ok=True)
        with args.seen.open("a", encoding="utf-8", newline="\n") as handle:
            for item in unique:
                handle.write(json.dumps(item, ensure_ascii=False, separators=(",", ":")) + "\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
