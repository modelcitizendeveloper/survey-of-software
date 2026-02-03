#!/usr/bin/env python3
"""
Convert research markdown files to Docusaurus format with tabs.
"""

import os
import yaml
from pathlib import Path
from typing import Dict, List, Optional, NamedTuple
import re


class ResearchContent(NamedTuple):
    """Container for discovered research content across all patterns."""
    s1: Optional[str]
    s2: Optional[str]
    s3: Optional[str]
    s4: Optional[str]
    explainer: Optional[str]
    pattern: str  # For debugging: which structure pattern was detected


def load_metadata(research_dir: Path) -> Optional[Dict]:
    """Load metadata.yaml from a research directory."""
    metadata_file = research_dir / "metadata.yaml"
    if not metadata_file.exists():
        return None

    try:
        with open(metadata_file, 'r') as f:
            # Handle multiple documents - just take the first one
            documents = list(yaml.safe_load_all(f))
            if documents:
                return documents[0]
            return None
    except yaml.YAMLError as e:
        print(f"Warning: Could not parse {metadata_file.name}: {str(e)[:100]}")
        return None


def is_hardware_store_content(research_dir: Path, metadata: Optional[Dict]) -> bool:
    """
    Validate that content is 'hardware store for software' - general-purpose
    tools and libraries, NOT application-specific implementations.

    Excludes:
    - Application-specific integrations (e.g., platform-specific apps)
    - Domain-specific business logic implementations
    - Vertical-specific solutions (e.g., language learning apps)

    Includes:
    - General-purpose libraries (sorting, JSON, ML frameworks)
    - Infrastructure tools (databases, messaging, caching)
    - Development tools (testing, logging, monitoring)
    """
    # Check metadata for application-specific markers
    if metadata:
        title = metadata.get('title', '').lower()
        description = metadata.get('description', '').lower()

        # Exclude application-specific patterns
        app_specific_markers = [
            'language learning',
            'flashcard',
            'spaced repetition',
            'duolingo',
            'anki',
            'educational app',
            'learning platform',
        ]

        for marker in app_specific_markers:
            if marker in title or marker in description:
                return False

    # Check directory name for known exclusions
    dir_name = research_dir.name.lower()
    if any(pattern in dir_name for pattern in [
        'flashcard',
        'anki',
        'language-learning',
        'spaced-repetition',
    ]):
        return False

    # Default: assume it's hardware store content
    return True


def extract_explainer_from_s4(s4_content: str) -> Optional[str]:
    """
    Extract EXPLAINER section from S4 synthesis if embedded.

    Looks for markers like:
    - # EXPLAINER: What is Sorting...
    - ## EXPLAINER

    Extracts from marker to next same-level heading or end.
    """
    if not s4_content:
        return None

    # Try different heading patterns
    patterns = [
        r'^(#{1,2}\s+EXPLAINER:.*?)(?=^#{1,2}\s+(?!#)|$)',  # With colon
        r'^(#{1,2}\s+EXPLAINER\b.*?)(?=^#{1,2}\s+(?!#)|$)',  # Without colon
    ]

    for pattern in patterns:
        match = re.search(pattern, s4_content, re.MULTILINE | re.DOTALL | re.IGNORECASE)
        if match:
            return match.group(1).strip()

    return None


def find_root_explainer_file(research_dir: Path) -> Optional[str]:
    """
    Search for standalone explainer files at root level.

    Tries naming patterns:
    - *EXPLAINER*.md (any with EXPLAINER in name)
    - {TOPIC}_EXPLAINER.md
    """
    # Try glob pattern (most flexible)
    explainer_files = list(research_dir.glob("*EXPLAINER*.md"))

    if explainer_files:
        # If multiple, prefer ones with EXPLAINER at start or end
        for file in sorted(explainer_files, key=lambda f: (
            not f.name.startswith("EXPLAINER"),
            not f.name.endswith("EXPLAINER.md"),
            f.name
        )):
            try:
                with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                    return f.read()
            except Exception:
                continue

    return None


