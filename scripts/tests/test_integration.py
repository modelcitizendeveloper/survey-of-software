"""
Tests for research integration automation.

Using TDD approach - tests first, then implementation.
"""

import pytest
from pathlib import Path
import sys

# Add parent directory to path so we can import the script
sys.path.insert(0, str(Path(__file__).parent.parent))
from integrate_research import SurveyIndexUpdater, SidebarUpdater


class TestSurveyIndexUpdater:
    """Test automatic updates to docs/survey/index.md"""

    def test_extract_existing_entries(self, tmp_path):
        """Should extract list of existing research entries from index"""
        # Create test directory structure
        docs_dir = tmp_path / "docs" / "survey"
        docs_dir.mkdir(parents=True)

        # Create index.md with entries
        index_content = """# Survey Catalog

- ✅ [**1.001** Sorting Libraries](/survey/1-001)
- ✅ [**1.003** Full-Text Search](/survey/1-003)
- ✅ [**1.035.1** Chinese Tokenization](/survey/1-035-1)
"""
        (docs_dir / "index.md").write_text(index_content)

        # Test extraction
        updater = SurveyIndexUpdater(tmp_path)
        indexed = updater.get_indexed_docs()

        assert indexed == {'1-001', '1-003', '1-035-1'}

    def test_find_missing_entries(self, tmp_path):
        """Should identify converted docs not yet in index"""
        # Create test directory structure
        docs_dir = tmp_path / "docs" / "survey"
        docs_dir.mkdir(parents=True)
        packages_dir = tmp_path / "packages" / "research"
        packages_dir.mkdir(parents=True)

        # Create converted docs
        (docs_dir / "1-001.md").write_text("# Doc 1")
        (docs_dir / "1-002.md").write_text("# Doc 2")
        (docs_dir / "1-003.md").write_text("# Doc 3")

        # Create index with only 1-001 and 1-003
        index_content = """# Survey Catalog
- ✅ [**1.001** Title](/survey/1-001)
- ✅ [**1.003** Title](/survey/1-003)
"""
        (docs_dir / "index.md").write_text(index_content)

        # Test missing detection
        updater = SurveyIndexUpdater(tmp_path)
        missing = updater.get_missing_docs()

        assert missing == ['1-002']

    def test_count_completed_per_section(self, tmp_path):
        """Should count completed research per section (e.g., 1.030-039)"""
        # Create test directory structure
        docs_dir = tmp_path / "docs" / "survey"
        docs_dir.mkdir(parents=True)

        # Create index with section
        index_content = """# Survey Catalog

## 1.030-039: String & Text Algorithms
**Completed: 5/10**

- ✅ [**1.030** Title](/survey/1-030)
- ✅ [**1.031** Title](/survey/1-031)
- ✅ [**1.033** Title](/survey/1-033)
"""
        (docs_dir / "index.md").write_text(index_content)

        updater = SurveyIndexUpdater(tmp_path)
        # This will require a new method - count_entries_in_section()
        # For now, just verify we can parse the content
        indexed = updater.get_indexed_docs()
        assert len(indexed) == 3

    def test_update_section_counts(self, tmp_path):
        """Should update 'Completed: X/Y' in section headers"""
        # Create test directory structure
        docs_dir = tmp_path / "docs" / "survey"
        docs_dir.mkdir(parents=True)

        # Create index with outdated count
        index_content = """# Survey Catalog

## 1.030-039: String & Text Algorithms
**Completed: 5/10**

- ✅ [**1.030** Title](/survey/1-030)
- ✅ [**1.031** Title](/survey/1-031)
- ✅ [**1.032** Title](/survey/1-032)
- ✅ [**1.033** Title](/survey/1-033)
- ✅ [**1.034** Title](/survey/1-034)
- ✅ [**1.035** Title](/survey/1-035)
- ✅ [**1.036** Title](/survey/1-036)
"""
        (docs_dir / "index.md").write_text(index_content)

        # This will require a new method - update_section_count()
        # The actual count is 7, not 5
        # Test will verify the update logic when implemented
        updater = SurveyIndexUpdater(tmp_path)
        indexed = updater.get_indexed_docs()
        assert len(indexed) == 7  # Actual count

    def test_add_new_entry_in_order(self, tmp_path):
        """Should insert new entries in numerical order"""
        # Create test directory structure
        docs_dir = tmp_path / "docs" / "survey"
        docs_dir.mkdir(parents=True)

        # Create index with gap
        index_content = """# Survey Catalog

## 1.001-009: Sorting & Search
**Completed: 2/9**

- ✅ [**1.001** Title One](/survey/1-001)
- ✅ [**1.003** Title Three](/survey/1-003)

## Total
**Completed**: 2 pieces
"""
        (docs_dir / "index.md").write_text(index_content)

        # This will require a new method - insert_entry()
        # Should insert 1.002 between 1.001 and 1.003
        # Test will verify insertion logic when implemented
        updater = SurveyIndexUpdater(tmp_path)
        indexed = updater.get_indexed_docs()
        assert '1-001' in indexed
        assert '1-003' in indexed


