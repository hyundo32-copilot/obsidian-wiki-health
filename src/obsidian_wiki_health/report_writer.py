from __future__ import annotations


def _render_list(items: list[str], empty_message: str) -> list[str]:
    if not items:
        return [f"- {empty_message}"]
    return [f"- {item}" for item in items]


def build_markdown_report(
    *,
    broken_links: list[dict[str, str]],
    orphan_candidates: list[str],
    related_notes: list[str],
) -> str:
    lines = [
        "# Obsidian Wiki Health Report",
        "",
        "## Broken Links",
    ]
    if broken_links:
        lines.extend(f"- {item['source']} -> {item['target']}" for item in broken_links)
    else:
        lines.append("- none")

    lines.extend([
        "",
        "## Orphan Candidates",
        *_render_list(orphan_candidates, "none"),
        "",
        "## Research-Deep Related Notes",
        *_render_list(related_notes, "none"),
        "",
    ])
    return "\n".join(lines)
