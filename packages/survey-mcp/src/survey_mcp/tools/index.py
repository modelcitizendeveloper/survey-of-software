"""
Index Tools - Get survey catalog and organization.
"""

from fastmcp import FastMCP
from survey_mcp.cache import get_cache_manager


def register_index_tools(mcp: FastMCP):
    """
    Register index tools with FastMCP.

    Tools:
    - get_survey_index: Get complete survey catalog

    Args:
        mcp: FastMCP instance
    """

    @mcp.tool()
    def get_survey_index() -> dict:
        """
        Get the complete survey index.

        Returns the full catalog of all 169 survey slots with completion status.

        Returns:
            dict: {
                "total_slots": int,
                "completed": int,
                "categories": [
                    {
                        "range": "1.001-009",
                        "title": "Sorting & Searching Algorithms",
                        "complete": 5,
                        "total": 9,
                        "resource_uri": "survey://1.001-009"
                    },
                    ...
                ]
            }

        Example:
            >>> index = get_survey_index()
            >>> print(f"Total surveys: {index['total_slots']}")
            >>> print(f"Completed: {index['completed']}")
            >>> for category in index['categories']:
            ...     print(f"{category['range']}: {category['title']} ({category['complete']}/{category['total']})")
        """
        cache = get_cache_manager()
        index = cache.get_survey_index()

        # Calculate totals
        categories = index.get("categories", [])
        total_slots = sum(cat.get("total", 0) for cat in categories)
        completed = sum(cat.get("complete", 0) for cat in categories)

        # Add resource URIs
        for cat in categories:
            cat["resource_uri"] = f"survey://{cat.get('range', '')}"

        return {
            "total_slots": total_slots,
            "completed": completed,
            "categories": categories
        }

    @mcp.tool()
    def get_category_tree() -> dict:
        """
        Get survey categories organized by technology domain.

        Returns hierarchical organization of survey categories.

        Returns:
            dict: {
                "Algorithms": {
                    "Sorting & Searching": "1.001-009",
                    "Graph & Network": "1.010-019",
                    ...
                },
                "Data Processing": {
                    ...
                },
                ...
            }

        Example:
            >>> tree = get_category_tree()
            >>> for domain, categories in tree.items():
            ...     print(f"{domain}:")
            ...     for title, category_id in categories.items():
            ...         print(f"  - {title}: {category_id}")
        """
        cache = get_cache_manager()
        index = cache.get_survey_index()

        # Group by domain
        # This is a simplified version - real implementation would parse actual domains
        tree = {}

        for cat in index.get("categories", []):
            # Extract domain from title (simplified)
            title = cat.get("title", "")
            range_id = cat.get("range", "")

            # For now, group by first number range
            # 1.001-009 = Algorithms, etc.
            # Real implementation would parse from site structure
            if "Algorithm" in title:
                domain = "Algorithms"
            elif "Machine Learning" in title or "LLM" in title:
                domain = "AI & ML"
            elif "Text" in title or "Document" in title:
                domain = "Text Processing"
            elif "Data Structure" in title:
                domain = "Data Structures"
            else:
                domain = "Other"

            if domain not in tree:
                tree[domain] = {}

            tree[domain][title] = range_id

        return tree
