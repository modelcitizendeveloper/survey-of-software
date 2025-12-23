# Test Plan: Fresh User Email Population

**Date:** 2025-12-23  
**Goal:** Verify that a brand new user gets their email populated from MAS via Authentik to Vikunja

---

## 🎯 Test Scenario

**What we're testing:** When a user who has never logged into Vikunja before authenticates via Matrix (through Authentik), does their email get populated correctly?

**Why this matters:** This is the core bug we patched - MAS wasn't returning email claims from the userinfo endpoint.

---

## 📋 Test Steps

### Preparation
1. **Choose a test user** (or create a new Matrix account)
   - Matrix ID: `@testuser:matrix.factumerit.app` (example)
   - Email: Should be registered in MAS/Synapse

2. **Clean slate in Authentik**
   - Go to https://auth.factumerit.app/if/admin/
   - Navigate to Directory → Users
   - Find and delete the test user (if exists)

3. **Clean slate in Vikunja**
   - Go to https://vikunja.factumerit.app
   - Login as admin
   - Navigate to Users
   - Find and delete the test user (if exists)

### Test Execution

4. **Logout from all services**
   - Logout from Vikunja
   - Logout from Authentik
   - Clear browser cookies (or use incognito mode)

5. **Initiate fresh login**
   - Go to https://vikunja.factumerit.app
   - Click "Login with Matrix" (or whatever the OIDC button says)

6. **OAuth Flow**
   - Should redirect to Authentik
   - Authentik should redirect to MAS
   - Login with Matrix credentials
   - MAS should ask for consent (first time)
   - Grant consent (including email scope)

7. **Observe the flow**
   - Authentik should receive userinfo from MAS (including email)
   - Authentik should create user account
   - Authentik should pass user info to Vikunja
   - Vikunja should create user account

### Verification

8. **Check Vikunja user**
   - After successful login, go to Vikunja settings/profile
   - **CRITICAL CHECK:** Is the email field populated?
   - Expected: Email should match the Matrix account email

9. **Check Authentik user**
   - Go to https://auth.factumerit.app/if/admin/
   - Navigate to Directory → Users
   - Find the test user
   - **CHECK:** Is the email field populated?

10. **Check MAS logs** (if needed)
    - SSH into Render or check logs
    - Look for userinfo endpoint calls
    - Verify email is being returned in the response

---

## ✅ Success Criteria

- [ ] User can login successfully
- [ ] Email is populated in Vikunja user profile
- [ ] Email is populated in Authentik user account
- [ ] Email matches the Matrix account email
- [ ] No errors in the OAuth flow

---

## ❌ Failure Scenarios

### If email is NOT populated in Vikunja:

**Possible causes:**
1. **MAS patch not working** - userinfo endpoint not returning email
2. **Authentik not requesting email scope** - check Authentik OIDC config
3. **Authentik not mapping email** - check Authentik property mappings
4. **Vikunja not accepting email** - check Vikunja OIDC config

**Debug steps:**
1. Check MAS logs for userinfo endpoint calls
2. Check Authentik logs for OIDC flow
3. Use browser dev tools to inspect OAuth tokens/responses
4. Verify email scope is being requested and granted

### If email is populated in Authentik but NOT in Vikunja:

**Cause:** Authentik → Vikunja mapping issue

**Fix:** Check Vikunja OIDC configuration:
- Ensure email claim mapping is correct
- Verify Authentik is passing email in the token/userinfo

---

## 🔍 How to Check MAS Userinfo Response

If you need to debug, you can manually test the MAS userinfo endpoint:

```bash
# 1. Get an access token (you'll need to extract this from the OAuth flow)
# Use browser dev tools → Network tab → Look for token exchange

# 2. Test userinfo endpoint
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  https://matrix.factumerit.app/oauth2/userinfo

# Expected response:
{
  "sub": "...",
  "username": "testuser",
  "email": "testuser@example.com",      # ← Should be present\!
  "email_verified": true                 # ← Should be present\!
}
```

---

## 📊 Current Architecture

```
User Browser
    ↓
Vikunja (OIDC Client)
    ↓
Authentik (OIDC Provider / Bridge)
    ↓
MAS (OIDC Provider - PATCHED)
    ↓
Synapse (Matrix Homeserver)
```

**The patch:** MAS now returns `email` and `email_verified` in userinfo response when email scope is granted.

---

## 🎯 Next Steps After Testing

### If test PASSES ✅
1. Update bead `solutions-fxwe` to COMPLETE
2. Document the successful test
3. Consider testing direct Vikunja → MAS (skip Authentik)
4. Potentially save $25/mo by removing Authentik

### If test FAILS ❌
1. Debug using the steps above
2. Check if the patch is actually being applied
3. Verify MAS configuration
4. Check Authentik/Vikunja OIDC configs

---

## 📝 Test Results

**Date:**  
**Tester:**  
**Result:** [ ] PASS / [ ] FAIL

**Notes:**

**Email populated in Vikunja:** [ ] YES / [ ] NO  
**Email populated in Authentik:** [ ] YES / [ ] NO  
**Email value:**  
**Any errors:**  

---

**Status:** Ready for testing
