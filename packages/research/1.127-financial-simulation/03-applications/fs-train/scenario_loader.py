#!/usr/bin/env python3
"""Load and validate training scenarios from YAML files."""

import yaml
from pathlib import Path
from typing import Dict, List, Any


class ScenarioLoader:
    """Load financial training scenarios from YAML."""

    def __init__(self, scenarios_dir: str = "scenarios"):
        self.scenarios_dir = Path(scenarios_dir)

    def load_scenario(self, scenario_file: str) -> Dict[str, Any]:
        """Load a single scenario from YAML file.

        Args:
            scenario_file: Path to YAML scenario file

        Returns:
            Parsed scenario dictionary
        """
        scenario_path = self.scenarios_dir / scenario_file

        if not scenario_path.exists():
            raise FileNotFoundError(f"Scenario not found: {scenario_path}")

        with open(scenario_path, 'r') as f:
            scenario = yaml.safe_load(f)

        # Validate required fields
        required = ['scenario_id', 'name', 'difficulty', 'financial_data', 'key_insights']
        missing = [field for field in required if field not in scenario]
        if missing:
            raise ValueError(f"Missing required fields: {missing}")

        return scenario

    def list_scenarios(self) -> List[Dict[str, str]]:
        """List all available scenarios.

        Returns:
            List of dicts with scenario metadata
        """
        scenarios = []

        if not self.scenarios_dir.exists():
            return scenarios

        for yaml_file in sorted(self.scenarios_dir.glob("*.yaml")):
            try:
                with open(yaml_file, 'r') as f:
                    data = yaml.safe_load(f)
                    scenarios.append({
                        'file': yaml_file.name,
                        'id': data.get('scenario_id', 'unknown'),
                        'name': data.get('name', 'Unknown'),
                        'difficulty': data.get('difficulty', 'unknown')
                    })
            except Exception as e:
                print(f"Warning: Could not load {yaml_file.name}: {e}")

        return scenarios

    def get_scenario_by_id(self, scenario_id: str) -> Dict[str, Any]:
        """Load scenario by its ID.

        Args:
            scenario_id: The scenario_id field from YAML

        Returns:
            Parsed scenario dictionary
        """
        for yaml_file in self.scenarios_dir.glob("*.yaml"):
            try:
                with open(yaml_file, 'r') as f:
                    data = yaml.safe_load(f)
                    if data.get('scenario_id') == scenario_id:
                        return data
            except Exception:
                continue

        raise ValueError(f"Scenario not found: {scenario_id}")

    def find_scenario(self, search: str) -> str:
        """Find scenario file by number, name, or partial match.

        Args:
            search: Can be:
                - Full filename: "001_simple_growth.yaml"
                - Just number: "001" or "002"
                - Partial name: "margin", "growth", "cash"
                - With prefix: "scenarios/001_simple_growth.yaml"

        Returns:
            Scenario filename (without scenarios/ prefix)

        Raises:
            ValueError: If no match or multiple matches found
        """
        # Strip scenarios/ prefix if present
        if search.startswith('scenarios/'):
            search = search[10:]

        # If it's a full filename that exists, use it
        if search.endswith('.yaml') and (self.scenarios_dir / search).exists():
            return search

        # Get all scenario files
        all_scenarios = list(self.scenarios_dir.glob("*.yaml"))

        # Try exact number match (e.g., "002" -> "002_*.yaml")
        if search.isdigit():
            matches = [f for f in all_scenarios if f.name.startswith(f"{search}_")]
            if len(matches) == 1:
                return matches[0].name
            elif len(matches) > 1:
                raise ValueError(f"Multiple scenarios match '{search}': {[m.name for m in matches]}")

        # Try partial name match (case-insensitive)
        search_lower = search.lower()
        matches = [f for f in all_scenarios if search_lower in f.name.lower()]

        if len(matches) == 1:
            return matches[0].name
        elif len(matches) > 1:
            raise ValueError(f"Multiple scenarios match '{search}': {[m.name for m in matches]}")

        raise ValueError(f"No scenario found matching: {search}")
