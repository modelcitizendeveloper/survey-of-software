# Vikunja → MAS Login Lifecycle Documentation

**Architecture:** Vikunja → MAS → Synapse (Direct OIDC, bypassing Authentik)

**Date:** 2025-12-23

---

## Overview

This document describes the complete OAuth 2.0 / OpenID Connect login flow from Vikunja through Matrix Authentication Service (MAS) to Synapse, including all the moving parts and common failure points.

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         User's Browser                          │
└─────────────────────────────────────────────────────────────────┘
         │                    │                    │
         │ (1) Click Login    │ (4) Authorize      │ (7) Callback
         │                    │                    │
         ▼                    ▼                    ▼
┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│   Vikunja    │◄────►│     MAS      │◄────►│   Synapse    │
│ (Task Mgmt)  │      │ (OIDC IdP)   │      │ (Matrix HS)  │
└──────────────┘      └──────────────┘      └──────────────┘
  Port: 3456           Port: 8080           Port: 8008
  
  Config:              Config:              Config:
  - authurl            - clients[]          - mas integration
  - clientid           - policy             - userinfo patch
  - clientsecret       - redirect_uris      
  - scope              - admin_clients      
```

---

## Step-by-Step Login Flow

### Step 1: User Clicks "Login with Factumerit"

**Location:** `https://vikunja.factumerit.app/login`

**What happens:**
1. Vikunja frontend displays login page
2. Calls `/api/v1/info` to get available auth providers
3. Shows "Login with Factumerit" button if provider is configured

**Config involved:**
```yaml
# vikunja-factumerit/config.yml
auth:
  openid:
    enabled: true
    providers:
      - name: Factumerit
        authurl: https://matrix.factumerit.app/
```

**Common failures:**
- ❌ **Empty providers array** → Check if config.yml is being processed by envsubst
- ❌ **No login button** → Check `/api/v1/info` response
- ❌ **Provider not showing** → Check Vikunja logs for OIDC discovery errors

**Debug commands:**
```bash
# Check if provider is configured
curl -s https://vikunja.factumerit.app/api/v1/info | jq '.auth.openid_connect.providers'

# Should return:
# [{"name": "Factumerit", "key": "factumerit", "auth_url": "...", ...}]
```

---

### Step 2: OIDC Discovery

**What happens:**
1. Vikunja appends `/.well-known/openid-configuration` to `authurl`
2. Fetches OIDC metadata from MAS
3. Discovers authorization, token, and userinfo endpoints

**URL called:**
```
GET https://matrix.factumerit.app/.well-known/openid-configuration
```

**Response from MAS:**
```json
{
  "issuer": "https://matrix.factumerit.app/",
  "authorization_endpoint": "https://matrix.factumerit.app/authorize",
  "token_endpoint": "https://matrix.factumerit.app/oauth2/token",
  "userinfo_endpoint": "https://matrix.factumerit.app/oauth2/userinfo",
  ...
}
```

**Common failures:**
- ❌ **404 Not Found** → `authurl` is wrong (e.g., includes `/authorize`)
- ❌ **Issuer mismatch** → Trailing slash mismatch between `authurl` and MAS issuer
- ❌ **Connection refused** → MAS is down or DNS not resolving

**Correct config:**
```yaml
# authurl must match the issuer exactly (including trailing slash)
authurl: https://matrix.factumerit.app/  # ← Note the trailing slash!
```

**Debug commands:**
```bash
# Test OIDC discovery manually
curl -s https://matrix.factumerit.app/.well-known/openid-configuration | jq .

# Check issuer matches authurl
curl -s https://matrix.factumerit.app/.well-known/openid-configuration | jq -r '.issuer'
# Should return: https://matrix.factumerit.app/
```

---

### Step 3: Authorization Request

**What happens:**
1. User clicks login button
2. Vikunja redirects browser to MAS authorization endpoint
3. Browser navigates to MAS with OAuth parameters

**Redirect URL:**
```
https://matrix.factumerit.app/authorize?
  client_id=0000000000000000000V1KYNJA&
  redirect_uri=https://vikunja.factumerit.app/auth/openid/factumerit&
  response_type=code&
  scope=openid%20email%20profile&
  state=<random_state>
```

**Parameters:**
- `client_id`: Vikunja's client ID in MAS config
- `redirect_uri`: Where MAS sends user after auth (must match MAS config exactly)
- `response_type`: Always `code` for authorization code flow
- `scope`: Requested claims (`openid email profile`)
- `state`: CSRF protection token

**Common failures:**
- ❌ **Invalid redirect_uri** → Mismatch between Vikunja and MAS config
- ❌ **Unknown client** → Client ID not in MAS config
- ❌ **Invalid scope** → Requested scope not allowed

