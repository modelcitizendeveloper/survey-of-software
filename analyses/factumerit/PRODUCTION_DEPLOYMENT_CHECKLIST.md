# Matrix Bot Production Deployment Checklist

**Date**: 2025-12-24  
**Task**: solutions-ylad - Matrix Bot Production Ready  
**Epic**: solutions-byt2 - Factumerit Platform: Production Ready

---

## Pre-Deployment Checklist

### 1. Code Review ✅

- [x] **Code review complete** (solutions-frik)
- [x] **Security audit passed** (solutions-5yun)
- [x] **All blockers resolved**
- [x] **Review document**: `analyses/factumerit/CODE_REVIEW_MATRIX_BOT.md`

**Status**: ✅ **APPROVED FOR PRODUCTION**

---

### 2. Environment Variables

**Required Render Env Vars** (set in Render dashboard):

- [ ] `MATRIX_HOMESERVER` - Matrix homeserver URL
  - Value: `https://matrix.factumerit.app`
  
- [ ] `MATRIX_USER_ID` - Bot's Matrix user ID
  - Value: `@eis:matrix.factumerit.app`
  
- [ ] `MATRIX_PASSWORD` - Bot's password
  - Value: (from password manager)
  - **CRITICAL**: Do not log or expose
  
- [ ] `ADMIN_IDS` - Comma-separated admin user IDs
  - Value: `@ivan:matrix.factumerit.app` (or your admin ID)
  - Format: `@user1:domain.com,@user2:domain.com`
  
- [ ] `VIKUNJA_MCP_ENCRYPTION_KEY` - For token encryption
  - Value: (generate with `openssl rand -hex 32`)
  
- [ ] `DATABASE_URL` - PostgreSQL connection
  - Value: (auto-set by Render)

**Optional Env Vars**:

- [ ] `MATRIX_DEVICE_ID` - For session persistence (optional)
- [ ] `LOG_LEVEL` - Logging level (default: INFO)

---

### 3. Dependencies

**Verify in `pyproject.toml`**:

- [x] `matrix-nio>=0.25.2` - Matrix protocol library
- [x] `markdown>=3.5.0` - Markdown formatting
- [x] `rapidfuzz>=3.14.3` - Fuzzy command matching

**Status**: ✅ All dependencies declared

---

### 4. Tests

**Run tests before deploy**:

```bash
cd /home/ivanadamin/vikunja-slack-bot
python -m pytest tests/test_matrix*.py -v
```

**Expected**: All tests pass (or skip if deps not installed locally)

**Note**: Tests will run in Render build environment

---

### 5. Deployment

**Steps**:

1. **Commit and push** to `vikunja-slack-bot` repo
   - Status: ✅ Already pushed (commit 99e5a13)

2. **Render auto-deploys** from main branch
   - Monitor: https://dashboard.render.com

3. **Check build logs** for errors
   - Look for: "Matrix bot initialized"
   - Look for: "Starting custom sync loop"

4. **Verify service starts** without crashes
   - Check: Service status = "Live"

---

### 6. Post-Deployment Testing

**Test in production Matrix**:

1. **Test bot login**:
   - [ ] Bot appears online in Matrix
   - [ ] No errors in Render logs

2. **Test DM (Direct Message)**:
   - [ ] Send DM to `@eis:matrix.factumerit.app`
   - [ ] Bot responds with welcome message
   - [ ] Test command: `!help`
   - [ ] Expected: Help text appears

3. **Test room mention**:
   - [ ] Invite bot to a room
   - [ ] Bot auto-joins
   - [ ] Mention bot: `@eis:matrix.factumerit.app hello`
   - [ ] Expected: Bot responds

4. **Test command parsing**:
   - [ ] Natural language: `show my tasks`
   - [ ] Expected: Bot parses and executes
   - [ ] Bang command: `!oops`
   - [ ] Expected: Shows overdue tasks (or connect prompt)

5. **Test room binding** (new feature):
   - [ ] `!bind <project-name>`
   - [ ] Expected: Room bound to project
   - [ ] `!binding`
   - [ ] Expected: Shows current binding
   - [ ] `add task "Test task"`
   - [ ] Expected: Task created in bound project

6. **Test admin protection**:
   - [ ] From non-admin account: `!credits`
   - [ ] Expected: "Admin only command" error
   - [ ] From admin account: `!credits`
   - [ ] Expected: Credits info displayed

7. **Test error handling**:
   - [ ] Invalid command: `!invalid`
   - [ ] Expected: "Unknown command" message
   - [ ] Malformed input: `create task with no title`
   - [ ] Expected: Graceful error message

---

### 7. Monitoring (First 24 Hours)

**Watch for**:

- [ ] **Memory usage** - Should stay under Vikunja $25/mo plan limits
- [ ] **Error rate** - Should be <1% of requests
- [ ] **Response time** - Should be <2 seconds average
- [ ] **Crash loops** - Should be zero

**Tools**:
- Render dashboard: https://dashboard.render.com
- Logs: `./scripts/fa.sh render logs vikunja-slack-bot`

---

### 8. Rollback Plan

**If critical issues found**:

1. **Revert to previous commit**:
   ```bash
   cd /home/ivanadamin/vikunja-slack-bot
   git revert HEAD
   git push
   ```

2. **Render auto-deploys** previous version

3. **Investigate issue** in dev environment

4. **Fix and re-deploy** when ready

---

## Success Criteria

**Deployment is successful when**:

- ✅ Bot appears online in Matrix
- ✅ Responds to DMs within 2 seconds
- ✅ Responds to room mentions
- ✅ Command parsing works (natural language + bang commands)
- ✅ Room binding feature works
- ✅ Admin protection works
- ✅ No crashes in first 24 hours
- ✅ Error rate <1%

---

## Post-Deployment Tasks

**After successful deployment**:

- [ ] **Close solutions-ylad** - Matrix Bot Production Ready
- [ ] **Close solutions-byt2** - Factumerit Platform: Production Ready
- [ ] **Announce in Vikunja Matrix room** (solutions-bgzy)
- [ ] **Update documentation** with production URLs
- [ ] **Create follow-up tasks** for minor issues:
  - solutions-q5w2 (Rate limiting)
  - solutions-2gn5 (Input sanitization)

---

## Notes

**Code Review**: See `analyses/factumerit/CODE_REVIEW_MATRIX_BOT.md`

**Security Audit**: See `analyses/factumerit/SECURITY_AUDIT.md`

**Minor Issues**: 3 non-blocking issues identified, all P2-P3 priority

**Estimated Deployment Time**: 30-60 minutes

---

**Prepared by**: Augment Agent (Claude Sonnet 4.5)  
**Date**: 2025-12-24  
**Status**: Ready for deployment

