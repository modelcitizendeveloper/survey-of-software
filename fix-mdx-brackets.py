#!/usr/bin/env python3
"""
Fix unescaped angle brackets in MDX files that cause compilation errors.
Escapes <, >, and <-> when they appear with numbers or in specific contexts.
"""

import re
from pathlib import Path

def fix_mdx_brackets(content):
    """Fix angle brackets that MDX interprets as HTML tags."""

    # Pattern 1: <-> bidirectional arrow
    content = re.sub(r'<->', r'&lt;-&gt;', content)

    # Pattern 2: <digit (less than with number)
    content = re.sub(r'<(\d)', r'&lt;\1', content)

    # Pattern 3: >digit (greater than with number)
    content = re.sub(r'>(\d)', r'&gt;\1', content)

    # Pattern 4: Backtick-wrapped comparisons like `<50`
    content = re.sub(r'`<(\d)', r'`&lt;\1', content)
    content = re.sub(r'`>(\d)', r'`&gt;\1', content)

    return content

def main():
    docs_dir = Path('docs/survey')

    fixed_count = 0
    for md_file in docs_dir.glob('*.md'):
        content = md_file.read_text(encoding='utf-8')
        original = content

        fixed_content = fix_mdx_brackets(content)

        if fixed_content != original:
            md_file.write_text(fixed_content, encoding='utf-8')
            fixed_count += 1
            print(f"✓ Fixed {md_file.name}")

    print(f"\n✓ Fixed {fixed_count} files")

if __name__ == '__main__':
    main()
