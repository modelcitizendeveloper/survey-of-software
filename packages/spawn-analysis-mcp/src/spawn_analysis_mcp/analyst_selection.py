"""
Analyst Selection - Intelligent analyst recommendation based on decision characteristics.

Recommends analysts based on decision profile to optimize analysis quality and cost.
"""

from typing import Dict, List, Literal


def suggest_analysts(
    decision_characteristics: Dict,
    max_analysts: int = 8,
) -> Dict:
    """
    Recommend analysts based on decision profile.

    Args:
        decision_characteristics: {
            "has_vikunja_data": bool,
            "has_quantitative_metrics": bool,
            "needs_innovation": bool,
            "needs_risk_assessment": bool,
            "has_dependencies": bool,
            "has_resource_constraints": bool,
            "complexity": "low" | "medium" | "high",
            "time_sensitivity": "low" | "medium" | "high"
        }
        max_analysts: Maximum analysts to recommend (default: 8)

    Returns: {
        "recommended_analysts": [analyst_id, ...],
        "reasoning": {analyst_id: "why this analyst is relevant"},
        "optional_analysts": [analyst_id, ...]  # If complexity is low
    }
    """
    recommended = []
    reasoning = {}
    optional = []

    # Extract characteristics with defaults
    has_vikunja_data = decision_characteristics.get("has_vikunja_data", False)
    has_quantitative = decision_characteristics.get("has_quantitative_metrics", False)
    needs_innovation = decision_characteristics.get("needs_innovation", False)
    needs_risk = decision_characteristics.get("needs_risk_assessment", False)
    has_dependencies = decision_characteristics.get("has_dependencies", False)
    has_resource_constraints = decision_characteristics.get(
        "has_resource_constraints", False
    )
    complexity = decision_characteristics.get("complexity", "medium")
    time_sensitivity = decision_characteristics.get("time_sensitivity", "medium")

    # Always include baseline analysts
    recommended.append("optimizer")
    reasoning["optimizer"] = "Core analyst for cost-benefit optimization"

    recommended.append("synthesizer")
    reasoning["synthesizer"] = "Core analyst for integrating perspectives"

    # Vikunja data available - capability assessment
    if has_vikunja_data:
        recommended.append("capability-auditor")
        reasoning["capability-auditor"] = (
            "Can assess current workload and capacity constraints"
        )

    # Needs innovation
    if needs_innovation:
        recommended.append("creator")
        reasoning["creator"] = "Provides innovative alternatives and creative solutions"

    # Needs risk assessment
    if needs_risk:
        recommended.append("probabilist")
        reasoning["probabilist"] = (
            "Analyzes uncertainty and risk with probabilistic thinking"
        )

    # Has dependencies
    if has_dependencies:
        recommended.append("systems-thinker")
        reasoning["systems-thinker"] = (
            "Maps dependencies and analyzes systemic impacts"
        )

    # Strategist for medium-high complexity or when time matters
    if complexity in ["medium", "high"] or time_sensitivity in ["medium", "high"]:
        if "strategist" not in recommended:
            recommended.append("strategist")
            reasoning["strategist"] = (
                "Provides strategic perspective on timing and sequencing"
            )

    # Experimentalist for high complexity or quantitative decisions
    if complexity == "high" or has_quantitative:
        if "experimentalist" not in recommended:
            recommended.append("experimentalist")
            reasoning["experimentalist"] = (
                "Designs experiments to test assumptions and validate choices"
            )

    # Handle complexity-based recommendations
    if complexity == "low":
        # For low complexity, keep only 3-4 core analysts
        core_analysts = ["optimizer", "synthesizer"]

        # Add most relevant specialist based on characteristics
        if needs_innovation and "creator" in recommended:
            core_analysts.append("creator")
        elif needs_risk and "probabilist" in recommended:
            core_analysts.append("probabilist")
        elif has_dependencies and "systems-thinker" in recommended:
            core_analysts.append("systems-thinker")
        elif has_vikunja_data and "capability-auditor" in recommended:
            core_analysts.append("capability-auditor")
        else:
            # Default: add strategist for basic strategic perspective
            core_analysts.append("strategist")
            if "strategist" not in reasoning:
                reasoning["strategist"] = "Provides strategic perspective on execution"

        # Ensure at least 3 analysts for low complexity
        if len(core_analysts) < 3:
            # Add strategist if not already included
            if "strategist" not in core_analysts:
                core_analysts.append("strategist")
                reasoning["strategist"] = "Provides strategic perspective on execution"

        # Move non-core to optional
        for analyst in recommended:
            if analyst not in core_analysts:
                optional.append(analyst)

        recommended = core_analysts

    elif complexity == "high":
        # For high complexity, use all 8 analysts
        all_analysts = [
            "optimizer",
            "strategist",
            "systems-thinker",
            "capability-auditor",
            "experimentalist",
            "probabilist",
            "creator",
            "synthesizer",
        ]

        for analyst in all_analysts:
            if analyst not in recommended:
                recommended.append(analyst)
                reasoning[analyst] = "High complexity benefits from comprehensive analysis"

    # Respect max_analysts limit
    if len(recommended) > max_analysts:
        # Keep most relevant analysts based on characteristics
        priority_order = _get_priority_order(decision_characteristics)

        # Sort recommended by priority
        recommended.sort(key=lambda a: priority_order.index(a) if a in priority_order else 99)

        # Move extras to optional
        optional.extend(recommended[max_analysts:])
        recommended = recommended[:max_analysts]

    return {
        "recommended_analysts": recommended,
        "reasoning": reasoning,
        "optional_analysts": optional,
    }


def _get_priority_order(characteristics: Dict) -> List[str]:
    """
    Get priority order of analysts based on decision characteristics.

    Args:
        characteristics: Decision characteristics dict

    Returns:
        List of analyst IDs in priority order
    """
    # Start with baseline
    priority = ["optimizer", "synthesizer"]

    # Add specialists based on characteristics
    if characteristics.get("needs_innovation"):
        priority.append("creator")

    if characteristics.get("needs_risk_assessment"):
        priority.append("probabilist")

    if characteristics.get("has_dependencies"):
        priority.append("systems-thinker")

    if characteristics.get("has_vikunja_data"):
        priority.append("capability-auditor")

    # Add strategist for timing-sensitive decisions
    if characteristics.get("time_sensitivity") in ["medium", "high"]:
        priority.append("strategist")

    # Add experimentalist for quantitative decisions
    if characteristics.get("has_quantitative_metrics"):
        priority.append("experimentalist")

    # Fill remaining slots
    all_analysts = [
        "optimizer",
        "strategist",
        "systems-thinker",
        "capability-auditor",
        "experimentalist",
        "probabilist",
        "creator",
        "synthesizer",
    ]

    for analyst in all_analysts:
        if analyst not in priority:
            priority.append(analyst)

    return priority