**MAS config:**
```yaml
# factumerit-matrix/mas/mas.template.yaml
clients:
  - client_id: 0000000000000000000V1KYNJA
    client_name: Vikunja
    client_secret: ${VIKUNJA_OIDC_SECRET}
    redirect_uris:
      - https://vikunja.factumerit.app/auth/openid/factumerit  # ← Must match exactly!
```

**Debug:**
```bash
# Check what redirect_uri Vikunja is sending
# Look in browser network tab for the /authorize request

# Verify MAS config has matching redirect_uri
cd ~/factumerit-matrix
grep -A10 "0000000000000000000V1KYNJA" mas/mas.template.yaml
```

---

### Step 4: User Authentication (Matrix Login)

**What happens:**
1. MAS checks if user is already logged in
2. If not, shows Matrix login form
3. User enters Matrix credentials
4. MAS validates against Synapse

**Login form:** `https://matrix.factumerit.app/login`

**MAS → Synapse communication:**
```
POST https://synapse.factumerit.app/_matrix/client/v3/login
{
  "type": "m.login.password",
  "identifier": {"type": "m.id.user", "user": "ivantohelpyou"},
  "password": "..."
}
```

**Common failures:**
- ❌ **Invalid credentials** → Wrong username/password
- ❌ **Synapse unreachable** → MAS can't connect to Synapse
- ❌ **Account locked** → Too many failed attempts

**Debug:**
```bash
# Check Synapse logs for login attempts
# Check MAS logs for Synapse connection errors
```

---

### Step 5: Policy Check & Consent

**What happens:**
1. MAS checks policy to see if client is allowed
2. If client is in `admin_clients`, shows consent screen
3. User reviews requested scopes and grants/denies consent

**Policy check:**
```yaml
# factumerit-matrix/mas/mas.template.yaml
policy:
  wasm_module: /usr/local/share/mas-cli/policy.wasm
  data:
    admin_clients:
      - "000000000000000000ATHNTK00"  # Authentik
      - "0000000000000000000V1KYNJA"  # Vikunja ← Must be here!
```

**Consent screen shows:**
- Client name: "Vikunja"
- Requested scopes: openid, email, profile
- User's email (from MAS userinfo patch)

**Common failures:**
- ❌ **Authorization denied by policy** → Client not in `admin_clients` list
- ❌ **Email not showing** → MAS userinfo patch not working
- ❌ **User denies consent** → User clicks "Deny" instead of "Allow"

**Debug:**
```bash
# Check if Vikunja is in admin_clients
cd ~/factumerit-matrix
grep -A5 "admin_clients:" mas/mas.template.yaml

# Should show both Authentik and Vikunja client IDs
```

---

### Step 6: Authorization Code Grant

**What happens:**
1. User clicks "Allow" on consent screen
2. MAS generates authorization code
3. MAS redirects browser back to Vikunja with code

**Redirect URL:**
```
https://vikunja.factumerit.app/auth/openid/factumerit?
  code=<authorization_code>&
  state=<original_state>
```

**Common failures:**
- ❌ **Redirect to wrong URL** → `redirect_uri` mismatch
- ❌ **State mismatch** → CSRF token doesn't match
- ❌ **Code already used** → Authorization code can only be used once

---

### Step 7: Token Exchange

**What happens:**
1. Vikunja receives authorization code
2. Vikunja makes backend request to MAS token endpoint
3. Exchanges code for access token and ID token

**Token request:**
```
POST https://matrix.factumerit.app/oauth2/token
Content-Type: application/x-www-form-urlencoded

grant_type=authorization_code&
code=<authorization_code>&
redirect_uri=https://vikunja.factumerit.app/auth/openid/factumerit&
client_id=0000000000000000000V1KYNJA&
client_secret=<client_secret>
```

**Response:**
```json
{
  "access_token": "...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "id_token": "...",
  "refresh_token": "..."
}
```

**Common failures:**
- ❌ **Invalid client secret** → Secret mismatch between Vikunja and MAS
- ❌ **Code expired** → Authorization code has 10-minute lifetime
- ❌ **Invalid grant** → Code already used or invalid

**Debug:**
```bash
# Verify client secret matches in both configs
# Vikunja env var:
echo $VIKUNJA_OIDC_CLIENT_SECRET

# MAS config:
cd ~/factumerit-matrix
grep -A5 "0000000000000000000V1KYNJA" mas/mas.template.yaml
```

---

### Step 8: UserInfo Request

**What happens:**
1. Vikunja uses access token to fetch user info
2. Calls MAS userinfo endpoint
3. Gets user's email, name, and username

**UserInfo request:**
```
GET https://matrix.factumerit.app/oauth2/userinfo
Authorization: Bearer <access_token>
```

**Response (with MAS email patch):**
```json
{
  "sub": "01JFQR8...",
  "email": "ivan@ivantohelpyou.com",  # ← From MAS patch!
  "email_verified": true,
  "preferred_username": "ivantohelpyou",
  "name": "Ivan Schneider"
}
```

