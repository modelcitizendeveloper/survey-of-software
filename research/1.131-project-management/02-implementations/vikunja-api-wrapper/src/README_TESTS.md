# Test Scripts - Quick Reference

Three scripts for testing and setting up the Vikunja API wrapper.

---

## 1. test_token.py - Smoke Test ✅

**Purpose**: Validate API token works

**Run time**: 5 seconds

**Usage**:
```bash
python test_token.py
```

**When**: First setup, after token rotation, troubleshooting

---

## 2. integration_tests.py - Full Test Suite ✅

**Purpose**: End-to-end CRUD tests (11/11 passing)

**Run time**: 30 seconds

**Usage**:
```bash
python integration_tests.py
```

**When**: Before production, after wrapper changes, CI/CD

**Note**: Creates test resources (clean up manually in Vikunja UI)

---

## 3. add_api_reminder.py - Setup Script 🔐

**Purpose**: Create API token renewal reminder

**Run time**: 10 seconds

**Usage**:
```bash
python add_api_reminder.py
```

**When**: Once after initial setup

**Creates**:
- 📁 Project: "spawn-solutions"
- 🏷️ Label: "Security" (red)
- ✅ Task: "Renew API token" (due in 30 days)

---

## Full Documentation

See [TESTING.md](./TESTING.md) for:
- Detailed test coverage
- Skipped tests explained
- API endpoint discovery
- Troubleshooting guide
- Production examples

---

**Status**: ✅ All tests passing (11/11)
**Last Updated**: November 7, 2025
