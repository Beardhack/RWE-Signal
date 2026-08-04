# RWE-Signal

A daily, source-linked briefing on high-signal public work at the intersection of frontier AI, real-world evidence, HIPAA Expert Determination, and healthcare tokenization.

The project follows the publishing pattern of AI Daily Ledger: reviewed static HTML, Markdown source notes, persistent deduplication state, and automatic deployment through GitHub Pages.

## What it tracks

- Agentic AI for evidence generation, causal inference, and target-trial emulation
- RWD/RWE regulatory policy and scientific evaluation
- Expert Determination, de-identification, and re-identification risk
- Privacy-preserving patient matching, tokenization, and data-linkage quality

Datavant employees and Datavant-authored material are deliberately excluded. Research is public-web and read-only; it never follows, connects, reacts, comments, or messages on the user's behalf.

## Local validation

```powershell
python scripts/validate_project.py
```

If Bash is available:

```bash
bash scripts/check-publication.sh
```

## Publishing a new edition

The scheduled Codex task reads `AGENTS.md` and `automation_prompt.md`, searches the configured sources, deduplicates against `state/seen_items.jsonl`, and writes:

- `sources/<slug>.md`
- `reports/daily/<slug>.md`
- `site/editions/<slug>/index.html`
- the latest edition to `site/index.html`
- updated edition and state indexes

After validation it commits and pushes to `main`. `.github/workflows/deploy-pages.yml` deploys `site/` to GitHub Pages.

## Schedule

Daily at 7:00 AM America/New_York, using a persistent local Codex project so deduplication and source-health state survive between runs. Friday editions add a weekly synthesis.

## Important limitation

Public search cannot guarantee complete LinkedIn coverage. The workflow triangulates indexed posts with author pages, papers, conference databases, institutional announcements, and regulatory sources. The watchlist page is therefore also a manual follow list.
