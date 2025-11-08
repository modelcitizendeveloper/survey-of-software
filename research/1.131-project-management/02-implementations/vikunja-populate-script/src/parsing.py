#!/usr/bin/env python3
"""
File parsing for Vikunja population script

Supports YAML and JSON input files.
"""

import json
import yaml
from pathlib import Path
from typing import Dict, Any


class ParsingError(Exception):
    """Raised when file parsing fails"""
    pass


def parse_input(file_path: Path) -> Dict[str, Any]:
    """
    Parse YAML or JSON file into dictionary

    Args:
        file_path: Path to input file (.yaml, .yml, or .json)

    Returns:
        Parsed dictionary

    Raises:
        ParsingError: If file cannot be parsed
    """
    if not isinstance(file_path, Path):
        file_path = Path(file_path)

    # Check file exists
    if not file_path.exists():
        raise ParsingError(f"File not found: {file_path}")

    # Check file extension
    extension = file_path.suffix.lower()
    if extension not in [".yaml", ".yml", ".json"]:
        raise ParsingError(
            f"Unsupported file format: {extension}. "
            f"Supported formats: .yaml, .yml, .json"
        )

    # Read file content
    try:
        content = file_path.read_text()
    except Exception as e:
        raise ParsingError(f"Error reading file: {e}")

    # Check for empty file
    if not content.strip():
        raise ParsingError(f"Empty file: {file_path}")

    # Parse based on extension
    try:
        if extension in [".yaml", ".yml"]:
            data = yaml.safe_load(content)
        else:  # .json
            data = json.loads(content)
    except yaml.YAMLError as e:
        raise ParsingError(f"Invalid YAML syntax: {e}")
    except json.JSONDecodeError as e:
        raise ParsingError(f"Invalid JSON syntax: {e}")
    except Exception as e:
        raise ParsingError(f"Error parsing file: {e}")

    # Ensure we got a dictionary
    if not isinstance(data, dict):
        raise ParsingError(
            f"File must contain a dictionary/object at root level, got {type(data).__name__}"
        )

    # Clean null values (YAML null/~ becomes None in Python)
    data = _clean_nulls(data)

    return data


def _clean_nulls(data: Any) -> Any:
    """
    Recursively remove None values from dictionaries

    Args:
        data: Data structure to clean

    Returns:
        Cleaned data structure
    """
    if isinstance(data, dict):
        return {
            k: _clean_nulls(v)
            for k, v in data.items()
            if v is not None
        }
    elif isinstance(data, list):
        return [_clean_nulls(item) for item in data]
    else:
        return data
