# Use Case: Full-Stack Monorepo

## Context

Full-stack monorepos combine frontend and backend code in a single repository, requiring:
- Coordinated testing across multiple packages
- Shared test utilities and fixtures
- Consistent testing patterns across languages
- Contract testing between frontend/backend
- Efficient CI/CD with selective test execution

Common structure:
```
monorepo/
├── packages/
│   ├── web/          (React + Vite)
│   ├── api/          (Python FastAPI)
│   ├── shared/       (TypeScript types)
│   └── mobile/       (React Native)
├── e2e/              (Playwright tests)
└── package.json
```

Testing pyramid emphasis: **50% unit, 35% integration, 15% E2E**

## Requirements

### Must-Have Capabilities
1. Multi-language support (TypeScript + Python)
2. Workspace-aware test running (only affected packages)
3. Shared test utilities across packages
4. Contract testing (API schema validation)
5. Parallel test execution per package
6. Unified coverage reporting
7. Coordinated E2E testing
8. Fast feedback loops

### Nice-to-Have
- Visual regression testing
- Component library testing in isolation
- Performance testing
- Accessibility testing across all packages

## Primary Recommendation: Hybrid Strategy

### Tool Selection by Layer

**Frontend Packages** (web, mobile, shared):
- **Vitest** - Fast, Vite-native testing
- **Testing Library** - Component testing
- **MSW** - API mocking

**Backend Packages** (api):
- **pytest** - Python testing standard
- **pytest-asyncio** - Async support
- **httpx** - API client testing

**E2E Testing** (cross-package):
- **Playwright** - Multi-browser automation
- **Shared fixtures** - Reusable test data

**Contract Testing**:
- **TypeScript types** - Shared API contracts
- **OpenAPI validation** - Schema testing

### Rationale
Different packages have different optimal tools. Forcing a single tool across languages sacrifices DX and performance.

The key is **consistent patterns** and **shared infrastructure**, not identical tooling.

## Setup Complexity: Medium

### Workspace Configuration
```json
// package.json
{
  "workspaces": ["packages/*", "e2e"],
  "scripts": {
    "test": "turbo run test",
    "test:watch": "turbo run test:watch",
    "test:ci": "turbo run test:ci --cache-dir=.turbo",
    "test:e2e": "playwright test"
  }
}
```

### Turbo Configuration for Selective Testing
```json
// turbo.json
{
  "pipeline": {
    "test": {
      "dependsOn": ["^build"],
      "outputs": ["coverage/**"],
      "cache": true,
      "inputs": ["src/**", "test/**"]
    }
  }
}
```

Time to full setup: **1-2 days**

## Package-Specific Patterns

### Frontend Package (packages/web)
```javascript
// packages/web/vitest.config.js
import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    setupFiles: ['../../test-setup/frontend.js'], // Shared setup
    coverage: {
      reporter: ['text', 'json', 'html']
    }
  }
})
```

### Backend Package (packages/api)
```python
# packages/api/pyproject.toml
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = [
    "--cov=app",
    "--cov-report=json",
    "-v"
]
```

### E2E Tests (e2e/)
```typescript
// e2e/playwright.config.ts
import { defineConfig } from '@playwright/test'

export default defineConfig({
  testDir: './tests',
  webServer: [
    {
      command: 'npm run dev -w packages/web',
      port: 3000
    },
    {
      command: 'cd packages/api && uvicorn app:app',
      port: 8000
    }
  ],
  use: {
    baseURL: 'http://localhost:3000'
  }
})
```

## Contract Testing Strategy

### Approach 1: Shared TypeScript Types
```typescript
// packages/shared/src/types/api.ts
export interface CreateOrderRequest {
  items: Array<{ productId: string; quantity: number }>
  shippingAddress: string
}

export interface CreateOrderResponse {
  orderId: string
  status: 'pending' | 'confirmed'
  total: number
}
```

