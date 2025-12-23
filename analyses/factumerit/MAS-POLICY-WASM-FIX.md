# MAS Policy WASM Fix

**Date**: 2025-12-23  
**Issue**: solutions-xfke  
**Related**: solutions-55jz (MAS email patch)  
**Status**: Deployed (build in progress)

---

## 🐛 Problem

MAS service crashed on startup with:

```
Error: failed to open OPA WASM policy file
Caused by:
    No such file or directory (os error 2)
2025-12-23 09:21:25,910 WARN exited: mas (exit status 1; not expected)
```

**Impact**: MAS entered FATAL state, Synapse started but OIDC endpoints returned 502.

---

## 🔍 Root Cause

The Dockerfile built MAS from source (for email patch) but **didn't build or copy the OPA policy WASM file**.

**What was missing**:
1. Building the `mas-policy` package as WASM
2. Copying `policy.wasm` to `/usr/local/share/mas-cli/`

**Why it happened**:
- Original Dockerfile used official MAS image (included policy.wasm)
- Patched Dockerfile built from source but only copied:
  - MAS binary: `/usr/local/bin/mas` ✅
  - Frontend assets: `/usr/local/share/mas-cli` ✅
  - Policy WASM: **MISSING** ❌

---

## ✅ Solution

### Changes to Dockerfile

**After MAS binary build** (line 107):
```dockerfile
# Build the OPA policy WASM module
RUN rustup target add wasm32-unknown-unknown
RUN cargo build --release --target wasm32-unknown-unknown --package mas-policy
RUN mkdir -p /build/share && \
    cp target/wasm32-unknown-unknown/release/mas_policy.wasm /build/share/policy.wasm
```

**After copying official assets** (line 127):
```dockerfile
# Copy policy WASM from builder
COPY --from=mas-builder /build/share/policy.wasm /usr/local/share/mas-cli/policy.wasm
```

### Commit

```
commit 32d8e3e
Author: Ivan Schneider
Date:   2025-12-23

Fix: Add OPA policy WASM build to MAS

MAS was crashing with 'failed to open OPA WASM policy file' because
the policy.wasm wasn't being built or copied into the final image.
```

---

## 📊 Build Timeline

| Time | Event |
|------|-------|
| 09:21 | First deploy (eae98a3) - MAS crashes |
| 09:22 | Synapse starts, MAS in FATAL state |
| 16:28 | Issue identified from logs |
| 16:30 | Fix committed (32d8e3e) and pushed |
| 16:31 | Render build started |
| ~16:46 | Expected: Build complete (15-20 min) |

---

## 🧪 Verification

Once build completes, run:

```bash
./analyses/factumerit/verify-mas-patch.sh
```

**Expected**:
- ✅ OIDC discovery endpoint responds
- ✅ MAS service healthy (no crash loop)
- ✅ Userinfo endpoint structure correct (manual test)

---

## 📚 Lessons Learned

1. **When building from source, check ALL dependencies**
   - Not just the binary, but assets, configs, WASM modules, etc.

2. **Test locally before deploying**
   - Could have caught this with `docker build` locally
   - Render build time is 15-20 minutes per iteration

3. **Check logs immediately after deploy**
   - "Service is live" doesn't mean "service is working"
   - MAS was crash-looping while Synapse appeared healthy

4. **OPA policy is required for MAS**
   - Defines authorization rules for OAuth2 clients
   - Without it, MAS can't start

---

## 🔗 Related Documentation

- **MAS Email Patch**: `DEPLOY_PATCH.md` in factumerit-matrix repo
- **Deployment Lessons**: `analyses/synapse/03-DEPLOYMENT_LESSONS.md`
- **Verification Script**: `analyses/factumerit/verify-mas-patch.sh`

---

## 📝 Next Steps

1. ⏳ Wait for Render build (~15 min remaining)
2. ✅ Run verification script
3. ✅ Test Vikunja login flow
4. ✅ Update deployment docs with this lesson
5. ✅ Close solutions-xfke

