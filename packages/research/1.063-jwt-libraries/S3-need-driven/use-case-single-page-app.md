# Use Case 4: Single Page Application Authentication

## Scenario Description

A React/Vue/Angular SPA that authenticates users and maintains session state
across page refreshes and browser tabs. Backend issues access tokens (short-lived)
and refresh tokens (long-lived). SPA stores tokens in memory/localStorage and
handles token refresh flows automatically.

## Concrete Requirements (Reality-Based)

### Authentication Flow
1. User submits login credentials in SPA
2. Backend validates credentials
3. Backend issues access_token (JWT, 15-min expiry) + refresh_token (opaque, 7-day expiry)
4. SPA stores access_token in memory, refresh_token in httpOnly cookie
5. SPA includes access_token in API requests
6. When access_token expires, SPA uses refresh_token to get new access_token
7. SPA validates access_token structure before using (basic checks)
8. Backend validates access_token signature on each API request

### Browser Constraints
- Tokens must survive page refresh (need localStorage/cookie)
- Must work across multiple tabs (shared state)
- XSS protection (don't expose tokens to malicious scripts)
- CSRF protection (especially for refresh token)
- Token auto-refresh without user interaction

## Must-Have Requirements (Non-Negotiable)

**R1: Client-Side Token Handling (JavaScript/TypeScript)**
- Decode JWT to check expiration (without verifying signature)
- Extract claims from JWT (user_id, roles, email)
- Determine if token is expired or about to expire
- No signature verification on client (secret not available)
- TypeScript type definitions for better DX

**R2: Token Refresh Logic**
- Detect token expiration before making request
- Automatically refresh token if expired (call /refresh endpoint)
- Queue concurrent requests during refresh (avoid multiple refresh calls)
- Retry failed requests after successful refresh
- Handle refresh token expiration (redirect to login)

**R3: Backend Token Generation (HS256)**
- Issue access_token with user claims and short expiration
- Issue refresh_token (opaque string, stored in database)
- Validate access_token signature on protected endpoints
- Exchange valid refresh_token for new access_token
- Invalidate refresh_token on logout

**R4: Security**
- Access tokens in memory (cleared on tab close, reduces XSS risk)
- Refresh tokens in httpOnly cookie (not accessible to JavaScript)
- CSRF tokens for refresh endpoint
- No sensitive data in JWT payload (tokens may be logged)
- Short access token lifetime (15-30 minutes)

**R5: User Experience**
- Silent token refresh (no user interaction)
- Seamless cross-tab synchronization (login in one tab, works in all)
- Automatic logout on refresh token expiration
- Loading states during authentication

### Nice-to-Have Requirements (Desirable)

**R6: Token Revocation**
- Logout invalidates all refresh tokens for user
- Admin can revoke specific user's tokens
- Token version/family tracking (detect stolen refresh tokens)

**R7: Fingerprinting**
- Bind refresh token to browser fingerprint
- Detect token theft (used from different device)
- Optional device management (view/revoke active sessions)

**R8: Offline Support**
- Cache user data when token valid
- Show cached data when offline
- Refresh token when back online

## Validation Tests

### Test 1: Decode Without Verification (Client-Side)
```python
# Client needs to check expiration, not verify signature
token = "eyJhbGc...valid.jwt.here"

# Decode without verification
decoded = library.decode(token, options={"verify_signature": False})
assert decoded["user_id"] == 123
assert decoded["exp"] > time.time()  # Not expired

# Must NOT require secret key for decode-only
```

### Test 2: Access Token Generation (Backend)
```python
secret = "backend-secret-key"
payload = {
    "user_id": 123,
    "email": "user@example.com",
    "roles": ["user"],
    "exp": datetime.utcnow() + timedelta(minutes=15),
    "iat": datetime.utcnow(),
    "type": "access"
}
access_token = library.encode(payload, secret, algorithm="HS256")
```

### Test 3: Token Refresh Flow (Backend)
```python
# Validate refresh token (from database)
refresh_token = request.cookies.get("refresh_token")
token_data = database.get_refresh_token(refresh_token)

if not token_data or token_data.expired:
    raise Unauthorized("Invalid refresh token")

# Issue new access token
new_access_token = create_access_token(token_data.user_id)
return {"access_token": new_access_token}
```

### Test 4: Expiration Check Before Use (Client)
```python
def is_token_expired(token: str, buffer_seconds: int = 60) -> bool:
    """Check if token expired or expires soon"""
    try:
        decoded = library.decode(token, options={"verify_signature": False})
        exp = decoded.get("exp")
        if not exp:
            return True
        return exp < (time.time() + buffer_seconds)
    except:
        return True  # Malformed token = expired

# Usage in API client
if is_token_expired(access_token, buffer_seconds=60):
    access_token = await refresh_token()
```

### Test 5: Concurrent Request Handling
```python
# Multiple requests made simultaneously while token expired
# Should only trigger ONE refresh, queue others

refresh_in_progress = None

async def get_valid_token():
    global refresh_in_progress

    if is_token_expired(access_token):
        if refresh_in_progress is None:
            refresh_in_progress = refresh_access_token()

        access_token = await refresh_in_progress
        refresh_in_progress = None

    return access_token

# Multiple concurrent calls
results = await asyncio.gather(
    api_call_1(),  # Triggers refresh
    api_call_2(),  # Waits for same refresh
    api_call_3()   # Waits for same refresh
)
# Only ONE refresh call made to backend
```

## Acceptance Criteria

A library is acceptable for this use case if:
1. Can decode JWT without verification (client-side)
2. Can encode/decode with HS256 (backend)
3. Provides easy access to exp claim for expiration checks
4. Works in both Python (backend) and JavaScript (frontend) OR
5. Python backend library + complementary JavaScript library exist
6. TypeScript definitions available for frontend library

## Edge Cases and Failure Modes

### Edge Case 1: Token Refresh Race Condition
- User has 3 tabs open
- Access token expires
- All 3 tabs try to refresh simultaneously
- Multiple refresh requests with same refresh_token
- Solution: Backend makes refresh token single-use (rotate on refresh)

### Edge Case 2: Refresh Token Stolen
- Attacker steals refresh_token from cookie
- Both user and attacker refresh tokens
- Detect: Refresh token used twice (one is stolen)
- Response: Invalidate entire token family, force re-login

### Edge Case 3: Clock Skew (Client vs Server)
- Client clock is 5 minutes fast
- Client thinks token expired, tries to refresh
- Token still valid on server
- Solution: Add buffer to client-side expiration check (refresh 1 minute early)

### Edge Case 4: Background Tab Token Expiration
- User has tab in background for 2 hours
- Access token and refresh token both expired
- Tab becomes active, makes API call
- Response: 401, redirect to login (clean expired state)

### Edge Case 5: Cross-Tab Logout
- User logs out in Tab 1
- Tab 2 still has access_token in memory
- Tab 2 makes request with valid access_token
- Backend invalidated refresh_token but access_token still valid until expiry
- Solution: Use short access token lifetime OR implement token blacklist

### Edge Case 6: Refresh During Request
- Long-running API request (file upload, 30 seconds)
- Access token expires during upload
- Request fails with 401
- Solution: Validate token before starting, accept slight overage on server

## Anti-Requirements (Avoid Over-Engineering)

**AR1: Client-Side Signature Verification**
- Client can't verify signature (secret not available in browser)
- Only server verifies signatures
- Client only decodes to check expiration

**AR2: JWT Refresh Tokens**
- Refresh tokens should be opaque (random string)
- JWT refresh tokens can't be revoked without database lookup
- Use simple random token + database lookup for refresh

**AR3: Complex Token Storage**
- Don't build elaborate token storage abstraction
- Simple: access_token in memory, refresh_token in cookie
- Avoid localStorage for access_token (XSS risk)

**AR4: Multiple Token Types**
- Don't need separate tokens for different API scopes
- Single access_token with roles/permissions is sufficient
- Avoid OAuth 2.0 scope complexity for simple SPA

## Implementation Footprint

### Backend (Python/FastAPI)
```python
import library
from datetime import datetime, timedelta
import secrets

SECRET_KEY = "strong-random-secret"
REFRESH_TOKEN_TTL = timedelta(days=7)
ACCESS_TOKEN_TTL = timedelta(minutes=15)

def create_access_token(user_id: int, email: str, roles: list) -> str:
    payload = {
        "user_id": user_id,
        "email": email,
        "roles": roles,
        "exp": datetime.utcnow() + ACCESS_TOKEN_TTL,
        "iat": datetime.utcnow(),
        "type": "access"
    }
    return library.encode(payload, SECRET_KEY, algorithm="HS256")

def create_refresh_token(user_id: int) -> str:
    token = secrets.token_urlsafe(32)
    database.store_refresh_token(
        token=token,
        user_id=user_id,
        expires_at=datetime.utcnow() + REFRESH_TOKEN_TTL
    )
    return token

@app.post("/login")
async def login(credentials: LoginRequest, response: Response):
    user = authenticate(credentials.email, credentials.password)
    if not user:
        raise Unauthorized("Invalid credentials")

    access_token = create_access_token(user.id, user.email, user.roles)
    refresh_token = create_refresh_token(user.id)

    # Set refresh token in httpOnly cookie
    response.set_cookie(
        "refresh_token",
        refresh_token,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=REFRESH_TOKEN_TTL.total_seconds()
    )

    return {"access_token": access_token}

@app.post("/refresh")
async def refresh(request: Request):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise Unauthorized("No refresh token")

    token_data = database.get_refresh_token(refresh_token)
    if not token_data or token_data.expires_at < datetime.utcnow():
        raise Unauthorized("Invalid or expired refresh token")

    # Rotate refresh token (invalidate old, issue new)
    database.invalidate_refresh_token(refresh_token)
    new_refresh_token = create_refresh_token(token_data.user_id)

    user = database.get_user(token_data.user_id)
    access_token = create_access_token(user.id, user.email, user.roles)

    response.set_cookie("refresh_token", new_refresh_token, ...)
    return {"access_token": access_token}

def validate_access_token(token: str) -> dict:
    try:
        return library.decode(token, SECRET_KEY, algorithms=["HS256"])
    except library.ExpiredSignatureError:
        raise Unauthorized("Token expired")
    except library.InvalidTokenError:
        raise Unauthorized("Invalid token")
```

### Frontend (TypeScript with hypothetical JS library)
```typescript
import { jwtDecode } from 'jwt-decode';  // Hypothetical library

let accessToken: string | null = null;
let refreshPromise: Promise<string> | null = null;

function isTokenExpired(token: string, bufferSeconds = 60): boolean {
  try {
    const decoded = jwtDecode<{ exp: number }>(token);
    const now = Math.floor(Date.now() / 1000);
    return decoded.exp < (now + bufferSeconds);
  } catch {
    return true;
  }
}

async function refreshAccessToken(): Promise<string> {
  const response = await fetch('/refresh', {
    method: 'POST',
    credentials: 'include'  // Include cookies
  });

  if (!response.ok) {
    // Refresh token expired or invalid
    window.location.href = '/login';
    throw new Error('Refresh failed');
  }

  const data = await response.json();
  accessToken = data.access_token;
  return accessToken;
}

async function getValidToken(): Promise<string> {
  if (!accessToken || isTokenExpired(accessToken)) {
    if (!refreshPromise) {
      refreshPromise = refreshAccessToken();
    }
    accessToken = await refreshPromise;
    refreshPromise = null;
  }
  return accessToken;
}

async function apiCall(endpoint: string, options: RequestInit = {}) {
  const token = await getValidToken();

  const response = await fetch(endpoint, {
    ...options,
    headers: {
      ...options.headers,
      'Authorization': `Bearer ${token}`
    }
  });

  if (response.status === 401) {
    // Token might have expired during request, try refresh
    accessToken = null;
    const newToken = await getValidToken();
    return fetch(endpoint, {
      ...options,
      headers: {
        ...options.headers,
        'Authorization': `Bearer ${newToken}`
      }
    });
  }

  return response;
}
```

Total: ~120 lines backend + ~60 lines frontend = 180 lines.

## Library Requirements Summary

For this use case, we need:
1. **Backend**: Full JWT library (encode/decode with HS256, signature verification)
2. **Frontend**: Lightweight JWT decoder (no verification, just parse + decode)

The frontend doesn't need a full JWT library - just ability to decode
and read claims (especially `exp`). Many SPAs use `jwt-decode` NPM package
(~500 bytes) instead of full JWT library.

Backend library must be same as Use Case 1 (REST API authentication).
