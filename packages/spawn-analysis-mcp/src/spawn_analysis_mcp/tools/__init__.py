"""
spawn-analysis MCP Tools - Modular tool registration.

This package contains MCP tool wrappers organized by category.
Each module exports a register_*_tools() function that registers its tools
with the FastMCP instance.

Architecture:
- tools/discovery.py: Analyst discovery and recommendation tools
- tools/execution.py: Analysis execution and status tools
- tools/history.py: User-scoped analysis history tools
- tools/export.py: Export tools for various formats and destinations

To add new tool categories:
1. Create tools/category.py with register_category_tools(mcp)
2. Import and call in register_all_tools() below
"""

from fastmcp import FastMCP

# Import registration functions
from .discovery import register_discovery_tools
from .execution import register_execution_tools
from .export import register_export_tools
from .history import register_history_tools


def register_all_tools(mcp: FastMCP):
    """
    Register all MCP tools from all modules.

    This function is called by server.py during initialization.
    All tools must be registered BEFORE mcp.run() is called.

    Args:
        mcp: FastMCP instance to register tools with
    """
    # Phase 2.1: Core tools
    register_discovery_tools(mcp)
    register_execution_tools(mcp)
    register_export_tools(mcp)  # Basic markdown export

    # Phase 2.2: History & Privacy
    register_history_tools(mcp)


__all__ = [
    'register_all_tools',
    'register_discovery_tools',
    'register_execution_tools',
    'register_export_tools',
    'register_history_tools',
]
