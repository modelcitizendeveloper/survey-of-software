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
