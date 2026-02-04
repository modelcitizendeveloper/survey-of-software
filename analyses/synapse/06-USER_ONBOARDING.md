# 06: User Onboarding Guide

**Date**: 2025-12-23
**Status**: Draft
**Context**: How users get started with Factumerit Matrix platform

---

## Overview

Guide for onboarding new users to `matrix.factumerit.app` and its bot services.

---

## Getting a Matrix Account

### Current: Self-Service Registration

**Status**: Enabled (as of 2025-12-23)

**Steps**:
1. Go to https://matrix.factumerit.app/register
2. Fill in:
   - Username (becomes `@username:factumerit.app`)
   - Email address (required for verification)
   - Password (min 8 characters)
3. Check email for verification link
4. Click link to verify email
5. Account activated!

**Configuration**:
```yaml
# mas.yaml
account:
  password_registration_enabled: true
  email_verification_required: true
```

---

### Future: Invite-Only Registration

**Why**: Prevent spam, control user base

**Implementation**:
```yaml
# mas.yaml
account:
  password_registration_enabled: false
  
# Generate invite tokens
mas-cli manage registration-token create \
  --uses-allowed 1 \
  --expiry-days 7
```

**User flow**:
1. Admin generates invite token
2. Admin sends invite link: `https://matrix.factumerit.app/register?token=<token>`
3. User clicks link, fills in details
4. Account created

---

## Choosing a Matrix Client

### Recommended Clients

| Client | Platform | Best For |
|--------|----------|----------|
| **Element** | Web, Desktop, Mobile | Full-featured, most compatible |
| **FluffyChat** | Mobile | Simple, lightweight |
| **Nheko** | Desktop | Native, fast |
| **Cinny** | Web | Modern UI |

### Element Setup (Recommended)

1. **Web**: Go to https://app.element.io
2. **Desktop**: Download from https://element.io/download
3. **Mobile**: Install from App Store / Play Store

**First-time setup**:
1. Click "Sign In"
2. Click "Edit" next to homeserver
3. Enter: `matrix.factumerit.app`
4. Enter username and password
5. (Optional) Set up encryption recovery key

---

## First Interaction with Bots

### Finding Bots

**Available bots** (as of 2025-12-23):
- `@tasks:factumerit.app` - Vikunja task management (deployed)
- `@research:factumerit.app` - Research library (future)
- `@assistant:factumerit.app` - General LLM assistant (future)

### Starting a DM with a Bot

**In Element**:
1. Click "+" next to "Direct Messages"
2. Enter bot address: `@tasks:factumerit.app`
3. Click "Go"
4. Type a message: "Hello!"

**Expected response**:
```
👋 Hi! I'm the Vikunja task bot.

I can help you:
- Create tasks
- List your tasks
- Update task status
- Search tasks

Try: "create task buy groceries"
```

---

## Connecting Vikunja Account

### First-Time Setup

**Prerequisite**: You need a Vikunja account

**Steps**:
1. Go to https://vikunja.factumerit.app
2. Click "Login with Matrix" (or "Login with Factumerit")
3. Redirects to Authentik (or MAS directly if simplified)
4. Enter Matrix credentials
5. Grant permissions (email, Matrix ID)
6. Redirected back to Vikunja
7. Account created automatically!

**What happens**:
- Vikunja creates account using your Matrix email
- Bot stores your Vikunja API token (encrypted)
- You can now manage tasks via Matrix DM

---

### Linking Existing Vikunja Account

**Scenario**: You already have a Vikunja account, want to link it to Matrix bot

**Steps** (future feature):
1. DM `@tasks:factumerit.app`
2. Send: "link account"
3. Bot replies with one-time link
4. Click link, login to Vikunja
5. Authorize bot access
6. Bot stores your token

**Current workaround**: Use "Login with Matrix" to create new account, manually migrate tasks

---

## Common First-Time Issues

### Issue: "User not found" when DMing bot

