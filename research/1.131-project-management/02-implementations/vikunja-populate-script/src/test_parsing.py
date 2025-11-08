#!/usr/bin/env python3
"""
Unit tests for file parsing (YAML/JSON)

Tests written BEFORE implementation (TDD).
"""

import pytest
import tempfile
from pathlib import Path
from parsing import parse_input, ParsingError


class TestParseYAML:
    """Test YAML file parsing"""

    def test_parse_valid_yaml(self, tmp_path):
        """Valid YAML should parse correctly"""
        yaml_file = tmp_path / "test.yaml"
        yaml_file.write_text("""
project:
  title: "My Project"
  description: "Test description"

labels:
  - title: "Bug"
    color: "FF0000"

tasks:
  - title: "Fix bug"
    priority: 5
    labels:
      - "Bug"
""")

        result = parse_input(yaml_file)

        assert result["project"]["title"] == "My Project"
        assert result["project"]["description"] == "Test description"
        assert len(result["labels"]) == 1
        assert result["labels"][0]["title"] == "Bug"
        assert len(result["tasks"]) == 1
        assert result["tasks"][0]["title"] == "Fix bug"

    def test_parse_minimal_yaml(self, tmp_path):
        """Minimal YAML (project only) should parse"""
        yaml_file = tmp_path / "minimal.yaml"
        yaml_file.write_text("""
project:
  title: "Minimal Project"
""")

        result = parse_input(yaml_file)

        assert result["project"]["title"] == "Minimal Project"
        assert "labels" not in result or result.get("labels") == []
        assert "tasks" not in result or result.get("tasks") == []

    def test_parse_yaml_with_multiline(self, tmp_path):
        """YAML with multiline strings should parse"""
        yaml_file = tmp_path / "multiline.yaml"
        yaml_file.write_text("""
project:
  title: "Project"
  description: |
    Line 1
    Line 2
    Line 3

tasks:
  - title: "Task"
    description: |
      Multi-line
      task description
""")

        result = parse_input(yaml_file)

        assert "Line 1\nLine 2\nLine 3" in result["project"]["description"]
        assert "Multi-line\ntask description" in result["tasks"][0]["description"]

    def test_parse_invalid_yaml(self, tmp_path):
        """Invalid YAML syntax should raise error"""
        yaml_file = tmp_path / "invalid.yaml"
        yaml_file.write_text("""
project:
  title: "Unclosed quote
  description: Test
""")

        with pytest.raises(ParsingError, match="Invalid YAML"):
            parse_input(yaml_file)

    def test_parse_yaml_wrong_extension(self, tmp_path):
        """YAML content with .yml extension should work"""
        yml_file = tmp_path / "test.yml"
        yml_file.write_text("""
project:
  title: "Project"
""")

        result = parse_input(yml_file)

        assert result["project"]["title"] == "Project"


class TestParseJSON:
    """Test JSON file parsing"""

    def test_parse_valid_json(self, tmp_path):
        """Valid JSON should parse correctly"""
        json_file = tmp_path / "test.json"
        json_file.write_text("""{
  "project": {
    "title": "My Project",
    "description": "Test description"
  },
  "labels": [
    {"title": "Bug", "color": "FF0000"}
  ],
  "tasks": [
    {
      "title": "Fix bug",
      "priority": 5,
      "labels": ["Bug"]
    }
  ]
}""")

        result = parse_input(json_file)

        assert result["project"]["title"] == "My Project"
        assert len(result["labels"]) == 1
        assert len(result["tasks"]) == 1

    def test_parse_minimal_json(self, tmp_path):
        """Minimal JSON (project only) should parse"""
        json_file = tmp_path / "minimal.json"
        json_file.write_text("""{
  "project": {"title": "Minimal Project"}
}""")

        result = parse_input(json_file)

        assert result["project"]["title"] == "Minimal Project"

    def test_parse_invalid_json(self, tmp_path):
        """Invalid JSON syntax should raise error"""
        json_file = tmp_path / "invalid.json"
        json_file.write_text("""{
  "project": {
    "title": "Missing closing brace"
  }
""")  # Missing closing }

        with pytest.raises(ParsingError, match="Invalid JSON"):
            parse_input(json_file)

    def test_parse_json_with_trailing_comma(self, tmp_path):
        """JSON with trailing comma should fail"""
        json_file = tmp_path / "trailing.json"
        json_file.write_text("""{
  "project": {
    "title": "Project",
  }
}""")

        with pytest.raises(ParsingError, match="Invalid JSON"):
            parse_input(json_file)


