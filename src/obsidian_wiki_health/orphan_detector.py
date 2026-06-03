from __future__ import annotations

from pathlib import Path

from .common import extract_wikilinks, iter_markdown_files, to_repo_path
from .index_parser import parse_index_links


def find_orphan_candidates(vault_root: Path) -> list[str]:
    wiki_root = vault_root / "wiki"
    index_links = set(parse_index_links(wiki_root / "index.md"))
    referenced = set(index_links)

    for path in iter_markdown_files(vault_root):
        if path.name in {"index.md", "log.md"}:
            continue
        referenced.update(extract_wikilinks(path.read_text(encoding="utf-8")))

    orphans: list[str] = []
    for path in iter_markdown_files(vault_root):
        if path.name in {"index.md", "log.md"}:
            continue
        logical = path.relative_to(wiki_root).with_suffix("").as_posix()
        if logical not in referenced:
            orphans.append(to_repo_path(path, vault_root))
    return orphans
