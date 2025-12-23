#!/bin/bash
# Verification script for MAS email patch deployment
# Related: solutions-55jz, ADR-024

set -e

echo "🧪 MAS Patch Verification Script"
echo "================================"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test 1: OIDC Discovery
echo "Test 1: OIDC Discovery Endpoint"
echo "--------------------------------"
DISCOVERY=$(curl -s https://matrix.factumerit.app/.well-known/openid-configuration)
if echo "$DISCOVERY" | jq -e '.issuer' > /dev/null 2>&1; then
    echo -e "${GREEN}✅ PASS${NC} - OIDC discovery endpoint responding"
    echo "   Issuer: $(echo "$DISCOVERY" | jq -r '.issuer')"
    echo "   Userinfo: $(echo "$DISCOVERY" | jq -r '.userinfo_endpoint')"
else
    echo -e "${RED}❌ FAIL${NC} - OIDC discovery endpoint not responding"
    echo "   Response: $DISCOVERY"
    exit 1
fi
echo ""

# Test 2: MAS Health
echo "Test 2: MAS Service Health"
echo "--------------------------------"
if curl -s -f https://matrix.factumerit.app/ > /dev/null; then
    echo -e "${GREEN}✅ PASS${NC} - MAS service is responding"
else
    echo -e "${RED}❌ FAIL${NC} - MAS service not responding"
    exit 1
fi
echo ""

# Test 3: Userinfo Endpoint (requires token)
echo "Test 3: Userinfo Endpoint Structure"
echo "--------------------------------"
echo -e "${YELLOW}⚠️  MANUAL TEST REQUIRED${NC}"
echo ""
echo "To test email claims, you need an access token:"
echo ""
echo "1. Go to https://vikunja.factumerit.app"
echo "2. Click 'Login with Matrix' (or Authentik)"
echo "3. Complete OAuth flow"
echo "4. In browser DevTools Network tab, find the token exchange"
echo "5. Copy the access_token"
echo "6. Run:"
echo ""
echo "   curl -H \"Authorization: Bearer <TOKEN>\" \\"
echo "     https://matrix.factumerit.app/oauth2/userinfo"
echo ""
echo "Expected response:"
echo "   {"
echo "     \"sub\": \"...\","
echo "     \"username\": \"...\","
echo "     \"email\": \"user@example.com\","
echo "     \"email_verified\": true"
echo "   }"
echo ""
echo "If email field is present → ${GREEN}PATCH WORKS!${NC}"
echo "If email field is missing → ${RED}PATCH FAILED${NC}"
echo ""

# Test 4: Synapse Health
echo "Test 4: Synapse Health"
echo "--------------------------------"
SYNAPSE_HEALTH=$(curl -s https://matrix.factumerit.app/_health || echo "FAIL")
if [ "$SYNAPSE_HEALTH" = "OK" ]; then
    echo -e "${GREEN}✅ PASS${NC} - Synapse is healthy"
else
    echo -e "${RED}❌ FAIL${NC} - Synapse health check failed"
    echo "   Response: $SYNAPSE_HEALTH"
fi
echo ""

# Test 5: Vikunja Health
echo "Test 5: Vikunja Health"
echo "--------------------------------"
VIKUNJA_HEALTH=$(curl -s https://vikunja.factumerit.app/health || echo "FAIL")
if [ "$VIKUNJA_HEALTH" = "OK" ]; then
    echo -e "${GREEN}✅ PASS${NC} - Vikunja is healthy"
else
    echo -e "${RED}❌ FAIL${NC} - Vikunja health check failed"
    echo "   Response: $VIKUNJA_HEALTH"
fi
echo ""

# Summary
echo "================================"
echo "📊 Verification Summary"
echo "================================"
echo ""
echo "Automated tests: Check results above"
echo "Manual test required: Userinfo endpoint with real token"
echo ""
echo "Next steps:"
echo "1. Wait for MAS to fully start (if 502 errors)"
echo "2. Test Vikunja login flow end-to-end"
echo "3. Verify email is populated in Vikunja account"
echo "4. Update beads: solutions-fxwe, solutions-hfes"
echo "5. Update docs: analyses/synapse/03-DEPLOYMENT_LESSONS.md"
echo ""

