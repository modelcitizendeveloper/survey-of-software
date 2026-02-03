#!/usr/bin/env python3
"""
Research Quality Validation

Validates that research pieces follow the 4PS methodology:
- S1: Rapid Discovery
- S2: Comprehensive Analysis
- S3: Need-Driven Discovery
- S4: Strategic Selection

Usage:
    python3 scripts/validate_research.py 1.007-pattern-matching
    python3 scripts/validate_research.py --all
"""

import sys
from pathlib import Path
from typing import Dict, List, Tuple
import re


class ResearchValidator:
    """Validates research follows 4PS methodology"""

    def __init__(self, root_dir: Path):
        self.root_dir = root_dir
        self.research_dir = root_dir / "packages" / "research"

    def validate_structure(self, research_code: str) -> Dict[str, any]:
        """Validate directory structure and required files"""
        results = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "score": 0,
            "max_score": 100
        }

        # Find research directory
        pattern = f"{research_code}-*"
        matches = list(self.research_dir.glob(pattern))

        if not matches:
            results["valid"] = False
            results["errors"].append(f"Research directory not found: {pattern}")
            return results

        research_path = matches[0]
        discovery_path = research_path / "01-discovery"

        # Check DOMAIN_EXPLAINER exists
        explainer_files = list(research_path.glob("*EXPLAINER*.md"))
        if explainer_files:
            results["score"] += 10
        else:
            results["errors"].append("Missing DOMAIN_EXPLAINER.md")
            results["valid"] = False

        # Check discovery directory
        if not discovery_path.exists():
            results["errors"].append("Missing 01-discovery/ directory")
            results["valid"] = False
            return results

        # Validate each phase
        phases = ["S1", "S2", "S3", "S4"]
        for phase in phases:
            phase_score = self._validate_phase(discovery_path, phase, results)
            results["score"] += phase_score

        # Check for DISCOVERY_TOC or synthesis
        toc_files = list(discovery_path.glob("*TOC*.md")) + \
                   list(discovery_path.glob("*SYNTHESIS*.md"))
        if toc_files:
            results["score"] += 10
        else:
            results["warnings"].append("Missing DISCOVERY_TOC.md or SYNTHESIS.md")

        return results

    def _validate_phase(
        self,
        discovery_path: Path,
        phase: str,
        results: Dict
    ) -> int:
        """Validate a single phase (S1-S4). Returns score (0-20)"""
        score = 0

        # Look for phase directory or files
        phase_patterns = [
            discovery_path / f"{phase}-rapid",
            discovery_path / f"{phase}-comprehensive",
            discovery_path / f"{phase}-need-driven",
            discovery_path / f"{phase}-strategic",
            discovery_path / phase.lower()
        ]

        phase_dir = None
        for pattern in phase_patterns:
            if pattern.exists():
                phase_dir = pattern
                break

        # Also check for phase files directly in discovery/
        phase_files = list(discovery_path.glob(f"{phase}_*.md"))

        if not phase_dir and not phase_files:
            results["errors"].append(f"Missing {phase} phase (no directory or files)")
            return 0

        # Phase exists - base score
        score += 5

        # Check for required files
        required = {
            "approach": f"{phase} should have approach.md or {phase}_*APPROACH*.md",
            "libraries": f"{phase} should have library files",
            "recommendation": f"{phase} should have recommendation.md"
        }

        if phase_dir:
            # Directory structure
            if (phase_dir / "approach.md").exists():
                score += 5
            elif list(phase_dir.glob("*approach*.md")):
                score += 3
                results["warnings"].append(f"{phase}: approach.md has non-standard name")
            else:
                results["warnings"].append(required["approach"])

            # Check for library files (should have multiple)
            lib_files = [
                f for f in phase_dir.glob("*.md")
                if "approach" not in f.name.lower()
                and "recommendation" not in f.name.lower()
            ]
            if len(lib_files) >= 2:
                score += 5
            elif len(lib_files) == 1:
                score += 2
                results["warnings"].append(f"{phase}: Only 1 library file (expect 3-5)")
            else:
                results["warnings"].append(required["libraries"])

            # Check for recommendation
            if (phase_dir / "recommendation.md").exists():
                score += 5
            elif list(phase_dir.glob("*recommendation*.md")):
                score += 3
                results["warnings"].append(f"{phase}: recommendation.md has non-standard name")
            else:
                results["warnings"].append(required["recommendation"])

        else:
            # File-based structure (S1_RAPID_DISCOVERY.md format)
            score += 10  # Give credit for having the file
            # Check file size as proxy for content
            for f in phase_files:
                if f.stat().st_size > 500:  # At least 500 bytes
                    score += 5
                    break

        return min(score, 20)  # Cap at 20 per phase

    def validate_content_quality(
        self,
        research_code: str
    ) -> Dict[str, any]:
        """Validate content quality (not just structure)"""
        results = {
            "valid": True,
            "issues": [],
            "score": 0,
            "max_score": 50
        }

        pattern = f"{research_code}-*"
        matches = list(self.research_dir.glob(pattern))

        if not matches:
            results["valid"] = False
            return results

        research_path = matches[0]

        # Check metadata.yaml exists and has required fields
        metadata_path = research_path / "metadata.yaml"
        if metadata_path.exists():
            results["score"] += 10
            content = metadata_path.read_text()

            # Check for key fields
            required_fields = ["title", "domain"]
            for field in required_fields:
                if f"{field}:" in content:
                    results["score"] += 5
                else:
                    results["issues"].append(f"metadata.yaml missing '{field}' field")
        else:
            results["issues"].append("Missing metadata.yaml")

        # Check EXPLAINER has substantial content
        explainer_files = list(research_path.glob("*EXPLAINER*.md"))
        if explainer_files:
            explainer = explainer_files[0]
            size = explainer.stat().st_size

            if size > 5000:  # At least 5KB
                results["score"] += 15
            elif size > 2000:
                results["score"] += 10
                results["issues"].append("EXPLAINER is short (< 5KB)")
            elif size > 500:
                results["score"] += 5
                results["issues"].append("EXPLAINER is very short (< 2KB)")
            else:
                results["issues"].append("EXPLAINER is too short (< 500 bytes)")

        # Check for code examples
        all_files = list(research_path.rglob("*.md"))
        has_code_blocks = False
        for f in all_files:
            content = f.read_text()
            if "```" in content:
                has_code_blocks = True
                break

        if has_code_blocks:
            results["score"] += 10
        else:
            results["issues"].append("No code examples found")

        return results

    def generate_report(
        self,
        research_code: str
    ) -> str:
        """Generate validation report"""
        structure = self.validate_structure(research_code)
        content = self.validate_content_quality(research_code)

        total_score = structure["score"] + content["score"]
        max_score = structure["max_score"] + content["max_score"]
        percentage = int((total_score / max_score) * 100) if max_score > 0 else 0

        report = []
        report.append(f"Research Validation Report: {research_code}")
        report.append("=" * 60)
        report.append("")

        # Overall status
        if percentage >= 90:
            status = "✅ EXCELLENT"
        elif percentage >= 75:
            status = "✓ GOOD"
        elif percentage >= 60:
            status = "⚠ ACCEPTABLE"
        else:
            status = "❌ NEEDS WORK"

        report.append(f"Overall Score: {total_score}/{max_score} ({percentage}%) - {status}")
        report.append("")

        # Structure validation
        report.append("Structure Validation:")
        report.append(f"  Score: {structure['score']}/{structure['max_score']}")

        if structure["errors"]:
            report.append("  ❌ Errors:")
            for error in structure["errors"]:
                report.append(f"    - {error}")

        if structure["warnings"]:
            report.append("  ⚠ Warnings:")
            for warning in structure["warnings"]:
                report.append(f"    - {warning}")

        report.append("")

        # Content validation
        report.append("Content Quality:")
        report.append(f"  Score: {content['score']}/{content['max_score']}")

        if content["issues"]:
            report.append("  Issues:")
            for issue in content["issues"]:
                report.append(f"    - {issue}")

        report.append("")

        # Recommendations
        if percentage < 75:
            report.append("Recommendations:")
            if structure["score"] < 70:
                report.append("  - Ensure all S1-S4 phases have proper structure")
                report.append("  - Each phase should have: approach, libraries, recommendation")
            if content["score"] < 30:
                report.append("  - Add more detailed content to EXPLAINER")
                report.append("  - Include code examples")
                report.append("  - Ensure metadata.yaml has all required fields")

        return "\n".join(report)


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/validate_research.py <research-code>")
        print("       python3 scripts/validate_research.py --all")
        sys.exit(1)

    root_dir = Path(__file__).parent.parent
    validator = ResearchValidator(root_dir)

    if sys.argv[1] == "--all":
        # Validate all research pieces
        research_dir = root_dir / "packages" / "research"
        all_research = sorted([
            d.name.split('-')[0]
            for d in research_dir.iterdir()
            if d.is_dir() and d.name[0].isdigit()
        ])

        print(f"Validating {len(all_research)} research pieces...")
        print()

        scores = []
        for code in all_research:
            result = validator.validate_structure(code)
            content = validator.validate_content_quality(code)
            total = result["score"] + content["score"]
            max_score = result["max_score"] + content["max_score"]
            pct = int((total / max_score) * 100) if max_score > 0 else 0
            scores.append((code, pct, total, max_score))

            status = "✅" if pct >= 75 else "⚠" if pct >= 60 else "❌"
            print(f"{status} {code}: {pct}% ({total}/{max_score})")

        print()
        avg_score = sum(s[1] for s in scores) / len(scores) if scores else 0
        print(f"Average Score: {avg_score:.1f}%")

    else:
        # Validate single research piece
        research_code = sys.argv[1]
        report = validator.generate_report(research_code)
        print(report)


if __name__ == "__main__":
    main()