**Common failures:**
- ❌ **Email missing** → MAS userinfo patch not applied
- ❌ **Invalid token** → Access token expired or invalid
- ❌ **Insufficient scope** → Token doesn't have `email` scope

**MAS userinfo patch:**
```rust
// mas/crates/handlers/src/oauth2/userinfo.rs
// Patch adds email from user_emails table to response
```

**Debug:**
```bash
# Test userinfo endpoint manually (need valid access token)
curl -H "Authorization: Bearer <token>" \
  https://matrix.factumerit.app/oauth2/userinfo | jq .

# Should include "email" field
```

---

### Step 9: User Account Creation in Vikunja

**What happens:**
1. Vikunja receives user info from MAS
2. Checks if user exists (by OIDC subject ID)
3. If new user, creates account with email from userinfo
4. Logs user in and creates session

**Vikunja user record:**
```
id: <auto-increment>
username: ivantohelpyou (from preferred_username)
email: ivan@ivantohelpyou.com (from email claim)
oidc_subject: 01JFQR8... (from sub claim)
```

**Common failures:**
- ❌ **Email required but missing** → Vikunja requires email for account creation
- ❌ **Duplicate email** → Email already exists (if using email matching)
- ❌ **Username conflict** → Username already taken

**Debug:**
```bash
# Check Vikunja logs for user creation
# Check Vikunja database for new user record
```

---

### Step 10: Session Creation & Redirect

**What happens:**
1. Vikunja creates JWT session token
2. Sets session cookie in browser
3. Redirects to Vikunja dashboard

**Success!** User is now logged into Vikunja with:
- ✅ Account created
- ✅ Email populated
- ✅ Session active
- ✅ Can create tasks

---

## Configuration Checklist

### Vikunja Configuration

**File:** `~/vikunja-factumerit/config.yml`

```yaml
service:
  enableregistration: false  # Disable local registration

auth:
  local:
    enabled: false  # Disable local auth
  openid:
    enabled: true
    redirecturl: https://vikunja.factumerit.app/auth/openid/
    providers:
      - name: Factumerit
        authurl: https://matrix.factumerit.app/  # ← Trailing slash!
        clientid: ${VIKUNJA_OIDC_CLIENT_ID}
        clientsecret: ${VIKUNJA_OIDC_CLIENT_SECRET}
        scope: openid email profile
```

**Environment variables (Render):**
```
VIKUNJA_OIDC_CLIENT_ID=0000000000000000000V1KYNJA
VIKUNJA_OIDC_CLIENT_SECRET=CiUaJN+4A8nWHklS0eVW6VTvfzioEOGprkwIqMKu/fY=
```

### MAS Configuration

**File:** `~/factumerit-matrix/mas/mas.template.yaml`

```yaml
clients:
  - client_id: 0000000000000000000V1KYNJA
    client_name: Vikunja
    client_uri: https://vikunja.factumerit.app
    client_auth_method: client_secret_post
    client_secret: ${VIKUNJA_OIDC_SECRET}
    redirect_uris:
      - https://vikunja.factumerit.app/auth/openid/factumerit  # ← Provider key!

policy:
  wasm_module: /usr/local/share/mas-cli/policy.wasm
  data:
    admin_clients:
      - "0000000000000000000V1KYNJA"  # ← Must be here!
```

**Environment variables (Render):**
```
VIKUNJA_OIDC_SECRET=CiUaJN+4A8nWHklS0eVW6VTvfzioEOGprkwIqMKu/fY=
```

### DNS Configuration (Cloudflare)

```
vikunja.factumerit.app  → CNAME → vikunja-latest-h97k.onrender.com (Proxy: OFF)
matrix.factumerit.app   → CNAME → factumerit-matrix.onrender.com (Proxy: OFF)
```

**Important:** Cloudflare proxy MUST be disabled for OAuth to work!

---

## Common Issues & Solutions

### Issue 1: Empty Providers Array

**Symptom:** `/api/v1/info` returns `"providers": []`

**Causes:**
1. Config file not being processed by envsubst
2. Environment variables not set in Render
3. Vikunja reading wrong config file

**Solution:**
```bash
# Check if start.sh is running
# Check Render environment variables
# Add debug logging to start.sh to verify config processing
```

### Issue 2: Issuer Mismatch

**Symptom:** `Error: issuer did not match, expected "X" got "Y"`

**Cause:** Trailing slash mismatch between `authurl` and MAS issuer

**Solution:**
```yaml
# authurl must match issuer exactly
authurl: https://matrix.factumerit.app/  # ← Add trailing slash
```

### Issue 3: Invalid Redirect URI

**Symptom:** `redirect_uri is not allowed for this client`

**Cause:** Mismatch between Vikunja's redirect URI and MAS config

