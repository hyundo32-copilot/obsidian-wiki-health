from obsidian_wiki_health.report_writer import build_markdown_report


def test_build_markdown_report_includes_summary_query_and_reasons():
    report = build_markdown_report(
        broken_links=[{"source": "wiki/a.md", "target": "missing", "reason": "missing"}],
        orphan_candidates=["wiki/orphan.md"],
        related_notes=["wiki/topic.md"],
        query="LLM Wiki maintenance",
    )

    assert "## Summary" in report
    assert "- Broken links: 1" in report
    assert "Query: `LLM Wiki maintenance`" in report
    assert "| wiki/a.md | missing | missing |" in report
