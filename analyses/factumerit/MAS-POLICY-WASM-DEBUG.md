# MAS Policy.wasm Debugging - Attempt 4

## Timeline

**Attempt 1** (commit 32d8e3e): Build policy as Rust WASM
- ❌ FAILED: `getrandom` crate doesn't support `wasm32-unknown-unknown`

**Attempt 2** (commit ede93d4): Download OPA and build from source  
- ❌ FAILED: 404 error on OPA download URL

**Attempt 3** (commit df7c17f): Copy from official image
- ❌ FAILED: Still getting "failed to open OPA WASM policy file"
- Deploy went live at 16:44 UTC
- MAS still crash-looping with same error

**Attempt 4** (commit 6c1027b): Debug - verify policy.wasm exists
- 🔍 IN PROGRESS: Added debug RUN commands to check if file exists
- Build started: ~17:00 UTC

## The Mystery

We're copying `/usr/local/share/mas-cli` from the official MAS image:

```dockerfile
COPY --from=mas-official /usr/local/share/mas-cli /usr/local/share/mas-cli
```

According to the official Dockerfile, this directory should contain:
- Frontend assets (templates, translations)
- **policy.wasm**

But MAS is still reporting:
```
Error: failed to open OPA WASM policy file
Caused by:
    No such file or directory (os error 2)
```

## Hypothesis

Either:
1. The official image doesn't actually have policy.wasm in that location
2. The COPY command isn't working as expected
3. MAS is looking in a different location than we think

## Debug Strategy

Added these commands to Dockerfile:
```dockerfile
RUN ls -la /usr/local/share/mas-cli/
RUN test -f /usr/local/share/mas-cli/policy.wasm && echo "✓ found" || echo "❌ MISSING"
```

This will show us exactly what's in the directory after the COPY.

## Next Steps

1. Wait for build to complete (~15 min)
2. Check build logs for debug output
3. If policy.wasm is missing: manually copy it or build it
4. If policy.wasm exists: check MAS config for path mismatch

---

**Status**: Waiting for build dep-d55cl12li9vc73c7c3r0
