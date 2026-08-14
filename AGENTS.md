# RWE-Signal

These instructions apply to the entire repository.

## Mission

Publish a concise, evidence-led daily briefing about the intersection of frontier AI and real-world data or real-world evidence. The core beat is agents, LLMs, and foundation-model workflows used to produce, evaluate, govern, or critique RWD/RWE.

Track causal inference, target-trial emulation, phenotyping, trial design, regulation, privacy, de-identification, tokenization, linkage, provenance, reproducibility, validation, and governance only when the reported development materially involves AI and materially involves RWD/RWE.

This is public-web research only. Never use, request, infer, summarize, or publish confidential Datavant information.

## Hard editorial intersection gate

Every candidate must pass both sides of this gate before it can be scored:

1. **AI side:** the primary source materially concerns an AI agent, multi-agent system, LLM, foundation model, generative-AI workflow, or the task-specific evaluation or governance of such a system.
2. **RWE side:** the primary source materially concerns RWD/RWE or a named part of the evidence lifecycle, such as cohort construction, phenotyping, target-trial specification, causal analysis, evidence synthesis, or regulatory evidence generation using real-world health data. Clinical-trial registries and outcome records, EHRs, claims, observational patient data, postmarket safety reports, and clinicogenomic datasets count when the AI system uses them to generate, structure, test, or synthesize evidence.

The source itself must establish the intersection. Do not manufacture it through editorial inference. Conventional predictive models, generic healthcare AI, generic causal inference, general RWE policy, ordinary RWD studies, standalone FDA submission counts, linkage, tokenization, Expert Determination, anonymisation, and de-identification do not qualify unless an agent, LLM, or foundation-model workflow is a material part of the same development.

RWE-only material may appear briefly as clearly dated supporting context inside a qualifying AI-plus-RWE story. It may not lead an edition, receive its own reported section, or count toward the item total. AI-only material outside the RWD/RWE lifecycle is likewise context-only. If no new source passes both sides, publish the no-new-signal edition.

## Hard exclusions

- Do not monitor, quote, or feature current Datavant employees as experts.
- Do not use Datavant-authored marketing, blogs, webinars, or social posts as evidence for an edition.
- Datavant may be mentioned only when unavoidable context in a primary third-party source requires it. Keep that mention factual and minimal.
- Before adding a person to `config/watchlist.json`, verify that the person is not currently employed by Datavant.
- Never follow, connect, like, react, comment, repost, subscribe, or message on any platform. Research is read-only.

## Definitions

### Frontier AI for RWE

Includes agentic or multi-agent systems, LLMs and foundation models used for scientific work, MCP servers and skills in evidence workflows, cohort construction, phenotyping, protocol work, target-trial emulation, causal inference, statistical-analysis generation or review, data-quality assessment, evidence synthesis, provenance, reproducibility, evaluation, error detection, and human oversight.

### Agentic scientific evidence infrastructure

Treat major projects such as paper-to-agent systems, executable research papers, AI scientists, virtual labs, virtual biotechs, autonomous research organizations, scientific-agent swarms, and agent-enabled digital twins as a permanent frontier-discovery lane.

Classify them by what they do:

- **Executable evidence:** turns a paper, method, codebase, or dataset into an agent that can reproduce analyses or apply the method to new health data.
- **Evidence intelligence:** uses agents to curate or synthesize clinical trials, registries, literature, safety reports, observational records, or multimodal patient evidence.
- **In-silico evidence generation:** uses agent teams, digital twins, synthetic cohorts, or synthetic control arms to inform trial or therapeutic decisions.

These labels are discovery routes, not automatic publication passes. A general paper agent or AI scientist is AI-only until a source shows a material health-evidence application. A system qualifies when it performs a concrete evidence-lifecycle task on relevant health data, even if its authors call the work biomedical discovery or clinical development rather than RWE. State whether the artifact is peer reviewed, a preprint, a repository, a demonstration, or an institutional announcement, and report the validation and human-oversight limits.

### Expert Determination

Means HIPAA 45 CFR 164.514(b)(1), statistical re-identification risk, quasi-identifiers, recipient and release-environment considerations, motivated-intruder analysis, k-anonymity and related methods, structured and unstructured health-data de-identification, composition risk, continuously refreshed data, and relevant synthetic-data privacy and utility.

This lane is publishable only when the same source materially connects those questions to agents, LLMs, foundation models, or AI-enabled RWE workflows.

### Tokenization

