"""
Discovery Tools - MCP tools for analyst discovery.

Tools:
- list_analysts: List all available analysts
- describe_analyst: Get detailed info about a specific analyst
- suggest_analysts: Recommend analysts based on decision characteristics (Phase 2.3)
"""

from fastmcp import FastMCP
from spawn_analysis_mcp.analyst_registry import get_registry
from spawn_analysis_mcp.analyst_selection import suggest_analysts as suggest_analysts_impl


def register_discovery_tools(mcp: FastMCP):
    """
    Register discovery tools with FastMCP.

    Args:
        mcp: FastMCP instance
    """

    @mcp.tool()
    def list_analysts() -> dict:
        """
        List all available spawn-analysis analysts/frameworks.

        Returns a list of analysts with their IDs, names, descriptions, and order.
        Use this to discover what analytical perspectives are available.

        Returns:
            dict: {
                "analysts": [
                    {
                        "id": str,
                        "name": str,
                        "description": str,
                        "order": int
                    },
                    ...
                ],
                "count": int
            }

        Example:
            >>> result = list_analysts()
            >>> print(f"Found {result['count']} analysts")
            >>> for analyst in result['analysts']:
            ...     print(f"  {analyst['order']}. {analyst['name']}")
        """
        registry = get_registry()
        analysts = registry.get_all_analysts()

        return {
            "analysts": [
                {
                    "id": a.id,
                    "name": a.name,
                    "description": a.description,
                    "order": a.order,
                }
                for a in analysts
            ],
            "count": len(analysts),
        }

    @mcp.tool()
    def describe_analyst(analyst_id: str) -> dict:
        """
        Get detailed information about a specific analyst.

        Returns the full prompt text and metadata for an analyst.
        Use this to understand what perspective an analyst brings.

        Args:
            analyst_id (str): Analyst identifier (e.g., "optimizer", "strategist")

        Returns:
            dict: {
                "id": str,
                "name": str,
                "description": str,
                "order": int,
                "prompt": str,          # Full prompt text
                "prompt_length": int,
                "file_path": str
            }

        Raises:
            ValueError: If analyst_id not found

        Example:
            >>> analyst = describe_analyst("optimizer")
            >>> print(analyst["name"])
            >>> print(f"Prompt length: {analyst['prompt_length']} chars")
        """
        registry = get_registry()
        analyst = registry.get_analyst(analyst_id)

        if not analyst:
            available = registry.get_analyst_ids()
            raise ValueError(
                f"Analyst '{analyst_id}' not found. "
                f"Available: {', '.join(available)}"
            )

        return {
            "id": analyst.id,
            "name": analyst.name,
            "description": analyst.description,
            "order": analyst.order,
            "prompt": analyst.prompt,
            "prompt_length": len(analyst.prompt),
            "file_path": analyst.file_path,
        }

    @mcp.tool()
    def suggest_analysts(
        decision_characteristics: dict,
        max_analysts: int = 8,
    ) -> dict:
        """
        Recommend analysts based on decision characteristics.

        Intelligently selects analysts based on the decision profile to optimize
        analysis quality and cost. For low complexity decisions, suggests 3-4 core
        analysts. For high complexity, recommends all 8 analysts.

        Args:
            decision_characteristics (dict): Decision profile with keys:
                - has_vikunja_data (bool): Whether Vikunja project data is available
                - has_quantitative_metrics (bool): Whether decision has numerical data
                - needs_innovation (bool): Whether creative alternatives are needed
                - needs_risk_assessment (bool): Whether uncertainty analysis is important
                - has_dependencies (bool): Whether decision affects other systems
                - has_resource_constraints (bool): Whether budget/time is limited
                - complexity (str): "low" | "medium" | "high"
                - time_sensitivity (str): "low" | "medium" | "high"
            max_analysts (int): Maximum analysts to recommend (default: 8)

        Returns:
            dict: {
                "recommended_analysts": [analyst_id, ...],
                "reasoning": {analyst_id: "why this analyst is relevant"},
                "optional_analysts": [analyst_id, ...]  # If complexity is low
            }

        Example:
            >>> result = suggest_analysts({
            ...     "has_vikunja_data": True,
            ...     "needs_innovation": True,
            ...     "complexity": "medium"
            ... })
            >>> print(f"Recommended: {result['recommended_analysts']}")
            >>> for analyst_id, reason in result['reasoning'].items():
            ...     print(f"  {analyst_id}: {reason}")
        """
        return suggest_analysts_impl(decision_characteristics, max_analysts)
