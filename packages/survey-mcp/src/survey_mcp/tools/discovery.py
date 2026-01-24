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

    @mcp.tool()
    def get_survey(survey_id: str, section: str = "summary") -> dict:
        """
        Fetch a specific survey by ID.

        Retrieves survey content. Use 'summary' for metadata only,
        or specify a section (s1, s2, s3, s4) to get that pass's content.

        Args:
            survey_id (str): Survey ID (e.g., "1-002", "1.002", "2-015")
                            Accepts both dot and dash formats
            section (str): Which content to return:
                          - "summary": Just title and metadata (default)
                          - "s1": S1 Rapid pass content only
                          - "s2": S2 Comprehensive pass content only
                          - "s3": S3 Need-Driven pass content only
                          - "s4": S4 Strategic pass content only
                          - "full": All content (may be very large)

        Returns:
            dict: Survey data based on section parameter

        Examples:
            >>> survey = get_survey("1-002")  # Summary only
            >>> print(survey["title"])
            "1.002 Fuzzy Search"

            >>> s1 = get_survey("1-002", section="s1")  # Just S1 content
            >>> print(s1["s1_rapid"][:100])
        """
        cache = get_cache_manager()
        full_survey = cache.parse_survey_page(survey_id)

        if section == "summary":
            # Return metadata only, no HTML content
            return {
                "category": full_survey["category"],
                "title": full_survey["title"],
                "has_s1": full_survey["s1_rapid"] is not None,
                "has_s2": full_survey["s2_comprehensive"] is not None,
                "has_s3": full_survey["s3_need_driven"] is not None,
                "has_s4": full_survey["s4_strategic"] is not None,
            }
        elif section == "s1":
            return {
                "category": full_survey["category"],
                "title": full_survey["title"],
                "s1_rapid": full_survey["s1_rapid"]
            }
        elif section == "s2":
            return {
                "category": full_survey["category"],
                "title": full_survey["title"],
                "s2_comprehensive": full_survey["s2_comprehensive"]
            }
        elif section == "s3":
            return {
                "category": full_survey["category"],
                "title": full_survey["title"],
                "s3_need_driven": full_survey["s3_need_driven"]
            }
        elif section == "s4":
            return {
                "category": full_survey["category"],
                "title": full_survey["title"],
                "s4_strategic": full_survey["s4_strategic"]
            }
        else:  # "full" or unknown
            return full_survey
