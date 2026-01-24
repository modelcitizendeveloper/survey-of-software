#!/bin/bash
# MCP Server launcher for spawn-analysis
# This script is called by Claude Desktop via WSL

set -e

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Use the script's directory (spawn-analysis-mcp package)
cd "$SCRIPT_DIR"

# Enable debug logging
export SPAWN_ANALYSIS_DEBUG=1

# Redirect stderr to log file (stdout is used for MCP protocol)
exec /home/ivanadamin/.local/bin/uv run spawn-analysis-mcp 2>> /tmp/spawn-analysis-mcp.log
