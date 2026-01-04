"""Tests to verify rules documentation files exist."""

from pathlib import Path


def get_project_root() -> Path:
    """Get the project root directory."""
    # tests/ is at project root, so go up one level
    return Path(__file__).parent.parent


class TestRulesFilesExist:
    """Tests for rules documentation files."""

    def test_comprehensive_rules_exists(self) -> None:
        """Verify the Comprehensive Rules txt file exists."""
        docs_dir = get_project_root() / "docs"
        txt_files = list(docs_dir.glob("*CompRules*.txt"))
        assert len(txt_files) >= 1, "No Comprehensive Rules .txt file found in docs/"
        assert txt_files[0].stat().st_size > 0, "Comprehensive Rules file is empty"

    def test_rules_index_exists(self) -> None:
        """Verify rules_index.md exists and is non-empty."""
        index_path = get_project_root() / "docs" / "rules_index.md"
        assert index_path.exists(), f"rules_index.md not found at {index_path}"
        assert index_path.stat().st_size > 0, "rules_index.md is empty"

    def test_rules_coverage_exists(self) -> None:
        """Verify rules_coverage.yml exists and is non-empty."""
        coverage_path = get_project_root() / "docs" / "rules_coverage.yml"
        assert coverage_path.exists(), f"rules_coverage.yml not found at {coverage_path}"
        assert coverage_path.stat().st_size > 0, "rules_coverage.yml is empty"

    def test_rules_index_has_content(self) -> None:
        """Verify rules_index.md contains expected content."""
        index_path = get_project_root() / "docs" / "rules_index.md"
        content = index_path.read_text(encoding="utf-8")

        # Should have main sections
        assert "Game Concepts" in content
        assert "Turn Structure" in content
        assert "Stack" in content or "405" in content

    def test_rules_coverage_has_entries(self) -> None:
        """Verify rules_coverage.yml contains entries."""
        coverage_path = get_project_root() / "docs" / "rules_coverage.yml"
        content = coverage_path.read_text(encoding="utf-8")

        # Should have YAML structure with key entries
        assert "id:" in content
        assert "status:" in content
        assert "todo" in content or "partial" in content or "done" in content

    def test_extract_script_exists(self) -> None:
        """Verify the extraction script exists."""
        script_path = get_project_root() / "tools" / "extract_rules_outline.py"
        assert script_path.exists(), f"extract_rules_outline.py not found at {script_path}"
        assert script_path.stat().st_size > 0, "extract_rules_outline.py is empty"
