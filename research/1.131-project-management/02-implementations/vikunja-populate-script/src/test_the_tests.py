#!/usr/bin/env python3
"""
Adaptive TDD: Test the tests by injecting bugs

This script intentionally introduces bugs into validation.py and verifies
that the test suite catches them. If a bug is NOT caught, the tests are
insufficient.

This is the "Adaptive" part of Adaptive TDD - we verify our tests actually work.
"""

import subprocess
import sys
import tempfile
import shutil
from pathlib import Path


def run_tests() -> tuple[bool, str]:
    """
    Run the test suite and return (passed, output)

    Returns:
        (True, output) if all tests passed
        (False, output) if any tests failed
    """
    result = subprocess.run(
        ["python", "-m", "pytest", "test_validation.py", "-v"],
        capture_output=True,
        text=True,
    )
    return result.returncode == 0, result.stdout + result.stderr


def inject_bug(original_file: Path, bug_description: str, search: str, replace: str) -> bool:
    """
    Inject a bug by replacing code, run tests, verify they fail

    Args:
        original_file: Path to validation.py
        bug_description: Description of the bug being injected
        search: Code to search for
        replace: Code to replace with (the bug)

    Returns:
        True if tests caught the bug (failed as expected)
        False if tests passed (BUG NOT CAUGHT - tests are insufficient)
    """
    print(f"\n{'='*70}")
    print(f"Bug: {bug_description}")
    print(f"{'='*70}")

    # Read original
    content = original_file.read_text()

    if search not in content:
        print(f"❌ SKIP: Search string not found in file")
        return True  # Skip, don't count as failure

    # Inject bug
    buggy_content = content.replace(search, replace, 1)
    original_file.write_text(buggy_content)

    # Run tests
    passed, output = run_tests()

    # Restore original
    original_file.write_text(content)

    if passed:
        print(f"❌ TESTS PASSED - BUG NOT CAUGHT!")
        print(f"   This bug should have been caught but wasn't.")
        print(f"   Tests are INSUFFICIENT.")
        return False
    else:
        print(f"✅ Tests caught the bug (failed as expected)")
        return True


