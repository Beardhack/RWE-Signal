#!/usr/bin/env python3
"""Canonicalize and deduplicate candidate research items.

Input is a JSON array or an object with an ``items`` array. Each item must have
``url`` and should have ``title``. Items may also provide ``stable_id``, ``doi``,
``pmid``, ``arxiv_id``, ``nct_id``, ``story_id``, and ``content_version``.
Existing published items are read from the append-only JSONL state file.
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


def normalize_identifier(value: object) -> str:
    return re.sub(r"\s+", "", str(value).strip().casefold())


def derive_stable_id(item: dict, canonical_url: str) -> str:
    explicit = item.get("stable_id")
    if explicit:
        return normalize_identifier(explicit)

    doi = item.get("doi")
    if doi:
        normalized = normalize_identifier(doi)
        normalized = re.sub(r"^(?:https?://(?:dx\.)?doi\.org/|doi:)", "", normalized)
        return f"doi:{normalized}"

    pmid = item.get("pmid")
    if pmid:
        return f"pmid:{normalize_identifier(pmid)}"

    arxiv_id = item.get("arxiv_id")
    if arxiv_id:
        normalized = re.sub(r"v\d+$", "", normalize_identifier(arxiv_id))
        return f"arxiv:{normalized}"

    nct_id = item.get("nct_id")
    if nct_id:
        return f"nct:{normalize_identifier(nct_id)}"

    parts = urlsplit(canonical_url)
    host = (parts.hostname or "").lower()
    if host in {"doi.org", "dx.doi.org"} and parts.path.strip("/"):
        return f"doi:{normalize_identifier(parts.path.strip('/'))}"
    if host in {"pubmed.ncbi.nlm.nih.gov", "www.ncbi.nlm.nih.gov"}:
        match = re.search(r"/(?:pubmed/)?(\d+)(?:/|$)", parts.path)
        if match:
            return f"pmid:{match.group(1)}"
    if host in {"arxiv.org", "www.arxiv.org"}:
        match = re.search(r"/(?:abs|pdf)/([^/]+)", parts.path)
        if match:
            return f"arxiv:{re.sub(r'v\d+$', '', match.group(1).casefold())}"

    return f"url:{canonical_url}"


def versioned_key(value: str, content_version: object) -> str:
    version = normalize_identifier(content_version) if content_version else ""
    return f"{value}::version:{version}" if version else value


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

    seen_identity_keys: set[str] = set()
    seen_url_keys: set[str] = set()
    seen_titles: set[str] = set()
    seen_story_ids: set[str] = set()
    seen_fingerprints: set[str] = set()
    for row in seen_rows:
        raw_url = row.get("canonical_url") or row.get("url")
        if isinstance(raw_url, str):
            try:
                canonical_url = canonicalize_url(raw_url)
                content_version = row.get("content_version")
                seen_url_keys.add(versioned_key(canonical_url, content_version))
                stable_id = derive_stable_id(row, canonical_url)
                seen_identity_keys.add(versioned_key(stable_id, content_version))
            except ValueError:
                pass
        normalized_title = normalize_title(str(row.get("title", "")))
        if normalized_title and not row.get("content_version"):
            seen_titles.add(normalized_title)
        story_id = row.get("story_id")
        if story_id:
            seen_story_ids.add(versioned_key(normalize_identifier(story_id), row.get("content_version")))
        if isinstance(row.get("fingerprint"), str):
            seen_fingerprints.add(row["fingerprint"])

    unique: list[dict] = []
    duplicates: list[dict] = []
    batch_identity_keys: set[str] = set()
    batch_url_keys: set[str] = set()
    batch_titles: set[str] = set()
    batch_story_ids: set[str] = set()
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
        item_title = normalize_title(str(item.get("title", "")))
        item_fingerprint = fingerprint(canonical_url, str(item.get("title", "")))
        stable_id = derive_stable_id(item, canonical_url)
        content_version = item.get("content_version")
        identity_key = versioned_key(stable_id, content_version)
        url_key = versioned_key(canonical_url, content_version)
        story_id = item.get("story_id")
        story_key = versioned_key(normalize_identifier(story_id), content_version) if story_id else ""
        normalized = {
            **item,
            "canonical_url": canonical_url,
            "stable_id": stable_id,
            "fingerprint": item_fingerprint,
        }

        seen_duplicate = identity_key in seen_identity_keys or url_key in seen_url_keys
        batch_duplicate = identity_key in batch_identity_keys or url_key in batch_url_keys
        if not content_version and item_title:
            seen_duplicate = seen_duplicate or item_title in seen_titles
            batch_duplicate = batch_duplicate or item_title in batch_titles
        if story_key:
            seen_duplicate = seen_duplicate or story_key in seen_story_ids
            batch_duplicate = batch_duplicate or story_key in batch_story_ids

        if seen_duplicate or (not content_version and item_fingerprint in seen_fingerprints):
            duplicates.append({**normalized, "dedupe_reason": "already_published"})
        elif batch_duplicate or (not content_version and item_fingerprint in batch_fingerprints):
            duplicates.append({**normalized, "dedupe_reason": "duplicate_in_batch"})
        else:
            unique.append(normalized)
            batch_identity_keys.add(identity_key)
            batch_url_keys.add(url_key)
            if not content_version and item_title:
                batch_titles.add(item_title)
            if story_key:
                batch_story_ids.add(story_key)
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
