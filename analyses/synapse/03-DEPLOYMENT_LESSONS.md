# 03: Synapse + MAS Deployment Lessons

**Date**: 2025-12-22
**Status**: Deployed (verification pending)
**Updated**: 2025-12-23 - MAS patched for email claims bug
**Context**: Deploying Synapse + MAS on Render for Vikunja OIDC

---

## Summary

Self-hosted Matrix homeserver with OIDC for "Login with Matrix" in external apps. Bundled Synapse + MAS + nginx in single container to save costs.

**Update 2025-12-23**: Discovered and patched MAS email claims bug. See "MAS Email Claims Bug" section below.

**Update 2025-12-24**: Enabled MSC4108 (QR code device sign-in). See "MSC4108 QR Code Sign-In" section below.

---

## Architecture Decisions

### ADR-020: Shared PostgreSQL, Separate Databases
- One Render PostgreSQL instance ($9/mo)
- Synapse uses `matrix` database (created by Render Blueprint)
- MAS uses `mas` database (created at container startup)
- Avoids table name conflicts (`users` exists in both)

### ADR-021: Synapse over Dendrite
- MAS only supports Synapse (not Dendrite)
- Higher RAM (~500MB vs ~100MB) but full OIDC support
- Required for "Login with Matrix" use case

---

## Critical nginx Routes for MAS

MAS exposes many endpoints. All must be routed through nginx to MAS (not Synapse):

```nginx
# REQUIRED MAS routes - missing any causes "No Such Resource" errors
location /.well-known/openid-configuration { proxy_pass http://mas; }
location /.well-known/webfinger { proxy_pass http://mas; }
location /authorize { proxy_pass http://mas; }  # OAuth authorize
location /token { proxy_pass http://mas; }      # OAuth token
location /oauth2/ { proxy_pass http://mas; }    # OAuth2 endpoints
location /login { proxy_pass http://mas; }
location /logout { proxy_pass http://mas; }
location /register { proxy_pass http://mas; }
location /account { proxy_pass http://mas; }
location /consent { proxy_pass http://mas; }    # OIDC consent screen
location /assets/ { proxy_pass http://mas; }
location /graphql { proxy_pass http://mas; }

# Matrix client login compatibility
location /_matrix/client/v3/login { proxy_pass http://mas; }
location /_matrix/client/r0/login { proxy_pass http://mas; }
```

**Lesson**: When OIDC flow fails with 404, check if MAS endpoint is being routed to Synapse by mistake.

---

## Render-Specific Issues

### 1. TLS Termination / X-Forwarded-Proto

Render terminates TLS at edge. Container receives HTTP on port 10000.

**Problem**: `proxy_set_header X-Forwarded-Proto $scheme` returns `http`, causing infinite redirect loops.

**Fix**: Hardcode to `https`:
```nginx
set $forwarded_proto https;
proxy_set_header X-Forwarded-Proto $forwarded_proto;
```

### 2. Port Leaking in Redirects

**Problem**: `return 302 /path` may include internal port (`:10000`) in Location header.

**Fix**: Use absolute URL:
```nginx
return 302 https://$host/path$is_args$args;
```

### 3. PostgreSQL Collation

**Problem**: Render PostgreSQL uses `en_US.UTF8`, Synapse wants `C`.

**Fix**: Add to Synapse config:
```yaml
database:
  allow_unsafe_locale: true
```

Safe because: single instance (no multi-region replica collation drift), Matrix data mostly ASCII.

### 4. DATABASE_URL Format

**Problem**: Render uses `postgresql://` (not `postgres://`) and may omit port.

**Fix**: Regex handles both:
```bash
if [[ "$DATABASE_URL" =~ postgres(ql)?://([^:]+):([^@]+)@([^:/]+)(:([0-9]+))?/([^?]+) ]]; then
    DB_PORT="${BASH_REMATCH[6]:-5432}"  # Default 5432
fi
```

---

## MAS Configuration

