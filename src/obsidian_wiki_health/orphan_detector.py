from __future__ import annotations

from pathlib import Path

from .common import extract_wikilinks, iter_markdown_files, resolve_wikilink_target, to_repo_path
from .index_parser import parse_index_links


def _collect_resolved_references(vault_root: Path) -> set[str]:
    referenced: set[str] = set()
    for path in iter_markdown_files(vault_root):
        for target in extract_wikilinks(path.read_text(encoding="utf-8")):
            target_path, reason = resolve_wikilink_target(target, vault_root)
            if reason is None and target_path is not None and target_path.exists():
                referenced.add(to_repo_path(target_path, vault_root))
    return referenced


def find_orphan_candidates(vault_root: Path) -> list[str]:
    wiki_root = vault_root / "wiki"
    index_path = wiki_root / "index.md"
    referenced = _collect_resolved_references(vault_root)

    if index_path.exists():
        for target in parse_index_links(index_path):
            target_path, reason = resolve_wikilink_target(target, vault_root)
            if reason is None and target_path is not None and target_path.exists():
                referenced.add(to_repo_path(target_path, vault_root))

    orphans: list[str] = []
    for path in iter_markdown_files(vault_root):
        if path.name in {"index.md", "log.md"}:
            continue
        repo_path = to_repo_path(path, vault_root)
        if repo_path not in referenced:
            orphans.append(repo_path)
    return orphans
