# Fix: Authentik Username Mapping

**Date:** 2025-12-23  
**Issue:** Authentik creates users with random username instead of Matrix username  
**Status:** ✅ Email patch WORKING\! Email is populated correctly.

---

## ✅ Confirmed Working

- **Email patch:** WORKING\! Email is populated in Authentik user account
- **OAuth flow:** WORKING\! User can login successfully
- **Issue:** Username is "humbly-noted-amoeba" instead of "ivantohelpyou"

---

## 🔧 Fix: Update Authentik Property Mappings

Authentik needs to be configured to use the `username` claim from MAS userinfo response.

### Step 1: Check Current Property Mappings

1. Go to https://auth.factumerit.app/if/admin/
2. Navigate to **Customization → Property Mappings**
3. Look for mappings related to the Matrix/MAS source
4. Check if there's a mapping for "username" or "preferred_username"

### Step 2: Check the MAS Source Configuration

1. Go to **Directory → Federation & Social Login → Sources**
2. Find the Matrix/MAS source (should be named something like "Matrix" or "MAS")
3. Click **Edit**
4. Check the following settings:

**User Matching Mode:**
- Should be: "Link to a user with identical username" or "Link to a user with identical email address"

**User Path Template:**
- Default is usually: `goauthentik.io/sources/%(slug)s`
- This is fine

**Property Mappings:**
- Check which property mappings are selected
- Make sure there's a mapping for username

### Step 3: Create/Update Username Property Mapping

If there's no proper username mapping:

1. Go to **Customization → Property Mappings**
2. Click **Create**
3. Select **Scope Mapping** (for OAuth/OIDC)
4. Fill in:
   - **Name:** `MAS Username Mapping`
   - **Scope name:** `profile`
   - **Expression:**
     ```python
     return {
         "username": request.context.get("username", request.context.get("preferred_username", "")),
         "name": request.context.get("name", request.context.get("username", "")),
     }
     ```
5. Save

### Step 4: Update the MAS Source to Use the Mapping

1. Go back to **Directory → Federation & Social Login → Sources**
2. Edit the Matrix/MAS source
3. In the **Property Mappings** section, make sure your new mapping is selected
4. Save

---

## 🎯 Alternative: Update User Path Template

Another approach is to use a custom User Path Template that uses the username claim:

1. Edit the MAS source
2. Find **User Path Template**
3. Change to: `goauthentik.io/sources/%(slug)s/%(username)s`

This will use the `username` claim from the userinfo response.

---

## 🔍 What MAS is Returning

Based on our patch, MAS userinfo endpoint returns:

```json
{
  "sub": "01KD69CRAGG7MT9TY08PZ1GYHB",
  "username": "ivantohelpyou",
  "email": "ivan@ivantohelpyou.com",
  "email_verified": true
}
```

Authentik should be using the `username` field, but it's currently either:
- Not finding it
- Using a different field
- Generating a random username

---

## 📊 Expected vs Actual

| Field | MAS Returns | Authentik Should Use | Authentik Actually Uses |
|-------|-------------|---------------------|------------------------|
| Email | ✅ ivan@... | ✅ ivan@... | ✅ ivan@... |
| Username | ✅ ivantohelpyou | ✅ ivantohelpyou | ❌ humbly-noted-amoeba |

---

## 🧪 Test After Fix

1. Delete the "humbly-noted-amoeba" user from Authentik
2. Delete the user from Vikunja
3. Do a fresh login
4. Check:
   - ✅ Email is populated (should still work)
   - ✅ Username is "ivantohelpyou" (should be fixed)

---

## 📝 Notes

- The email patch is confirmed working\! ✅
- This is purely an Authentik configuration issue
- Once fixed, usernames will be correct
- Existing users with wrong usernames may need to be recreated

---

**Next Step:** Check Authentik property mappings and source configuration