### Client IDs Must Be ULIDs
- 26 characters
- Crockford Base32 (no I, L, O, U)
- Example: `0000000000000000000SYNAPSE`

### Separate Database Required
Synapse and MAS both have `users` table. Cannot share database.

### Email for Registration
If `password_registration_enabled: true`, users must verify email.
Configure SMTP (e.g., Resend):
```yaml
email:
  transport: smtp
  mode: tls
  hostname: smtp.resend.com
  port: 465
  username: resend
  password: ${RESEND_API_KEY}
```

### Account Settings for Registration
```yaml
account:
  password_registration_enabled: true
  password_change_allowed: true
  email_change_allowed: true
  displayname_change_allowed: true
```

---

## OIDC Client Setup (Vikunja Example)

### MAS Side (mas.template.yaml)
```yaml
clients:
  - client_id: 0000000000000000000V1KYNJA
    client_auth_method: client_secret_post
    client_secret: ${VIKUNJA_OIDC_SECRET}
    redirect_uris:
      - https://vikunja.factumerit.app/auth/openid/matrix
```

### Client App Side (Vikunja config.yml)
```yaml
auth:
  local:
    enabled: false  # Optional: disable password login
  openid:
    enabled: true
    redirecturl: https://vikunja.factumerit.app/auth/openid/
    providers:
      - name: Matrix
        authurl: https://matrix.factumerit.app/
        clientid: "$VIKUNJA_OIDC_CLIENT_ID"
        clientsecret: "$VIKUNJA_OIDC_CLIENT_SECRET"
        scope: openid email  # NOT 'profile' - MAS default policy denies it!
```

### Allowed Scopes (MAS Default Policy)

Only these scopes are allowed by default:
- `openid` ✓
- `email` ✓
- `urn:mas:graphql:*` (GraphQL API)
- `urn:matrix:org.matrix.msc2967.client:api:*` (Matrix Client API)

**NOT allowed** (causes "authorization denied by policy"):
- `profile` ✗ - common OIDC scope but blocked by MAS default

**Gotcha**: If you update your client config to remove `profile` but the OIDC flow still fails, check that the client container was actually redeployed. The old config may be cached in the running container.

### Getting redirect_uri Right
1. Check what URL the client actually sends (browser Network tab)
2. Match exactly in MAS `redirect_uris`
3. Common mistake: `/callback` suffix mismatch

---

## Debugging Checklist

| Symptom | Likely Cause |
|---------|--------------|
| "No Such Resource" on MAS page | Missing nginx route to MAS |
| Redirect loop (ERR_TOO_MANY_REDIRECTS) | X-Forwarded-Proto not set to `https` |
| Port :10000 in URL | Relative redirect leaking internal port |
| "relation already exists" on startup | Synapse/MAS sharing database |
| OIDC "invalid redirect_uri" | redirect_uri mismatch in MAS config |
| Registration form missing | `password_registration_enabled: false` |
| Consent page 404 | Missing `/consent` route to MAS |
| "Authorization denied by policy" | Requested scope not allowed (e.g., `profile`) |
| "No email address available" (client) | MAS userinfo not returning email (see MAS Email Claims Bug) |
| GitGuardian warnings about .pem files | Committed test files from mas-patched/ directory |
| TypeError: MSC3861.__init__() got unexpected keyword | `msc4108_enabled` inside `msc3861` block (see MSC4108 section) |

---

## MSC4108 QR Code Sign-In

**Date**: 2025-12-24
**Status**: ✅ Working
**Feature**: Sign in to new devices by scanning QR code

### Configuration

MSC4108 must be enabled in **two places**:

#### 1. MAS (Matrix Authentication Service)

In `mas/mas.template.yaml`:

```yaml
experimental:
  # Enable OIDC Native Authentication (required for QR code login)
  oidc_native_authentication: true
```

#### 2. Synapse

In `synapse/homeserver.template.yaml`:

