#!/usr/bin/env python3
"""
Migration Script: Markdown → SQLite Database

Imports spawn-experiments data from markdown files into SQLite database:
- EXPERIMENT_INDEX.md → experiments + methodology_results tables
- EXPERIMENT_HISTORY.md → findings table
- NEXT_EXPERIMENTS_CHECKLIST.md → planned_experiments table

Usage:
    python migrate_from_markdown.py
    python migrate_from_markdown.py --validate-only  # Dry run
    python migrate_from_markdown.py --verbose        # Show progress
"""

import sqlite3
import re
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional

# Paths (adjust based on execution location)
DB_PATH = Path(__file__).parent.parent / "spawn_experiments.db"
SPAWN_EXPERIMENTS_ROOT = Path(__file__).parent.parent.parent.parent.parent / "spawn-experiments"
EXPERIMENT_INDEX = SPAWN_EXPERIMENTS_ROOT / "docs" / "EXPERIMENT_INDEX.md"
EXPERIMENT_HISTORY = SPAWN_EXPERIMENTS_ROOT / "docs" / "EXPERIMENT_HISTORY.md"
NEXT_EXPERIMENTS = SPAWN_EXPERIMENTS_ROOT / "docs" / "NEXT_EXPERIMENTS_CHECKLIST.md"