def find_explainer_content(research_dir: Path, s4_content: Optional[str]) -> Optional[str]:
    """
    Find explainer content using multiple strategies.

    Tries:
    1. Standalone root file: {TOPIC}_EXPLAINER.md
    2. Embedded in S4 synthesis: Extract EXPLAINER section
    3. Standalone in discovery: 01-discovery/EXPLAINER.md
    4. S4 directory: S4-strategic/*EXPLAINER*.md
    """
    strategies = [
        # Strategy 1: Root-level standalone (most common in Pattern B)
        lambda: find_root_explainer_file(research_dir),

        # Strategy 2: Extract from S4 synthesis (common in Pattern A)
        lambda: extract_explainer_from_s4(s4_content) if s4_content else None,

        # Strategy 3: Discovery folder
        lambda: (research_dir / "01-discovery" / "EXPLAINER.md").read_text(encoding='utf-8', errors='ignore')
            if (research_dir / "01-discovery" / "EXPLAINER.md").exists() else None,

        # Strategy 4: S4 directory with EXPLAINER files
        lambda: find_s4_directory_explainer(research_dir),
    ]

    for strategy in strategies:
        try:
            content = strategy()
            if content:
                return content
        except Exception:
            continue

    return None


def find_s4_directory_explainer(research_dir: Path) -> Optional[str]:
    """Find EXPLAINER files in S4-strategic directory."""
    # Try both nested and top-level S4 directories
    s4_dirs = [
        research_dir / "01-discovery" / "S4-strategic",
        research_dir / "S4-strategic"
    ]

    for s4_dir in s4_dirs:
        if s4_dir.exists():
            # Look for files with EXPLAINER in the name
            for file in s4_dir.glob("*EXPLAINER*.md"):
                try:
                    with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                        return f.read()
                except Exception:
                    continue

    return None


def escape_mdx_content(content: str) -> str:
    """Escape problematic patterns for MDX."""
    import re

    # Step 0: Unescape backslash-escaped backticks (\`\`\` -> ```)
    # This handles cases where source markdown has escaped code blocks
    content = content.replace(r'\`', '`')

    # Step 1: Protect existing code (inline and blocks) from modification
    # Store protected content and replace with placeholders
    protected = []

    def protect(match):
        protected.append(match.group(0))
        return f"___PROTECTED_{len(protected)-1}___"

    # Protect code blocks (```...```)
    content = re.sub(r'```[\s\S]*?```', protect, content)

    # Protect inline code (`...`)
    content = re.sub(r'`[^`]+`', protect, content)

    # Step 2: Remove HTML tags that MDX will handle via markdown
    content = re.sub(r'</?(?:br|hr|em|strong|b|i|u|s|sub|sup|mark)/?>', '', content, flags=re.IGNORECASE)

    # Step 3: Escape problematic patterns

    # Shift operators (<<, >>)
    content = re.sub(r'(<<|>>)', r'`\1`', content)

    # Curly braces (but not in URLs or already protected)
    content = re.sub(r'\{([^}]+)\}', r'`{\1}`', content)

    # Less-than with dollar amounts: <$100, <$50K, <$100/month
    content = re.sub(r'<\$(\d+[KMB]?(?:/\w+)?)', r'`<$\1`', content)

    # Greater-than with dollar amounts: >$100
    content = re.sub(r'>\$(\d+[KMB]?(?:/\w+)?)', r'`>$\1`', content)

    # Comparison operators with numbers: <1, >100, <=4.0.0, >=2.1.0
    # Match multi-part version numbers (1.2.3.4...) and size units (MB, GB, KB)
    content = re.sub(r'([<>]=?)(\d+(?:\.\d+)*(?:MB|GB|KB)?)', r'`\1\2`', content)

    # Standalone comparison operators: <=, >=, ==, != (not followed by digits)
    # Match when they appear standalone (e.g., in lists or descriptions)
    content = re.sub(r'(?<!\w)([<>!=]=)(?!\d)', r'`\1`', content)

    # Less-than followed by word characters (like <Analysis:)
    # But be careful not to match markdown links or other valid uses
    content = re.sub(r'<([A-Z][a-z]*:)', r'`<\1`', content)

    # Generic type parameters (like IAsyncEnumerable<StreamingTextContent>, Task<AIResponse>)
    # Match word characters on both sides of angle brackets
    content = re.sub(r'(\w+<[\w\.]+>)', r'`\1`', content)

    # HTML tag names in text (like <button>, <div>, <span>)
    # Match lowercase tag names that look like HTML tags
    content = re.sub(r'<([a-z]+)>', r'`<\1>`', content)

    # Catch any remaining standalone < or > at end of line or before whitespace
    # Only match if not part of backtick-wrapped content
    content = re.sub(r'(?<!`)\s+([<>])\s*$', r' `\1`', content, flags=re.MULTILINE)

    # Step 4: Restore protected content
    for i, text in enumerate(protected):
        content = content.replace(f"___PROTECTED_{i}___", text)

    return content