```yaml
experimental_features:
  # Enable QR code device sign-in (MSC4108)
  msc4108_enabled: true  # ✅ ONLY HERE, NOT inside msc3861!
  msc3861:
    enabled: true
    # DO NOT put msc4108_enabled here - it's not a valid MSC3861 parameter!
    issuer: "http://localhost:8080/"
    client_id: 0000000000000000000SYNAPSE
    # ... rest of config
```

### ⚠️ CRITICAL: Config Gotcha

**WRONG (causes crash):**
```yaml
experimental_features:
  msc4108_enabled: true
  msc3861:
    enabled: true
    msc4108_enabled: true  # ❌ INVALID - MSC3861 class doesn't accept this!
```

**Error:**
```
TypeError: MSC3861.__init__() got an unexpected keyword argument 'msc4108_enabled'
```

**RIGHT:**
```yaml
experimental_features:
  msc4108_enabled: true  # ✅ Only at top level
  msc3861:
    enabled: true
    # No msc4108_enabled here!
```

### How It Works

1. **User initiates QR login** in Element (Settings → Sessions → Link new device)
2. **Element generates QR code** with OIDC authorization URL
3. **User scans QR** with new device
4. **MAS handles OIDC flow** (oidc_native_authentication)
5. **Synapse validates** via MSC4108 + MSC3861 delegation
6. **New device authenticated** without password

### Testing

**In Element Web:**
1. Go to Settings → Sessions
2. Click "Link new device"
3. Should see "Sign in with QR code" option
4. Scan with mobile device
5. Should redirect to MAS login/consent flow

**Known Issue:**
- QR code redirects to homepage (`/`) instead of Element Web (`/chat`)
- This is cosmetic - the authentication still works
- User can manually navigate to `/chat` after login

### Troubleshooting

| Issue | Solution |
|-------|----------|
| "QR code not supported" in Element | Check `msc4108_enabled: true` in Synapse config |
| Synapse crashes on startup | Remove `msc4108_enabled` from inside `msc3861` block |
| QR code shows but fails | Check MAS has `oidc_native_authentication: true` |
| Redirects to wrong page | Known issue, user can navigate manually |

### References

- [MSC4108: OIDC Native Flow](https://github.com/matrix-org/matrix-spec-proposals/pull/4108)
- [Synapse Issue #18027](https://github.com/element-hq/synapse/issues/18027) (misleading - suggests putting in both places)
- Synapse source: `synapse/config/experimental.py` line 510 (MSC3861 class definition)

### Deployment History

- **2025-12-24 09:25** - Commit 444a2c4: Added MSC4108 (broke - had it in both places)
- **2025-12-24 18:19** - Commit 0753b7e: Fixed (removed from msc3861 block)
- **2025-12-24 18:22** - Deploy successful, QR code working ✅

---

## File Structure

```
factumerit-matrix/
├── Dockerfile           # Multi-stage: MAS binary + Synapse base + nginx
├── nginx.conf           # Routes MAS vs Synapse endpoints
├── supervisord.conf     # Runs nginx, mas, synapse
├── start.sh             # Creates MAS database, generates configs
├── synapse/
│   ├── homeserver.template.yaml  # MSC3861 MAS delegation
│   └── log.config
├── mas/
│   └── mas.template.yaml         # Clients, auth, email
├── static/
│   └── index.html       # Landing page
└── render.yaml          # Blueprint
```

---

## Cost Summary

| Component | Plan | Monthly |
|-----------|------|---------|
| factumerit-matrix (Synapse+MAS) | Starter 512MB | $7 |
| factumerit-db (PostgreSQL) | Basic 256MB | $7 |
| **Total** | | **$14/mo** |

May need to upgrade to Standard ($25) if RAM constrained under load.

---

## Related

- [01-PLATFORM_VISION.md](./01-PLATFORM_VISION.md) - Multi-project bot vision
- [02-SYNAPSE_CAPABILITIES.md](./02-SYNAPSE_CAPABILITIES.md) - Capabilities gained
- ADR-020: Shared PostgreSQL Strategy
- ADR-021: Synapse over Dendrite