Means privacy-preserving patient matching and record linkage—not cryptocurrency and not LLM text tokens. Track match quality, false and missed matches, split or broken identities, source coverage, durability, endpoint capture, longitudinal observability, enrichment, and fitness for a stated research question.

Tokenization is not, by itself, a HIPAA de-identification method. Linkage quality and evidence fitness are separate questions.

This lane is publishable only when the same source materially connects tokenization or linkage to an AI-enabled RWD/RWE workflow.

## Start every daily run here

1. Read this file, `automation_prompt.md`, and all files in `config/`.
2. Read `state/seen_items.jsonl`, `state/run_log.jsonl`, `state/source_health.json`, and `state/watchlist_candidates.json`.
3. Determine the local date in `America/New_York`.
4. Use a 30-day discovery window for all source types. For posts and fast-moving news, prioritize the most recent 48 hours first, then search the remainder of the month for missed high-signal work.
5. Search the named people first, then the frontier institutional radar and its conferences or project launches, then the remaining institutional feeds and thematic queries.
6. Treat an institutional story as a discovery lead: trace named systems and claims to the paper, preprint, repository, dataset, proceedings, talk, or direct author post whenever one exists.
7. Verify every included item at the most primary accessible source.

## Source hierarchy

Prefer, in order:

1. regulations, regulator guidance, official proceedings, papers, preprints, posters, protocols, code repositories, and direct author posts;
2. university, journal, society, conference, sponsor, and company research pages;
3. interviews or trade publications with attributable statements;
4. search snippets and aggregators only for discovery.

Do not present a snippet as verified evidence. If a primary source is inaccessible, either use a credible accessible source and label the limitation, or omit the item. LinkedIn coverage will be incomplete; triangulate with author pages, publications, conference programs, and institutional posts.

An official university or conference announcement may anchor a story when it is the first public record of a material launch, demonstration, or result and no more primary artifact is yet public. Say that plainly and do not imply peer review. When an announcement summarizes an existing paper or project, cluster them as one story and anchor to the underlying artifact.

## Search and verification rules

- Search exact names in quotes with the topic terms and date window.
- Use the source's electronic publication or substantive update date, not a nominal journal issue month, when deciding whether it falls inside the discovery window.
- Confirm the author, publication date, direct URL, and relevance before scoring.
- Record a one-sentence `ai_rwe_intersection` test in the research notes for every scored candidate. Reject the candidate before scoring if either side is missing.
- Separate what the source establishes from your inference.
- Do not overstate early results, preprints, abstracts, posters, vendor claims, or social posts.
- Treat commercial perspective as useful but disclose the commercial context.
- Prefer concrete methods, data, numerical results, limitations, validation, failure modes, and clearly bounded use cases.
- Downgrade tokenization claims that report match rate without source coverage, error rates, durability, or clinical observability.
- Downgrade AI claims that lack task-specific evaluation, reproducibility, provenance, or human accountability.
- Downgrade “regulatory grade” claims that omit study design, endpoint validity, estimands, bias, or auditability.
- Downgrade “HIPAA compliant” claims that do not identify the de-identification basis, recipient, intended use, and risk logic.
- Respect copyright. Quote sparingly and prefer paraphrase.

## Novelty and deduplication

The 30-day window is for discovery, not republication. Every public section must be anchored to a source or event that has not already been published by RWE-Signal.

- Check `state/seen_items.jsonl` and run `python scripts/dedupe.py` before drafting. Deduplicate by stable identifier as well as URL: DOI, PMID, arXiv ID, NCT number, regulator document and version, then canonical URL.
- Treat a paper, its press release, an author post, and trade coverage of that paper as one story. Anchor the section to the most primary source and use the other links only as supporting context.
- Assign the same `story_id` to different sources covering the same underlying event. Only the first primary-source-backed treatment is eligible for publication.
- Exact or substantially equivalent titles at different URLs are duplicates unless the later source documents a material change.
- A previously covered source may return only when there is a substantive new version, dataset, result, correction, policy decision, or regulatory action. Record a `content_version` and state the precise delta in the research notes and public prose.
- For living pages that retain one URL, such as annual regulator ledgers, a changed page is not automatically new. Publish it again only when the new version adds decision-relevant evidence.
- Older sources may appear as clearly dated background inside a genuinely new story; they do not make a story new.
- If no new candidate clears both the novelty gate and the signal threshold, publish the short no-new-signal edition instead of recycling prior coverage.

## Signal score

Only candidates that pass the hard intersection gate may be scored. Score each qualifying candidate out of 10:

