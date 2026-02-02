#!/usr/bin/env python3
"""
Update docs/survey/index.md to reflect all completed research.
Adds ✅ markers and updates counts automatically.
"""

import re
from pathlib import Path
from collections import defaultdict

def get_completed_research():
    """Get set of completed research codes from docs/survey/"""
    docs_dir = Path('docs/survey')
    completed = set()

    for md_file in docs_dir.glob('1-*.md'):
        # Extract code: 1-001.md -> 001, 1-033-1.md -> 033-1
        code = md_file.stem.replace('1-', '')
        completed.add(code)

    return completed

def update_index(completed_set):
    """Update the index.md file with completion markers and counts"""
    index_path = Path('docs/survey/index.md')
    content = index_path.read_text(encoding='utf-8')

    lines = content.split('\n')
    updated_lines = []
    section_counts = defaultdict(lambda: {'total': 0, 'completed': 0})
    current_section = None

    for line in lines:
        # Track current section
        section_match = re.match(r'^## (1\.\d+-\d+):', line)
        if section_match:
            current_section = section_match.group(1)

        # Check if line is a research item
        item_match = re.match(r'^- (✅ )?\[?\*?\*?1\.(\d+(?:-\d+)?)\*?\*?', line)
        if item_match:
            code = item_match.group(2)

            if current_section:
                section_counts[current_section]['total'] += 1

            # Check if completed
            if code in completed_set:
                # Add ✅ if not already there
                if not line.startswith('- ✅'):
                    line = line.replace('- **', '- ✅ [**', 1).replace('** ', '**]', 1)
                    if '](/survey/' not in line:
                        # Add link if missing
                        line = re.sub(
                            r'- ✅ \*\*1\.(' + code + r')\*\* ([^-]+)',
                            r'- ✅ [**1.\1** \2](/survey/1-' + code + r')',
                            line
                        )

                if current_section:
                    section_counts[current_section]['completed'] += 1
            else:
                # Remove ✅ if present but file doesn't exist
                if line.startswith('- ✅'):
                    line = line.replace('- ✅ [**', '- **', 1).replace('**]', '** ', 1)
                    # Remove link
                    line = re.sub(r'\]\(/survey/1-[^)]+\)', '', line)

        # Update section count lines
        count_match = re.match(r'^\*\*Completed: \d+/\d+\*\*', line)
        if count_match and current_section:
            counts = section_counts[current_section]
            line = f"**Completed: {counts['completed']}/{counts['total']}**"

        updated_lines.append(line)

    # Update total counts at bottom
    total_completed = len(completed_set)
    total_remaining = 189 - total_completed
    total_pct = int((total_completed / 189) * 100)

    updated_content = '\n'.join(updated_lines)
    updated_content = re.sub(
        r'\*\*Completed\*\*: \d+ pieces \(\d+%\)',
        f'**Completed**: {total_completed} pieces ({total_pct}%)',
        updated_content
    )
    updated_content = re.sub(
        r'\*\*Remaining\*\*: \d+ pieces',
        f'**Remaining**: {total_remaining} pieces',
        updated_content
    )

    index_path.write_text(updated_content, encoding='utf-8')
    print(f"✓ Updated index.md: {total_completed} completed ({total_pct}%)")

    # Show section breakdown
    print("\nSection breakdown:")
    for section in sorted(section_counts.keys()):
        counts = section_counts[section]
        print(f"  {section}: {counts['completed']}/{counts['total']}")

def main():
    completed = get_completed_research()
    print(f"Found {len(completed)} completed research docs")
    update_index(completed)

if __name__ == '__main__':
    main()
