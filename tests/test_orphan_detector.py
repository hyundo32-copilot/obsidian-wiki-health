from pathlib import Path

from obsidian_wiki_health.orphan_detector import find_orphan_candidates


def test_find_orphan_candidates_excludes_index_and_linked_pages():
    vault_root = Path(__file__).parent / "fixtures" / "sample_vault"

    orphans = find_orphan_candidates(vault_root)

    assert orphans == []
