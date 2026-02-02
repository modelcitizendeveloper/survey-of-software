#!/usr/bin/env python3
"""
Update sidebars.ts to include all completed research in numerical order.
"""

import re
from pathlib import Path

def get_completed_research():
    """Get sorted list of completed research codes from docs/survey/"""
    docs_dir = Path('docs/survey')
    completed = []

    for md_file in sorted(docs_dir.glob('1-*.md')):
        # Extract code: 1-001.md -> 1-001
        code = md_file.stem
        completed.append(code)

    return completed

def update_sidebar(completed_list):
    """Update sidebars.ts with all completed research"""
    sidebar_path = Path('sidebars.ts')
    content = sidebar_path.read_text(encoding='utf-8')

    # Find the survey section
    # Look for the survey items array
    survey_section_start = content.find('items: [')
    if survey_section_start == -1:
        print("ERROR: Could not find survey items array")
        return

    # Find the end of the survey array (look for the closing bracket)
    # We need to find where the survey items end
    # Strategy: find all existing survey entries, then rebuild that section

    # Extract current sidebar entries
    current_entries = set(re.findall(r'"survey/1-[^"]*"', content))
    print(f"Current sidebar has {len(current_entries)} entries")

    # Build new entries
    new_entries = [f'{{type: "doc", id: "survey/{code}"}},' for code in completed_list]

    # Find the survey section and replace it
    # Look for the pattern between survey intro and the next section
    pattern = r'(\{type: "doc", id: "survey-intro"\},\s*)(.*?)(\s*\{type: "category")'

    def replacement(match):
        intro = match.group(1)
        closing = match.group(3)
        # Insert all survey items
        items_str = '\n        '.join(new_entries)
        return f"{intro}\n        {items_str}{closing}"

    updated_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    if updated_content != content:
        sidebar_path.write_text(updated_content, encoding='utf-8')
        print(f"✓ Updated sidebars.ts with {len(completed_list)} research docs")

        # Show newly added
        new_ids = set(f'"survey/{code}"' for code in completed_list)
        added = new_ids - current_entries
        if added:
            print(f"\nAdded {len(added)} new entries:")
            for entry in sorted(added)[:10]:
                print(f"  {entry}")
            if len(added) > 10:
                print(f"  ... and {len(added) - 10} more")
    else:
        print("No changes needed")

def main():
    completed = get_completed_research()
    print(f"Found {len(completed)} completed research docs")
    update_sidebar(completed)

if __name__ == '__main__':
    main()
