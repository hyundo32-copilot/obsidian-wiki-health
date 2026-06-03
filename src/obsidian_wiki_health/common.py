from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable

WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")


def extract_wikilinks(text: str) -> list[str]:
    return [match.strip() for match in WIKILINK_RE.findall(text)]


def iter_markdown_files(vault_root: Path) -> Iterable[Path]:
    wiki_root = vault_root / "wiki"
    return sorted(path for path in wiki_root.rglob("*.md") if path.is_file())


def to_repo_path(path: Path, vault_root: Path) -> str:
    return path.relative_to(vault_root).as_posix()


def target_to_path(target: str, vault_root: Path) -> Path:
    return (vault_root / "wiki" / f"{target}.md").resolve()
