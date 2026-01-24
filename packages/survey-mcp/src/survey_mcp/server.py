"""
survey-mcp MCP Server

Exposes research.modelcitizendeveloper.com surveys as MCP resources and tools.
"""

from fastmcp import FastMCP
from survey_mcp.resources.surveys import register_survey_resources
from survey_mcp.tools.discovery import register_discovery_tools
from survey_mcp.tools.index import register_index_tools


# Create MCP server
mcp = FastMCP("survey")

# Register resources and tools
register_survey_resources(mcp)
register_discovery_tools(mcp)
register_index_tools(mcp)


def main():
    """Main entry point for MCP server."""
    import sys

    # Run MCP server
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
