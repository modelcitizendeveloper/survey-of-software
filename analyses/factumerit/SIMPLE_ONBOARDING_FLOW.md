# Super Simple Onboarding Flow (Registration Token)

**Date**: 2025-12-25  
**Goal**: Onboard first test user in 5 minutes  
**Method**: Registration token (no Authentik, no SSO complexity)

---

## Admin: Create Registration Token

### Option 1: Using `fa` CLI (Recommended)

```bash
fa matrix tokens create
```

This shows you the instructions. Then:

1. Open Render shell: https://dashboard.render.com/web/srv-d54s143e5dus73bqhpb0/shell
2. Run: `mas manage issue-user-registration-token --uses-allowed 1`

### Option 2: Direct Render Shell

Go to: https://dashboard.render.com/web/srv-d54s143e5dus73bqhpb0/shell

Then run:

```bash
mas manage issue-user-registration-token --uses-allowed 1
```

**Output**:
```
Registration token: mat_2J8xN4K9mP3qR7sT
```

**Copy this token** - you'll send it to the user.

---

## User: Register with Token

### Step 1: Go to Registration Page

https://matrix.factumerit.app/register

### Step 2: Fill in Form

- **Username**: `alice` (becomes @alice:factumerit.app)
- **Email**: `alice@example.com`
- **Password**: (min 8 characters)
- **Registration Token**: `mat_2J8xN4K9mP3qR7sT` (from admin)

### Step 3: Verify Email

Check inbox for verification link, click it.

**Done!** Matrix account created.

---

## User: Install Element

### Desktop

https://element.io/download

### Mobile

- iOS: https://apps.apple.com/app/element-messenger/id1083446067
- Android: https://play.google.com/store/apps/details?id=im.vector.app

### Login

- **Homeserver**: `matrix.factumerit.app`
- **Username**: `@alice:factumerit.app`
- **Password**: (from Step 2)

---

## User: Create Vikunja Account

### Step 1: Go to Vikunja

https://vikunja.factumerit.app

### Step 2: Login with Matrix

Click **"Login with Factumerit"**

**Flow**:
1. Redirects to MAS (matrix.factumerit.app)
2. Enter Matrix credentials
3. Grant consent (email, Matrix ID)
4. Redirected back to Vikunja

**Done!** Vikunja account created automatically.

---

## User: Get Vikunja API Token

### Step 1: Open Settings

In Vikunja web UI:
1. Click profile icon (top right)
2. Go to **Settings** → **API Tokens**

### Step 2: Create Token

1. Click **"Create a new token"**
2. Name: `Matrix Bot`
3. Permissions: **Check ALL boxes** (or minimum: tasks, projects, labels)
4. Click **"Create"**

### Step 3: Copy Token

**Copy the token** (starts with `tk_...`)

⚠️ **Important**: Token only shown once! Copy it now.

---

## User: Connect Bot

### Step 1: Start DM with Bot

In Element, start new DM with: `@eis:factumerit.app`

Bot auto-joins the room.

### Step 2: Send Token

```
!vik tk_YOUR_TOKEN_HERE
```

(Replace with actual token from previous step)

**Expected response**:
```
✅ Connected to Vikunja at https://vikunja.factumerit.app
```

---

## User: Test Bot

### Try Commands

```
!help
```
Expected: List of all commands

```
!stats
```
Expected: Task summary

```
create task buy groceries tomorrow
```
Expected: Bot creates task, confirms with task ID

```
!now
```
Expected: Shows tasks due today (including "buy groceries")

---

## Success! 🎉

**User can now**:
- ✅ Manage tasks via Matrix DM
- ✅ Use ECO commands (!help, !now, !fire, etc.)
- ✅ Use natural language ("show my tasks", "create task X")
- ✅ See tasks in both Element and Vikunja web UI

---

## Admin: Create More Tokens

### Using `fa` CLI

```bash
# Show instructions
fa matrix tokens create

# List existing tokens (via database)
fa matrix tokens list
```

### Direct Commands (in Render shell)

**Single-use (recommended for beta)**:
```bash
mas manage issue-user-registration-token --uses-allowed 1
```

**5-use token (for small group)**:
```bash
mas manage issue-user-registration-token --uses-allowed 5
```

**List all tokens**:
```bash
mas manage list-user-registration-tokens
```

**Disable a token**:
```bash
# Check help for exact command
mas manage --help | grep -i registration
```

---

## Troubleshooting

### "Invalid registration token"

**Cause**: Token already used (single-use) or expired

**Fix**: Admin creates new token

---

### "User not found" when DMing bot

**Cause**: Bot address typo or federation delay

**Fix**:
1. Verify address: `@eis:factumerit.app` (not .com)
2. Wait 30 seconds, try again
3. Check bot is running: `curl https://vikunja-slack-bot.onrender.com/health`

---

### Bot doesn't respond to commands

**Cause**: Token not stored, or bot not connected to Vikunja

**Fix**:
1. Send `!test` to check connection status
2. If not connected, send `!vik tk_TOKEN` again
3. Check token has correct permissions in Vikunja

---

## Why This Is Better

**vs Authentik SSO**:
- ✅ No Authentik deployment needed
- ✅ No email sync issues
- ✅ No username selection confusion
- ✅ Works immediately

**vs Open Registration**:
- ✅ Controlled access (invite-only)
- ✅ No spam risk
- ✅ Can track who invited whom

**vs Manual User Creation**:
- ✅ User sets own password
- ✅ No admin password knowledge
- ✅ Self-service after token provided

---

## Next Steps

1. **Create token** for first test user
2. **Send token** via email/DM
3. **User follows** this guide
4. **Gather feedback** - what worked? what didn't?
5. **Iterate** - improve docs based on feedback
6. **Scale** - create more tokens for more users

---

**Estimated time**: 5-10 minutes per user  
**Admin effort**: 30 seconds (create token)  
**User effort**: 5 minutes (register, install, connect)

**Status**: Ready to onboard first test user! 🚀

