from __future__ import annotations

from pathlib import Path

from .common import extract_wikilinks, iter_markdown_files, resolve_wikilink_target, to_repo_path


def find_broken_links(vault_root: Path) -> list[dict[str, str]]:
    broken: list[dict[str, str]] = []
    for path in iter_markdown_files(vault_root):
        text = path.read_text(encoding="utf-8")
        for target in extract_wikilinks(text):
            target_path, reason = resolve_wikilink_target(target, vault_root)
            if target_path is None:
                broken.append({
                    "source": to_repo_path(path, vault_root),
                    "target": target,
                    "reason": reason or "invalid-target",
                })
                continue
            if not target_path.exists():
                broken.append({
                    "source": to_repo_path(path, vault_root),
                    "target": target,
                    "reason": reason or "missing",
                })
    return broken
