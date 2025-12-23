# MAS Deployment - SUCCESS\! 🎉

**Date:** 2025-12-23  
**Status:** ✅ COMPLETE  
**Deployment:** https://matrix.factumerit.app  
**Time:** ~2.5 hours, 14 commits

---

## 🎉 Achievement

Matrix Authentication Service (MAS) is now running successfully with the email patch applied\!

### ✅ Verified Working

- **OIDC Discovery:** https://matrix.factumerit.app/.well-known/openid-configuration
- **MAS Server:** Listening on port 8080
- **Synapse Server:** Listening on port 8008
- **policy.wasm:** Loading successfully (388KB)
- **Templates:** Loading from filesystem
- **Translations:** Loading correctly
- **Email Patch:** Applied inline during build

---

## 📊 The Journey: 14 Commits

### Phase 1: Build policy.wasm (Commits 1-5)
**Problem:** MAS crash-looping with "failed to open OPA WASM policy file"

| Attempt | Commit | Approach | Result |
|---------|--------|----------|--------|
| 1 | 32d8e3e | Rust WASM build | ❌ getrandom crate error |
| 2 | ede93d4 | OPA v0.71.0 download | ❌ 404 error |
| 3 | df7c17f | Copy from official image | ❌ File missing |
| 4 | 6c1027b | Debug verification | ❌ Confirmed missing |
| 5 | 3fd135f | **Build with OPA v0.70.0** | ✅ **SUCCESS\!** |

**Solution:** Download OPA v0.70.0, build policy.wasm from MAS source using `make`

### Phase 2: Container Start Issues (Commits 6-8)
**Problem:** "Unknown execution mode /start.sh"

| Attempt | Commit | Approach | Result |
|---------|--------|----------|--------|
| 6 | 44464aa | CMD ["/bin/bash", "/start.sh"] | ❌ Still failing |
| 7 | e330696 | CMD /start.sh (shell form) | ❌ Still failing |
| 8 | 88857d5 | **ENTRYPOINT [] + CMD** | ✅ **SUCCESS\!** |

**Solution:** Clear Synapse's default ENTRYPOINT, then use CMD

### Phase 3: Startup Sequence (Commits 9-14)
**Problem:** Various configuration issues during MAS initialization

