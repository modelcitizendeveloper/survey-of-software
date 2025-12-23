# 05: Monitoring & Operations Runbook

**Date**: 2025-12-23
**Status**: Draft
**Context**: Operational monitoring for Synapse + MAS + bot services

---

## Health Check Endpoints

### Synapse

```bash
# Health check
curl https://matrix.factumerit.app/_synapse/health
# Expected: {"status": "OK"}

# Version info
curl https://matrix.factumerit.app/_synapse/admin/v1/server_version
# Requires: Authorization: Bearer <admin_token>
```

### MAS

```bash
# Health check
curl https://matrix.factumerit.app/.well-known/openid-configuration
# Expected: JSON with issuer, authorization_endpoint, etc.

# Readiness check
curl https://matrix.factumerit.app/health
# Expected: 200 OK (if MAS exposes health endpoint)
```

### Vikunja

```bash
# Health check
curl https://vikunja.factumerit.app/health
# Expected: {"status": "ok"}

# API check
curl https://vikunja.factumerit.app/api/v1/info
# Expected: JSON with version, frontend_url, etc.
```

### Authentik

```bash
# Health check
curl https://auth.factumerit.app/-/health/ready/
# Expected: 200 OK

# Version
curl https://auth.factumerit.app/api/v3/admin/version/
# Requires: Authorization: Bearer <api_token>
```

---

## Key Metrics to Monitor

### Synapse Metrics

| Metric | Threshold | Alert Level |
|--------|-----------|-------------|
| Memory usage | > 450 MB (Starter) | WARNING |
| Memory usage | > 500 MB (Starter) | CRITICAL |
| CPU usage | > 80% sustained | WARNING |
| Database connections | > 90% pool | WARNING |
| Federation lag | > 5 minutes | WARNING |
| Event processing lag | > 1 minute | CRITICAL |

**Access metrics**:
```bash
# Synapse exposes Prometheus metrics at /_synapse/metrics
curl https://matrix.factumerit.app/_synapse/metrics
```

### MAS Metrics

| Metric | Threshold | Alert Level |
|--------|-----------|-------------|
| Memory usage | > 100 MB | WARNING |
| Failed logins | > 10/minute | WARNING |
| Token generation errors | > 1/minute | CRITICAL |
| Database query time | > 500ms p95 | WARNING |

### PostgreSQL Metrics

| Metric | Threshold | Alert Level |
|--------|-----------|-------------|
| Connection count | > 90% max | WARNING |
| Disk usage | > 80% | WARNING |
| Disk usage | > 90% | CRITICAL |
| Query time | > 1s p95 | WARNING |
| Replication lag | > 1 minute | CRITICAL |

**Access via Render dashboard** or `pg_stat_*` views.

---

## Render-Specific Monitoring

### Service Status

```bash
# Check via Render API
curl -H "Authorization: Bearer $RENDER_API_KEY" \
  https://api.render.com/v1/services/<service-id>
```

### Deployment Status

```bash
# List recent deploys
curl -H "Authorization: Bearer $RENDER_API_KEY" \
  https://api.render.com/v1/services/<service-id>/deploys
```

### Logs

```bash
# Tail logs (last 100 lines)
# Via Render dashboard or CLI
render logs <service-name> --tail 100
```

---

## Common Issues & Troubleshooting

### Issue: Synapse Out of Memory

**Symptoms**:
- Service restarts frequently
- 502/503 errors
- Slow response times

**Diagnosis**:
```bash
# Check memory usage in Render dashboard
# Check Synapse logs for OOM errors
render logs factumerit-matrix | grep -i "memory\|oom"
```

**Fix**:
1. **Short-term**: Restart service
2. **Medium-term**: Reduce worker count, enable caching
3. **Long-term**: Upgrade to Standard plan (2GB RAM)

---

### Issue: MAS Database Connection Errors

**Symptoms**:
- Login fails with 500 error
- MAS logs show "connection refused" or "too many connections"

**Diagnosis**:
```bash
# Check PostgreSQL connection count
psql $DATABASE_URL -c "SELECT count(*) FROM pg_stat_activity;"

# Check MAS logs
render logs factumerit-matrix | grep -i "mas\|database"
```

**Fix**:
1. Check `DATABASE_URL` is correct
2. Verify `mas` database exists
3. Check PostgreSQL connection limits
4. Restart MAS service

---

### Issue: OIDC Flow Fails

**Symptoms**:
- Vikunja login redirects to error page
- "No Such Resource" or 404 on MAS endpoints

**Diagnosis**:
```bash
# Check nginx routing
render logs factumerit-matrix | grep -i "nginx\|404"

# Test OIDC discovery
curl https://matrix.factumerit.app/.well-known/openid-configuration

# Check MAS is running
render logs factumerit-matrix | grep -i "mas-cli"
```

