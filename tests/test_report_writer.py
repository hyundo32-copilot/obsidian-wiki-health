from obsidian_wiki_health.report_writer import build_markdown_report


def test_build_markdown_report_renders_scan_results():
    report = build_markdown_report(
        broken_links=[{"source": "wiki/a.md", "target": "missing"}],
        orphan_candidates=["wiki/orphan.md"],
        related_notes=["wiki/topic.md"],
    )

    assert "# Obsidian Wiki Health Report" in report
    assert "- wiki/a.md -> missing" in report
    assert "- wiki/orphan.md" in report
    assert "- wiki/topic.md" in report
