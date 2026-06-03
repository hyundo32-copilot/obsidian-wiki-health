from __future__ import annotations

from pathlib import Path

from .common import extract_wikilinks


def parse_index_links(index_path: Path) -> list[str]:
    return extract_wikilinks(index_path.read_text(encoding="utf-8"))
