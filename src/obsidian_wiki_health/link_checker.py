from __future__ import annotations

from pathlib import Path

from .common import extract_wikilinks, iter_markdown_files, target_to_path, to_repo_path


def find_broken_links(vault_root: Path) -> list[dict[str, str]]:
    broken: list[dict[str, str]] = []
    for path in iter_markdown_files(vault_root):
        text = path.read_text(encoding="utf-8")
        for target in extract_wikilinks(text):
            if not target_to_path(target, vault_root).exists():
                broken.append({"source": to_repo_path(path, vault_root), "target": target})
    return broken