**Cause**: Bot not registered yet, or federation issue

**Fix**:
1. Check bot address spelling: `@tasks:factumerit.app` (not `.com`)
2. Wait 30 seconds, try again (federation delay)
3. If persists, contact admin

---

### Issue: "No email address available" during Vikunja login

**Cause**: MAS not returning email claim (should be fixed by patch)

**Fix**:
1. Verify you have email set in Matrix account
2. Check email is verified (check inbox for verification email)
3. Try logout/login from Matrix client
4. If persists, contact admin

**Status**: Should be resolved by MAS patch (solutions-55jz)

---

### Issue: Bot doesn't respond to messages

**Cause**: Bot service down, or not monitoring DMs

**Fix**:
1. Check bot is online (presence indicator in Element)
2. Wait 1 minute (bot may be processing)
3. Try sending "help" or "ping"
4. If no response, contact admin

---

### Issue: Can't verify email

**Cause**: Email not sent, or spam filtered

**Fix**:
1. Check spam folder
2. Check email address is correct (typo?)
3. Request new verification email (future feature)
4. Contact admin to manually verify

---

## Bot Command Reference

### @tasks:factumerit.app (Vikunja Bot)

**Status**: Deployed (verification pending)

**Basic commands**:
```
create task <title>           - Create new task
list tasks                    - Show all tasks
show task <id>                - Show task details
update task <id> <status>     - Update task status
search tasks <query>          - Search tasks
help                          - Show all commands
```

**Examples**:
```
create task Buy groceries
list tasks due today
update task 42 done
search tasks project:work
```

---

### @research:factumerit.app (Research Bot)

**Status**: Future

**Planned commands**:
```
search <query>                - Search research library
show <finding-id>             - Show research finding
related <finding-id>          - Find related research
topics                        - List research topics
```

---

### @assistant:factumerit.app (General Assistant)

**Status**: Future

**Planned behavior**:
- Natural language interaction
- Routes to specialist bots as needed
- General Q&A, summarization, etc.

---

## Privacy & Data

### What Data is Stored?

| Data | Where | Encrypted? | Retention |
|------|-------|------------|-----------|
| Matrix account (username, email, password) | PostgreSQL (MAS) | Password: Yes (bcrypt) | Until account deleted |
| Matrix messages | PostgreSQL (Synapse) | No (unless E2EE room) | Indefinite |
| Vikunja API tokens | PostgreSQL (bot service) | Yes (Fernet) | Until unlinked |
| Bot command logs | Render logs | No | 7 days |

### Who Can See My Data?

- **Matrix messages**: Server admin (unless E2EE)
- **Vikunja tasks**: You + Vikunja collaborators
- **Bot commands**: Bot service + server admin

### How to Delete My Data?

**Delete Matrix account**:
1. Contact admin (no self-service yet)
2. Admin deactivates account via Synapse admin API
3. Messages remain (Matrix protocol limitation)

**Unlink Vikunja**:
1. DM bot: "unlink account" (future feature)
2. Bot deletes your API token
3. Vikunja account remains (delete separately in Vikunja)

---

## Getting Help

### Self-Service

- **Bot help**: Send "help" to any bot
- **Documentation**: https://github.com/ivantohelpyou/spawn-solutions/tree/main/analyses/synapse
- **Matrix help**: https://matrix.org/docs/chat_basics/matrix-for-im/

### Contact Admin

- **Matrix DM**: `@ivan:factumerit.app` (if registered)
- **Email**: ivan@ivantohelpyou.com
- **GitHub Issues**: https://github.com/ivantohelpyou/spawn-solutions/issues

---

## Related

- [01-PLATFORM_VISION.md](./01-PLATFORM_VISION.md) - Platform overview
- [04-SECURITY_MODEL.md](./04-SECURITY_MODEL.md) - Security & privacy details
- [Element User Guide](https://element.io/user-guide) - Matrix client help

