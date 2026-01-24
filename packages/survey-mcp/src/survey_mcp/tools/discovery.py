"""
Discovery Tools - Search and find surveys.
"""

from typing import List
from fastmcp import FastMCP
from survey_mcp.cache import get_cache_manager


def register_discovery_tools(mcp: FastMCP):
    """
    Register discovery tools with FastMCP.

    Tools:
    - search_surveys: Find surveys matching a query

    Args:
        mcp: FastMCP instance
    """

    @mcp.tool()
    def search_surveys(query: str, max_results: int = 10) -> List[dict]:
        """
        Search for surveys matching a query.

        Searches survey titles and categories for the query string.

        Args:
            query (str): Search query (e.g., "testing", "sorting", "machine learning")
            max_results (int): Maximum number of results to return. Default: 10

        Returns:
            List[dict]: List of matching surveys:
                [
                    {
                        "category": "1.001-009",
                        "title": "Sorting & Searching Algorithms",
                        "complete": 5,
                        "total": 9,
                        "resource_uri": "survey://1.001-009"
                    },
                    ...
                ]

        Example:
            >>> results = search_surveys("testing frameworks")
            >>> for survey in results:
            ...     print(f"{survey['category']}: {survey['title']}")
        """
        cache = get_cache_manager()
        index = cache.get_survey_index()

        # Simple text search
        query_lower = query.lower()
        results = []

        for category_info in index.get("categories", []):
            title = category_info.get("title", "")
            category = category_info.get("range", "")

            # Match query in title or category
            if query_lower in title.lower() or query_lower in category.lower():
                results.append(
                    {
                        "category": category,
                        "title": title,
                        "complete": category_info.get("complete", 0),
                        "total": category_info.get("total", 0),
                        "resource_uri": f"survey://{category}"
                    }
                )

                if len(results) >= max_results:
                    break

        return results