**Solution:**
```yaml
# MAS config must match Vikunja's format: /auth/openid/{provider_key}
redirect_uris:
  - https://vikunja.factumerit.app/auth/openid/factumerit
```

### Issue 4: Policy Denied

**Symptom:** `The authorization request was denied by the policy`

**Cause:** Client not in `admin_clients` list

**Solution:**
```yaml
# Add Vikunja client ID to admin_clients
policy:
  data:
    admin_clients:
      - "0000000000000000000V1KYNJA"
```

### Issue 5: Email Not Populated

**Symptom:** User created but email is empty

**Cause:** MAS userinfo patch not applied or not working

**Solution:**
```bash
# Verify MAS userinfo patch is applied
# Check MAS logs for userinfo endpoint calls
# Test userinfo endpoint manually
```

---

## Testing the Flow

### End-to-End Test

1. **Clear browser cookies** for vikunja.factumerit.app
2. **Go to** https://vikunja.factumerit.app
3. **Verify** "Login with Factumerit" button appears
4. **Click** login button
5. **Verify** redirects to matrix.factumerit.app
6. **Login** with Matrix credentials
7. **Verify** consent screen shows email
8. **Click** "Allow"
9. **Verify** redirects back to Vikunja
10. **Verify** logged in with email populated

### API Tests

```bash
# Test 1: Check provider is configured
curl -s https://vikunja.factumerit.app/api/v1/info | jq '.auth.openid_connect.providers'

# Test 2: Check OIDC discovery
curl -s https://matrix.factumerit.app/.well-known/openid-configuration | jq .

# Test 3: Check issuer matches
curl -s https://matrix.factumerit.app/.well-known/openid-configuration | jq -r '.issuer'
```

---

## Architecture Benefits

### Why Direct MAS Connection?

**Before (with Authentik):**
```
Vikunja → Authentik → MAS → Synapse
Cost: $65/mo
Complexity: High (3 auth layers)
```

**After (direct MAS):**
```
Vikunja → MAS → Synapse
Cost: $40/mo (saves $25/mo)
Complexity: Medium (2 auth layers)
```

**Benefits:**
- 💰 **Cost savings:** $25/mo by removing Authentik
- 🔧 **Simpler architecture:** One less service to maintain
- 🚀 **Faster auth:** One less redirect hop
- 📧 **Email works:** MAS userinfo patch provides email directly

---

## Maintenance Notes

### When to Restart Services

**MAS restart required when:**
- Changing client configuration
- Updating policy (admin_clients)
- Changing redirect URIs
- Updating client secrets

**Vikunja restart required when:**
- Changing OIDC provider config
- Updating environment variables
- Changing authurl

### Monitoring

**Check these regularly:**
- Vikunja logs for OIDC errors
- MAS logs for policy denials
- User creation success rate
- Email population rate

---

## Related Documents

- [MAS Email Patch Analysis](./mas-email-patch-analysis.md)
- [Vikunja-MAS Direct Debug Map](./VIKUNJA-MAS-DIRECT-DEBUG.md)
- [Sign-in Lifecycle Diagnostic](./sign-in-lifecycle-diagnostic.md)

---

**Last Updated:** 2025-12-23
**Status:** ✅ Working (Vikunja → MAS direct connection established)

---

## Appendix: Non-Technical Explanation

This appendix explains the Factumerit system in simple terms for non-specialists.

### What is Factumerit?

**The Big Picture:** Factumerit is a task management assistant that lives in Matrix (a chat app). You talk to a bot in chat, and it manages your tasks for you.

**The Magic:** The bot is connected to Vikunja (a task management web app), so you can:
- Manage tasks by chatting with the bot in Matrix
- OR use the Vikunja web interface when you want a visual dashboard
- Your tasks sync between both - they're the same data

**Why This Matters:**
- Natural language: "remind me to buy groceries tomorrow" instead of clicking through forms
- Always accessible: Matrix works on phone, desktop, web
- One account: Your Matrix account works for both chat and web interface

---

### The Complete User Journey

#### Step 1: You Join Matrix
- You create a Matrix account at https://matrix.factumerit.app
- This is like creating a Slack or Discord account
- You get a username like `@yourname:factumerit.app`
- You can use any Matrix client (Element, FluffyChat, etc.)

#### Step 2: You DM the Bot
- You send a direct message to `@tasks:factumerit.app`
- The bot says: "Hi! Click this link to get started"
- The link is unique to you and expires in 1 hour

#### Step 3: One-Click Provisioning
- You click the link
- Behind the scenes, the system:
  - Creates a Vikunja account for you (using your Matrix email)
  - Sets up default projects (Inbox, Personal, Work)
  - Generates an API token so the bot can access your tasks
  - Stores the connection between your Matrix ID and Vikunja account
- You see: "✓ All set! Go back to Matrix and try: 'add buy groceries'"

