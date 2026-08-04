# Daily automation prompt

Run today's RWE-Signal newspaper from this project directory.

Read and follow `AGENTS.md` completely. Load all configuration and persistent state before searching. Research a 30-day discovery window across posts, news, papers, conference materials, regulatory updates, and other primary sources, prioritizing the most recent 48 hours first. Search the named external experts first, then institutional feeds, then thematic queries.

Verify, score, and deduplicate every candidate. The month-long window is for discovery, not repeated reporting: cluster alternate coverage of the same event, check DOI, PMID, arXiv ID, NCT number, regulator document/version, canonical URL, normalized title, and `story_id`, and publish a previously covered source only after a material new version or decision-relevant update whose delta is explicit. Apply all internal source exclusions from `AGENTS.md`. Use public sources only and remain read-only on social platforms. Never manufacture an edition: if no candidate reaches both the novelty and inclusion thresholds, publish a concise no-new-signal edition with source-health notes.

Write the public edition as an RWE newspaper, closely matching AI Daily Ledger in look and feel: a large uppercase headline, a one-sentence deck, a short dateline, a crisp executive opening, and reported narrative sections separated by heavy rules. Lead with what changed and what the evidence means. Embed direct links in the prose and state limitations naturally. Do not publish scores, rankings, search logic, watchlist logic, employer exclusions, configuration details, automation instructions, or explanations of how the project works. The public page is the journalism, never the machinery behind it.

Create the Markdown source notes, daily report, public HTML edition, latest homepage, edition index entry, and state updates required by `AGENTS.md`. On Friday, include the weekly synthesis. Preserve all existing history.

Run the validation and privacy checks. Inspect the final diff. If checks pass, commit only this run's files with `Publish RWE signal watch <slug>` and push `main` so GitHub Pages deploys the edition. If authentication, permissions, or a publication check blocks the push, do not bypass it; leave the reviewed files locally and report the exact blocker.

In the task result, summarize the lead finding, link the new edition when the public URL is known, list meaningful source-access failures, and state whether the commit and push succeeded.