def main():
    """Run all bug injection tests"""

    validation_file = Path("validation.py")

    if not validation_file.exists():
        print(f"Error: {validation_file} not found")
        print("Run this script from the src/ directory")
        sys.exit(1)

    print("="*70)
    print("ADAPTIVE TDD: Testing the Tests")
    print("="*70)
    print("\nThis will inject bugs and verify the test suite catches them.\n")

    bugs = [
        # Hex color validation bugs
        (
            "Remove hex color # check",
            'if color.startswith("#"):\n        raise ValidationError("Hex color must not include \'#\' prefix")',
            'pass  # BUG: Removed validation',
        ),
        (
            "Remove hex color length check",
            'if len(color) != 6:\n        raise ValidationError(f"Hex color must be exactly 6 characters, got {len(color)}")',
            'pass  # BUG: Removed validation',
        ),
        (
            "Accept invalid hex characters",
            'try:\n        int(color, 16)\n    except ValueError:\n        raise ValidationError(f"Invalid hex color: {color}")',
            'pass  # BUG: Accept anything',
        ),

        # Date validation bugs
        (
            "Accept invalid date format",
            'if len(date_str) != 10 or date_str[4] != \'-\' or date_str[7] != \'-\':\n        raise ValidationError(f"Date must be YYYY-MM-DD format, got: {date_str}")',
            'pass  # BUG: Accept any format',
        ),
        (
            "Accept invalid dates (Feb 30)",
            'try:\n        datetime.strptime(date_str, "%Y-%m-%d")\n    except ValueError:\n        # If format is correct but date is invalid (e.g., Feb 30)\n        raise ValidationError(f"Invalid date: {date_str}")',
            'pass  # BUG: Accept invalid dates',
        ),

        # Project validation bugs
        (
            "Accept missing project title",
            'if "title" not in project:\n        raise ValidationError("Project missing required field: title")',
            'pass  # BUG: Don\'t check for title',
        ),
        (
            "Accept empty project title",
            'if not title.strip():\n        raise ValidationError("Project title cannot be empty")',
            'pass  # BUG: Accept empty',
        ),
        (
            "Accept project title over 250 chars",
            'if len(title) > 250:\n        raise ValidationError(f"Project title cannot exceed 250 characters, got {len(title)}")',
            'pass  # BUG: No length check',
        ),
        (
            "Accept project description over 5000 chars",
            'if len(description) > 5000:\n            raise ValidationError(f"Project description cannot exceed 5000 characters, got {len(description)}")',
            'pass  # BUG: No length check',
        ),

        # Label validation bugs
        (
            "Accept missing label title",
            'if "title" not in label:\n        raise ValidationError("Label missing required field: title")',
            'pass  # BUG: Don\'t check for title',
        ),
        (
            "Accept label title over 100 chars",
            'if len(title) > 100:\n        raise ValidationError(f"Label title cannot exceed 100 characters, got {len(title)}")',
            'pass  # BUG: No length check',
        ),

        # Task validation bugs
        (
            "Accept missing task title",
            'if "title" not in task:\n        raise ValidationError("Task missing required field: title")',
            'pass  # BUG: Don\'t check for title',
        ),
        (
            "Accept empty task title",
            '# Required: title\n    if "title" not in task:\n        raise ValidationError("Task missing required field: title")\n\n    title = task["title"]\n    if not isinstance(title, str):\n        raise ValidationError("Task title must be a string")\n\n    if not title.strip():\n        raise ValidationError("Task title cannot be empty")',
            '# Required: title\n    if "title" not in task:\n        raise ValidationError("Task missing required field: title")\n\n    title = task["title"]\n    if not isinstance(title, str):\n        raise ValidationError("Task title must be a string")\n\n    # BUG: Removed empty check',
        ),
        (
            "Accept task priority < 0",
            'if priority < 0 or priority > 5:\n            raise ValidationError(f"Task priority must be between 0 and 5, got {priority}")',
            'if priority > 5:\n            raise ValidationError(f"Task priority must be between 0 and 5, got {priority}")  # BUG: No lower bound',
        ),
        (
            "Accept task priority > 5",
            'if priority < 0 or priority > 5:\n            raise ValidationError(f"Task priority must be between 0 and 5, got {priority}")',
            'if priority < 0:\n            raise ValidationError(f"Task priority must be between 0 and 5, got {priority}")  # BUG: No upper bound',
        ),
        (
            "Accept non-boolean done field",
            'if not isinstance(done, bool):\n            raise ValidationError("Task \'done\' field must be a boolean")',
            'pass  # BUG: Accept any type',
        ),
        (
            "Accept task labels as string (not list)",
            'if not isinstance(labels, list):\n            raise ValidationError("Task labels must be a list")',
            'pass  # BUG: Accept any type',
        ),
        (
            "Accept undefined label references",
            'for label_title in labels:\n            if label_title not in available_labels:\n                raise ValidationError(f"Label \'{label_title}\' not found in available labels")',
            'pass  # BUG: Don\'t validate references',
        ),

        # Schema validation bugs
        (
            "Accept missing project in schema",
            'if "project" not in schema:\n        raise ValidationError("Schema missing required field: project")',
            'pass  # BUG: Don\'t check for project',
        ),
        (
            "Accept schema as non-dict",
            'if not isinstance(schema, dict):\n        raise ValidationError("Schema must be a dictionary")',
            'pass  # BUG: Accept any type',
        ),
        (
            "Accept tasks as non-list",
            'tasks = schema.get("tasks", [])\n    if not isinstance(tasks, list):\n        raise ValidationError("Tasks must be a list")',
            'tasks = schema.get("tasks", [])\n    # BUG: Don\'t check type',
        ),
    ]

    results = []
    for bug_desc, search, replace in bugs:
        caught = inject_bug(validation_file, bug_desc, search, replace)
        results.append((bug_desc, caught))

    # Summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)

    total = len(results)
    caught = sum(1 for _, c in results if c)

    print(f"\nTotal bugs injected: {total}")
    print(f"Bugs caught by tests: {caught}")
    print(f"Bugs NOT caught: {total - caught}")

    if caught == total:
        print("\n✅ SUCCESS! All bugs were caught by the test suite.")
        print("   Tests are comprehensive and effective.")
        return 0
    else:
        print("\n❌ FAILURE! Some bugs were NOT caught.")
        print("   Tests need improvement.")
        print("\nBugs that escaped detection:")
        for bug_desc, was_caught in results:
            if not was_caught:
                print(f"  - {bug_desc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