#### Step 4: You Chat with the Bot
- You return to Matrix and chat with the bot
- "what's due today" → Bot shows your tasks
- "add buy groceries tomorrow" → Bot creates the task
- "I finished task 42" → Bot marks it done
- The bot is talking to Vikunja's API on your behalf

#### Step 5: (Optional) You Use the Web Interface
- Sometimes you want to see all your tasks visually
- You go to https://vikunja.factumerit.app
- You click "Login with Factumerit"
- **This is where the OAuth flow in this document happens**
- You log in with your Matrix credentials
- You see the same tasks you've been managing via chat

---

### The Players (In Context)

#### 1. **Matrix** (The Chat Platform)
- **What it is:** An open-source chat platform (like Slack or Discord)
- **Your account:** `@yourname:factumerit.app`
- **What you do here:** Chat with the task bot, get instant responses
- **Clients:** Element (web/mobile), FluffyChat, Nheko, etc.

#### 2. **The Bot** (`@tasks:factumerit.app`)
- **What it is:** An AI assistant that understands natural language
- **What it does:**
  - Parses your messages ("buy groceries tomorrow" → create task with due date)
  - Calls Vikunja API to create/update/list tasks
  - Formats responses in chat-friendly way
- **Where it runs:** On a server, connected to both Matrix and Vikunja

#### 3. **Vikunja** (The Task Management Backend)
- **What it is:** A task management application (like Trello or Todoist)
- **What it stores:** Your tasks, projects, labels, due dates
- **Two interfaces:**
  - API: The bot talks to this
  - Web UI: You can use this directly at https://vikunja.factumerit.app

#### 4. **MAS** (The Gatekeeper for Web Login)
- **Full name:** Matrix Authentication Service
- **What it is:** A security service that verifies who you are
- **When you use it:** Only when logging into the Vikunja web interface
- **What it does:** Checks your Matrix password, tells Vikunja your email
- **Location:** https://matrix.factumerit.app

#### 5. **Synapse** (The Matrix Server)
- **What it is:** The server that runs Matrix
- **What it stores:** Your Matrix messages, contacts, account info
- **Its job:** Handle chat messages, federation with other Matrix servers
- **Note:** MAS talks to Synapse to verify your password

---

### The Web Login Journey (In Plain English)

**Context:** This is what happens when you want to use the Vikunja web interface instead of chatting with the bot.

**Note:** Most users primarily use the bot in Matrix. The web interface is for when you want a visual dashboard or need to do bulk operations.

---

Imagine you're trying to get into a VIP club (Vikunja web interface), but you don't have a membership card. However, you DO have a membership at a partner club (Matrix). Here's what happens:

#### Step 1: You Ask to Enter
- You go to https://vikunja.factumerit.app and click "Login with Factumerit"
- Vikunja says: "I don't know you, but I trust MAS. Go ask MAS to vouch for you."

#### Step 2: Vikunja Sends You to MAS
- Your browser is redirected to MAS (the gatekeeper)
- Vikunja gives you a note to carry that says: "Please verify this person and tell me their email"

#### Step 3: MAS Asks for Your Credentials
- MAS shows you a login screen
- You enter your Matrix username and password
- MAS checks with Synapse: "Is this password correct?"
- Synapse says: "Yes, that's the right password"

#### Step 4: MAS Asks for Your Permission
- MAS shows you a consent screen that says:
  - "Vikunja wants to know your email address"
  - "Do you allow this?"
- You click "Allow"

#### Step 5: MAS Gives Vikunja a Secret Code
- MAS says: "OK, I verified them. Here's a secret code."
- MAS sends your browser back to Vikunja with this code
- The code is like a claim ticket - it proves MAS verified you

#### Step 6: Vikunja Exchanges the Code for Information
- Vikunja takes the secret code and calls MAS directly (not through your browser)
- Vikunja says: "Here's the code you gave me. Now give me the user's information."
- MAS says: "OK, here's their email: ivan@ivantohelpyou.com and username: ivantohelpyou"

#### Step 7: You're In!
- Vikunja finds your existing account (created during bot provisioning) using your email
- You're logged in and can see all the tasks you've been managing via chat
- Next time you log in, Vikunja recognizes you

---

### Key Concepts Explained

#### What is OAuth / OpenID Connect?

**Simple analogy:** It's like a valet parking system.

- You (the user) want to park your car (log in)
- The restaurant (Vikunja) doesn't want to handle your car keys (password)
- So they use a valet service (MAS) that you already trust
- The valet verifies you own the car and parks it for you
- The restaurant never touches your keys, but you still get in

**Technical version:**
- OAuth 2.0 is a protocol for authorization (proving you have permission)
- OpenID Connect adds identity (proving who you are)
- Together, they let one service verify your identity without seeing your password

#### What is a "Scope"?

