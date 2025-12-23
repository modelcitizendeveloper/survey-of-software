# Debug: Username Mapping Issue

**Date:** 2025-12-23  
**Issue:** Fresh user login shows wrong username "humbly-noted-amoeba" instead of "ivantohelpyou"

---

## 🐛 Observed Behavior

**Test scenario:**
1. Deleted Vikunja account
2. Deleted "ivantohelpyou" from Authentik
3. Started fresh login at vikunja.factumerit.app
4. Clicked "Log in with factumerit" → Authentik → Matrix login
5. **Result:** Username shows as "humbly-noted-amoeba" (not "ivantohelpyou")

**Hypothesis:** This might be:
- A Matrix room alias
- A session ID
- A device ID
- Wrong claim being mapped as username

---

## 🔍 What to Check

### 1. Check Authentik User Account

Go to https://auth.factumerit.app/if/admin/ → Directory → Users

**Look for the newly created user:**
- What is the username?
- What is the email?
- What are the attributes?

### 2. Check MAS Userinfo Response

The MAS userinfo endpoint should return:
```json
{
  "sub": "01234567890ABCDEF...",  // MAS internal user ID
  "username": "ivantohelpyou",    // Matrix localpart
  "email": "ivan@ivantohelpyou.com",
  "email_verified": true
}
```

**Question:** Is MAS returning the correct username?

### 3. Check Authentik OIDC Source Configuration

In Authentik admin:
- Go to Directory → Federation & Social Login → Sources
- Find the MAS/Matrix source
- Check the **User Matching Mode**
- Check the **User Path Template**

**Possible issue:** Authentik might be using the wrong claim for username

### 4. Check Authentik Property Mappings

In Authentik admin:
- Go to Customization → Property Mappings
- Find the mappings used by the MAS source
- Check what claim is mapped to "username"

**Expected:** Should map `username` claim to username
**Actual:** Might be mapping `sub` or some other field

---

## 🔧 Likely Root Cause

**Theory:** Authentik is using the `sub` claim (MAS internal user ID) as the username instead of the `username` claim.

The `sub` claim in MAS is a ULID (Universally Unique Lexicographically Sortable Identifier) that looks like: `01KD69CRAGG7MT9TY08PZ1GYHB`

But "humbly-noted-amoeba" doesn't look like a ULID... 🤔

**Alternative theory:** Authentik is generating a random username because it can't find the username claim.

---

## 🔍 Debug Steps

### Step 1: Check MAS Logs

Look for userinfo endpoint calls in MAS logs:

```bash
# Check recent MAS logs
# Look for lines containing "userinfo" or "oauth2"
```

Expected to see:
```
INFO mas_handlers::oauth2::userinfo - Returning userinfo for user: ivantohelpyou
```

### Step 2: Inspect OAuth Flow in Browser

1. Open browser dev tools (F12)
2. Go to Network tab
3. Do the login flow again
4. Look for request to `/oauth2/userinfo`
5. Check the response body

**What to look for:**
- Is `username` field present?
- What value does it have?
- Is `email` field present?

### Step 3: Check Authentik Logs

In Authentik admin:
- Go to Events → Logs
- Filter for recent authentication events
- Look for the OAuth flow
- Check what claims Authentik received from MAS

---

## 🎯 Possible Fixes

### Fix 1: Update Authentik Property Mappings

If Authentik is using the wrong claim for username:

1. Go to Customization → Property Mappings
2. Find/create a mapping for username:
   ```python
   return request.context.get('username', request.context.get('preferred_username', ''))
   ```

### Fix 2: Update Authentik Source Configuration

If the source is configured incorrectly:

1. Go to Directory → Federation & Social Login → Sources
2. Edit the MAS source
3. Check "User Matching Mode" - should be "Link to a user with identical username"
4. Check "User Path Template" - should use the username claim

### Fix 3: Check MAS Client Configuration

In MAS config (`mas.yaml`), check the Authentik client configuration:

```yaml
clients:
  - client_id: "000000000000000000ATHNTK00"
    client_auth_method: client_secret_basic
    client_secret: "..."
    redirect_uris:
      - "https://auth.factumerit.app/source/oauth/callback/matrix/"
```

Make sure the redirect URI matches exactly.

---

## 📊 Expected Flow

```
1. User clicks "Login with Matrix" in Vikunja
   ↓
2. Vikunja redirects to Authentik
   ↓
3. Authentik redirects to MAS with scope=openid email profile
   ↓
4. User logs in with Matrix credentials
   ↓
5. MAS returns authorization code
   ↓
6. Authentik exchanges code for access token
   ↓
7. Authentik calls MAS /oauth2/userinfo with access token
   ↓
8. MAS returns:
   {
     "sub": "01KD69...",
     "username": "ivantohelpyou",  ← This should be used\!
     "email": "ivan@...",
     "email_verified": true
   }
   ↓
9. Authentik creates/updates user with username="ivantohelpyou"
   ↓
10. Authentik redirects to Vikunja with user info
    ↓
11. Vikunja creates user with username="ivantohelpyou"
```

**Where it's breaking:** Step 9 - Authentik is using wrong value for username

---

## 🔍 Quick Test

To quickly check what MAS is returning, you can:

1. Login to get an access token (extract from browser dev tools)
2. Test the userinfo endpoint:

```bash
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  https://matrix.factumerit.app/oauth2/userinfo
```

Expected response should include `"username": "ivantohelpyou"`

---

## 📝 Investigation Results

**MAS userinfo response:**
```
(paste response here)
```

**Authentik user attributes:**
```
(paste attributes here)
```

**Authentik property mappings:**
```
(list mappings here)
```

---

**Status:** Investigating username mapping issue
