from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .common import validate_vault_root
from .link_checker import find_broken_links
from .orphan_detector import find_orphan_candidates
from .report_writer import build_markdown_report
from .research_deep import suggest_related_notes


def _scan(vault_root: Path, query: str | None = None) -> str:
    related_notes = suggest_related_notes(vault_root, query) if query else []
    return build_markdown_report(
        broken_links=find_broken_links(vault_root),
        orphan_candidates=find_orphan_candidates(vault_root),
        related_notes=related_notes,
        query=query,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="obsidian-wiki-health")
    subparsers = parser.add_subparsers(dest="command", required=True)

    scan_parser = subparsers.add_parser("scan")
    scan_parser.add_argument("vault_root")
    scan_parser.add_argument("--query", default=None)

    report_parser = subparsers.add_parser("report")
    report_parser.add_argument("vault_root")
    report_parser.add_argument("--output", required=True)
    report_parser.add_argument("--query", default=None)

    query_parser = subparsers.add_parser("research-deep")
    query_parser.add_argument("vault_root")
    query_parser.add_argument("query")

    suggest_parser = subparsers.add_parser("suggest")
    suggest_parser.add_argument("vault_root")
    suggest_parser.add_argument("query")

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    vault_root = Path(args.vault_root)

    try:
        validate_vault_root(vault_root)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(2) from exc

    if args.command == "scan":
        print(_scan(vault_root, args.query))
        return 0

    if args.command == "report":
        report = _scan(vault_root, args.query)
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(report, encoding="utf-8")
        print(output_path)
        return 0

    if args.command in {"research-deep", "suggest"}:
        for note in suggest_related_notes(vault_root, args.query):
            print(note)
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
