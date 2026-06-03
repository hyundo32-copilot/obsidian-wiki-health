from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable

WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")


def extract_wikilinks(text: str) -> list[str]:
    return [match.strip() for match in WIKILINK_RE.findall(text)]


def validate_vault_root(vault_root: Path) -> None:
    if not vault_root.exists():
        raise ValueError(f"vault path does not exist: {vault_root}")
    if not vault_root.is_dir():
        raise ValueError(f"vault path is not a directory: {vault_root}")

    wiki_root = vault_root / "wiki"
    if not wiki_root.exists():
        raise ValueError(f"wiki directory not found under vault root: {wiki_root}")
    if not wiki_root.is_dir():
        raise ValueError(f"wiki path is not a directory: {wiki_root}")

    index_path = wiki_root / "index.md"
    if not index_path.exists():
        raise ValueError(f"wiki index not found: {index_path}")


def iter_markdown_files(vault_root: Path) -> Iterable[Path]:
    wiki_root = vault_root / "wiki"
    return sorted(path for path in wiki_root.rglob("*.md") if path.is_file())


def to_repo_path(path: Path, vault_root: Path) -> str:
    return path.resolve().relative_to(vault_root.resolve()).as_posix()


def _with_markdown_suffix(target: str) -> str:
    return target if target.lower().endswith(".md") else f"{target}.md"


def _is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
    except ValueError:
        return False
    return True


def resolve_wikilink_target(target: str, vault_root: Path) -> tuple[Path | None, str | None]:
    """Resolve an Obsidian wikilink target under ``vault_root/wiki``.

    Returns ``(path, None)`` when the target safely resolves inside the wiki.
    Returns ``(None, reason)`` for unsafe or ambiguous targets.
    Missing safe targets return the path they would map to; callers can check
    ``path.exists()`` and report a regular broken link.
    """
    wiki_root = (vault_root / "wiki").resolve()
    clean_target = target.strip()

    if not clean_target:
        return None, "empty-target"

    raw_path = Path(clean_target)
    if raw_path.is_absolute():
        return None, "outside-wiki"

    target_with_suffix = _with_markdown_suffix(clean_target)
    candidate = (wiki_root / target_with_suffix).resolve()
    if not _is_relative_to(candidate, wiki_root):
        return None, "outside-wiki"

    if "/" in clean_target or "\\" in clean_target:
        return candidate, None

    if candidate.exists():
        return candidate, None

    matches = sorted(path.resolve() for path in wiki_root.rglob(target_with_suffix) if path.is_file())
    safe_matches = [path for path in matches if _is_relative_to(path, wiki_root)]
    if len(safe_matches) == 1:
        return safe_matches[0], None
    if len(safe_matches) > 1:
        return None, "ambiguous-target"

    return candidate, None


def target_to_path(target: str, vault_root: Path) -> Path:
    path, reason = resolve_wikilink_target(target, vault_root)
    if path is None:
        raise ValueError(f"unsafe or ambiguous wikilink target {target!r}: {reason}")
    return path