- strength and specificity of the AI-plus-RWE intersection: 0–3;
- evidence quality and primary-source support: 0–3;
- novelty or decision value: 0–2;
- practical decision value for an RWE reader: 0–1;
- timeliness: 0–1.

Apply penalties after the subtotal:

- unsupported promotional framing: −2;
- secondhand claim when a primary source should exist: −1;
- undisclosed or unclear commercial interest: −1;
- materially recycled content with no new information: −2.

Include items scoring 6 or higher. Lead items should normally score 8 or higher. A quiet edition with one strong item is better than a padded edition. If nothing qualifies, publish a short “No new high-signal items” edition that lists the sources checked and any access limitations.

## Daily edition format

The public edition is a newspaper-style analysis, not a research log, scorecard, watchlist update, or explanation of the automation. Keep scoring, exclusions, search process, and source-management logic backstage in `sources/`, state, and configuration files.

### Editorial posture: constructive and tech-positive

The default public posture is optimistic, curious, and capability-led. Lead with what the technology now makes possible, what materially improved, and why the development advances AI-enabled evidence work.

- Write descriptive, capability-first headlines. Prefer the new system, result, deployment, or scientific advance as the subject.
- Do not default to the repeated contrast formula “the AI did X, but missed/failed/could not do Y.” Avoid gotcha framing, failure-first headlines, and headlines that turn one limitation into the identity of the story.
- Report material limitations, uncertainty, and validation needs accurately in the body. Frame them as the conditions for responsible scale, the next engineering or evidence frontier, or the boundary of the demonstrated result—not as an automatic rebuttal to the advance.
- Give concrete progress at least as much narrative weight as caveats. When a source publishes code, benchmarks, audit trails, human checkpoints, or reproducibility materials, treat that transparency as a positive technical contribution.
- Tech-positive does not mean promotional. Do not suppress contradictory evidence, soften a genuine safety event, or present a vendor claim as an independent result. A material failure may lead when the failure itself is the verified news.
- End with the opportunity, next unlock, or practical path forward whenever the evidence supports one.

Every substantive public section must be anchored to a qualifying AI-plus-RWE source and use `data-scope="ai-rwe"` on its `<section>` element. Mark the article `data-editorial-scope="ai-rwe"`. RWE-only background belongs inside the qualifying section that it helps explain, never in a standalone section.

Match the visual and editorial language of AI Daily Ledger: one large uppercase headline, a precise deck, a short dateline, an executive opening, and continuous reported prose divided by strong section headlines. Use the restrained beige-paper layout and inline CSS established by the reference ledger. Do not use cards, score badges, topic tags, ranked-item labels, or public methodology copy.

Each edition must contain:

1. a specific, non-clickbait headline;
2. a one-sentence deck that explains the editorial through-line;
3. a two-to-four paragraph executive readout;
4. one to five reported sections in descending importance, written as analysis rather than item cards;
5. direct source links embedded where the claims appear, with publication dates and evidence limits stated naturally in the prose;
6. a concluding section that distinguishes genuinely new signal from recurring themes;
7. a source-health note when meaningful sources were inaccessible; and
8. on Fridays, a compact weekly synthesis of repeated themes and contradictions.

Each substantive edition must also contain two or three evidence-led visuals. Do not force a visual into every section. Prefer native, responsive HTML/CSS charts, comparison tables, timelines, process diagrams, or other editorial graphics derived from the reported evidence. Use screenshots only when the appearance of the original post or document is itself newsworthy and a clean, legible crop can be made.

- Every visual must advance the reporting rather than decorate the page.
- Anchor every visual to one or more verified sources and include a concise source caption. Clearly label editorial synthesis or inference as such.
- Include a quantitative visual when the edition contains decision-relevant numerical evidence; use comparison or process graphics when numbers are not the clearest form.
- Make visuals accessible and responsive: use semantic figure markup, a useful accessible label, readable text, and a mobile layout with no horizontal overflow.
- Never invent missing values, imply false precision, or turn incomparable measures into a common scale.
- A no-new-signal edition may omit visuals rather than manufacture them.

Internal scores never appear in public HTML or the public daily report. Do not mention employer exclusions, the watchlist-selection process, search windows, deduplication, configuration, automation, or publishing mechanics in a public edition. Do not pad a quiet day with old or weak material; older sources may be used only as clearly dated context for a genuinely current development.

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
- Store `stable_id`, `story_id`, and `content_version` when available so alternate URLs and living pages can be checked reliably.
- A revised, substantially new version of a prior source may be included, but record and explain the delta.
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