class MarkdownMigrator:
    """Migrate spawn-experiments markdown to SQLite database"""

    def __init__(self, db_path: Path, verbose: bool = False):
        self.db_path = db_path
        self.verbose = verbose
        self.conn = None
        self.cursor = None

        # Statistics
        self.stats = {
            'experiments': 0,
            'methodology_results': 0,
            'findings': 0,
            'patterns': 0,
            'planned_experiments': 0,
            'errors': []
        }

    def connect(self):
        """Connect to SQLite database"""
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

        # Enable foreign keys
        self.cursor.execute("PRAGMA foreign_keys = ON")

        if self.verbose:
            print(f"✓ Connected to database: {self.db_path}")

    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.commit()
            self.conn.close()
            if self.verbose:
                print("✓ Database connection closed")

    def parse_experiment_entry(self, text: str) -> Optional[Dict]:
        """
        Parse experiment entry from EXPERIMENT_INDEX.md

        Example:
        ### ⭐ **[1.608 - Story-to-Haiku Converter](...)**
        **Tier 1 LLM Integration** | **4 Runs** | Python + Ollama

        Returns dict with: id, tier, domain, title, status, etc.
        """
        # Extract experiment ID and title
        id_match = re.search(r'\[(\d+\.\d+[A-Z]?)\s*-\s*([^\]]+)\]', text)
        if not id_match:
            return None

        exp_id = id_match.group(1)
        title = id_match.group(2).strip()

        # Extract tier
        tier_match = re.search(r'Tier\s+(\d)', text, re.IGNORECASE)
        tier = int(tier_match.group(1)) if tier_match else 1

        # Extract domain
        domain = "Unknown"
        if "LLM Integration" in text:
            domain = "LLM Integration"
        elif "Database" in text or "ORM" in text or "Migration" in text:
            domain = "Database Integration"
        elif "Simulation" in text or "DES" in text:
            domain = "Simulation & Optimization"
        elif "Library Wrapper" in text:
            domain = "Library Integration"
        elif "Input Validation" in text:
            domain = "Input Validation"

        # Determine domain code
        domain_code = f"{tier}.{exp_id.split('.')[1][0]}XX"

        # Extract completion date (look for dates in format: October 29, 2025)
        date_match = re.search(r'(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{1,2}),?\s+(\d{4})', text)
        completed_date = None
        if date_match:
            month_map = {
                'January': 1, 'February': 2, 'March': 3, 'April': 4,
                'May': 5, 'June': 6, 'July': 7, 'August': 8,
                'September': 9, 'October': 10, 'November': 11, 'December': 12
            }
            month = month_map.get(date_match.group(1))
            day = int(date_match.group(2))
            year = int(date_match.group(3))
            completed_date = f"{year}-{month:02d}-{day:02d}"

        # Determine status
        status = "completed"  # Most entries in EXPERIMENT_INDEX are completed

        return {
            'id': exp_id,
            'tier': tier,
            'domain': domain,
            'domain_code': domain_code,
            'title': title,
            'status': status,
            'completed_date': completed_date,
        }

    def parse_methodology_results(self, text: str, exp_id: str) -> List[Dict]:
        """
        Parse methodology results from experiment text

        Example:
        - **Winner**: Method 2 (Specification-Driven) - 95/100
        - Method 1: 6m 48s
        - Method 2: 12m 20s, 456 LOC, 95/100
        - Method 3: 10m 15s, 320 LOC, 88/100
        - Method 4: 15m 30s, 520 LOC, 90/100
        """
        results = []

        # Extract winner
        winner_match = re.search(r'\*\*Winner\*\*:?\s*Method\s+(\d)', text, re.IGNORECASE)
        winner_method = int(winner_match.group(1)) if winner_match else None

        # Method names
        method_names = {
            1: "Immediate",
            2: "Specification-Driven",
            3: "Pure TDD",
            4: "Adaptive TDD"
        }

        # Look for method results (simple heuristic - improve as needed)
        # Pattern: Method X: Ym Zs, NNN LOC, PP/100
        method_pattern = r'Method\s+(\d).*?(\d+)m\s+(\d+)s.*?(\d+)\s+LOC.*?(\d+)/100'

        for match in re.finditer(method_pattern, text):
            method_num = int(match.group(1))
            time_min = int(match.group(2)) + int(match.group(3)) / 60.0
            loc = int(match.group(4))
            quality = int(match.group(5))

            results.append({
                'experiment_id': exp_id,
                'method_number': method_num,
                'method_name': method_names.get(method_num, f"Method {method_num}"),
                'time_minutes': time_min,
                'lines_of_code': loc,
                'quality_score': quality,
                'is_winner': (method_num == winner_method),
                'rank': 1 if method_num == winner_method else None
            })

        # If no detailed results found, create minimal entries
        if not results and winner_method:
            for method_num in range(1, 5):
                results.append({
                    'experiment_id': exp_id,
                    'method_number': method_num,
                    'method_name': method_names.get(method_num),
                    'is_winner': (method_num == winner_method)
                })

        return results

    def migrate_experiments(self, file_path: Path) -> int:
        """
        Migrate experiments from EXPERIMENT_INDEX.md

        Returns: Number of experiments imported
        """
        if not file_path.exists():
            print(f"✗ File not found: {file_path}")
            return 0

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Split by experiment sections (### headers)
        sections = re.split(r'\n###\s+', content)

        count = 0
        for section in sections:
            if not section.strip():
                continue

            # Parse experiment
            exp_data = self.parse_experiment_entry(section)
            if not exp_data:
                continue

            try:
                # Insert experiment
                self.cursor.execute("""
                    INSERT OR IGNORE INTO experiments
                    (id, tier, domain, domain_code, title, status, completed_date)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    exp_data['id'],
                    exp_data['tier'],
                    exp_data['domain'],
                    exp_data['domain_code'],
                    exp_data['title'],
                    exp_data['status'],
                    exp_data['completed_date']
                ))

                if self.cursor.rowcount > 0:
                    count += 1
                    if self.verbose:
                        print(f"  ✓ Imported: {exp_data['id']} - {exp_data['title']}")

                    # Parse and insert methodology results
                    results = self.parse_methodology_results(section, exp_data['id'])
                    for result in results:
                        self.cursor.execute("""
                            INSERT OR IGNORE INTO methodology_results
                            (experiment_id, method_number, method_name, time_minutes,
                             lines_of_code, quality_score, is_winner, rank)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        """, (
                            result['experiment_id'],
                            result['method_number'],
                            result['method_name'],
                            result.get('time_minutes'),
                            result.get('lines_of_code'),
                            result.get('quality_score'),
                            result.get('is_winner', False),
                            result.get('rank')
                        ))
                        self.stats['methodology_results'] += self.cursor.rowcount

            except Exception as e:
                self.stats['errors'].append(f"Error importing {exp_data.get('id', 'unknown')}: {e}")
                if self.verbose:
                    print(f"  ✗ Error: {e}")

        self.stats['experiments'] = count
        return count

    def migrate_planned_experiments(self, file_path: Path) -> int:
        """
        Migrate planned experiments from NEXT_EXPERIMENTS_CHECKLIST.md

        Returns: Number of planned experiments imported
        """
        if not file_path.exists():
            print(f"✗ File not found: {file_path}")
            return 0

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Simple heuristic: Lines starting with "- [ ]" or "- [x]" are planned experiments
        # Example: - [ ] **1.620 - Cash Flow NPV Calculator** (Simple Financial)

        pattern = r'-\s+\[([ x])\]\s+\*\*(\d+\.\d+)\s*-\s*([^*]+)\*\*'

        count = 0
        for match in re.finditer(pattern, content, re.MULTILINE):
            is_completed = (match.group(1).strip().lower() == 'x')
            exp_id = match.group(2)
            title = match.group(3).strip()

            # Extract priority from section header (requires context parsing - simplified here)
            priority = "MEDIUM"  # Default
            if "HIGH PRIORITY" in content[:content.find(match.group(0))].split('\n')[-10:]:
                priority = "HIGH"

            try:
                self.cursor.execute("""
                    INSERT OR IGNORE INTO planned_experiments
                    (experiment_id, title, priority, is_completed)
                    VALUES (?, ?, ?, ?)
                """, (exp_id, title, priority, is_completed))

                if self.cursor.rowcount > 0:
                    count += 1
                    if self.verbose:
                        status = "completed" if is_completed else "planned"
                        print(f"  ✓ Planned: {exp_id} - {title} ({status})")

            except Exception as e:
                self.stats['errors'].append(f"Error importing planned {exp_id}: {e}")
                if self.verbose:
                    print(f"  ✗ Error: {e}")

        self.stats['planned_experiments'] = count
        return count

    def run(self):
        """Execute full migration"""
        print("=" * 60)
        print("spawn-experiments Markdown → SQLite Migration")
        print("=" * 60)

        self.connect()

        # Migrate completed experiments
        print("\n📊 Migrating completed experiments...")
        exp_count = self.migrate_experiments(EXPERIMENT_INDEX)
        print(f"   Imported {exp_count} experiments")
        print(f"   Imported {self.stats['methodology_results']} methodology results")

        # Migrate planned experiments
        print("\n📋 Migrating planned experiments...")
        planned_count = self.migrate_planned_experiments(NEXT_EXPERIMENTS)
        print(f"   Imported {planned_count} planned experiments")

        # Patterns and findings already in schema.sql (INSERT statements)
        print("\n🔍 Patterns and Findings...")
        self.cursor.execute("SELECT COUNT(*) FROM patterns")
        pattern_count = self.cursor.fetchone()[0]
        print(f"   {pattern_count} patterns (from schema.sql)")

        self.cursor.execute("SELECT COUNT(*) FROM findings")
        finding_count = self.cursor.fetchone()[0]
        print(f"   {finding_count} findings (from schema.sql)")

        # Summary
        print("\n" + "=" * 60)
        print("Migration Summary:")
        print("=" * 60)
        print(f"✓ Experiments:          {self.stats['experiments']}")
        print(f"✓ Methodology Results:  {self.stats['methodology_results']}")
        print(f"✓ Planned Experiments:  {self.stats['planned_experiments']}")
        print(f"✓ Patterns:             {pattern_count}")
        print(f"✓ Findings:             {finding_count}")

        if self.stats['errors']:
            print(f"\n⚠ Errors: {len(self.stats['errors'])}")
            for error in self.stats['errors'][:5]:  # Show first 5
                print(f"  - {error}")
        else:
            print("\n✓ No errors!")

        self.close()
        print("\n✅ Migration complete!")
        print(f"📁 Database: {self.db_path}")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Migrate spawn-experiments markdown to SQLite")
    parser.add_argument('--db', type=Path, default=DB_PATH, help='Database path')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    parser.add_argument('--validate-only', action='store_true', help='Dry run (no database writes)')

    args = parser.parse_args()

    if args.validate_only:
        print("🔍 Validation mode (dry run)")
        # TODO: Implement validation-only mode
        return

    migrator = MarkdownMigrator(args.db, verbose=args.verbose)
    migrator.run()


if __name__ == '__main__':
    main()
