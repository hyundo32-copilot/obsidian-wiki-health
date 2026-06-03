from pathlib import Path

from obsidian_wiki_health.link_checker import find_broken_links


def test_find_broken_links_reports_missing_wikilinks():
    vault_root = Path(__file__).parent / "fixtures" / "sample_vault"

    broken = find_broken_links(vault_root)

    assert broken == [
        {
            "source": "wiki/syntheses/synthesis-a.md",
            "target": "topics/missing-topic",
        }
    ]
