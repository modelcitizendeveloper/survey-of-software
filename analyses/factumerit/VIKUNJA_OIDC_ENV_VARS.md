# Vikunja OpenID Connect (OIDC) Environment Variables

Configuration guide for Vikunja OIDC authentication with MAS (Matrix Authentication Service).

## Source Documentation

- [Vikunja OpenID Documentation](https://vikunja.io/docs/openid/)
- [OpenID Example Configurations](https://vikunja.io/docs/openid-example-configurations/)
- [Full Configuration Options](https://vikunja.io/docs/config-options/#auth)

## Required Environment Variables

All OIDC configuration uses environment variables with the prefix `VIKUNJA_AUTH_OPENID_`.

### Enable OIDC (Required!)

```bash
VIKUNJA_AUTH_OPENID_ENABLED=true
```

**Critical**: Without this, OIDC login will not appear. Login will redirect to password reset instead.

### Provider Configuration

Each provider is configured with a numeric index (0 for first provider):

```bash
# Provider name (used in redirect URL - see below)
VIKUNJA_AUTH_OPENID_PROVIDERS_0_NAME=Factumerit

# Display name shown on login button
VIKUNJA_AUTH_OPENID_PROVIDERS_0_LOGOUTURL=  # Optional

# OIDC endpoints from your identity provider
VIKUNJA_AUTH_OPENID_PROVIDERS_0_AUTHURL=https://matrix.factumerit.app/_matrix/client/v3/auth
VIKUNJA_AUTH_OPENID_PROVIDERS_0_TOKENURL=https://matrix.factumerit.app/oauth2/token
VIKUNJA_AUTH_OPENID_PROVIDERS_0_CLIENTID=your-client-id
VIKUNJA_AUTH_OPENID_PROVIDERS_0_CLIENTSECRET=your-client-secret
```

### Redirect URL

```bash
VIKUNJA_AUTH_OPENID_REDIRECTURL=https://vikunja.factumerit.app/auth/openid/factumerit
```

**Important**: The redirect URL path uses the **lowercase** provider name:

- Provider name: `Factumerit`
- Redirect path: `/auth/openid/factumerit` (lowercase!)

From [Vikunja OpenID Example Configurations](https://vikunja.io/docs/openid-example-configurations/):
> Use the `name` field value (lowercase) as the identifier in the redirect URL path.

### Complete Example

For MAS at `matrix.factumerit.app` with Vikunja at `vikunja.factumerit.app`:

```bash
# Enable OIDC
VIKUNJA_AUTH_OPENID_ENABLED=true

# Redirect URL (lowercase provider name in path!)
VIKUNJA_AUTH_OPENID_REDIRECTURL=https://vikunja.factumerit.app/auth/openid/factumerit

# Provider 0: Factumerit (MAS)
VIKUNJA_AUTH_OPENID_PROVIDERS_0_NAME=Factumerit
VIKUNJA_AUTH_OPENID_PROVIDERS_0_AUTHURL=https://matrix.factumerit.app/_matrix/client/v3/auth
VIKUNJA_AUTH_OPENID_PROVIDERS_0_TOKENURL=https://matrix.factumerit.app/oauth2/token
VIKUNJA_AUTH_OPENID_PROVIDERS_0_CLIENTID=your-vikunja-client-id
VIKUNJA_AUTH_OPENID_PROVIDERS_0_CLIENTSECRET=your-vikunja-client-secret
```

## MAS Client Registration

Register Vikunja as an OAuth client in MAS configuration:

```yaml
# mas/config.yaml
clients:
  - client_id: your-vikunja-client-id
    client_auth_method: client_secret_post
    client_secret: your-vikunja-client-secret
    redirect_uris:
      - https://vikunja.factumerit.app/auth/openid/factumerit
```

## Finding OIDC Endpoints

Query your MAS OpenID configuration:

```bash
curl https://matrix.factumerit.app/.well-known/openid-configuration
```

This returns endpoints including:
- `authorization_endpoint` → use for `AUTHURL`
- `token_endpoint` → use for `TOKENURL`

## Troubleshooting

### Login redirects to password-reset instead of OIDC

**Cause**: `VIKUNJA_AUTH_OPENID_ENABLED` is not set to `true`.

**Fix**: Add `VIKUNJA_AUTH_OPENID_ENABLED=true` to environment.

### "Invalid redirect_uri" error

**Cause**: Redirect URL mismatch between Vikunja and MAS.

**Fix**:
1. Ensure `VIKUNJA_AUTH_OPENID_REDIRECTURL` uses lowercase provider name
2. Ensure MAS client `redirect_uris` matches exactly
3. Check for trailing slashes (should not have one)

### Token exchange fails

**Cause**: Missing or incorrect `TOKENURL`.

**Fix**: Ensure `VIKUNJA_AUTH_OPENID_PROVIDERS_0_TOKENURL` is set to the correct token endpoint from your OIDC provider's `.well-known/openid-configuration`.

## Multiple Providers

To add additional OIDC providers, increment the index:

```bash
# Provider 1: Another IdP
VIKUNJA_AUTH_OPENID_PROVIDERS_1_NAME=Google
VIKUNJA_AUTH_OPENID_PROVIDERS_1_AUTHURL=https://accounts.google.com/o/oauth2/v2/auth
VIKUNJA_AUTH_OPENID_PROVIDERS_1_TOKENURL=https://oauth2.googleapis.com/token
VIKUNJA_AUTH_OPENID_PROVIDERS_1_CLIENTID=google-client-id
VIKUNJA_AUTH_OPENID_PROVIDERS_1_CLIENTSECRET=google-client-secret
```

---

Last updated: 2025-12-25
