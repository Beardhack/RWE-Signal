# Daily automation prompt

Run today's External RWE Signal Watch from this project directory.

Read and follow `AGENTS.md` completely. Load all configuration and persistent state before searching. Research the previous 48 hours for posts and news and the previous 14 days for papers, conference materials, regulatory updates, and other slow-moving primary sources. Search the named external experts first, then institutional feeds, then thematic queries.

Verify, score, and deduplicate every candidate. Exclude current Datavant employees and Datavant-authored material. Use public sources only and remain read-only on social platforms. Never manufacture an edition: if no candidate reaches the inclusion threshold, publish a concise no-new-signal edition with source-health notes.

Create the Markdown source notes, daily report, public HTML edition, latest homepage, edition index entry, and state updates required by `AGENTS.md`. On Friday, include the weekly synthesis. Preserve all existing history.

Run the validation and privacy checks. Inspect the final diff. If checks pass, commit only this run's files with `Publish RWE signal watch <slug>` and push `main` so GitHub Pages deploys the edition. If authentication, permissions, or a publication check blocks the push, do not bypass it; leave the reviewed files locally and report the exact blocker.

In the task result, summarize the highest-signal findings, link the new edition when the public URL is known, list meaningful source-access failures, and state whether the commit and push succeeded.
