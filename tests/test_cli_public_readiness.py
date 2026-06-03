import sys
from pathlib import Path

import pytest

from obsidian_wiki_health import find_broken_links, suggest_related_notes
from obsidian_wiki_health.cli import main


def test_package_exports_public_api():
    assert callable(find_broken_links)
    assert callable(suggest_related_notes)


def test_cli_reports_clear_error_for_missing_vault(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["obsidian-wiki-health", "scan", "/path/that/does/not/exist"])

    with pytest.raises(SystemExit) as exc:
        main()

    assert exc.value.code == 2
    captured = capsys.readouterr()
    assert "vault path does not exist" in captured.err


def test_cli_suggest_alias_prints_related_notes(tmp_path: Path, monkeypatch, capsys):
    vault_root = tmp_path / "vault"
    wiki_root = vault_root / "wiki"
    wiki_root.mkdir(parents=True)
    (wiki_root / "index.md").write_text("# Index\n", encoding="utf-8")
    (wiki_root / "alpha.md").write_text("LLM wiki maintenance\n", encoding="utf-8")

    monkeypatch.setattr(sys, "argv", ["obsidian-wiki-health", "suggest", str(vault_root), "LLM"])

    assert main() == 0
    captured = capsys.readouterr()
    assert "wiki/alpha.md" in captured.out
