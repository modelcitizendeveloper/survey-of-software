#!/bin/bash
# Pre-commit hook to prevent build-breaking changes
# Install: cp scripts/pre-commit-hook.sh .git/hooks/pre-commit && chmod +x .git/hooks/pre-commit

set -e

echo "🔍 Running pre-commit validation..."

# Track if we found any issues
ISSUES=0

# 1. Check for problematic MDX imports in docs
echo "  → Checking for Storybook/incompatible imports..."
if git diff --cached --name-only | grep -q "^docs/survey/.*\.md$"; then
    # Check staged files only
    for file in $(git diff --cached --name-only | grep "^docs/survey/.*\.md$"); do
        if [ -f "$file" ]; then
            # Look for imports outside of code blocks (simplified check)
            if grep -n "^import.*from '@storybook" "$file" 2>/dev/null; then
                echo "    ❌ Found Storybook import in $file"
                echo "       These break Docusaurus builds. Wrap in code blocks or comment out."
                ISSUES=$((ISSUES + 1))
            fi
            if grep -n "^import.*Canvas\|^import.*Meta\|^import.*Story" "$file" 2>/dev/null | grep -v "^import Tabs\|^import TabItem"; then
                echo "    ⚠️  Found potentially problematic import in $file"
                echo "       Verify this is in a code block or properly escaped."
            fi
        fi
    done
fi

# 2. Check for broken internal links
echo "  → Checking for broken relative links..."
if git diff --cached --name-only | grep -q "^docs/.*\.md$"; then
    for file in $(git diff --cached --name-only | grep "^docs/.*\.md$"); do
        if [ -f "$file" ]; then
            # Check for links to non-existent local files
            while IFS= read -r link; do
                # Extract relative path from markdown link
                if [[ $link =~ \[.*\]\((.*\.md)\) ]]; then
                    target="${BASH_REMATCH[1]}"
                    # Skip absolute URLs
                    if [[ ! $target =~ ^https?:// ]]; then
                        dir=$(dirname "$file")
                        target_path="$dir/$target"
                        if [ ! -f "$target_path" ]; then
                            echo "    ⚠️  Broken link in $file: $target"
                            echo "       Target file doesn't exist: $target_path"
                        fi
                    fi
                fi
            done < <(grep -o '\[.*\](.*\.md)' "$file" 2>/dev/null || true)
        fi
    done
fi

# 3. Validate research pieces being committed
echo "  → Validating research quality..."
if git diff --cached --name-only | grep -q "^packages/research/"; then
    # Extract research codes from staged files
    research_codes=$(git diff --cached --name-only | grep "^packages/research/" | cut -d'/' -f3 | cut -d'-' -f1 | sort -u)

    for code in $research_codes; do
        if [ -d "packages/research" ]; then
            # Run validation if the script exists
            if [ -f "scripts/validate_research.py" ]; then
                score=$(python3 scripts/validate_research.py "$code" 2>/dev/null | grep "Overall Score" | grep -oP '\d+(?=%)' || echo "0")
                if [ "$score" -lt 60 ]; then
                    echo "    ❌ Research $code scored ${score}% (minimum: 60%)"
                    echo "       Run: python3 scripts/validate_research.py $code"
                    ISSUES=$((ISSUES + 1))
                elif [ "$score" -lt 75 ]; then
                    echo "    ⚠️  Research $code scored ${score}% (recommended: 75%+)"
                else
                    echo "    ✅ Research $code scored ${score}%"
                fi
            fi
        fi
    done
fi

# 4. Check for large files
echo "  → Checking for large files..."
for file in $(git diff --cached --name-only); do
    if [ -f "$file" ]; then
        size=$(stat -f%z "$file" 2>/dev/null || stat -c%s "$file" 2>/dev/null)
        # Warn if file > 1MB
        if [ "$size" -gt 1048576 ]; then
            size_mb=$((size / 1048576))
            echo "    ⚠️  Large file: $file (${size_mb}MB)"
            echo "       Consider adding to .gitignore or using Git LFS"
        fi
    fi
done

# 5. Check for common typos in commit message
echo "  → Checking commit message..."
commit_msg=$(git log -1 --pretty=%B 2>/dev/null || echo "")
if [ -n "$commit_msg" ]; then
    # Check for WIP commits
    if echo "$commit_msg" | grep -iq "wip\|todo\|fixme\|xxx"; then
        echo "    ⚠️  Commit message contains WIP/TODO markers"
        echo "       Message: $commit_msg"
    fi
fi

# 6. Run quick syntax check on modified Python files
echo "  → Checking Python syntax..."
for file in $(git diff --cached --name-only | grep "\.py$"); do
    if [ -f "$file" ]; then
        if ! python3 -m py_compile "$file" 2>/dev/null; then
            echo "    ❌ Python syntax error in $file"
            ISSUES=$((ISSUES + 1))
        fi
    fi
done

# Summary
echo ""
if [ $ISSUES -eq 0 ]; then
    echo "✅ All checks passed!"
    exit 0
else
    echo "❌ Found $ISSUES issue(s) that need to be fixed before committing."
    echo ""
    echo "To bypass these checks (NOT recommended):"
    echo "  git commit --no-verify"
    exit 1
fi