**Fix**:
1. Verify nginx routes MAS endpoints correctly (see 03-DEPLOYMENT_LESSONS.md)
2. Check MAS is running (supervisord status)
3. Verify client configuration in `mas.yaml`

---

### Issue: Vikunja "No Email Address Available"

**Symptoms**:
- User can authenticate but account creation fails
- Error: "No email address available"

**Diagnosis**:
```bash
# Test MAS userinfo endpoint
# (Get token from OAuth flow first)
curl -H "Authorization: Bearer $TOKEN" \
  https://matrix.factumerit.app/oauth2/userinfo

# Should return email field
```

**Fix**:
1. Verify MAS patch is deployed (check Dockerfile has patch)
2. Check MAS logs for userinfo errors
3. Verify user has email in MAS database
4. Test with different user

**Status**: Should be fixed by MAS patch (solutions-55jz)

---

### Issue: High Database Disk Usage

**Symptoms**:
- PostgreSQL disk > 80%
- Slow queries
- Render alerts about disk space

**Diagnosis**:
```bash
# Check database sizes
psql $DATABASE_URL -c "
  SELECT pg_database.datname,
         pg_size_pretty(pg_database_size(pg_database.datname))
  FROM pg_database
  ORDER BY pg_database_size(pg_database.datname) DESC;
"

# Check table sizes
psql $DATABASE_URL -d matrix -c "
  SELECT relname, pg_size_pretty(pg_total_relation_size(relid))
  FROM pg_stat_user_tables
  ORDER BY pg_total_relation_size(relid) DESC
  LIMIT 10;
"
```

**Fix**:
1. **Synapse media**: Purge old remote media
   ```bash
   # In Synapse container
   synapse-admin purge-remote-media --before <days>
   ```
2. **Synapse events**: Purge old rooms (careful!)
3. **Upgrade PostgreSQL plan**: Basic (256MB) → Standard (1GB)

---

## Backup & Recovery

### PostgreSQL Backups

**Render automatic backups**:
- Daily backups (retained 7 days on Basic plan)
- Point-in-time recovery available on higher plans

**Manual backup**:
```bash
# Dump all databases
pg_dump $DATABASE_URL > backup-$(date +%Y%m%d).sql

# Dump specific database
pg_dump $DATABASE_URL -d matrix > matrix-backup-$(date +%Y%m%d).sql
```

### Synapse Media Store

**Current**: Stored in container (ephemeral!)

**TODO**: Configure S3 or persistent volume for media
```yaml
# homeserver.yaml
media_store_path: /data/media_store
# OR
media_storage_providers:
  - module: s3_storage_provider.S3StorageProviderBackend
```

### MAS Crypto Keys

**Location**: `/data/mas/` (in container)

**Backup**:
```bash
# Copy from running container
render ssh factumerit-matrix
tar -czf mas-keys-backup.tar.gz /data/mas/*.pem
# Download via Render shell or scp
```

**Recovery**: Restore keys to same path, restart MAS

---

## Alerting Strategy (Future)

### Critical Alerts (Page Immediately)

- [ ] Synapse down (health check fails)
- [ ] MAS down (OIDC discovery fails)
- [ ] PostgreSQL down
- [ ] Disk > 90%
- [ ] Memory > 95%

### Warning Alerts (Review Daily)

- [ ] Memory > 80%
- [ ] Disk > 80%
- [ ] High error rate (> 5% of requests)
- [ ] Slow queries (> 1s p95)

### Info Alerts (Review Weekly)

- [ ] New user registrations
- [ ] Failed login attempts
- [ ] Rate limit violations

### Tools to Consider

- **Render metrics**: Built-in CPU/memory/disk monitoring
- **UptimeRobot**: External health check monitoring (free tier)
- **Sentry**: Error tracking for bot services
- **Prometheus + Grafana**: Self-hosted metrics (overkill for now)

---

## Maintenance Windows

### Regular Maintenance

| Task | Frequency | Estimated Downtime |
|------|-----------|-------------------|
| Synapse updates | Monthly | 5-10 minutes |
| MAS updates | As needed | 5-10 minutes |
| PostgreSQL minor updates | Automatic (Render) | 0 minutes |
| PostgreSQL major updates | Yearly | 10-30 minutes |
| Certificate renewal | Automatic (Render) | 0 minutes |

### Update Procedure

1. **Announce**: Post in Matrix room (if users exist)
2. **Backup**: Take manual PostgreSQL backup
3. **Deploy**: Push update to Render
4. **Monitor**: Watch logs for errors
5. **Verify**: Test health checks, OIDC flow
6. **Rollback if needed**: Revert to previous deploy

---

## Related

- [03-DEPLOYMENT_LESSONS.md](./03-DEPLOYMENT_LESSONS.md) - Deployment configuration
- [04-SECURITY_MODEL.md](./04-SECURITY_MODEL.md) - Security incidents
- [Render Docs](https://render.com/docs) - Platform-specific monitoring

