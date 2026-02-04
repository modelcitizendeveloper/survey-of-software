# Onboarding Quick Start

**Goal**: Get first test user up and running in 5 minutes

---

## Admin: Create Token (30 seconds)

### Step 1: Open Render Shell

https://dashboard.render.com/web/srv-d54s143e5dus73bqhpb0/shell

### Step 2: Create Token

```bash
mas manage issue-user-registration-token --uses-allowed 1
```

**Output**:
```
Registration token: mat_2J8xN4K9mP3qR7sT
```

### Step 3: Send to User

Email or DM the user:
- Registration token: `mat_2J8xN4K9mP3qR7sT`
- Registration URL: https://matrix.factumerit.app/register

---

## User: Register & Connect (5 minutes)

### 1. Register Matrix Account

Go to: https://matrix.factumerit.app/register

Fill in:
- Username: `alice`
- Email: `alice@example.com`
- Password: (min 8 chars)
- **Registration Token**: `mat_2J8xN4K9mP3qR7sT`

Verify email (check inbox).

---

### 2. Install Element

Download: https://element.io/download

Login:
- Homeserver: `matrix.factumerit.app`
- Username: `@alice:factumerit.app`
- Password: (from step 1)

---

### 3. Create Vikunja Account

Go to: https://vikunja.factumerit.app

Click **"Login with Factumerit"** → Enter Matrix credentials → Grant consent

---

### 4. Get API Token

In Vikunja:
1. Settings → API Tokens
2. Create new token: "Matrix Bot"
3. Check ALL permissions
4. Copy token (starts with `tk_...`)

---

### 5. Connect Bot

In Element, DM: `@eis:factumerit.app`

Send:
```
!vik tk_YOUR_TOKEN_HERE
```

Expected: `✅ Connected to Vikunja`

---

### 6. Test

```
!help
!stats
create task buy milk tomorrow
!now
```

---

## Done! 🎉

User can now manage tasks via Matrix DM.

---

## Admin: More Tokens

```bash
# Single-use (recommended)
mas manage issue-user-registration-token --uses-allowed 1

# 5-use token
mas manage issue-user-registration-token --uses-allowed 5

# List tokens
mas manage list-user-registration-tokens
```

---

## Troubleshooting

**"Invalid token"** → Create new token (single-use already consumed)

**"User not found" when DMing bot** → Check spelling: `@eis:factumerit.app`

**Bot doesn't respond** → Send `!test` to check connection

---

**Full guide**: See `SIMPLE_ONBOARDING_FLOW.md`

