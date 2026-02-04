# 30: Architecture Simplification Opportunity

**Date**: 2025-12-23
**Status**: ✅ Implemented (2025-12-23)

> **Outcome**: Authentik was deployed, then bypassed and torn down. Vikunja now connects directly to MAS. Saving $25/mo.
>
> See [vikunja-mas-login-lifecycle.md](./vikunja-mas-login-lifecycle.md) for the canonical system documentation.

---

## Current Architecture

```
Vikunja → Authentik → MAS (patched) → Synapse
```

**Monthly Cost**: $65
- Synapse+MAS: $7
- PostgreSQL: $7
- Authentik: $25
- Vikunja: $7
- Render Pro: $19

---

## Proposed Simplified Architecture

```
Vikunja → MAS (patched) → Synapse
```

**Monthly Cost**: $40 (-$25/mo savings)
- Synapse+MAS: $7
- PostgreSQL: $7
- Vikunja: $7
- Render Pro: $19

---

## Why This Works Now

### The MAS Patch Changed Everything

**Before patch (why Authentik was needed):**
- MAS userinfo: `{"sub":"...", "username":"..."}` ❌
- No email claim returned
- Vikunja couldn't create accounts (requires email)
- Authentik manually injected email as workaround

**After patch (current state):**
- MAS userinfo: `{"sub":"...", "username":"...", "email":"...", "email_verified":true}` ✅
- Email claim properly returned
- **Authentik's primary purpose (email workaround) is obsolete**

### What Authentik Currently Provides

1. ~~Email claim workaround~~ ← **Fixed by MAS patch**
2. ~~Scope translation~~ ← **Can configure Vikunja to only request `openid email`**
3. User management UI ← Nice-to-have, not essential
4. MFA support ← Not currently used
5. Audit logs ← Not currently used

**Verdict**: Paying $25/mo for features we're not using.

---

## Migration Plan

### Phase 1: Test Direct Connection (Low Risk)

**Goal**: Verify MAS patch works with Vikunja directly

**Steps**:
1. Create test Vikunja OIDC provider in MAS
2. Update Vikunja config to point to MAS instead of Authentik
3. Test login flow with test user
4. Verify email is populated in Vikunja user account

**Vikunja config change**:
```yaml
# OLD (via Authentik)
auth:
  openid:
    enabled: true
    providers:
      - name: Factumerit
        authurl: https://auth.factumerit.app/application/o/vikunja/
        clientid: "$VIKUNJA_OIDC_CLIENT_ID"
        clientsecret: "$VIKUNJA_OIDC_CLIENT_SECRET"
        scope: openid email profile

# NEW (direct to MAS)
auth:
  openid:
    enabled: true
    providers:
      - name: Matrix
        authurl: https://matrix.factumerit.app/
        clientid: "$MAS_VIKUNJA_CLIENT_ID"
        clientsecret: "$MAS_VIKUNJA_CLIENT_SECRET"
        scope: openid email  # Note: NO 'profile' - MAS doesn't support it
```

**MAS client registration**:
```bash
# In factumerit-matrix container
mas-cli manage register-client \
  --client-id <generate-ulid> \
  --redirect-uri https://vikunja.factumerit.app/auth/openid/matrix \
  --client-name "Vikunja Direct"
```

**Expected outcome**:
- ✅ Login flow completes
- ✅ Vikunja creates user with email from MAS
- ✅ No "No email address available" error

**If successful**: Proceed to Phase 2
**If fails**: Document failure, keep Authentik

### Phase 2: Cutover (Reversible)

**Goal**: Switch production Vikunja to MAS, deprecate Authentik

**Steps**:
1. Backup Vikunja database
2. Update Vikunja config to use MAS
3. Redeploy Vikunja
4. Test with existing users
5. Monitor for 1 week
6. If stable, shut down Authentik

**Rollback plan**:
- Revert Vikunja config to Authentik
- Redeploy Vikunja
- Authentik still running (don't delete until confirmed stable)

---

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| MAS scope incompatibility | Login fails | Only request `openid email` (no `profile`) |
| Existing users can't login | Service disruption | Test with new user first, keep Authentik running during migration |
| Email claim missing | Account creation fails | Verify patch deployed: `curl -H "Authorization: Bearer $TOKEN" https://matrix.factumerit.app/oauth2/userinfo` |
| Vikunja config error | Service down | Test in staging first, have rollback ready |

---

## Decision Criteria

**Proceed with simplification if:**
- ✅ MAS userinfo returns email claim (verify with curl)
- ✅ Test user can login to Vikunja via MAS
- ✅ Email is populated in Vikunja user account
- ✅ No errors in MAS or Vikunja logs

**Keep Authentik if:**
- ❌ MAS userinfo still missing email (patch not working)
- ❌ Vikunja requires `profile` scope (MAS doesn't support)
- ❌ Need MFA or advanced user management features
- ❌ Planning to add more apps that need Authentik features

---

## Alternative: Keep Authentik for Future Features

**Argument**: Even if not needed now, Authentik provides value for future apps

**Counter-argument**:
- YAGNI (You Aren't Gonna Need It) - $25/mo for unused features
- Can always re-deploy Authentik later if needed
- MAS is improving (upstream may fix email bug, add features)
- Simpler architecture = less to maintain

**Recommendation**: Simplify now, re-evaluate in 6 months

---

## Next Steps

1. **Verify MAS patch is working**:
   ```bash
   # Get access token from MAS
   TOKEN="<get-from-oauth-flow>"
   
   # Test userinfo endpoint
   curl -H "Authorization: Bearer $TOKEN" \
     https://matrix.factumerit.app/oauth2/userinfo
   
   # Should return:
   # {"sub":"...","username":"...","email":"...","email_verified":true}
   ```

2. **Create test MAS client for Vikunja**

3. **Test login flow with test user**

4. **Document results** in this file

5. **Decide**: Simplify or keep Authentik

---

## Related

- [ADR-022: Authentik as IdP Bridge](../development/projects/impl-1131-vikunja/vikunja-mcp/docs/adr/022-authentik-idp-bridge.md)
- [ADR-024: Patch MAS for Email Claims](../development/projects/impl-1131-vikunja/vikunja-mcp/docs/adr/024-patch-mas-for-email-claims.md)
- [25-ARCHITECTURE.md](25-ARCHITECTURE.md)

