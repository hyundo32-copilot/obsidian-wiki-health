from pathlib import Path

from obsidian_wiki_health.index_parser import parse_index_links


def test_parse_index_links_extracts_wikilinks_from_index():
    index_path = Path(__file__).parent / "fixtures" / "sample_vault" / "wiki" / "index.md"

    links = parse_index_links(index_path)

    assert links == [
        "topics/topic-a",
        "topics/topic-b",
        "syntheses/synthesis-a",
    ]