def remove_embedded_explainer(s4_content: str, found_explainer: Optional[str]) -> str:
    """
    Remove explainer section from S4 if it was extracted.

    Only removes if we successfully extracted explainer to avoid duplication.
    """
    if not found_explainer or not s4_content:
        return s4_content

    # Check if the explainer was actually embedded in s4_content
    # (vs found as standalone file)
    if found_explainer.strip() not in s4_content:
        # Explainer came from elsewhere, don't modify S4
        return s4_content

    # Remove explainer section using same patterns as extract
    cleaned = re.sub(
        r'^#{1,2}\s+EXPLAINER.*?(?=^#{1,2}\s+(?!#)|$)',
        '',
        s4_content,
        flags=re.MULTILINE | re.DOTALL | re.IGNORECASE
    )

    return cleaned.strip()


def read_nested_stage(stage_dir: Path) -> Optional[str]:
    """Read content from a nested stage directory (Pattern A)."""
    if not stage_dir.exists():
        return None

    content_parts = []

    # Read synthesis file first if it exists
    synthesis_file = stage_dir / "00-SYNTHESIS.md"
    if synthesis_file.exists():
        try:
            with open(synthesis_file, 'r', encoding='utf-8', errors='ignore') as f:
                content_parts.append(f.read())
        except Exception as e:
            print(f"Warning: Could not read {synthesis_file.name}: {str(e)[:100]}")

    # Read all other markdown files
    for md_file in sorted(stage_dir.glob("*.md")):
        if md_file.name == "00-SYNTHESIS.md":
            continue
        try:
            with open(md_file, 'r', encoding='utf-8', errors='ignore') as f:
                content_parts.append(f.read())
        except Exception as e:
            print(f"Warning: Could not read {md_file.name}: {str(e)[:100]}")

    return "\n\n---\n\n".join(content_parts) if content_parts else None


def read_single_file(file_path: Path) -> Optional[str]:
    """Read content from a single file if it exists."""
    if not file_path.exists():
        return None
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except Exception:
        return None


def find_stage_directory(base_dir: Path, stage: str) -> Optional[Path]:
    """Find a stage directory using glob pattern to match variants."""
    # Look for directories that start with S1-, S2-, etc.
    pattern = f"{stage}-*"
    matching_dirs = list(base_dir.glob(pattern))

    # Return first match (should only be one per stage)
    return matching_dirs[0] if matching_dirs else None


def find_stage_content(research_dir: Path, stage: str) -> Optional[str]:
    """
    Find stage content using multiple strategies across all patterns.

    Tries:
    1. Nested directory: 01-discovery/S{N}-*/  (glob pattern)
    2. Top-level nested: S{N}-*/  (glob pattern)
    3. Flat file in discovery: 01-discovery/S{N}_{NAME}_DISCOVERY.md
    4. Legacy file variants
    """
    # Map stage names for file variants
    stage_names = {
        "S1": ("rapid", ["S1_RAPID_DISCOVERY.md"]),
        "S2": ("comprehensive", ["S2_COMPREHENSIVE_DISCOVERY.md"]),
        "S3": ("need-driven", ["S3_NEED_DRIVEN_DISCOVERY.md", "S3_METHODOLOGY_SUMMARY.md"]),
        "S4": ("strategic", ["S4_STRATEGIC_SELECTION.md", "S4_STRATEGIC_DISCOVERY.md"]),
    }

    stage_name, file_variants = stage_names.get(stage, (stage.lower(), []))

    strategies = [
        # Strategy 1: Glob for nested directory in 01-discovery (Pattern A + variants)
        lambda: (stage_dir := find_stage_directory(research_dir / "01-discovery", stage)) and read_nested_stage(stage_dir),

        # Strategy 2: Glob for top-level nested directory (Pattern A variant)
        lambda: (stage_dir := find_stage_directory(research_dir, stage)) and read_nested_stage(stage_dir),

        # Strategy 3: Flat file in discovery (Pattern B)
        lambda: next((read_single_file(research_dir / "01-discovery" / f)
                     for f in file_variants
                     if (research_dir / "01-discovery" / f).exists()), None),

        # Strategy 4: Top-level flat file (Pattern B variant)
        lambda: next((read_single_file(research_dir / f)
                     for f in file_variants
                     if (research_dir / f).exists()), None),
    ]

    for strategy in strategies:
        try:
            content = strategy()
            if content:
                return content
        except Exception:
            continue

    return None


