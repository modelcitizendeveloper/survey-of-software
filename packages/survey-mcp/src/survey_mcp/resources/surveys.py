"""
MCP Resources for survey data.

Exposes research.modelcitizendeveloper.com surveys as MCP resources.
"""

from fastmcp import FastMCP
from survey_mcp.cache import get_cache_manager


def register_survey_resources(mcp: FastMCP):
    """
    Register survey resources with FastMCP.

    Resources:
    - survey://<category> - Full survey (all 4PS passes)
    - survey://<category>/s1-rapid - Quick comparison
    - survey://<category>/s2-comprehensive - Feature matrix
    - survey://<category>/s3-need-driven - Use case scenarios
    - survey://<category>/s4-strategic - Maturity analysis

    Args:
        mcp: FastMCP instance
    """

    @mcp.resource("survey://{category}")
    def get_survey(category: str) -> str:
        """
        Get full survey for a category.

        Args:
            category: Survey category (e.g., "1.001-009")

        Returns:
            str: Full survey content (all 4PS passes)

        Example:
            >>> content = mcp.resource("survey://1.001-009")
            >>> # Returns full Sorting & Searching survey
        """
        cache = get_cache_manager()
        survey = cache.parse_survey_page(category)

        # Return full content
        return survey["content"]

    @mcp.resource("survey://{category}/s1-rapid")
    def get_survey_s1(category: str) -> str:
        """
        Get S1 (Rapid) pass for a survey.

        S1 provides a quick comparison of libraries in the category.

        Args:
            category: Survey category (e.g., "1.001-009")

        Returns:
            str: S1 Rapid pass content

        Example:
            >>> content = mcp.resource("survey://1.001-009/s1-rapid")
            >>> # Returns quick comparison of sorting algorithms
        """
        cache = get_cache_manager()
        survey = cache.parse_survey_page(category)

        return survey.get("s1_rapid") or "S1 Rapid pass not available for this survey"

    @mcp.resource("survey://{category}/s2-comprehensive")
    def get_survey_s2(category: str) -> str:
        """
        Get S2 (Comprehensive) pass for a survey.

        S2 provides detailed feature comparison matrices.

        Args:
            category: Survey category (e.g., "1.001-009")

        Returns:
            str: S2 Comprehensive pass content
        """
        cache = get_cache_manager()
        survey = cache.parse_survey_page(category)

        return survey.get("s2_comprehensive") or "S2 Comprehensive pass not available for this survey"

    @mcp.resource("survey://{category}/s3-need-driven")
    def get_survey_s3(category: str) -> str:
        """
        Get S3 (Need-Driven) pass for a survey.

        S3 provides use case scenarios and decision trees.

        Args:
            category: Survey category (e.g., "1.001-009")

        Returns:
            str: S3 Need-Driven pass content
        """
        cache = get_cache_manager()
        survey = cache.parse_survey_page(category)

        return survey.get("s3_need_driven") or "S3 Need-Driven pass not available for this survey"

    @mcp.resource("survey://{category}/s4-strategic")
    def get_survey_s4(category: str) -> str:
        """
        Get S4 (Strategic) pass for a survey.

        S4 provides maturity assessment and strategic analysis.

        Args:
            category: Survey category (e.g., "1.001-009")

        Returns:
            str: S4 Strategic pass content
        """
        cache = get_cache_manager()
        survey = cache.parse_survey_page(category)

        return survey.get("s4_strategic") or "S4 Strategic pass not available for this survey"