class TestParseErrors:
    """Test error handling"""

    def test_file_not_found(self):
        """Non-existent file should raise error"""
        with pytest.raises(ParsingError, match="File not found"):
            parse_input(Path("/nonexistent/file.yaml"))

    def test_unsupported_extension(self, tmp_path):
        """File with unsupported extension should raise error"""
        txt_file = tmp_path / "test.txt"
        txt_file.write_text("project:\n  title: Test")

        with pytest.raises(ParsingError, match="Unsupported file format"):
            parse_input(txt_file)

    def test_empty_file(self, tmp_path):
        """Empty file should raise error"""
        empty_file = tmp_path / "empty.yaml"
        empty_file.write_text("")

        with pytest.raises(ParsingError, match="Empty file"):
            parse_input(empty_file)

    def test_whitespace_only_file(self, tmp_path):
        """File with only whitespace should raise error"""
        ws_file = tmp_path / "whitespace.yaml"
        ws_file.write_text("   \n  \n  ")

        with pytest.raises(ParsingError, match="Empty file"):
            parse_input(ws_file)


class TestParseIntegration:
    """Integration tests for parsing + validation"""

    def test_parse_and_validate_success(self, tmp_path):
        """Valid file should parse and validate"""
        from validation import validate_schema

        yaml_file = tmp_path / "valid.yaml"
        yaml_file.write_text("""
project:
  title: "Valid Project"

labels:
  - title: "Bug"

tasks:
  - title: "Fix bug"
    labels: ["Bug"]
""")

        result = parse_input(yaml_file)
        assert validate_schema(result) is True

    def test_parse_success_but_validate_fail(self, tmp_path):
        """File that parses but fails validation"""
        from validation import validate_schema, ValidationError

        yaml_file = tmp_path / "invalid_schema.yaml"
        yaml_file.write_text("""
project:
  title: ""

tasks: []
""")

        result = parse_input(yaml_file)

        # Should parse successfully
        assert "project" in result

        # But validation should fail (empty title)
        with pytest.raises(ValidationError, match="cannot be empty"):
            validate_schema(result)

    def test_parse_yaml_boolean_types(self, tmp_path):
        """YAML boolean values should parse correctly"""
        yaml_file = tmp_path / "bool.yaml"
        yaml_file.write_text("""
project:
  title: "Test"

tasks:
  - title: "Task 1"
    done: true
  - title: "Task 2"
    done: false
  - title: "Task 3"
    done: yes
  - title: "Task 4"
    done: no
""")

        result = parse_input(yaml_file)

        # YAML yes/no should convert to True/False
        assert result["tasks"][0]["done"] is True
        assert result["tasks"][1]["done"] is False
        assert result["tasks"][2]["done"] is True
        assert result["tasks"][3]["done"] is False

    def test_parse_yaml_null_values(self, tmp_path):
        """YAML null values should be removed from output"""
        yaml_file = tmp_path / "null.yaml"
        yaml_file.write_text("""
project:
  title: "Test"
  description: null
  color: ~

tasks:
  - title: "Task"
    description: null
    due_date: ~
""")

        result = parse_input(yaml_file)

        # Null values should be removed entirely (not present in output)
        assert "description" not in result["project"]
        assert "color" not in result["project"]
        assert "description" not in result["tasks"][0]
        assert "due_date" not in result["tasks"][0]