def detect_pattern(research_dir: Path) -> str:
    """
    Detect which structural pattern this research follows.
    Returns pattern name for logging/debugging.
    """
    has_nested_s1 = (research_dir / "01-discovery" / "S1-rapid").exists()
    has_flat_s1 = (research_dir / "01-discovery" / "S1_RAPID_DISCOVERY.md").exists()
    has_root_explainer = len(list(research_dir.glob("*EXPLAINER*.md"))) > 0

    if has_nested_s1:
        return "pattern-a-nested"  # Nested directories
    elif has_flat_s1:
        return "pattern-b-flat"  # Flat files
    elif has_root_explainer:
        return "pattern-e-explainer-only"  # Explainer only
    else:
        return "pattern-unknown"


def discover_research_content(research_dir: Path) -> ResearchContent:
    """
    Discover and classify research content across all patterns.

    Returns structured content with:
    - S1-S4 stage content (None if missing)
    - Explainer content (None if missing, separated from S4 if embedded)
    - Pattern metadata for debugging
    """
    pattern = detect_pattern(research_dir)

    # Discover all stages
    s1 = find_stage_content(research_dir, "S1")
    s2 = find_stage_content(research_dir, "S2")
    s3 = find_stage_content(research_dir, "S3")
    s4_raw = find_stage_content(research_dir, "S4")

    # Extract explainer (tries multiple strategies including embedded in S4)
    explainer = find_explainer_content(research_dir, s4_raw)

    # Remove explainer from S4 if it was embedded
    s4_clean = remove_embedded_explainer(s4_raw, explainer) if s4_raw else None

    return ResearchContent(
        s1=s1,
        s2=s2,
        s3=s3,
        s4=s4_clean,
        explainer=explainer,
        pattern=pattern
    )


def generate_docusaurus_doc(research_dir: Path, output_dir: Path) -> bool:
    """Generate a Docusaurus document for a research piece."""
    metadata = load_metadata(research_dir)

    # Validate this is hardware store content (not application-specific)
    if not is_hardware_store_content(research_dir, metadata):
        print(f"⊘ Skipping {research_dir.name}: application-specific content (not hardware store)")
        return False

    # Extract code from directory name (e.g., "1.142-flashcard-systems" -> "1.142")
    match = re.match(r'(\d+\.\d+(?:\.\d+)?)-(.+)', research_dir.name)
    if not match:
        print(f"Skipping {research_dir.name}: invalid directory name format")
        return False

    code = match.group(1)
    dir_title = match.group(2).replace('-', ' ').title()

    # Get title and description from metadata if available, otherwise use directory name
    if metadata:
        title = metadata.get('title', dir_title)
        description = metadata.get('description', '').strip()
    else:
        title = dir_title
        description = ''

    # Discover all content using multi-strategy discovery
    content = discover_research_content(research_dir)

    # Track which stages have content
    has_s1 = content.s1 is not None
    has_s2 = content.s2 is not None
    has_s3 = content.s3 is not None
    has_s4 = content.s4 is not None
    has_explainer = content.explainer is not None

    # Debug for 1.131
    if "1.131" in code:
        print(f"DEBUG 1.131: has_s1={has_s1}, has_s2={has_s2}, has_s3={has_s3}, has_s4={has_s4}")

    # Generate frontmatter - properly escape description
    desc = description[:160] if description else f"Research on {title}"
    # Replace quotes and newlines
    desc = desc.replace('"', '\\"').replace('\n', ' ')

    # Build tabs only for stages that have content
    s1_tab = f"""<TabItem value="s1" label="S1: Rapid Discovery" default>

{escape_mdx_content(content.s1).rstrip()}

</TabItem>""" if has_s1 else ""

    s2_tab = f"""<TabItem value="s2" label="S2: Comprehensive">

{escape_mdx_content(content.s2).rstrip()}

</TabItem>""" if has_s2 else ""

    s3_tab = f"""<TabItem value="s3" label="S3: Need-Driven">

{escape_mdx_content(content.s3).rstrip()}

</TabItem>""" if has_s3 else ""

    s4_tab = f"""<TabItem value="s4" label="S4: Strategic">

{escape_mdx_content(content.s4).rstrip()}

</TabItem>""" if has_s4 else ""

    explainer_tab = f"""<TabItem value="explainer" label="Explainer">

{escape_mdx_content(content.explainer).rstrip()}

</TabItem>""" if has_explainer else ""

    frontmatter = f"""---
id: {code.replace('.', '-')}
title: "{code} {title}"
sidebar_label: "{code} {title}"
description: "{desc}"
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# {code} {title}

{description}

---

<Tabs>
{s1_tab}{s2_tab}{s3_tab}{s4_tab}{explainer_tab}
</Tabs>
"""

    # Write to output directory
    output_file = output_dir / f"{code.replace('.', '-')}.md"
    with open(output_file, 'w') as f:
        f.write(frontmatter)

    print(f"✓ Generated {output_file.name}")
    return True


