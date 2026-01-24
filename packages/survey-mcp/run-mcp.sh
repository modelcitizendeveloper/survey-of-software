#!/bin/bash
# MCP Server launcher for survey-mcp
# This script is called by Claude Desktop via WSL

set -e

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Use the script's directory (survey-mcp package)
cd "$SCRIPT_DIR"

# Enable debug logging
export SURVEY_MCP_DEBUG=1

# Redirect stderr to log file (stdout is used for MCP protocol)
exec /home/ivanadamin/.local/bin/uv run python -m survey_mcp.server 2>> /tmp/survey-mcp.log
