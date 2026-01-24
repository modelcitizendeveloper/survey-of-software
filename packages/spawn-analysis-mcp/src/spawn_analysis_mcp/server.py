"""
spawn-analysis MCP Server

MCP server for decision analysis capability.
Provides tools for:
- Analyst discovery (list_analysts, describe_analyst, suggest_analysts)
- Analysis execution (conduct_analysis, get_analysis_status)
- History management (list_analyses, get_analysis) - user-scoped
- Export (save_analysis, export_to_vikunja_task, export_to_qrcards)

This server uses a modular architecture following the qrcards-mcp pattern.
"""

import logging
import os

from fastmcp import FastMCP

# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================

logger = logging.getLogger("spawn-analysis-mcp")
logger.setLevel(logging.DEBUG if os.environ.get("SPAWN_DEBUG") else logging.INFO)

if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    ))
    logger.addHandler(handler)


# ============================================================================
# FASTMCP INITIALIZATION
# ============================================================================

mcp = FastMCP(
    "spawn-analysis",
    instructions=(
        "Decision analysis using spawn-analysis framework with Vikunja integration. "
        "Conduct multi-perspective analysis with Bayesian confidence tracking."
    )
)


# ============================================================================
# TOOL REGISTRATION
# ============================================================================
# All tools are registered via the modular tools/ package.
# This keeps server.py clean and makes it easy to add new tool categories.
#
# To add new tools:
# 1. Create tools/category.py with register_category_tools(mcp)
# 2. Import and call in tools/__init__.py register_all_tools()

from spawn_analysis_mcp.tools import register_all_tools

register_all_tools(mcp)


# ============================================================================
# SERVER ENTRY POINT
# ============================================================================

def main():
    """Main entry point for spawn-analysis-mcp server."""
    import argparse

    parser = argparse.ArgumentParser(description="spawn-analysis MCP Server")
    parser.add_argument("--transport", choices=["stdio", "sse", "http"],
                        default="stdio",
                        help="Transport mode (default: stdio for Claude Desktop)")
    parser.add_argument("--port", type=int, default=8000,
                        help="Port for SSE/HTTP transport (default: 8000)")
    parser.add_argument("--host", default="0.0.0.0",
                        help="Host for SSE/HTTP transport (default: 0.0.0.0)")
    args = parser.parse_args()

    logger.info(f"Starting spawn-analysis MCP server (transport: {args.transport})")

    if args.transport in ("sse", "http"):
        # SSE/HTTP mode for remote deployment
        import uvicorn
        app = mcp.http_app(transport=args.transport)
        logger.info(f"Starting {args.transport.upper()} server on {args.host}:{args.port}")
        uvicorn.run(app, host=args.host, port=args.port)
    else:
        # STDIO mode for local Claude Desktop
        logger.info("Starting STDIO server for Claude Desktop")
        mcp.run(show_banner=False)


if __name__ == "__main__":
    main()