def get_cluster_for_code(code: str) -> str:
    """Determine which cluster a research piece belongs to based on its code."""
    # Parse the numeric part - handle three-level codes like 1.033.1
    try:
        # Convert "1.033.1" to 1.0331 for comparison
        parts = code.split('.')
        if len(parts) == 3:
            code_num = float(f"{parts[0]}.{parts[1]}{parts[2]}")
        else:
            code_num = float(code)
    except ValueError:
        return "other"

    if 1.200 <= code_num < 1.210:
        return "llm-ai-stack"
    elif 1.110 <= code_num < 1.120:
        return "frontend"
    elif 1.140 <= code_num < 1.160:
        return "language-learning"
    elif 1.130 <= code_num < 1.140:
        return "self-hosted"
    elif 1.100 <= code_num < 1.110:
        return "document-processing"
    elif 1.010 <= code_num < 1.020:
        return "graph-algorithms"
    elif 1.030 <= code_num < 1.040:
        return "text-processing"
    elif 1.050 <= code_num < 1.070:
        return "data-serialization"
    elif 1.060 <= code_num < 1.070:
        return "security-crypto"
    elif 1.070 <= code_num < 1.080:
        return "ml-deep-learning"
    elif 3.000 <= code_num < 3.100:
        return "saas-infrastructure"
    elif 3.080 <= code_num < 3.090:
        return "event-management"
    elif 3.090 <= code_num < 3.200:
        return "productivity"
    elif 3.300 <= code_num < 3.500:
        return "platform-integration"
    else:
        return "other"


def main():
    """Main conversion function."""
    # Script is now in crew/ivan/scripts/
    # Paths relative to crew/ivan (parent of scripts/)
    script_dir = Path(__file__).resolve().parent
    repo_root = script_dir.parent

    research_dir = repo_root / "packages" / "research"
    output_dir = repo_root / "docs" / "survey"
    completed_yaml = repo_root / "COMPLETED-RESEARCH.yaml"

    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)

    # Find all research directories (simplified - no COMPLETED-RESEARCH.yaml required)
    research_pieces = []
    for item in sorted(research_dir.iterdir()):
        if not item.is_dir():
            continue

        # Extract code from directory name (e.g., "1.001-sorting-libraries" -> "1.001")
        match = re.match(r'(\d+\.\d+(?:\.\d+)?)', item.name)
        if not match:
            continue

        # Verify it has either metadata.yaml or S1-S4 content
        has_metadata = (item / "metadata.yaml").exists()
        has_discovery = (item / "01-discovery").exists() or any((item / f"S{i}-{s}").exists()
            for i, s in [(1, "rapid"), (2, "comprehensive"), (3, "need-driven"), (4, "strategic")])

        if has_metadata or has_discovery:
            research_pieces.append(item)

    print(f"Matched {len(research_pieces)} directories to completed codes")

    # Convert each piece
    converted = 0
    for piece in research_pieces:
        if generate_docusaurus_doc(piece, output_dir):
            converted += 1

    print(f"\n✓ Converted {converted}/{len(research_pieces)} research pieces")


if __name__ == "__main__":
    main()
