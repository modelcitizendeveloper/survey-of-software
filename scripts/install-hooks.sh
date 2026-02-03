#!/bin/bash
# Install Git hooks for the project

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "Installing Git hooks..."

# Install pre-commit hook
if [ -f "$SCRIPT_DIR/pre-commit-hook.sh" ]; then
    cp "$SCRIPT_DIR/pre-commit-hook.sh" "$REPO_ROOT/.git/hooks/pre-commit"
    chmod +x "$REPO_ROOT/.git/hooks/pre-commit"
    echo "✅ Installed pre-commit hook"
else
    echo "❌ pre-commit-hook.sh not found"
    exit 1
fi

echo ""
echo "Git hooks installed successfully!"
echo ""
echo "The pre-commit hook will now:"
echo "  - Check for Storybook/incompatible imports"
echo "  - Validate research quality (60%+ required)"
echo "  - Check for broken relative links"
echo "  - Warn about large files"
echo "  - Validate Python syntax"
echo ""
echo "To bypass hooks (NOT recommended):"
echo "  git commit --no-verify"
