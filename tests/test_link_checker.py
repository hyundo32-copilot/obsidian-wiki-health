from pathlib import Path

from obsidian_wiki_health.link_checker import find_broken_links


def test_find_broken_links_reports_missing_wikilinks():
    vault_root = Path(__file__).parent / "fixtures" / "sample_vault"

    broken = find_broken_links(vault_root)

    assert broken == [
        {
            "source": "wiki/syntheses/synthesis-a.md",
            "target": "topics/missing-topic",
            "reason": "missing",
        }
    ]


def test_find_broken_links_treats_path_traversal_as_broken(tmp_path):
    vault_root = tmp_path / "vault"
    traversal_note = vault_root / "wiki" / "topics" / "traversal.md"
    traversal_note.parent.mkdir(parents=True, exist_ok=True)
    traversal_note.write_text("# Traversal\n\n[[../../outside]]\n", encoding="utf-8")

    broken = find_broken_links(vault_root)

    assert {
        "source": "wiki/topics/traversal.md",
        "target": "../../outside",
        "reason": "outside-wiki",
    } in broken
