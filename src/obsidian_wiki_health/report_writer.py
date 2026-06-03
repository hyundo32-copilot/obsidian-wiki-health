from __future__ import annotations


def _render_list(items: list[str], empty_message: str) -> list[str]:
    if not items:
        return [f"- {empty_message}"]
    return [f"- {item}" for item in items]


def _render_broken_links_table(broken_links: list[dict[str, str]]) -> list[str]:
    if not broken_links:
        return ["- none"]

    lines = [
        "| Source | Target | Reason |",
        "| --- | --- | --- |",
    ]
    for item in broken_links:
        lines.append(f"| {item['source']} | {item['target']} | {item.get('reason', 'missing')} |")
    return lines


def build_markdown_report(
    *,
    broken_links: list[dict[str, str]],
    orphan_candidates: list[str],
    related_notes: list[str],
    query: str | None = None,
) -> str:
    lines = [
        "# Obsidian Wiki Health Report",
        "",
        "## Summary",
        f"- Broken links: {len(broken_links)}",
        f"- Orphan candidates: {len(orphan_candidates)}",
        f"- Related notes: {len(related_notes)}",
    ]
    if query:
        lines.append(f"- Query: `{query}`")

    lines.extend([
        "",
        "## Broken Links",
        *_render_broken_links_table(broken_links),
        "",
        "## Orphan Candidates",
        *_render_list(orphan_candidates, "none"),
        "",
        "## Suggested Reading Before Query",
        *_render_list(related_notes, "none"),
        "",
    ])
    return "\n".join(lines)
