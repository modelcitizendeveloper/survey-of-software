# First Test User Onboarding Checklist

**Date**: 2025-12-25  
**Platform**: Factumerit (Matrix + Vikunja)  
**Goal**: Onboard first external test user successfully

---

## Prerequisites (Admin)

### ✅ Infrastructure Ready

- ✅ Synapse homeserver running (matrix.factumerit.app)
- ✅ MAS authentication service running
- ✅ Vikunja running (vikunja.factumerit.app)
- ✅ Matrix bot deployed (@eis:matrix.factumerit.app)
- ✅ Bot has LLM integration (natural language works)
- ✅ All tests passing (20/20 integration tests)

### ✅ Configuration Verified

- ✅ Self-service registration enabled (mas.yaml)
- ✅ Email verification required
- ✅ Vikunja OIDC configured (Login with Factumerit)
- ✅ Bot access token set (MATRIX_ACCESS_TOKEN)
- ✅ Anthropic API key set (for LLM)

---

## User Onboarding Flow

### Step 1: User Creates Matrix Account

**User action**:
1. Go to https://matrix.factumerit.app/register
2. Fill in:
   - Username (becomes @username:factumerit.app)
   - Email address
   - Password (min 8 characters)
3. Check email for verification link
4. Click link to verify email

**Expected result**: Account activated, can login to Element

**Admin verification**:
```bash
# Check user exists in MAS
# (via Render shell or psql)
```

---

### Step 2: User Installs Matrix Client

**Recommended**: Element (https://element.io/download)

**User action**:
1. Download Element for desktop/mobile
2. Login with:
   - Homeserver: matrix.factumerit.app
   - Username: @username:factumerit.app
   - Password: (from Step 1)

**Expected result**: Logged into Element, sees empty room list

---

### Step 3: User Creates Vikunja Account

**User action**:
1. Go to https://vikunja.factumerit.app
2. Click **"Login with Factumerit"**
3. Redirects to MAS (matrix.factumerit.app)
4. Enter Matrix credentials
5. Grant consent (email, Matrix ID)
6. Redirected back to Vikunja

**Expected result**: 
- Vikunja account created automatically
- User sees empty Vikunja dashboard
- Can create projects and tasks in web UI

**Admin verification**:
```bash
# Check Vikunja user exists
curl -H "Authorization: Bearer $ADMIN_TOKEN" \
  https://vikunja.factumerit.app/api/v1/users
```

---

### Step 4: User Gets Vikunja API Token

**User action**:
1. In Vikunja web UI, click profile icon (top right)
2. Go to **Settings** → **API Tokens**
3. Click **"Create a new token"**
4. Name: "Matrix Bot"
5. Permissions: Check ALL boxes (or at minimum: tasks, projects, labels)
6. Click **"Create"**
7. **Copy the token** (starts with `tk_...`)

**Expected result**: User has API token copied to clipboard

**⚠️ Important**: Token only shown once! User must copy it now.

---

### Step 5: User Connects Bot

**User action**:
1. In Element, start new DM with: **@eis:factumerit.app**
2. Bot auto-joins the room
3. Send command:
   ```
   !vik tk_YOUR_TOKEN_HERE
   ```
   (Replace with actual token from Step 4)

**Expected result**:
```
✅ Connected to Vikunja at https://vikunja.factumerit.app
```

**Admin verification**:
```bash
# Check user token stored in bot config
# (via Render shell or config file)
cat ~/.vikunja-mcp/config.yaml | grep -A5 "@username:factumerit.app"
```

---

### Step 6: User Tests Bot

**User action**: Send test commands in DM:

```
!help
```
Expected: List of all commands

```
!stats
```
Expected: Task summary (Total: 0, Open: 0, etc.)

```
!now
```
Expected: "No tasks due today" (or list if tasks exist)

```
create task buy groceries tomorrow
```
Expected: Bot creates task, confirms with task ID

**Expected result**: All commands work, bot responds quickly

---

## Troubleshooting

### Issue: "User not found" when DMing bot

**Cause**: Bot address typo or federation delay

**Fix**:
1. Verify address: `@eis:factumerit.app` (not .com)
2. Wait 30 seconds, try again
3. Check bot is running: `curl https://vikunja-slack-bot.onrender.com/health`

---

### Issue: "No email address available" during Vikunja login

**Cause**: Matrix account doesn't have verified primary email

**Fix**:
1. User: Go to Element → Settings → General → Email Addresses
2. Add email, verify it
3. Set as primary
4. Try Vikunja login again

**Admin fix** (if needed):
```bash
# Via Render shell for MAS
mas manage verify-email -c /etc/mas/mas.yaml username email@example.com
```

---

### Issue: Bot doesn't respond to commands

**Cause**: Token not stored, or bot not connected to Vikunja

**Fix**:
1. User: Send `!test` to check connection status
2. If not connected, send `!vik tk_TOKEN` again
3. Check token has correct permissions in Vikunja

**Admin check**:
```bash
# Check bot logs
# Via Render dashboard → vikunja-slack-bot → Logs
```

---

### Issue: Natural language doesn't work

**Cause**: LLM integration issue or API key missing

**Fix**:
1. Check ANTHROPIC_API_KEY is set in Render env vars
2. User can set own key: `!apikey set sk-ant-...`
3. Check usage limits: `!credits`

---

## Success Criteria

**User can**:
- ✅ Create Matrix account
- ✅ Login to Element
- ✅ Create Vikunja account via SSO
- ✅ Get Vikunja API token
- ✅ Connect bot with `!vik` command
- ✅ Use ECO commands (!help, !now, !stats, etc.)
- ✅ Use natural language ("create task buy milk")
- ✅ See tasks in both Element and Vikunja web UI

---

## Post-Onboarding

### User Education

Send user these resources:
1. **Command reference**: `!help` in bot DM
2. **Natural language examples**: "show my tasks", "create task X", "mark task Y done"
3. **Cost control**: `!credits` to check usage, `!apikey` to set own key

### Feedback Collection

Ask user:
1. Was onboarding clear?
2. Any confusing steps?
3. What features do you want?
4. Any bugs or issues?

---

## Admin Notes

### User Data Stored

**MAS database**:
- Matrix user ID
- Email (verified)
- Password hash

**Vikunja database**:
- Vikunja user ID
- Email (from Matrix)
- Projects and tasks

**Bot config** (~/.vikunja-mcp/config.yaml):
- Matrix user ID → Vikunja API token (encrypted)
- Usage tracking (tokens, budget)
- User preferences (timezone, model, etc.)

### Monitoring

**Check regularly**:
- Bot uptime: https://vikunja-slack-bot.onrender.com/health
- User activity: Bot logs in Render
- Error rates: Check for exceptions in logs

---

## Next Steps After First User

1. **Gather feedback** - What worked? What didn't?
2. **Fix issues** - Create beads for any bugs found
3. **Improve docs** - Update onboarding guide based on feedback
4. **Onboard more users** - Repeat process with 2-3 more testers
5. **Public launch** - Announce in #vikunja:matrix.org

---

**Status**: Ready for first test user onboarding  
**Estimated time**: 15-20 minutes per user  
**Support**: Available via Matrix DM or email

