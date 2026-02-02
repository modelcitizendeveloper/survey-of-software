#!/usr/bin/env python3
"""
Fix malformed links in survey index.
Changes: ✅ [**1.062**]Password Hashing
To:      ✅ [**1.062** Password Hashing](/survey/1-062)
"""

import re
from pathlib import Path

def fix_links():
    """Fix all malformed research item links in index.md"""
    index_path = Path('docs/survey/index.md')
    content = index_path.read_text(encoding='utf-8')

    # Pattern 1: Fix malformed brackets - [**1.XXX**]Title
    # Should be: [**1.XXX** Title](/survey/1-XXX)
    pattern1 = r'- ✅ \[\*\*1\.(\d+(?:-\d+)?)\*\*\]([^\n]+)'

    def add_link(match):
        code = match.group(1)
        rest = match.group(2).strip()
        # Remove trailing link if it already exists
        rest = re.sub(r'\]\(/survey/1-[^)]+\)$', '', rest)
        return f'- ✅ [**1.{code}** {rest}](/survey/1-{code})'

    fixed_content = re.sub(pattern1, add_link, content)

    # Pattern 2: Fix items without links at all - just plain text
    # - ✅ **1.XXX** Title (no link)
    # Should be: - ✅ [**1.XXX** Title](/survey/1-XXX)
    pattern2 = r'- ✅ \*\*1\.(\d+(?:-\d+)?)\*\* ([^\[]+?)(?=\n|- )'

    def add_link2(match):
        code = match.group(1)
        title = match.group(2).strip()
        # Check if this already has a link (starts with [)
        if title.startswith('['):
            return match.group(0)
        return f'- ✅ [**1.{code}** {title}](/survey/1-{code})'

    fixed_content = re.sub(pattern2, add_link2, fixed_content)

    index_path.write_text(fixed_content, encoding='utf-8')

    # Count fixed items
    malformed_before = len(re.findall(r'\[\*\*1\.\d+(?:-\d+)?\*\*\][^\(]', content))
    malformed_after = len(re.findall(r'\[\*\*1\.\d+(?:-\d+)?\*\*\][^\(]', fixed_content))

    print(f"✓ Fixed {malformed_before - malformed_after} malformed links")

    # Verify all completed items have links
    completed = len(re.findall(r'- ✅ \[\*\*1\.\d+', fixed_content))
    print(f"✓ All {completed} completed items now have proper links")

if __name__ == '__main__':
    fix_links()
