# MAS Policy.wasm Solution - Attempt 5

## The Problem

MAS crash-looping on startup with:
```
Error: failed to open OPA WASM policy file
Caused by:
    No such file or directory (os error 2)
```

MAS expects policy.wasm at: `/usr/local/share/mas-cli/policy.wasm`

## Failed Attempts (1-4)

### Attempt 1: Build as Rust WASM (commit 32d8e3e)
```dockerfile
RUN rustup target add wasm32-unknown-unknown
RUN cargo build --release --target wasm32-unknown-unknown --package mas-policy
```
**Result:** ❌ FAILED - `getrandom` crate doesn't support `wasm32-unknown-unknown`

### Attempt 2: Download OPA and build (commit ede93d4)
```dockerfile
ADD --chmod=755 https://github.com/open-policy-agent/opa/releases/download/v0.71.0/opa_linux_amd64_static /usr/local/bin/opa
```
**Result:** ❌ FAILED - 404 error (v0.71.0 doesn't exist or wrong URL)

### Attempt 3: Copy from official image (commit df7c17f)
```dockerfile
COPY --from=mas-official /usr/local/share/mas-cli /usr/local/share/mas-cli
```
**Result:** ❌ FAILED - policy.wasm still missing (file not in official image at that path)

### Attempt 4: Debug verification (commit 6c1027b)
Added debug commands to verify file existence.
**Result:** ❌ FAILED - Confirmed policy.wasm is missing

## Solution: Attempt 5 (commit 3fd135f)

### Strategy

Build policy.wasm ourselves using OPA, following the official MAS Dockerfile approach.

### Key Changes

1. **Download OPA v0.70.0** (known good version):
```dockerfile
RUN curl -L -o /usr/local/bin/opa \
    https://github.com/open-policy-agent/opa/releases/download/v0.70.0/opa_linux_amd64_static \
    && chmod +x /usr/local/bin/opa
```

2. **Build policy from source**:
```dockerfile
WORKDIR /build/policies
RUN make -B && chmod a+r ./policy.wasm
```

3. **Explicitly copy policy.wasm**:
```dockerfile
COPY --from=mas-builder /build/policies/policy.wasm /usr/local/share/mas-cli/policy.wasm
```

4. **Verify it exists** (fail build if missing):
```dockerfile
RUN test -f /usr/local/share/mas-cli/policy.wasm && \
    echo "✓ policy.wasm found" || \
    (echo "❌ policy.wasm MISSING" && exit 1)
```

5. **Copy frontend assets from official image**:
```dockerfile
COPY --from=policy-source /usr/local/share/mas-cli/templates /usr/local/share/mas-cli/templates
COPY --from=policy-source /usr/local/share/mas-cli/translations /usr/local/share/mas-cli/translations
```

### Why This Works

The official MAS Dockerfile builds policy.wasm using OPA and a Makefile in the `policies/` directory. We're replicating that exact process:

1. Clone MAS source (includes `policies/` directory with Rego files)
2. Download OPA binary
3. Run `make` in `policies/` directory (compiles Rego → WASM)
4. Copy the built `policy.wasm` to the final image

### Build Status

- **Commit:** 3fd135f
- **Started:** ~17:22 UTC
- **ETA:** ~17:37-17:42 UTC (15-20 minutes)
- **Status:** 🔄 IN PROGRESS

### Next Steps

1. Wait for build to complete
2. Check if MAS starts successfully
3. Test OIDC discovery endpoint
4. Run full verification script
5. Test Vikunja login flow

---

**This should be the final fix\!** 🤞
