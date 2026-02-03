#!/bin/bash
# Wrapper script for recipe-emb CLI using uv
# Usage: recipe-emb.sh <command> [args...]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"
uv run python -m recipe_emb.cli "$@"
