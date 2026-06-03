# obsidian-wiki-health

Obsidian 기반 LLM Wiki를 위한 local-first 유지보수 보조 툴킷입니다.

이 프로젝트는 단순 broken link 검사기를 넘어서 다음 문제를 더 빨리 찾는 데 초점을 둡니다.
- orphan note candidate
- stale/contradiction 검토 출발점
- query 전에 먼저 읽어야 할 관련 노트 후보

## Why
LLM Wiki는 만들수록 가치가 커지지만, 시간이 갈수록 유지보수가 더 어려워집니다.
이 도구는 "새 노트를 더 많이 만드는 것"보다 "기존 위키를 건강하게 유지하는 것"을 돕기 위해 만들어졌습니다.

## Features (v0.1)
- scan Obsidian vault
- parse `wiki/index.md`
- detect broken internal wikilinks
- find orphan candidates
- generate markdown report
- support research-deep pre-query note suggestions

## Install
```bash
pip install -e .
```

## Quick Start
```bash
obsidian-wiki-health scan /path/to/vault
obsidian-wiki-health report /path/to/vault --output report.md --query "LLM Wiki 유지보수"
obsidian-wiki-health research-deep /path/to/vault "LLM Wiki 유지보수"
```

## Philosophy
- local-first
- markdown-first
- human review before destructive edits
- assist maintenance, do not silently rewrite knowledge

## Non-goals (v0.1)
- automatic rewriting of notes
- vendor-locked LLM workflow
- heavy GUI plugin
- background sync or database server

## Project Layout
```text
src/obsidian_wiki_health/
  cli.py
  common.py
  index_parser.py
  link_checker.py
  orphan_detector.py
  research_deep.py
  report_writer.py
tests/
  fixtures/sample_vault/
```

## Status
Prototype scaffold with passing tests.

## License
MIT
