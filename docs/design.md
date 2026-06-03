# Design

## v0.1 scope

`obsidian-wiki-health` is a local-first pre-flight checker for Obsidian-based LLM wikis.

It intentionally starts with deterministic markdown/file-graph checks before adding any LLM-assisted behavior.

Current scope:

- Parse `wiki/index.md` as the main knowledge map.
- Scan markdown files under `wiki/`.
- Detect broken or unsafe Obsidian wikilinks.
- Detect orphan note candidates.
- Suggest related notes before an LLM query.
- Emit a human-reviewable markdown report.

## Link resolution policy

Supported wikilink forms:

- `[[topics/topic-a]]`
- `[[topics/topic-a.md]]`
- `[[topics/topic-a#heading]]`
- `[[topics/topic-a|alias]]`
- `[[Topic A]]` when exactly one `Topic A.md` exists under `wiki/`

Safety policy:

- Links are resolved only inside `vault/wiki`.
- Absolute paths and `..` traversal outside `wiki/` are reported as `outside-wiki`.
- Ambiguous basename links are reported as `ambiguous-target`.

## Principles

- No silent note rewrites.
- File-based only.
- Easy to run in CI or cron.
- Report first, let humans decide.
