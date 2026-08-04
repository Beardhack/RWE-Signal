# RWE-Signal

A daily, source-linked newspaper about the intersection of frontier AI and real-world evidence: agents, LLMs, and foundation-model workflows changing how evidence is produced and judged.

The publication follows the editorial and visual pattern of AI Daily Ledger: a reported lead, evidence-led analysis, restrained newspaper typography, two or three sourced editorial visuals per substantive edition, permanent editions, and automatic deployment through GitHub Pages.

## What it tracks

- Agents and LLMs for evidence generation, causal inference, and target-trial emulation
- Foundation-model workflows for cohort construction, phenotyping, protocol work, and evidence synthesis
- Evaluation, provenance, reproducibility, human oversight, and governance of AI-enabled RWE
- Privacy, de-identification, tokenization, linkage, and regulation only when they materially intersect with an AI-enabled RWD/RWE workflow

Research is public-web and read-only; it never follows, connects, reacts, comments, or messages on the user's behalf.

## Local validation

```powershell
python scripts/validate_project.py
```

If Bash is available:

```bash
bash scripts/check-publication.sh
```

## Publishing a new edition

The scheduled Codex task reads `AGENTS.md` and `automation_prompt.md`, researches current developments, verifies primary sources, and writes:

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
