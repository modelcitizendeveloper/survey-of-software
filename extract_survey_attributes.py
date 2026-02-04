#!/usr/bin/env python3
"""
Extract library attributes from survey S1 sections.
Task: research-v6vi
"""

import re
import json
from pathlib import Path
from collections import defaultdict

# Pattern-based extraction
PATTERNS = {
    'performance': {
        'fast': r'\b(faster|fastest|speed|speedup|performance|efficient|optimized)\b',
        'slow': r'\b(slower|slow performance|overhead)\b',
        'scalable': r'\b(scale|scalable|scales to)\b',
        'memory_efficient': r'\b(memory efficient|low memory|memory footprint)\b',
        'multiplier': r'\b(\d+x)\s*(faster|speedup|performance)'
    },
    'maturity': {
        'stable': r'\b(stable|production-ready|mature|battle-tested)\b',
        'beta': r'\b(beta|experimental|alpha|preview)\b',
        'maintained': r'\b(active maintenance|actively maintained|well-maintained|active development)\b',
        'abandoned': r'\b(no longer maintained|abandoned|deprecated)\b',
        'growing': r'\b(rapidly growing|growing ecosystem)\b'
    },
    'learning': {
        'easy': r'\b(beginner-friendly|easy|simple|straightforward|drop-in replacement)\b',
        'complex': r'\b(steep learning curve|complex|advanced|difficult)\b',
        'compatible': r'\b(compatibility|compatible|migration path)\b'
    }
}

def extract_attributes(survey_file: Path) -> dict:
    """Extract attributes from a survey S1 section."""
    content = survey_file.read_text()

    # Find S1 section - handle multiple formats
    # Match any header containing "S1" followed by content until next section marker
    s1_match = re.search(
        r'#[^\n]*\bS1\b[^\n]*\n.*?(?=<\/TabItem>|# S[234]|<TabItem|$)',
        content,
        re.DOTALL | re.IGNORECASE
    )
    if not s1_match:
        return {}

    s1_text = s1_match.group(0)

    # Extract library names from "### N. LibraryName" patterns
    raw_libraries = re.findall(r'###\s+\d+\.\s+(.+?)(?:\s+⭐|\n|$)', s1_text)

    # Fallback: Try numbered bold pattern "1. **LibraryName**" if no ### pattern found
    if not raw_libraries:
        raw_libraries = re.findall(r'^\s*\d+\.\s+\*\*([^\*]+)\*\*', s1_text, re.MULTILINE)

    # Clean library names
    libraries = []

    for lib in raw_libraries:
        # Remove markdown bold
        lib = re.sub(r'\*\*', '', lib)
        # Remove content in parentheses
        lib = re.sub(r'\([^)]*\)', '', lib)
        # Remove special markers like ⭐
        lib = re.sub(r'[⭐🏆]', '', lib)

        # Split on common delimiters (-, /, :) and take first part
        lib = re.split(r'[\-/:–]', lib)[0].strip()

        # Take first 1-3 words before descriptive text
        # Stop at words like "for", "with", "library", etc.
        stop_pattern = r'\b(for|with|use|when|library|framework|bindings?|based)\b'
        match = re.search(stop_pattern, lib, re.IGNORECASE)
        if match:
            lib = lib[:match.start()].strip()

        # Take only first 1-3 capitalized words
        words = []
        for word in lib.split():
            # Keep word if it's capitalized or all caps (like API, AWS)
            if word and (word[0].isupper() or word.isupper()):
                words.append(word)
                if len(words) >= 3:
                    break

        lib = ' '.join(words)

        # Skip if too short or empty
        if lib and len(lib) > 1:
            libraries.append(lib)

    attributes = {}
    for lib in libraries[:5]:  # Top 5 libraries
        lib_attrs = {'performance': [], 'maturity': [], 'learning': []}

        # Find section for this library (case-insensitive)
        # Match from "### N. LibraryName" to next "###" or end
        lib_section = re.search(
            rf'###.*?{re.escape(lib)}.*?(?=###|## Quick Decision|## Key \d{{4}}|$)',
            s1_text,
            re.DOTALL | re.IGNORECASE
        )

        if lib_section:
            lib_text = lib_section.group(0)

            # Apply patterns
            for category, patterns in PATTERNS.items():
                for attr_name, pattern in patterns.items():
                    if re.search(pattern, lib_text, re.IGNORECASE):
                        lib_attrs[category].append(attr_name)

        # Only include if we found at least one attribute
        if any(lib_attrs.values()):
            attributes[lib] = lib_attrs

    return attributes

# Main extraction loop
survey_dir = Path.home() / 'gt/research/crew/ivan/docs/survey'
results = {}
processed_count = 0
attribute_count = 0

print("Starting survey attribute extraction...")
print(f"Survey directory: {survey_dir}")

for survey_file in sorted(survey_dir.glob('1-*.md')):
    survey_id = survey_file.stem

    try:
        attrs = extract_attributes(survey_file)

        if attrs:
            results[survey_id] = attrs
            lib_count = len(attrs)
            attribute_count += sum(
                len(cat_attrs)
                for lib_attrs in attrs.values()
                for cat_attrs in lib_attrs.values()
            )
            print(f"✓ {survey_id:<10} - {lib_count} libraries with attributes")
        else:
            print(f"✗ {survey_id:<10} - No S1 section or attributes found")

        processed_count += 1

    except Exception as e:
        print(f"✗ {survey_id:<10} - Error: {e}")

# Save results
output_file = Path('data/library_attributes.json')
with open(output_file, 'w') as f:
    json.dump(results, f, indent=2)

# Summary statistics
survey_count = len(results)
total_libraries = sum(len(attrs) for attrs in results.values())

print("\n" + "="*60)
print("EXTRACTION COMPLETE")
print("="*60)
print(f"Processed files:      {processed_count}")
print(f"Surveys with attrs:   {survey_count}")
print(f"Total libraries:      {total_libraries}")
print(f"Total attributes:     {attribute_count}")
print(f"Output file:          {output_file}")
print("="*60)

# Validation
if survey_count < 50:
    print(f"\n⚠️  WARNING: Only {survey_count} surveys with attributes (target: 50+)")
else:
    print(f"\n✅ SUCCESS: {survey_count} surveys with attributes (target: 50+)")

# Show sample
print("\nSample output (first survey):")
if results:
    first_survey = next(iter(results.items()))
    print(f"\n{first_survey[0]}:")
    print(json.dumps(first_survey[1], indent=2))