**Frontend uses types**:
```typescript
// packages/web/src/api/orders.ts
import type { CreateOrderRequest, CreateOrderResponse } from '@monorepo/shared'

async function createOrder(data: CreateOrderRequest): Promise<CreateOrderResponse> {
  // TypeScript ensures contract compliance
}
```

**Backend validates against types**:
```python
# packages/api/app/schemas.py
from pydantic import BaseModel

class CreateOrderRequest(BaseModel):
    items: list[dict]
    shipping_address: str

# Test validates Pydantic matches TypeScript
```

### Approach 2: OpenAPI Schema Testing
```typescript
// e2e/tests/api-contract.spec.ts
import { test, expect } from '@playwright/test'

test('API matches OpenAPI schema', async ({ request }) => {
  const response = await request.get('/openapi.json')
  const schema = await response.json()

  // Validate schema structure
  expect(schema.paths['/api/orders']).toBeDefined()
  expect(schema.components.schemas['CreateOrderRequest']).toMatchObject({
    type: 'object',
    required: ['items', 'shipping_address']
  })
})
```

## Selective Test Execution

### Run Only Affected Tests
```bash
# Turbo automatically determines which packages changed
npm run test

# Example output:
# • packages/web:test       [CACHE MISS]
# • packages/shared:test    [CACHE MISS]
# • packages/api:test       [CACHE SKIP] (no changes)
# • packages/mobile:test    [CACHE SKIP] (no changes)
```

### Manual Package Selection
```bash
# Test single package
npm run test -w packages/web

# Test multiple packages
npm run test -w packages/web -w packages/api

# Test changed files only (Vitest)
cd packages/web && npm run test:changed
```

## Shared Test Utilities

### Shared Frontend Setup
```javascript
// test-setup/frontend.js
import { cleanup } from '@testing-library/react'
import { afterEach } from 'vitest'
import '@testing-library/jest-dom/vitest'

// Cleanup after each test
afterEach(() => {
  cleanup()
})

// Global test utilities
global.testUtils = {
  mockUser: () => ({ id: '123', name: 'Test User' }),
  mockApiResponse: (data) => Promise.resolve({ data })
}
```

### Shared Backend Fixtures
```python
# test-setup/backend.py
import pytest
from sqlalchemy import create_engine
from app.database import Base

@pytest.fixture(scope="session")
def db_engine():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    return engine

@pytest.fixture
def sample_user():
    return {
        "id": "123",
        "email": "test@example.com",
        "name": "Test User"
    }
```

### Shared E2E Fixtures
```typescript
// e2e/fixtures/auth.ts
import { test as base } from '@playwright/test'

export const test = base.extend({
  authenticatedPage: async ({ page }, use) => {
    // Login before each test
    await page.goto('/login')
    await page.fill('[name="email"]', 'test@example.com')
    await page.fill('[name="password"]', 'password')
    await page.click('button[type="submit"]')
    await page.waitForURL('/dashboard')

    await use(page)
  }
})
```

## CI/CD Integration

### GitHub Actions Workflow
```yaml
# .github/workflows/test.yml
name: Test

on: [push, pull_request]

jobs:
  test-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Node
        uses: actions/setup-node@v3
        with:
          node-version: 20
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run frontend tests
        run: npm run test:ci -w packages/web -w packages/shared

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          flags: frontend

  test-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
          cache: 'pip'

      - name: Install dependencies
        run: |
          cd packages/api
          pip install -e ".[test]"

      - name: Run backend tests
        run: |
          cd packages/api
          pytest --cov --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          flags: backend

  test-e2e:
    runs-on: ubuntu-latest
    needs: [test-frontend, test-backend]
    steps:
      - uses: actions/checkout@v3

      - name: Setup Node
        uses: actions/setup-node@v3

      - name: Setup Python
        uses: actions/setup-python@v4

      - name: Install dependencies
        run: |
          npm ci
          cd packages/api && pip install -e .

      - name: Install Playwright
        run: npx playwright install --with-deps

      - name: Run E2E tests
        run: npm run test:e2e

      - name: Upload Playwright report
        uses: actions/upload-artifact@v3
        if: always()
        with:
          name: playwright-report
          path: playwright-report/
```