**Simple analogy:** It's like permissions on a permission slip.

When you sign a permission slip for a school field trip, you might check boxes:
- ✅ Can take photos
- ✅ Can give emergency medical treatment
- ❌ Cannot leave the state

In our system, "scopes" are the permissions Vikunja is asking for:
- `openid` = "I want to know who this user is"
- `email` = "I want to know their email address"
- ~~`profile`~~ = "I want their full name" (we removed this because MAS doesn't support it)

#### What is a "Redirect URI"?

**Simple analogy:** It's like a return address on a letter.

When Vikunja sends you to MAS, it includes a "redirect URI" that says:
- "After you verify this person, send them back to this address"
- Example: `https://vikunja.factumerit.app/auth/openid/factumerit`

If the redirect URI doesn't match what MAS expects, it's like sending a letter to the wrong address - it gets rejected for security.

#### What is a "Client ID" and "Client Secret"?

**Simple analogy:** It's like a username and password for Vikunja itself.

- **Client ID:** Vikunja's username (public, like `0000000000000000000V1KYNJA`)
- **Client Secret:** Vikunja's password (secret, like `CiUaJN+4A8nWHklS0eVW6VTvfzioEOGprkwIqMKu/fY=`)

When Vikunja talks to MAS, it proves it's really Vikunja by showing these credentials.

#### What is the "Userinfo Endpoint"?

**Simple analogy:** It's like an information desk.

After MAS verifies you, Vikunja can call the "userinfo endpoint" to ask:
- "What's this user's email?"
- "What's their username?"

MAS responds with a package of information:
```json
{
  "email": "ivan@ivantohelpyou.com",
  "preferred_username": "ivantohelpyou",
  "email_verified": true
}
```

---

### What We Fixed (In Plain English)

#### Problem 1: Random Usernames
**What was happening:**
- Users were getting random usernames like "happily-absolute-oriole"
- This made it hard to find people or know who was who

**Why it happened:**
- MAS wasn't telling Vikunja what the user's Matrix username was
- Vikunja said: "I don't know their username, so I'll make one up"

**How we fixed it:**
- We modified MAS to include `preferred_username` in the information it sends
- Now Vikunja knows your Matrix username and uses that

#### Problem 2: Policy Denied Errors
**What was happening:**
- Users clicked "Allow" on the consent screen
- But then got an error: "The authorization request was denied by the policy"

**Why it happened:**
- Vikunja was asking for the `profile` scope
- MAS has a policy that says: "I only allow `openid` and `email` scopes"
- MAS rejected the request because `profile` wasn't allowed

**How we fixed it:**
- We removed `profile` from Vikunja's configuration
- Now Vikunja only asks for `openid` and `email`, which MAS allows

#### Problem 3: Missing Email
**What was happening:**
- Users could log in, but their email wasn't showing up in Vikunja

**Why it happened:**
- MAS had a bug - it wasn't including email in the userinfo response
- Even though MAS knew the user's email, it wasn't telling Vikunja

**How we fixed it:**
- We patched MAS's source code to include email in the userinfo response
- Now when Vikunja asks "What's this user's email?", MAS actually tells it

---

### Architecture Benefits

#### Why This Design?

**The Complete System:**
```
User → Matrix (chat) → Bot → Vikunja API
                ↓
        (optional) Vikunja Web UI
                ↓
              MAS → Synapse
```

**Primary Flow (Bot):**
- User chats with bot in Matrix
- Bot calls Vikunja API directly
- Fast, natural language interface
- No web login needed

**Secondary Flow (Web UI):**
- User wants visual dashboard
- Logs into Vikunja web interface via MAS
- Same tasks as in chat (shared backend)

**Before (Complex Web Login):**
```
Vikunja Web → Authentik → MAS → Synapse
```
- 4 services to maintain
- More points of failure
- Cost: $65/month

**After (Simple Web Login):**
```
Vikunja Web → MAS → Synapse
```
- 3 services to maintain
- Fewer points of failure
- Cost: $40/month (saves $25/month)

**Why we removed Authentik:**
- Authentik was acting as a "middleman" between Vikunja and MAS
- It wasn't adding value - just passing information through
- By connecting Vikunja directly to MAS, we simplified the system
- The bot doesn't need Authentik at all - it uses API tokens

**Why the bot is the primary interface:**
- **Faster:** Type "what's due today" vs clicking through web UI
- **Natural:** Conversational instead of forms and buttons
- **Accessible:** Works on any device with Matrix client
- **AI-powered:** Bot understands context and intent
- **Always available:** Matrix notifications work everywhere

---

### Common Questions

#### Q: Do I need to use the web interface at all?

**A:** No! Most users only use the bot.

- The bot can do everything: create tasks, list tasks, update status, search, etc.
- The web interface is optional - for when you want a visual dashboard
- Some users never use the web interface and that's perfectly fine

#### Q: How does the bot access my tasks?

**A:** Through an API token created during provisioning.

- When you click the one-click setup link, the system creates a Vikunja account for you
- It generates an API token (like a password just for the bot)
- The bot stores this token (encrypted) and uses it to call Vikunja's API
- The bot never sees your Matrix password

#### Q: Why can't Vikunja just ask for my password directly?

**A:** Security and convenience.

- **Security:** If Vikunja stored your password, and Vikunja got hacked, your Matrix password would be compromised
- **Convenience:** You only need to remember one password (Matrix), not separate passwords for every app
- **Trust:** MAS is the only service that sees your password, and it's designed specifically for security
- **Note:** This only applies to web login - the bot uses API tokens, not passwords

#### Q: What happens if the bot goes down?

**A:** You can still use the web interface.

- Your tasks are stored in Vikunja, not the bot
- If the bot is down, you can log into https://vikunja.factumerit.app
- Once the bot comes back up, it will see all the tasks you created via web

#### Q: What happens if MAS goes down?

**A:** The bot keeps working, but you can't log into the web interface.

- The bot uses API tokens, not MAS, so it's unaffected
- If you're already logged into the web interface, you can keep using it
- If you try to log in while MAS is down, you'll get an error
- Once MAS comes back up, web login works again

#### Q: Can the bot see my Matrix messages?

**A:** Only messages you send directly to it.

- The bot only receives messages in DMs with you
- It cannot see your messages in other rooms or with other people
- It cannot see your contacts or any other Matrix data
- It only knows what you tell it

#### Q: Can Vikunja (web) see my Matrix messages?

**A:** No, absolutely not.

- Vikunja only asks for `openid` and `email` scopes
- These scopes only give access to your email address and username
- Vikunja cannot read your messages, contacts, or any other Matrix data

#### Q: Why does the consent screen ask for permission every time?

**A:** It shouldn't - this might be a configuration issue.

- Normally, you grant permission once, and MAS remembers
- If you're seeing the consent screen every time, it might be because:
  - Your browser is blocking cookies
  - MAS isn't configured to remember consent
  - You're using incognito/private mode

#### Q: What if I want to revoke Vikunja's access?

**A:** You can revoke web access in MAS settings.

- Go to https://matrix.factumerit.app
- Log in
- Go to Settings → Sessions & Devices
- Find Vikunja and click "Revoke"
- This only affects web login - the bot will still work (it uses API tokens)

#### Q: Can I use my own Vikunja instance instead of the hosted one?

**A:** Yes! (Advanced users)

- DM the bot: "config add https://my.vikunja.io vkt_yourtoken"
- The bot will connect to your instance instead
- You can have multiple Vikunja instances connected
- This is called "BYOV" (Bring Your Own Vikunja)

---

### How Bot Provisioning Works (Technical)

**When you click the one-click setup link, here's what happens behind the scenes:**

#### Step 1: Link Validation
- The link contains your Matrix ID and a one-time nonce (random code)
- The system checks: Is this nonce valid? Has it expired? (1 hour limit)
- If invalid: "Link expired or invalid"
- If valid: Continue to Step 2

#### Step 2: Vikunja Account Creation
- System calls Vikunja Admin API: "Create user with email from Matrix"
- Username is sanitized from Matrix ID: `@alice:matrix.org` → `alice_matrix_org`
- Email comes from your Matrix account (from MAS)
- Password is randomly generated (you'll never need it - you use Matrix login)

#### Step 3: Default Projects Setup
- System creates three starter projects:
  - "Inbox" (for quick captures)
  - "Personal" (for personal tasks)
  - "Work" (for work tasks)
- You can rename/delete these later

#### Step 4: API Token Generation
- System generates an API token for the bot
- This token allows the bot to access your tasks
- Token is stored encrypted in the bot's database
- Token is linked to your Matrix ID

#### Step 5: Database Storage
- System stores the connection:
  ```
  Matrix ID: @alice:matrix.org
  Vikunja URL: https://vikunja.factumerit.app
  API Token: vkt_abc123... (encrypted)
  ```
- This is how the bot knows which Vikunja account belongs to which Matrix user

#### Step 6: Nonce Invalidation
- The one-time link is marked as used
- If someone tries to use it again, it won't work
- Security: Prevents replay attacks

#### Step 7: Success!
- You see a success page
- You return to Matrix
- Bot now responds to your commands with your tasks

**Security Notes:**
- The nonce expires in 1 hour
- The nonce can only be used once
- API tokens are stored encrypted
- The bot never sees your Matrix password
- Each user's tasks are completely isolated

---

### Troubleshooting for Non-Specialists

#### "The bot isn't responding to my messages"

**Possible causes:**
1. Bot is offline or restarting
2. You're not in a DM with the bot (you're in a room)
3. Bot hasn't been provisioned yet

**Try:**
- Check if you're DMing `@tasks:factumerit.app` directly
- Wait 30 seconds and try again
- Send "help" to see if bot responds

#### "I clicked the setup link but got an error"

**Possible causes:**
1. Link expired (1 hour limit)
2. Link already used
3. Vikunja service is down

**Try:**
- DM the bot again to get a new link
- Check if https://vikunja.factumerit.app is accessible
- Contact administrator

#### "I clicked login but nothing happened"

**Possible causes:**
1. JavaScript is disabled in your browser
2. Pop-up blocker is blocking the redirect
3. Network connectivity issue

**Try:**
- Refresh the page
- Disable pop-up blocker for vikunja.factumerit.app
- Try a different browser

#### "I see a white screen after clicking login"

**Possible causes:**
1. MAS frontend assets aren't loading
2. Browser cache issue

**Try:**
- Clear your browser cache
- Try incognito/private mode
- Wait a few seconds - it might just be slow

#### "I get 'authorization denied by policy'"

**Possible causes:**
1. Vikunja is asking for scopes that MAS doesn't allow
2. Your account is banned or restricted

**Try:**
- Contact the administrator
- Check if your Matrix account is active

#### "My username is random gibberish"

**Possible causes:**
1. You created your account before we fixed the `preferred_username` issue
2. MAS isn't sending the username

**Solution:**
- Unfortunately, usernames can't be changed after account creation
- You'll need to create a new account (after the fix is deployed)
- Or contact the administrator to manually update your username in the database

---

### For Administrators

#### How to Check if Everything is Working

**1. Check Vikunja can reach MAS:**
```bash
curl https://matrix.factumerit.app/.well-known/openid-configuration
```
Should return JSON with `authorization_endpoint`, `token_endpoint`, etc.

**2. Check MAS is running:**
```bash
# In Render dashboard, check MAS service status
# Should show "Live" with green indicator
```

**3. Check Vikunja configuration:**
```bash
# In Render dashboard, check Vikunja environment variables
# Should have:
# - VIKUNJA_OIDC_CLIENT_ID
# - VIKUNJA_OIDC_CLIENT_SECRET
```

**4. Test the login flow:**
- Go to https://vikunja.factumerit.app
- Click "Login with Factumerit"
- Should redirect to MAS
- Login with Matrix credentials
- Should redirect back to Vikunja
- Should be logged in with email populated

#### How to Add a New OAuth Client

If you want to connect another app (like Grafana, Nextcloud, etc.) to MAS:

**1. Generate a client ID and secret:**
```bash
# Client ID: 26 random characters (use a generator)
# Client Secret: Base64-encoded random string
openssl rand -base64 32
```

**2. Add to MAS config:**
```yaml
# In factumerit-matrix/mas/mas.template.yaml
clients:
  - client_id: YOUR_CLIENT_ID
    client_name: Your App Name
    client_uri: https://yourapp.factumerit.app
    client_auth_method: client_secret_post
    client_secret: ${YOUR_APP_OIDC_SECRET}
    redirect_uris:
      - https://yourapp.factumerit.app/oauth/callback
```

**3. Add environment variable to Render:**
```
YOUR_APP_OIDC_SECRET=<your-secret>
```

**4. Deploy MAS:**
- Commit and push changes
- MAS will restart with new client

**5. Configure your app:**
- Set OIDC provider URL: `https://matrix.factumerit.app/`
- Set client ID and secret
- Set scopes: `openid email`
- Set redirect URI to match MAS config

---

### Glossary

**Authentication:** Proving who you are (like showing ID)

**Authorization:** Proving you have permission (like showing a ticket)

**Bearer Token:** A secret code that proves you're authorized (like a claim ticket)

**Claim:** A piece of information about you (like "email" or "username")

**Client:** An application that wants to log users in (like Vikunja)

**Consent:** Your permission for an app to access your information

**Discovery Endpoint:** A URL that tells apps how to connect to MAS (`.well-known/openid-configuration`)

**Grant:** Permission to access something (like "authorization grant")

**Identity Provider (IdP):** A service that verifies who you are (MAS is our IdP)

**Issuer:** The service that creates tokens (MAS is the issuer)

**OAuth 2.0:** A protocol for authorization (letting apps access your data)

**OpenID Connect (OIDC):** An extension of OAuth that adds identity

**Policy:** Rules that determine what's allowed (like "only allow email scope")

**Redirect URI:** Where to send the user after authentication

**Scope:** A permission being requested (like "email" or "openid")

**Session:** Your logged-in state (like "you're logged in for 30 days")

**Subject (sub):** Your unique user ID (like "01JFQR8...")

**Token:** A secret code that proves something (like an access token or ID token)

**Userinfo Endpoint:** A URL where apps can get information about you

---

**End of Appendix**

