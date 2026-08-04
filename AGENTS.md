# External RWE Signal Watch

These instructions apply to the entire repository.

## Mission

Publish a concise, evidence-led daily briefing on public material about:

1. frontier and agentic AI applied to real-world data and real-world evidence;
2. causal inference, target-trial emulation, phenotyping, and trial design;
3. HIPAA Expert Determination and statistical de-identification;
4. re-identification risk, quasi-identifiers, and privacy-enhancing methods;
5. healthcare tokenization, privacy-preserving linkage, patient matching, and identity resolution;
6. regulatory use of RWD and RWE; and
7. scientific evaluation, provenance, reproducibility, validation, and governance.

This is public-web research only. Never use, request, infer, summarize, or publish confidential Datavant information.

## Hard exclusions

- Do not monitor, quote, or feature current Datavant employees as experts.
- Do not use Datavant-authored marketing, blogs, webinars, or social posts as evidence for an edition.
- Datavant may be mentioned only when unavoidable context in a primary third-party source requires it. Keep that mention factual and minimal.
- Before adding a person to `config/watchlist.json`, verify that the person is not currently employed by Datavant.
- Never follow, connect, like, react, comment, repost, subscribe, or message on any platform. Research is read-only.

## Definitions

### Frontier AI for RWE

Includes agentic or multi-agent systems, LLMs and foundation models used for scientific work, MCP servers and skills in evidence workflows, cohort construction, phenotyping, protocol work, target-trial emulation, causal inference, statistical-analysis generation or review, data-quality assessment, evidence synthesis, provenance, reproducibility, evaluation, error detection, and human oversight.

### Expert Determination

Means HIPAA 45 CFR 164.514(b)(1), statistical re-identification risk, quasi-identifiers, recipient and release-environment considerations, motivated-intruder analysis, k-anonymity and related methods, structured and unstructured health-data de-identification, composition risk, continuously refreshed data, and relevant synthetic-data privacy and utility.

### Tokenization

Means privacy-preserving patient matching and record linkage—not cryptocurrency and not LLM text tokens. Track match quality, false and missed matches, split or broken identities, source coverage, durability, endpoint capture, longitudinal observability, enrichment, and fitness for a stated research question.

Tokenization is not, by itself, a HIPAA de-identification method. Linkage quality and evidence fitness are separate questions.

## Start every daily run here

1. Read this file, `automation_prompt.md`, and all files in `config/`.
2. Read `state/seen_items.jsonl`, `state/run_log.jsonl`, `state/source_health.json`, and `state/watchlist_candidates.json`.
3. Determine the local date in `America/New_York`.
4. Use a 48-hour overlap for posts and news, and a 14-day overlap for papers, conference records, standards, and regulatory pages.
5. Search the named people first, then institutional feeds, then the thematic queries.
6. Verify every included item at the most primary accessible source.

## Source hierarchy

Prefer, in order:

1. regulations, regulator guidance, official proceedings, papers, preprints, posters, protocols, code repositories, and direct author posts;
2. university, journal, society, conference, sponsor, and company research pages;
3. interviews or trade publications with attributable statements;
4. search snippets and aggregators only for discovery.

Do not present a snippet as verified evidence. If a primary source is inaccessible, either use a credible accessible source and label the limitation, or omit the item. LinkedIn coverage will be incomplete; triangulate with author pages, publications, conference programs, and institutional posts.

## Search and verification rules

- Search exact names in quotes with the topic terms and date window.
- Confirm the author, publication date, direct URL, and relevance before scoring.
- Separate what the source establishes from your inference.
- Do not overstate early results, preprints, abstracts, posters, vendor claims, or social posts.
- Treat commercial perspective as useful but disclose the commercial context.
- Prefer concrete methods, data, numerical results, limitations, validation, failure modes, and clearly bounded use cases.
- Downgrade tokenization claims that report match rate without source coverage, error rates, durability, or clinical observability.
- Downgrade AI claims that lack task-specific evaluation, reproducibility, provenance, or human accountability.
- Downgrade “regulatory grade” claims that omit study design, endpoint validity, estimands, bias, or auditability.
- Downgrade “HIPAA compliant” claims that do not identify the de-identification basis, recipient, intended use, and risk logic.
- Respect copyright. Quote sparingly and prefer paraphrase.

## Signal score

Score each candidate out of 10:

- relevance to the watch topics: 0–3;
- evidence quality and primary-source support: 0–3;
- novelty or decision value: 0–2;
- useful external viewpoint for a Datavant reader: 0–1;
- timeliness: 0–1.

Apply penalties after the subtotal:

- unsupported promotional framing: −2;
- secondhand claim when a primary source should exist: −1;
- undisclosed or unclear commercial interest: −1;
- materially recycled content with no new information: −2.

Include items scoring 6 or higher. Lead items should normally score 8 or higher. A quiet edition with one strong item is better than a padded edition. If nothing qualifies, publish a short “No new high-signal items” edition that lists the sources checked and any access limitations.

## Daily edition format

Each edition must contain:

1. a specific, non-clickbait headline;
2. a one-paragraph executive readout;
3. 1–7 ranked items, each with the direct source link, author or institution, date, topic label, score, what happened, why it matters, evidence limits, and practical follow-up question;
4. a “What changed” section that distinguishes new signal from recurring themes;
5. a source-health note when meaningful sources were inaccessible;
6. on Fridays, a compact weekly synthesis of repeated themes and contradictions.

Do not claim completeness. Do not imply that lack of an indexed LinkedIn post means the person did not post.

## Files created by a successful run

Choose the edition slug `YYYY-MM-DD`. If it already exists, use `YYYY-MM-DD-2`, then `-3`, and so on.

- Write the research notes and citations to `sources/<slug>.md`.
- Write the concise daily report to `reports/daily/<slug>.md`.
- Write the public HTML to `site/editions/<slug>/index.html`.
- Copy that reviewed HTML to `site/index.html`, adjusting root-relative navigation if required.
- Add the new edition at the top of `site/editions/index.html`.
- Append included URLs to `state/seen_items.jsonl` only after the edition is complete.
- Append one run record to `state/run_log.jsonl`.
- Update `state/source_health.json` and `state/watchlist_candidates.json` when warranted.

Use `python scripts/dedupe.py` to canonicalize and check candidate URLs. Never remove prior editions or history during a normal run.

## State rules

- `seen_items.jsonl` is append-only and contains one JSON object per published item.
- A revised, substantially new version of a prior source may be included, but explain the delta.
- `run_log.jsonl` is append-only and records date, slug, item count, sources checked, access failures, and outcome.
- Add a watchlist candidate only after at least two independently useful artifacts or one unusually strong primary artifact. Do not promote candidates to the watchlist automatically.

## Publication checks

Before publishing:

1. run `python scripts/validate_project.py`;
2. run `bash scripts/check-publication.sh` when Bash is available;
3. inspect `git diff --check` and `git status --short`;
4. stage only files created or updated by this run;
5. commit with `Publish RWE signal watch <slug>` and push `main`.

The GitHub Pages workflow publishes `site/`. Never place secrets, local paths, private URLs, email addresses, internal company material, credentials, or personal browsing data under `site/`, `sources/`, `reports/`, `config/`, or `README.md`.
