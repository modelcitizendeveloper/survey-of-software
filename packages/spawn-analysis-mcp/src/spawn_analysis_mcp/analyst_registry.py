"""
Analyst Registry - Business logic for managing analyst prompts.

Discovers and loads analyst prompts from the analysts/ directory.
Each analyst is a markdown file with structured metadata.
"""

import os
from pathlib import Path
from typing import Dict, List, Optional
import re


class Analyst:
    """Represents a spawn-analysis analyst/framework."""

    def __init__(
        self,
        id: str,
        name: str,
        description: str,
        prompt: str,
        order: int,
        file_path: str,
    ):
        self.id = id
        self.name = name
        self.description = description
        self.prompt = prompt
        self.order = order
        self.file_path = file_path

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "order": self.order,
            "file_path": self.file_path,
            "prompt_length": len(self.prompt),
        }


class AnalystRegistry:
    """Registry for spawn-analysis analysts."""

    def __init__(self, analysts_dir: Optional[Path] = None):
        """
        Initialize the analyst registry.

        Args:
            analysts_dir: Directory containing analyst prompt files.
                         If None, uses analysts/ relative to this module.
        """
        if analysts_dir is None:
            # Default: analysts/ directory next to the package
            module_dir = Path(__file__).parent
            analysts_dir = module_dir.parent.parent / "analysts"

        self.analysts_dir = Path(analysts_dir)
        self._analysts: Dict[str, Analyst] = {}
        self._load_analysts()

    def _load_analysts(self):
        """Load all analyst prompts from the analysts directory."""
        if not self.analysts_dir.exists():
            raise FileNotFoundError(
                f"Analysts directory not found: {self.analysts_dir}"
            )

        for file_path in sorted(self.analysts_dir.glob("*.md")):
            analyst = self._parse_analyst_file(file_path)
            if analyst:
                self._analysts[analyst.id] = analyst

    def _parse_analyst_file(self, file_path: Path) -> Optional[Analyst]:
        """
        Parse an analyst prompt file.

        Expected format:
        ```
        # Analyst Name

        **Description**: Brief description

        ... rest of prompt ...
        ```

        Args:
            file_path: Path to analyst markdown file

        Returns:
            Analyst object or None if parsing fails
        """
        try:
            content = file_path.read_text(encoding="utf-8")

            # Extract order from filename (e.g., "01-optimizer.md" -> 1)
            filename = file_path.stem
            order_match = re.match(r"(\d+)-(.+)", filename)
            if order_match:
                order = int(order_match.group(1))
                id_base = order_match.group(2)
            else:
                order = 99
                id_base = filename

            # Extract name from first heading
            name_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
            name = name_match.group(1).strip() if name_match else id_base.title()

            # Extract description from **Description:** line
            desc_match = re.search(
                r"\*\*Description\*\*:\s*(.+?)(?:\n\n|\n\*\*|$)",
                content,
                re.DOTALL,
            )
            description = (
                desc_match.group(1).strip() if desc_match else "No description"
            )

            return Analyst(
                id=id_base,
                name=name,
                description=description,
                prompt=content,
                order=order,
                file_path=str(file_path),
            )

        except Exception as e:
            print(f"Error parsing analyst file {file_path}: {e}")
            return None

    def get_all_analysts(self) -> List[Analyst]:
        """
        Get all analysts sorted by order.

        Returns:
            List of Analyst objects
        """
        return sorted(self._analysts.values(), key=lambda a: a.order)

    def get_analyst(self, analyst_id: str) -> Optional[Analyst]:
        """
        Get a specific analyst by ID.

        Args:
            analyst_id: Analyst identifier (e.g., "optimizer", "strategist")

        Returns:
            Analyst object or None if not found
        """
        return self._analysts.get(analyst_id)

    def get_analyst_ids(self) -> List[str]:
        """
        Get list of all analyst IDs.

        Returns:
            List of analyst identifiers
        """
        return [a.id for a in self.get_all_analysts()]

    def __len__(self) -> int:
        """Return number of registered analysts."""
        return len(self._analysts)


# Singleton instance for easy access
_registry: Optional[AnalystRegistry] = None


def get_registry() -> AnalystRegistry:
    """
    Get the singleton analyst registry instance.

    Returns:
        AnalystRegistry instance
    """
    global _registry
    if _registry is None:
        _registry = AnalystRegistry()
    return _registry
