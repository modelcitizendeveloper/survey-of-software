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
            # Simple case: '1-001' -> '1.001' (preserve leading zeros)
            num_part = parts[1]
            pattern = f"1.{num_part}-*"
        else:
            # Sub-number case: '1-104-2' -> '1.104.2' (preserve leading zeros)
            main_num = parts[1]
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
                    # Handle multi-document YAML by loading all and taking first
                    docs = list(yaml.safe_load_all(f))
                    metadata = docs[0] if docs else {}

                    # Handle different metadata formats
                    title = (
                        metadata.get("title") or
                        metadata.get("experiment_info", {}).get("experiment_name") or
                        None
                    )

                    # If no title, try to extract from directory name
                    if not title:
                        dir_name = research_dir.name
                        # Extract readable name from directory (e.g., "1.104.2-code-formatting" -> "Code Formatting")
                        match = re.match(r'[\d.]+-(.*)', dir_name)
                        if match:
                            name_part = match.group(1)
                            # Convert kebab-case to Title Case
                            title = name_part.replace('-', ' ').title()

                    description = (
                        metadata.get("short_description") or
                        metadata.get("description") or
                        metadata.get("notes") or
                        ""
                    )
                    return {"title": title or "Unknown", "description": description}
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

    def find_section_for_entry(self, doc_code: str) -> Tuple[int, int]:
        """Find the section (e.g., 1.030-039) that contains this doc code.
        Returns (start_num, end_num) or raises ValueError if not found."""
        # Extract the main number (e.g., '1-035' -> 35)
        parts = doc_code.split('-')
        if len(parts) >= 2:
            main_num = int(parts[1])
        else:
            raise ValueError(f"Invalid doc code: {doc_code}")

        # Sections are 1.000-009, 1.010-019, 1.020-029, etc.
        # Find which section this belongs to
        section_start = (main_num // 10) * 10
        section_end = section_start + 9

        return (section_start, section_end)

    def insert_entries(self, content: str, missing: List[str]) -> str:
        """Insert missing entries into index content in numerical order."""
        lines = content.split('\n')
        result_lines = []
        i = 0

        while i < len(lines):
            line = lines[i]
            result_lines.append(line)

            # Check if this is a survey entry line
            entry_match = re.search(r'\[.*?\]\(/survey/(1-[\d-]+)\)', line)
            if entry_match:
                current_code = entry_match.group(1)

                # Check if any missing entries should go after this one
                to_insert = []
                for doc_code in missing[:]:  # Iterate over copy
                    if self._should_insert_after(current_code, doc_code, lines, i):
                        to_insert.append(doc_code)
                        missing.remove(doc_code)

                # Insert entries
                for doc_code in sorted(to_insert):
                    entry_line = self.format_entry(doc_code)
                    # Match indentation of current line
                    indent = len(line) - len(line.lstrip())
                    result_lines.append(' ' * indent + entry_line)

            i += 1

        return '\n'.join(result_lines)

    def _should_insert_after(self, current_code: str, new_code: str, lines: List[str], current_idx: int) -> bool:
        """Determine if new_code should be inserted after current_code."""
        # Check if they're in the same section
        try:
            current_section = self.find_section_for_entry(current_code)
            new_section = self.find_section_for_entry(new_code)
            if current_section != new_section:
                return False
        except ValueError:
            return False

        # Compare numerical order
        current_num = self._extract_sort_key(current_code)
        new_num = self._extract_sort_key(new_code)

        if new_num <= current_num:
            return False

        # Check if there's a next entry - don't insert if next entry would come before
        next_entry_code = self._find_next_entry(lines, current_idx)
        if next_entry_code:
            next_num = self._extract_sort_key(next_entry_code)
            if next_num <= new_num:
                return False

        return True

    def _extract_sort_key(self, doc_code: str) -> Tuple[int, ...]:
        """Extract sortable tuple from doc code (e.g., '1-035-1' -> (35, 1))."""
        parts = doc_code.split('-')
        if len(parts) == 2:
            return (int(parts[1]),)
        else:
            return (int(parts[1]), int(parts[2]))

    def _find_next_entry(self, lines: List[str], current_idx: int) -> str:
        """Find the next survey entry after current_idx."""
        for i in range(current_idx + 1, len(lines)):
            match = re.search(r'\[.*?\]\(/survey/(1-[\d-]+)\)', lines[i])
            if match:
                return match.group(1)
        return None

    def update_section_counts(self, content: str) -> str:
        """Update 'Completed: X/Y' counts in section headers."""
        lines = content.split('\n')
        result_lines = []

        i = 0
        while i < len(lines):
            line = lines[i]

            # Check if this is a section header with count
            if line.startswith('## 1.') and '**Completed:' in lines[i+1] if i+1 < len(lines) else False:
                result_lines.append(line)
                i += 1

                # Count completed entries in this section
                completed = 0
                total = 0
                j = i + 1
                while j < len(lines) and not lines[j].startswith('##'):
                    entry_line = lines[j]
                    if re.search(r'- (?:✅ )?\[?\*\*1\.\d+', entry_line):
                        total += 1
                        if '✅' in entry_line:
                            completed += 1
                    j += 1

                # Update count line
                result_lines.append(f"\n**Completed: {completed}/{total}**")
                i += 1
                continue

            result_lines.append(line)
            i += 1

        return '\n'.join(result_lines)

    def update_total_counts(self, content: str) -> str:
        """Update total counts in Research Status section."""
        lines = content.split('\n')

        # Count total completed entries
        completed = 0
        for line in lines:
            if '✅' in line and re.search(r'\[.*?\]\(/survey/1-', line):
                completed += 1

        # Find and update Research Status section
        result_lines = []
        for i, line in enumerate(lines):
            if line.startswith('**Total Defined**'):
                # Keep total defined count as-is (manually maintained)
                result_lines.append(line)
            elif line.startswith('**Completed**'):
                # Extract total defined from previous line
                prev_line = lines[i-1] if i > 0 else ''
                match = re.search(r'(\d+) research slots', prev_line)
                total = int(match.group(1)) if match else 189  # fallback
                remaining = total - completed
                percentage = int((completed / total) * 100) if total > 0 else 0
                result_lines.append(f"**Completed**: {completed} pieces ({percentage}%)")
            elif line.startswith('**Remaining**'):
                # Extract total from previous lines
                total_match = None
                for prev_line in result_lines[-5:]:
                    match = re.search(r'(\d+) research slots', prev_line)
                    if match:
                        total_match = match
                        break
                total = int(total_match.group(1)) if total_match else 189
                remaining = total - completed
                result_lines.append(f"**Remaining**: {remaining} pieces")
            else:
                result_lines.append(line)

        return '\n'.join(result_lines)

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

        # Read current content
        content = self.index_path.read_text()

        # Insert missing entries
        content = self.insert_entries(content, missing.copy())

        # Update section counts
        content = self.update_section_counts(content)

        # Update total counts
        content = self.update_total_counts(content)

        # Write back
        self.index_path.write_text(content)
        print(f"\n✓ Updated {self.index_path} with {len(missing)} new entries")

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

    def insert_sidebar_entries(self, content: str, missing: List[str]) -> str:
        """Insert missing entries into sidebars.ts in numerical order."""
        lines = content.split('\n')
        result_lines = []
        i = 0

        while i < len(lines):
            line = lines[i]
            result_lines.append(line)

            # Check if this is a sidebar entry line
            entry_match = re.search(r'"survey/(1-[\d-]+)"', line)
            if entry_match:
                current_code = entry_match.group(1)

                # Skip index entry
                if current_code == 'index':
                    i += 1
                    continue

                # Check if any missing entries should go after this one
                to_insert = []
                for doc_code in missing[:]:  # Iterate over copy
                    if self._should_insert_sidebar_after(current_code, doc_code, lines, i):
                        to_insert.append(doc_code)
                        missing.remove(doc_code)

                # Insert entries
                for doc_code in sorted(to_insert, key=lambda x: self._extract_sort_key(x)):
                    # Match indentation of current line
                    indent = len(line) - len(line.lstrip())
                    result_lines.append(' ' * indent + f'{{type: "doc", id: "survey/{doc_code}"}},')

            i += 1

        return '\n'.join(result_lines)

    def _should_insert_sidebar_after(self, current_code: str, new_code: str, lines: List[str], current_idx: int) -> bool:
        """Determine if new_code should be inserted after current_code in sidebar."""
        # Compare numerical order
        current_num = self._extract_sort_key(current_code)
        new_num = self._extract_sort_key(new_code)

        if new_num <= current_num:
            return False

        # Check if there's a next entry - don't insert if next entry would come before
        next_entry_code = self._find_next_sidebar_entry(lines, current_idx)
        if next_entry_code:
            next_num = self._extract_sort_key(next_entry_code)
            if next_num <= new_num:
                return False

        return True

    def _find_next_sidebar_entry(self, lines: List[str], current_idx: int) -> str:
        """Find the next sidebar entry after current_idx."""
        for i in range(current_idx + 1, len(lines)):
            match = re.search(r'"survey/(1-[\d-]+)"', lines[i])
            if match:
                code = match.group(1)
                if code != 'index':
                    return code
        return None

    def _extract_sort_key(self, doc_code: str) -> Tuple[int, ...]:
        """Extract sortable tuple from doc code (e.g., '1-035-1' -> (35, 1))."""
        parts = doc_code.split('-')
        if len(parts) == 2:
            return (int(parts[1]),)
        else:
            return (int(parts[1]), int(parts[2]))

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

        # Read current content
        content = self.sidebar_path.read_text()

        # Insert missing entries
        content = self.insert_sidebar_entries(content, missing.copy())

        # Write back
        self.sidebar_path.write_text(content)
        print(f"\n✓ Updated {self.sidebar_path} with {len(missing)} new entries")

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

    # Return 0 for success (standard Unix convention)
    return 0


if __name__ == "__main__":
    sys.exit(main())
