#!/bin/bash
# Validate research before committing
# Usage: ./scripts/validate-and-commit.sh 1.007 "commit message"

set -e

if [ $# -lt 2 ]; then
    echo "Usage: $0 <research-code> <commit-message>"
    echo "Example: $0 1.007 'Complete Pattern Matching research'"
    exit 1
fi

RESEARCH_CODE="$1"
COMMIT_MSG="$2"

echo "🔍 Validating research $RESEARCH_CODE..."
python3 scripts/validate_research.py "$RESEARCH_CODE"

# Extract score
SCORE=$(python3 scripts/validate_research.py "$RESEARCH_CODE" 2>/dev/null | grep "Overall Score" | grep -oP '\d+(?=%)' || echo "0")

if [ "$SCORE" -lt 75 ]; then
    echo ""
    echo "❌ Research validation failed: ${SCORE}% (minimum: 75%)"
    echo ""
    echo "Cannot commit incomplete research. Please fix issues and try again."
    exit 1
fi

if [ "$SCORE" -lt 90 ]; then
    echo ""
    echo "⚠️  Research scored ${SCORE}% (target: 90%+)"
    read -p "Commit anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Commit cancelled"
        exit 1
    fi
fi

echo ""
echo "✅ Validation passed: ${SCORE}%"
echo ""
echo "📝 Committing research..."

git add packages/research/"$RESEARCH_CODE"-*/
git commit -m "$COMMIT_MSG"

echo ""
echo "✓ Research committed successfully!"
echo ""
echo "Next steps:"
echo "  1. Push: git push"
echo "  2. Convert: python3 scripts/convert_research.py"
echo "  3. Integrate: python3 scripts/integrate_research.py"