**Parallel execution**: Jobs run in parallel
**Cache strategy**: Turbo cache + npm/pip cache
**Typical runtime**: 3-5 minutes total (parallel jobs)

## Validation Results

### Speed Benchmarks
- **Frontend only**: 4s for 300 tests (cached dependencies)
- **Backend only**: 8s for 200 tests
- **E2E suite**: 120s for 50 tests (parallel workers)
- **Full CI with cache**: 180s total (parallel jobs)

### Developer Experience Metrics
- Workspace setup time: 30 minutes (one-time)
- Time to run affected tests: 2-10s (Turbo cache)
- Debugging complexity: Medium (multiple tools)
- Learning curve: Medium (different tools per package)

### Maintenance Burden
- **Medium**: Multiple tool configurations to maintain
- Contract testing prevents integration issues
- Shared utilities reduce duplication
- Turbo caching dramatically improves iteration speed

## Known Gaps

### What This Strategy Cannot Handle
1. **Cross-language refactoring** - Type changes need manual sync
2. **Real production environment** - Needs staging tests
3. **Performance at scale** - Needs dedicated load testing
4. **Mobile-specific testing** - Needs Detox or Appium

### Scenarios Requiring Additional Tools
- **Visual regression**: Add Chromatic or Percy
- **Load testing**: Add k6 or Artillery
- **Mobile testing**: Add Detox (React Native)
- **Database migrations**: Add migration testing strategy

## Recommended Tool Stack

**Core testing tools**:
```
Vitest (frontend)
pytest (backend)
Playwright (E2E)
Turborepo (orchestration)
```

**Supporting tools**:
```
MSW (API mocking)
Testing Library (component testing)
OpenAPI validation
TypeScript (contract enforcement)
```

**CI/CD integration**:
```
GitHub Actions or similar
Codecov (coverage reporting)
Turbo remote cache
Playwright trace viewer
```

## Cost-Benefit Analysis

### Setup Investment
- **Time**: 2-3 days for full monorepo testing setup
- **Training**: 1-2 days for team onboarding
- **Tooling cost**: Free (all open source)

### Ongoing Returns
- **Fast feedback**: Turbo cache makes subsequent runs instant
- **Confidence**: Contract testing prevents integration bugs
- **Selective testing**: Only test what changed
- **Unified reporting**: Single coverage dashboard

## Common Pitfalls and Solutions

### Pitfall 1: Slow E2E Tests
**Problem**: E2E tests take 10+ minutes
**Solution**:
- Run E2E tests only on changed features
- Use Playwright sharding (`--shard 1/4`)
- Mock external services
- Parallelize with multiple workers

### Pitfall 2: Contract Drift
**Problem**: Frontend and backend APIs out of sync
**Solution**:
- Generate TypeScript types from OpenAPI
- Add contract tests in E2E suite
- Use Pydantic for runtime validation
- CI fails on schema mismatches

### Pitfall 3: Duplicate Test Setup
**Problem**: Every package has identical setup code
**Solution**:
- Extract shared test utilities to `test-setup/` directory
- Use workspace resolution for imports
- Document patterns in testing guide

### Pitfall 4: Cache Invalidation Issues
**Problem**: Turbo doesn't detect certain changes
**Solution**:
- Explicitly list inputs in turbo.json
- Include `.env.test` files in inputs
- Force refresh with `--force` flag when needed

## Migration Path

### From Polyrepo to Monorepo
1. Move repos into `packages/` directory
2. Set up workspace configuration
3. Extract shared code to `packages/shared`
4. Add Turbo for orchestration
5. Set up E2E tests across packages

**Effort**: 1-2 weeks
**Risk**: Medium (coordination needed)

### Adding Testing to Existing Monorepo
1. Start with one package (highest value)
2. Extract shared patterns
3. Gradually add to other packages
4. Add E2E tests last

**Effort**: 2-4 weeks
**Risk**: Low (incremental)
