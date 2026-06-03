from pathlib import Path

from obsidian_wiki_health.link_checker import find_broken_links


def test_find_broken_links_accepts_targets_with_markdown_extension(tmp_path: Path):
    vault_root = tmp_path / "vault"
    wiki_root = vault_root / "wiki"
    (wiki_root / "topics").mkdir(parents=True)
    (wiki_root / "index.md").write_text("See [[topics/topic-a.md]]\n", encoding="utf-8")
    (wiki_root / "topics" / "topic-a.md").write_text("# Topic A\n", encoding="utf-8")

    assert find_broken_links(vault_root) == []


def test_find_broken_links_reports_traversal_outside_wiki(tmp_path: Path):
    vault_root = tmp_path / "vault"
    wiki_root = vault_root / "wiki"
    wiki_root.mkdir(parents=True)
    (wiki_root / "index.md").write_text("See [[../private-note]]\n", encoding="utf-8")
    (vault_root / "private-note.md").write_text("# Outside wiki\n", encoding="utf-8")

    assert find_broken_links(vault_root) == [
        {
            "source": "wiki/index.md",
            "target": "../private-note",
            "reason": "outside-wiki",
        }
    ]


def test_find_broken_links_resolves_basename_wikilinks(tmp_path: Path):
    vault_root = tmp_path / "vault"
    wiki_root = vault_root / "wiki"
    (wiki_root / "topics").mkdir(parents=True)
    (wiki_root / "index.md").write_text("See [[Topic A]]\n", encoding="utf-8")
    (wiki_root / "topics" / "Topic A.md").write_text("# Topic A\n", encoding="utf-8")

    assert find_broken_links(vault_root) == []
