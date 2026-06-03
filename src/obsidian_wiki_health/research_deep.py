from __future__ import annotations

from pathlib import Path

from .common import iter_markdown_files, to_repo_path


def suggest_related_notes(vault_root: Path, query: str) -> list[str]:
    terms = [term for term in query.lower().split() if term]
    scored: list[tuple[int, str]] = []

    for path in iter_markdown_files(vault_root):
        if path.name in {"index.md", "log.md"}:
            continue
        text = path.read_text(encoding="utf-8").lower()
        score = sum(text.count(term) for term in terms)
        if score > 0:
            scored.append((score, to_repo_path(path, vault_root)))

    scored.sort(key=lambda item: (-item[0], item[1]))
    return [path for _, path in scored]
