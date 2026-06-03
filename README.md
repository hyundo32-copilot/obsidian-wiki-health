# obsidian-wiki-health

`obsidian-wiki-health` is a local-first CLI toolkit for maintaining Obsidian-based LLM wikis.

Think of it as a **pre-flight checker** before you ask an LLM to reason over your notes. It helps you find what is broken, orphaned, or worth reviewing first — without sending your vault anywhere and without rewriting your notes automatically.

## Why

LLM wikis grow quickly. Over time, even a useful Obsidian vault can accumulate:

- broken internal wikilinks
- notes that are no longer connected to the main knowledge map
- missing context before an LLM query
- maintenance work that is hard to review consistently

Generic link checkers can tell you whether a link is broken. `obsidian-wiki-health` focuses on the broader health of a markdown knowledge base used with LLMs, NotebookLM-style workflows, and AI agents.

## What it checks

Current v0.1 features:

- scan an Obsidian vault that uses `wiki/index.md` as its knowledge map
- parse internal Obsidian wikilinks such as `[[topics/topic-a]]`, `[[topics/topic-a.md]]`, `[[topics/topic-a#heading]]`, and `[[topics/topic-a|alias]]`
- resolve simple basename links such as `[[Topic A]]` when there is exactly one matching markdown file
- detect broken or unsafe internal wikilinks
- find orphan note candidates
- suggest notes to review before asking an LLM a query
- generate a human-reviewable markdown report

## Install

From a local checkout (Python 3.10+):

```bash
git clone https://github.com/hyundo32-copilot/obsidian-wiki-health.git
cd obsidian-wiki-health
python -m pip install -e .
```

For development:

```bash
python -m pip install -e .
python -m pytest -q
ruff check .
```

## Quick Start

Print a health report:

```bash
obsidian-wiki-health scan /path/to/vault
```

Write a markdown report:

```bash
obsidian-wiki-health report /path/to/vault --output report.md --query "LLM Wiki maintenance"
```

Suggest notes to read before an LLM query:

```bash
obsidian-wiki-health suggest /path/to/vault "LLM Wiki maintenance"
```

`research-deep` is kept as a backward-compatible alias for `suggest`.

## Example Output

```md
# Obsidian Wiki Health Report

## Summary
- Broken links: 1
- Orphan candidates: 0
- Related notes: 3
- Query: `LLM Wiki maintenance`

## Broken Links
| Source | Target | Reason |
| --- | --- | --- |
| wiki/syntheses/synthesis-a.md | topics/missing-topic | missing |

## Orphan Candidates
- none

## Suggested Reading Before Query
- wiki/syntheses/synthesis-a.md
- wiki/topics/topic-a.md
- wiki/topics/topic-b.md
```

## Philosophy

- **local-first**: runs against local markdown files
- **markdown-first**: no database or server required
- **human review before destructive edits**: reports first, no silent rewrites
- **LLM workflow aware**: helps prepare context before asking an LLM

## Current Limitations

This is an early prototype. The scope is intentionally small.

- Assumes a vault layout with `wiki/index.md`.
- Checks markdown files under `wiki/` only.
- Handles Obsidian-style wikilinks, not every markdown link form.
- Does not rewrite notes automatically.
- Does not yet perform semantic stale-note or contradiction detection.
- Basename links are supported only when they resolve to exactly one markdown file.

## Roadmap

See [`docs/roadmap.md`](docs/roadmap.md).

## License

MIT
