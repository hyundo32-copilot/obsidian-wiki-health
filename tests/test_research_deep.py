from pathlib import Path

from obsidian_wiki_health.research_deep import suggest_related_notes


def test_suggest_related_notes_returns_ranked_matching_notes():
    vault_root = Path(__file__).parent / "fixtures" / "sample_vault"

    matches = suggest_related_notes(vault_root, "topic synthesis")

    assert matches == [
        "wiki/syntheses/synthesis-a.md",
        "wiki/topics/topic-a.md",
        "wiki/topics/topic-b.md",
    ]