class TestSidebarUpdater:
    """Test automatic updates to sidebars.ts"""

    def test_extract_existing_sidebar_entries(self, tmp_path):
        """Should extract survey entries from sidebars.ts"""
        # Create sidebars.ts
        sidebar_content = """{
  survey: [
    {type: "doc", id: "survey/index"},
    {type: "doc", id: "survey/1-001"},
    {type: "doc", id: "survey/1-003"},
    {type: "doc", id: "survey/1-035-1"},
  ]
}"""
        (tmp_path / "sidebars.ts").write_text(sidebar_content)
        (tmp_path / "docs" / "survey").mkdir(parents=True)

        updater = SidebarUpdater(tmp_path)
        entries = updater.get_sidebar_docs()

        assert entries == {'1-001', '1-003', '1-035-1'}
        assert 'index' not in entries  # Should exclude index

    def test_find_missing_sidebar_entries(self, tmp_path):
        """Should identify docs not in sidebar"""
        # Create docs
        docs_dir = tmp_path / "docs" / "survey"
        docs_dir.mkdir(parents=True)
        (docs_dir / "1-001.md").write_text("# Doc 1")
        (docs_dir / "1-002.md").write_text("# Doc 2")
        (docs_dir / "1-003.md").write_text("# Doc 3")

        # Create sidebar with only 1-001 and 1-003
        sidebar_content = """{
  survey: [
    {type: "doc", id: "survey/index"},
    {type: "doc", id: "survey/1-001"},
    {type: "doc", id: "survey/1-003"},
  ]
}"""
        (tmp_path / "sidebars.ts").write_text(sidebar_content)

        updater = SidebarUpdater(tmp_path)
        missing = updater.get_missing_docs()

        assert missing == ['1-002']

    def test_add_sidebar_entry_in_order(self, tmp_path):
        """Should insert sidebar entries in numerical order"""
        # Create sidebar with gap
        sidebar_content = """{
  survey: [
    {type: "doc", id: "survey/index"},
    {type: "doc", id: "survey/1-001"},
    {type: "doc", id: "survey/1-003"},
  ]
}"""
        (tmp_path / "sidebars.ts").write_text(sidebar_content)
        (tmp_path / "docs" / "survey").mkdir(parents=True)

        # This will require a new method - insert_sidebar_entry()
        # Should insert 1-002 between 1-001 and 1-003
        updater = SidebarUpdater(tmp_path)
        entries = updater.get_sidebar_docs()
        assert '1-001' in entries
        assert '1-003' in entries


class TestMetadataExtractor:
    """Test extraction of metadata from research pieces"""

    def test_parse_metadata_yaml(self, tmp_path):
        """Should parse metadata.yaml from research directory"""
        # Create research directory structure (matches actual format with leading zeros)
        research_dir = tmp_path / "packages" / "research" / "1.001-sorting-libraries"
        research_dir.mkdir(parents=True)

        # Create metadata.yaml
        metadata_content = """title: Sorting Libraries
short_description: Timsort, NumPy, radix sort
domain: algorithms
"""
        (research_dir / "metadata.yaml").write_text(metadata_content)

        # Create minimal docs structure
        docs_dir = tmp_path / "docs" / "survey"
        docs_dir.mkdir(parents=True)
        (tmp_path / "docs" / "survey" / "index.md").write_text("# Survey")

        updater = SurveyIndexUpdater(tmp_path)
        metadata = updater.get_research_metadata('1-001')

        assert metadata['title'] == 'Sorting Libraries'
        assert metadata['description'] == 'Timsort, NumPy, radix sort'

    def test_extract_title_from_explainer(self, tmp_path):
        """Should extract title from EXPLAINER.md if metadata missing"""
        # Create research directory without metadata.yaml (matches actual format)
        research_dir = tmp_path / "packages" / "research" / "1.002-search-algorithms"
        research_dir.mkdir(parents=True)

        # Create EXPLAINER.md (try common patterns)
        explainer_content = """# Full-Text Search Libraries

This document explains search algorithms.
"""
        (research_dir / "DOMAIN_EXPLAINER.md").write_text(explainer_content)

        # Create minimal docs structure
        docs_dir = tmp_path / "docs" / "survey"
        docs_dir.mkdir(parents=True)
        (tmp_path / "docs" / "survey" / "index.md").write_text("# Survey")

        updater = SurveyIndexUpdater(tmp_path)
        metadata = updater.get_research_metadata('1-002')

        assert metadata['title'] == 'Full-Text Search Libraries'

    def test_parse_multi_document_yaml(self, tmp_path):
        """Should handle multi-document YAML files gracefully"""
        # Create research directory with multi-doc YAML (matches actual format)
        research_dir = tmp_path / "packages" / "research" / "1.104.2-code-formatting-tools"
        research_dir.mkdir(parents=True)

        # Create multi-document YAML (like the problematic one)
        metadata_content = """title: Code Formatting
short_description: Black, Prettier, gofmt
---
# Second document (should be ignored)
other_data: value
"""
        (research_dir / "metadata.yaml").write_text(metadata_content)

        # Create minimal docs structure
        docs_dir = tmp_path / "docs" / "survey"
        docs_dir.mkdir(parents=True)
        (tmp_path / "docs" / "survey" / "index.md").write_text("# Survey")

        updater = SurveyIndexUpdater(tmp_path)
        metadata = updater.get_research_metadata('1-104-2')

        # Should successfully extract from first document only
        assert metadata['title'] == 'Code Formatting'
        assert metadata['description'] == 'Black, Prettier, gofmt'


@pytest.fixture
def sample_index_content():
    """Sample docs/survey/index.md content for testing"""
    return """# Survey Catalog

## 1.001-009: Sorting & Search
**Completed: 5/9**

- ✅ [**1.001** Sorting Libraries](/survey/1-001) - Timsort, NumPy, radix sort
- ✅ [**1.003** Full-Text Search](/survey/1-003) - Elasticsearch, Whoosh, Tantivy

## Total
**Total Defined**: 189 research slots
**Completed**: 98 pieces (52%)
**Remaining**: 91 pieces
"""


@pytest.fixture
def sample_sidebars_content():
    """Sample sidebars.ts content for testing"""
    return """{
  survey: [
    {type: "doc", id: "survey/index"},
    {type: "doc", id: "survey/1-001"},
    {type: "doc", id: "survey/1-003"},
  ]
}"""
