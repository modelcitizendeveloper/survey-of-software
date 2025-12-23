#\!/bin/bash
# Quick script to check MAS build and deployment status

# Requires RENDER_API_KEY to be set in environment
if [ -z "$RENDER_API_KEY" ]; then
    echo "❌ Error: RENDER_API_KEY environment variable not set"
    echo "Please set it in your ~/.bashrc or run:"
    echo "  export RENDER_API_KEY='your_key_here'"
    exit 1
fi

echo "🔍 MAS BUILD & DEPLOYMENT STATUS"
echo "================================="
echo ""

# Get latest deploy
echo "Latest Deploy:"
curl -s -H "Authorization: Bearer $RENDER_API_KEY" \
  -H "Accept: application/json" \
  https://api.render.com/v1/services/srv-d54s143e5dus73bqhpb0/deploys?limit=1 | \
  jq -r '.[] | .deploy | "  Status: \(.status)\n  Commit: \(.commit.id[0:7]) - \(.commit.message[0:60])\n  Started: \(.createdAt)\n  Updated: \(.updatedAt)"'

echo ""
echo "---"
echo ""

# Test endpoints
echo "Endpoint Tests:"
echo -n "  /health: "
curl -s https://matrix.factumerit.app/health || echo "FAILED"

echo ""
echo -n "  OIDC Discovery: "
if curl -s https://matrix.factumerit.app/.well-known/openid-configuration | jq -e '.issuer' > /dev/null 2>&1; then
    echo "✅ WORKING\!"
else
    echo "❌ 502 (MAS not responding)"
fi

echo ""