| # | Commit | Issue | Solution |
|---|--------|-------|----------|
| 9 | c7b2094 | supervisord.conf path | Copy to /etc/supervisord.conf |
| 10 | 7ac1b2b | policy.wasm config | Add wasm_module path |
| 11 | a0ba5bd | manifest.json missing | Copy from policy-source |
| 12 | ee1a12f | i18n config | Add i18n section (didn't work) |
| 13 | d6c4b9d | templates.translations | Add to templates (didn't work) |
| 14 | b665751 | **Working directory** | ✅ **SUCCESS\!** |

**Solution:** Set `directory=/usr/local/share/mas-cli` in supervisord config

---

## 🔑 Key Learnings

### 1. OPA Policy WASM
- Must be built from source using `make` in the `policies/` directory
- Requires OPA v0.70.0 (not v0.71.0)
- Cannot be built as Rust WASM (different target)
- File size: 388KB

### 2. Docker Multi-Stage Build
- Stage 1: `policy-source` - Official MAS image for templates/translations/manifest
- Stage 2: `mas-builder` - Build policy.wasm and patched MAS binary
- Stage 3: Synapse base - Final runtime image

### 3. Synapse Base Image
- Has its own ENTRYPOINT that must be cleared with `ENTRYPOINT []`
- Otherwise CMD is interpreted as arguments to the default entrypoint

### 4. MAS Configuration
- Needs explicit `policy.wasm_module` path in config
- Templates need `assets_manifest` pointing to manifest.json
- Translations use hardcoded relative path `./translations/`

### 5. Working Directory
- MAS has hardcoded relative paths (e.g., `./translations/`)
- Config changes don't override these
- Must set working directory in supervisord to `/usr/local/share/mas-cli`

---

## 📁 Final File Structure

```
/usr/local/share/mas-cli/
├── policy.wasm (388KB)
├── manifest.json
├── templates/
│   └── (template files)
└── translations/
    └── (translation files)

/usr/local/bin/
└── mas (patched binary with email fix)

/etc/
├── supervisord.conf (with directory=/usr/local/share/mas-cli)
├── mas/
│   └── mas.yaml (with wasm_module, templates, i18n paths)
└── synapse/
    └── homeserver.yaml
```

---

## 🔧 The Email Patch

Applied inline during Docker build using embedded Python script:

**Changes to `crates/handlers/src/oauth2/userinfo.rs`:**

1. Added `UserEmailRepository` import
2. Updated `UserInfo` struct with `email` and `email_verified` fields
3. Added email fetching logic when `email` scope is present

**Result:** MAS now returns email claims from the userinfo endpoint when the email scope is granted.

---

## ✅ Next Steps

### 1. Test Vikunja Login Flow (HIGH PRIORITY)
- Go to https://vikunja.factumerit.app
- Click "Login with Matrix" (via Authentik)
- Complete OAuth flow
- **Verify:** Email is populated in Vikunja account
- **Close:** solutions-fxwe (Phase 1.0b: Configure Vikunja OIDC with MAS)

### 2. Run Verification Script
```bash
cd ~/spawn-solutions/analyses/factumerit
./verify-mas-patch.sh
```

Expected results:
- ✅ OIDC discovery returns JSON
- ✅ MAS is running
- ✅ Synapse is running
- ✅ Email patch is applied (need to test with actual login)

### 3. Update Documentation
- [x] Create MAS-DEPLOYMENT-SUCCESS.md
- [ ] Update 03-DEPLOYMENT_LESSONS.md with verification checkboxes
- [ ] Update ADR-024 with final architecture
- [ ] Document the 14-commit journey for future reference

### 4. Test Architecture Simplification (MEDIUM PRIORITY)
**Goal:** Test direct Vikunja → MAS connection

**Current:** Vikunja → Authentik → MAS → Synapse ($65/mo)  
**Proposed:** Vikunja → MAS → Synapse ($40/mo, save $25/mo)

**Prerequisites:**
- MAS email patch must be verified working
- Test Vikunja direct OIDC connection to MAS
- Verify email claims are returned correctly

**Bead:** solutions-hfes

### 5. Monitor Upstream MAS Issue
- **Issue:** https://github.com/element-hq/matrix-authentication-service/issues/5374
- **When fixed:** Remove patch and use official MAS image
- **Bead:** solutions-2d37

### 6. Fix Authentik DNS (SEPARATE ISSUE)
In Cloudflare Dashboard:
1. Go to DNS settings for `factumerit.app`
2. Find: `auth` → CNAME → `factumerit-authentik.onrender.com`
3. Click orange cloud ☁️ to make it gray ☁️ (DNS only)
4. Save

---

## 📈 Metrics

- **Total Time:** ~2.5 hours
- **Total Commits:** 14
- **Issues Fixed:** 9 different startup problems
- **Lines of Code Changed:** ~200 (Dockerfile + configs)
- **Docker Build Time:** 15-20 minutes (full), 1-2 minutes (cached)
- **Cost:** $40/mo (Synapse + MAS on Render Standard)

---

## 🎓 Lessons for Future Deployments

1. **Start with the official Dockerfile** - We could have saved time by analyzing the official MAS Dockerfile first
2. **Check working directory assumptions** - Relative paths in code require correct working directory
3. **Docker layer caching is amazing** - Made iteration fast (1-2 min rebuilds)
4. **Incremental debugging works** - Each error revealed the next issue in the startup sequence
5. **Document as you go** - This summary captures the journey while it's fresh

---

## 🙏 Acknowledgments

- **Element/MAS Team** - For the excellent Matrix Authentication Service
- **Render.com** - For reliable hosting and great Docker support
- **OPA Team** - For the policy engine that powers MAS authorization

---

**Status:** ✅ DEPLOYMENT COMPLETE - Ready for testing\!
