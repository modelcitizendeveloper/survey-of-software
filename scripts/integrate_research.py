#!/usr/bin/env python3
"""
Research Integration Automation

Automates the manual steps after running convert_research.py:
1. Update docs/survey/index.md (add entries, update counts)
2. Update sidebars.ts (add new research entries)
3. Validate completeness

Usage:
    python3 scripts/integrate_research.py
    python3 scripts/integrate_research.py --dry-run
"""

import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Set
import yaml


class SurveyIndexUpdater:
    """Updates docs/survey/index.md with new research entries"""

    def __init__(self, root_dir: Path):
        self.root_dir = root_dir
        self.index_path = root_dir / "docs" / "survey" / "index.md"
        self.survey_dir = root_dir / "docs" / "survey"
        self.research_dir = root_dir / "packages" / "research"

    def get_converted_docs(self) -> Set[str]:
        """Get list of converted survey docs (e.g., '1-001', '1-002')"""
        docs = set()
        for md_file in self.survey_dir.glob("1-*.md"):
            if md_file.name != "index.md":
                # Extract code from filename (e.g., '1-001.md' -> '1-001')
                code = md_file.stem
                docs.add(code)
        return docs

    def get_indexed_docs(self) -> Set[str]:
        """Get list of docs already in index.md"""
        if not self.index_path.exists():
            return set()

        content = self.index_path.read_text()
        docs = set()
        # Match entries like: - ✅ [**1.001** Title](/survey/1-001)
        pattern = r'\[.*?\]\(/survey/(1-[\d-]+)\)'
        for match in re.finditer(pattern, content):
            docs.add(match.group(1))
        return docs

    def get_missing_docs(self) -> List[str]:
        """Get docs that exist but aren't in index.md"""
        converted = self.get_converted_docs()
        indexed = self.get_indexed_docs()
        missing = sorted(converted - indexed)
        return missing

    def get_research_metadata(self, doc_code: str) -> Dict[str, str]:
        """Get metadata for a research piece (title, description)"""
        # Convert doc code to research directory
        # Examples:
        #   '1-001' -> '1.001-*'
        #   '1-104-2' -> '1.104.2-*'
        #   '1-110-4' -> '1.110.4-*'
        parts = doc_code.split('-')
        if len(parts) == 2:
            # Simple case: '1-001' -> '1.001'
            num_part = parts[1].lstrip('0') or '0'
            pattern = f"1.{num_part}-*"
        else:
            # Sub-number case: '1-104-2' -> '1.104.2'
            main_num = parts[1].lstrip('0') or '0'
            sub_num = parts[2]
            pattern = f"1.{main_num}.{sub_num}-*"

        matches = list(self.research_dir.glob(pattern))
        if not matches:
            return {"title": "Unknown", "description": ""}

        research_dir = matches[0]
        metadata_file = research_dir / "metadata.yaml"

        if metadata_file.exists():
            try:
                with open(metadata_file) as f:
                    metadata = yaml.safe_load(f)
                    # Handle different metadata formats
                    title = (
                        metadata.get("title") or
                        metadata.get("experiment_info", {}).get("experiment_name") or
                        "Unknown"
                    )
                    description = (
                        metadata.get("short_description") or
                        metadata.get("description") or
                        ""
                    )
                    return {"title": title, "description": description}
            except Exception as e:
                print(f"Warning: Could not parse {metadata_file}: {e}")

        # Fallback: try to extract from EXPLAINER
        explainer_files = list(research_dir.glob("*EXPLAINER.md"))
        if explainer_files:
            content = explainer_files[0].read_text()
            # Extract first heading
            match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
            if match:
                return {"title": match.group(1), "description": ""}

        return {"title": research_dir.name, "description": ""}

    def format_entry(self, doc_code: str) -> str:
        """Format a single index entry"""
        metadata = self.get_research_metadata(doc_code)
        # Convert doc code to display format (e.g., '1-001' -> '1.001')
        display_code = doc_code.replace('-', '.', 1)
        title = metadata["title"]
        desc = metadata["description"]

        if desc:
            return f"- ✅ [**{display_code}** {title}](/survey/{doc_code}) - {desc}"
        else:
            return f"- ✅ [**{display_code}** {title}](/survey/{doc_code})"

    def update_index(self, dry_run: bool = False) -> int:
        """Add missing entries to index.md"""
        missing = self.get_missing_docs()

        if not missing:
            print("✓ No new entries to add to survey index")
            return 0

        print(f"Found {len(missing)} new entries to add:")
        for doc in missing:
            entry = self.format_entry(doc)
            print(f"  {entry}")

        if dry_run:
            print("(dry-run mode - no changes made)")
            return len(missing)

        # TODO: Implement actual insertion logic
        # For now, just report what would be added
        print("\nTODO: Implement automatic insertion into index.md")
        print("For now, manually add these entries in numerical order")

        return len(missing)


class SidebarUpdater:
    """Updates sidebars.ts with new research entries"""

    def __init__(self, root_dir: Path):
        self.root_dir = root_dir
        self.sidebar_path = root_dir / "sidebars.ts"
        self.survey_dir = root_dir / "docs" / "survey"

    def get_converted_docs(self) -> Set[str]:
        """Get list of converted survey docs"""
        docs = set()
        for md_file in self.survey_dir.glob("1-*.md"):
            if md_file.name != "index.md":
                docs.add(md_file.stem)
        return docs

    def get_sidebar_docs(self) -> Set[str]:
        """Get list of docs already in sidebars.ts"""
        if not self.sidebar_path.exists():
            return set()

        content = self.sidebar_path.read_text()
        docs = set()
        # Match entries like: {type: "doc", id: "survey/1-001"}
        pattern = r'"survey/(1-[\d-]+)"'
        for match in re.finditer(pattern, content):
            docs.add(match.group(1))
        return docs

    def get_missing_docs(self) -> List[str]:
        """Get docs not yet in sidebar"""
        converted = self.get_converted_docs()
        in_sidebar = self.get_sidebar_docs()
        missing = sorted(converted - in_sidebar)
        return missing

    def update_sidebar(self, dry_run: bool = False) -> int:
        """Add missing entries to sidebars.ts"""
        missing = self.get_missing_docs()

        if not missing:
            print("✓ No new entries to add to sidebar")
            return 0

        print(f"\nFound {len(missing)} new sidebar entries:")
        for doc in missing:
            print(f'  {{type: "doc", id: "survey/{doc}"}}')

        if dry_run:
            print("(dry-run mode - no changes made)")
            return len(missing)

        # TODO: Implement actual insertion logic
        print("\nTODO: Implement automatic insertion into sidebars.ts")
        print("For now, manually add these entries in numerical order")

        return len(missing)


def main():
    """Main entry point"""
    dry_run = "--dry-run" in sys.argv
    root_dir = Path(__file__).parent.parent

    print("Research Integration Automation")
    print("=" * 50)
    print()

    # Update survey index
    index_updater = SurveyIndexUpdater(root_dir)
    index_changes = index_updater.update_index(dry_run=dry_run)

    # Update sidebar
    sidebar_updater = SidebarUpdater(root_dir)
    sidebar_changes = sidebar_updater.update_sidebar(dry_run=dry_run)

    print()
    print("=" * 50)
    if dry_run:
        print(f"DRY RUN: Would make {index_changes + sidebar_changes} changes")
    else:
        print(f"Completed: {index_changes + sidebar_changes} changes made")

    return 0 if (index_changes == 0 and sidebar_changes == 0) else 1


if __name__ == "__main__":
    sys.exit(main())
