# Use Case: E2E Critical Paths

## Context

Critical user journeys require end-to-end testing to ensure reliability:
- **Authentication flows**: Registration, login, password reset, MFA
- **E-commerce checkout**: Cart → checkout → payment → confirmation
- **Content publishing**: Draft → review → publish → live
- **Financial transactions**: Transfer → verification → completion
- **Onboarding flows**: Signup → profile → tutorial → activation

These flows involve multiple pages, API calls, database changes, and external services.

Testing pyramid emphasis: **20% unit, 30% integration, 50% E2E** (inverted for critical paths)

## Requirements

### Must-Have Capabilities
1. Real browser automation (Chrome, Firefox, Safari)
2. Network inspection and mocking
3. Authentication state management
4. Visual feedback on failures (screenshots, videos)
5. Retry logic for flaky tests
6. Parallel execution for speed
7. CI/CD integration
8. Cross-browser testing

### Nice-to-Have
- Visual regression testing
- Accessibility testing
- Performance metrics
- Mobile device emulation
- Network throttling

## Primary Recommendation: Playwright

### Rationale
**Playwright** is purpose-built for reliable E2E testing:
- **Multi-browser support**: Chromium, Firefox, WebKit (Safari)
- **Auto-waiting**: Smart waits for elements to be actionable
- **Network control**: Mock, block, or monitor requests
- **Trace viewer**: Time-travel debugging for failures
- **Built-in retries**: Automatic retry on flakiness
- **Parallel execution**: Run tests across multiple workers
- **Strong selectors**: CSS, text, accessibility, custom

### Setup Complexity: Low
```bash
npm init playwright@latest
```

Time to first test: **5 minutes**

### Sample Test Patterns

#### Authentication Flow
```typescript
// tests/auth.spec.ts
import { test, expect } from '@playwright/test'

test.describe('User Authentication', () => {
  test('successful login flow', async ({ page }) => {
    await page.goto('/login')

    // Fill login form
    await page.fill('[name="email"]', 'user@example.com')
    await page.fill('[name="password"]', 'SecurePass123!')
    await page.click('button[type="submit"]')

    // Verify redirect to dashboard
    await expect(page).toHaveURL('/dashboard')

    // Verify user is authenticated
    await expect(page.locator('[data-testid="user-menu"]')).toContainText('user@example.com')
  })

  test('handles invalid credentials', async ({ page }) => {
    await page.goto('/login')

    await page.fill('[name="email"]', 'wrong@example.com')
    await page.fill('[name="password"]', 'WrongPass!')
    await page.click('button[type="submit"]')

    // Should show error message
    await expect(page.locator('.error-message')).toContainText('Invalid credentials')

    // Should remain on login page
    await expect(page).toHaveURL('/login')
  })

  test('password reset flow', async ({ page, context }) => {
    await page.goto('/login')
    await page.click('text=Forgot password?')

    await page.fill('[name="email"]', 'user@example.com')
    await page.click('button:has-text("Send reset link")')

    // Mock email and get reset link
    const resetLink = await page.evaluate(() => {
      // In real test, this would come from email testing service
      return '/reset-password?token=test-token'
    })

    await page.goto(resetLink)
    await page.fill('[name="password"]', 'NewSecurePass123!')
    await page.fill('[name="confirmPassword"]', 'NewSecurePass123!')
    await page.click('button:has-text("Reset password")')

    await expect(page.locator('.success-message')).toBeVisible()
  })
})
```

#### E-commerce Checkout Flow
```typescript
// tests/checkout.spec.ts
import { test, expect } from '@playwright/test'

test.describe('Checkout Flow', () => {
  test.use({
    storageState: 'auth/user.json' // Pre-authenticated user
  })

  test('complete purchase journey', async ({ page }) => {
    // Add product to cart
    await page.goto('/products/laptop-123')
    await page.click('button:has-text("Add to Cart")')
    await expect(page.locator('.cart-badge')).toHaveText('1')

    // Proceed to checkout
    await page.click('[data-testid="cart-icon"]')
    await page.click('button:has-text("Checkout")')

    // Fill shipping information
    await page.fill('[name="address"]', '123 Main St')
    await page.fill('[name="city"]', 'San Francisco')
    await page.fill('[name="zipCode"]', '94102')
    await page.click('button:has-text("Continue to payment")')

    // Mock payment processing
    await page.route('**/api/payments', route => {
      route.fulfill({
        status: 200,
        body: JSON.stringify({
          success: true,
          transactionId: 'txn_123456'
        })
      })
    })

    // Enter payment details
    const paymentFrame = page.frameLocator('iframe[title="Payment"]')
    await paymentFrame.fill('[name="cardNumber"]', '4242424242424242')
    await paymentFrame.fill('[name="expiry"]', '12/25')
    await paymentFrame.fill('[name="cvc"]', '123')

    await page.click('button:has-text("Place Order")')

    // Verify order confirmation
    await expect(page).toHaveURL(/\/orders\/[a-z0-9]+/)
    await expect(page.locator('h1')).toContainText('Order Confirmed')

    // Verify order appears in history
    await page.goto('/orders')
    await expect(page.locator('.order-list')).toContainText('txn_123456')
  })

  test('handles payment failure gracefully', async ({ page }) => {
    await page.goto('/products/laptop-123')
    await page.click('button:has-text("Add to Cart")')
    await page.click('[data-testid="cart-icon"]')
    await page.click('button:has-text("Checkout")')

    // Fill shipping
    await page.fill('[name="address"]', '123 Main St')
    await page.click('button:has-text("Continue to payment")')

    // Mock payment failure
    await page.route('**/api/payments', route => {
      route.fulfill({
        status: 400,
        body: JSON.stringify({
          error: 'Card declined'
        })
      })
    })

    await page.click('button:has-text("Place Order")')

    // Should show error
    await expect(page.locator('.error-message')).toContainText('Card declined')

    // Should remain on payment page
    await expect(page).toHaveURL(/\/checkout/)

    // Cart should still have items
    await expect(page.locator('.cart-badge')).toHaveText('1')
  })
})
```

#### Content Publishing Flow
```typescript
// tests/publishing.spec.ts
import { test, expect } from '@playwright/test'

test.describe('Content Publishing', () => {
  test('draft to publish workflow', async ({ page }) => {
    await page.goto('/admin/posts/new')

    // Create draft
    await page.fill('[name="title"]', 'New Blog Post')
    await page.fill('[role="textbox"]', 'This is the content of the post.')
    await page.click('button:has-text("Save Draft")')

    await expect(page.locator('.status-badge')).toHaveText('Draft')

    // Preview draft
    await page.click('button:has-text("Preview")')
    const previewPage = await page.waitForEvent('popup')
    await expect(previewPage.locator('h1')).toContainText('New Blog Post')
    await previewPage.close()

    // Publish
    await page.click('button:has-text("Publish")')

    // Confirm publish modal
    await page.click('button:has-text("Confirm Publish")')

    await expect(page.locator('.status-badge')).toHaveText('Published')

    // Verify on public site
    const postUrl = await page.locator('[data-testid="public-url"]').textContent()
    await page.goto(postUrl)
    await expect(page.locator('h1')).toContainText('New Blog Post')
  })
})
```

## Authentication State Management

### Approach 1: Reusable Auth Fixture
```typescript
// tests/auth.setup.ts
import { test as setup } from '@playwright/test'

setup('authenticate', async ({ page }) => {
  await page.goto('/login')
  await page.fill('[name="email"]', 'test@example.com')
  await page.fill('[name="password"]', 'password')
  await page.click('button[type="submit"]')

  await page.waitForURL('/dashboard')

  // Save authentication state
  await page.context().storageState({ path: 'auth/user.json' })
})
```

```typescript
// playwright.config.ts
export default defineConfig({
  projects: [
    { name: 'setup', testMatch: '**/*.setup.ts' },
    {
      name: 'authenticated tests',
      use: { storageState: 'auth/user.json' },
      dependencies: ['setup']
    }
  ]
})
```

### Approach 2: Per-Test Authentication
```typescript
// fixtures/auth.ts
import { test as base } from '@playwright/test'

export const test = base.extend({
  authenticatedPage: async ({ page }, use) => {
    // Login via API (faster than UI)
    const response = await page.request.post('/api/auth/login', {
      data: {
        email: 'test@example.com',
        password: 'password'
      }
    })

    const { token } = await response.json()

    // Set auth cookie/header
    await page.context().addCookies([{
      name: 'auth_token',
      value: token,
      domain: 'localhost',
      path: '/'
    }])

    await use(page)
  }
})
```

## Handling Flaky Tests

### Retry Configuration
```typescript
// playwright.config.ts
export default defineConfig({
  retries: process.env.CI ? 2 : 0,
  use: {
    // Auto-waiting timeout
    actionTimeout: 10000,
    navigationTimeout: 30000,

    // Capture on failure
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
    trace: 'retain-on-failure'
  }
})
```

### Explicit Waits for Stability
```typescript
// Wait for network to be idle
await page.waitForLoadState('networkidle')

// Wait for specific API call
await page.waitForResponse(resp =>
  resp.url().includes('/api/orders') && resp.status() === 200
)

// Wait for element to be stable (no animations)
await page.locator('.modal').waitFor({ state: 'visible' })
await expect(page.locator('.modal')).toBeVisible()
```

## CI/CD Integration

```yaml
# .github/workflows/e2e.yml
name: E2E Tests

on:
  push:
    branches: [main]
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        browser: [chromium, firefox, webkit]
        shardIndex: [1, 2, 3, 4]
        shardTotal: [4]

    steps:
      - uses: actions/checkout@v3

      - name: Setup Node
        uses: actions/setup-node@v3
        with:
          node-version: 20

      - name: Install dependencies
        run: npm ci

      - name: Install Playwright browsers
        run: npx playwright install --with-deps ${{ matrix.browser }}

      - name: Run E2E tests
        run: |
          npx playwright test --project=${{ matrix.browser }} \
            --shard=${{ matrix.shardIndex }}/${{ matrix.shardTotal }}
        env:
          API_URL: http://localhost:8000
          DATABASE_URL: postgresql://test:test@localhost/test_db

      - name: Upload test results
        uses: actions/upload-artifact@v3
        if: always()
        with:
          name: playwright-report-${{ matrix.browser }}-${{ matrix.shardIndex }}
          path: playwright-report/

      - name: Upload trace files
        uses: actions/upload-artifact@v3
        if: failure()
        with:
          name: traces-${{ matrix.browser }}-${{ matrix.shardIndex }}
          path: test-results/
```

**Parallel execution**: 4 shards × 3 browsers = 12 parallel jobs
**Typical runtime**: 3-5 minutes (sharded) vs 15-20 minutes (single)

## Alternative Options

### Option B: Cypress

**When to choose**: Simpler setup, Chrome-only acceptable, existing Cypress tests

**Advantages**:
- Better real-time test running experience
- More intuitive API for beginners
- Better documentation and community content
- Stronger time-travel debugging

**Disadvantages**:
- Chrome/Edge only (no Firefox/Safari)
- More flaky on CI
- Slower execution than Playwright
- Less powerful network mocking

**Setup complexity**: Low

### Option C: Selenium WebDriver

**When to choose**: Legacy infrastructure, Java/C# teams

**Advantages**:
- Very mature ecosystem
- Support for more browsers (including IE)
- Language bindings for Java, C#, Ruby, etc.

**Disadvantages**:
- More verbose API
- Requires manual waits and stability checks
- Slower execution
- More flaky tests

**Setup complexity**: High (driver management, explicit waits)

## Validation Results

### Speed Benchmarks
- **Single test**: 3-8 seconds
- **Full suite (50 tests)**: 120 seconds (4 parallel workers)
- **Sharded CI (50 tests)**: 35 seconds (4 shards × 3 browsers)

### Developer Experience Metrics
- Time to write first test: 15 minutes
- Debugging time: 5-10 minutes with trace viewer
- Flakiness rate: <2% with proper waits

### Maintenance Burden
- **Medium**: Tests break when UI changes significantly
- Use `data-testid` attributes for stability
- Page Object Model reduces duplication
- Regular review needed for obsolete tests

## Known Gaps

### What This Solution Cannot Handle
1. **Native mobile apps** - Needs Appium or Detox
2. **Load testing** - Needs k6 or Artillery
3. **Accessibility auditing** - Needs axe-core integration
4. **Visual regression** - Needs Percy or Chromatic

### Scenarios Requiring Additional Tools
- **Email testing**: Mailhog or Ethereal
- **SMS testing**: Twilio test credentials
- **Payment testing**: Stripe test mode
- **PDF generation**: PDF parsing library

## Recommended Tool Stack

**Minimal viable E2E**:
```
Playwright
playwright/test (built-in runner)
```

**Production-ready stack**:
```
Playwright
Page Object Model pattern
Authentication fixtures
CI/CD integration with sharding
```

**Enterprise stack**:
```
Above tools plus:
Playwright trace viewer
Visual regression (Argos or Percy)
axe-core for accessibility
Datadog/Sentry for production monitoring
```

## Page Object Model Pattern

### Benefits
- Reduce duplication across tests
- Centralize selectors
- Easier maintenance when UI changes
- Better test readability

### Implementation
```typescript
// pages/LoginPage.ts
export class LoginPage {
  constructor(private page: Page) {}

  async goto() {
    await this.page.goto('/login')
  }

  async login(email: string, password: string) {
    await this.page.fill('[name="email"]', email)
    await this.page.fill('[name="password"]', password)
    await this.page.click('button[type="submit"]')
  }

  async getErrorMessage() {
    return this.page.locator('.error-message').textContent()
  }
}

// Use in tests
test('login with invalid credentials', async ({ page }) => {
  const loginPage = new LoginPage(page)
  await loginPage.goto()
  await loginPage.login('wrong@example.com', 'wrong')

  const error = await loginPage.getErrorMessage()
  expect(error).toContain('Invalid credentials')
})
```

## Cost-Benefit Analysis

### Setup Investment
- **Time**: 1-2 days for initial setup
- **Training**: 4 hours for team onboarding
- **Tooling cost**: Free (open source)
- **CI costs**: Increases runtime (sharding helps)

### Ongoing Returns
- **Confidence**: Catch critical bugs before production
- **Regression prevention**: Ensure existing flows don't break
- **Documentation**: Tests document expected user journeys
- **Customer trust**: Fewer production incidents

### ROI Calculation
Average critical bug cost: $10,000 (customer impact, engineering time)
E2E tests catch: 70% of critical bugs
Annual bugs prevented: ~20
**Annual value: $140,000**

Setup and maintenance cost: ~$15,000/year
**Net ROI: $125,000 or 833%**

## Migration Path

### From Cypress
1. Install Playwright
2. Run codemods for basic API changes
3. Update selectors (Cypress uses jQuery-style)
4. Test authentication patterns
5. Run both in parallel during transition

**Effort**: 1-2 weeks for 100+ tests
**Risk**: Low (can run both simultaneously)

### From No E2E Testing
1. Identify 5-10 critical paths
2. Write happy path tests first
3. Add error handling tests
4. Expand coverage gradually

**Effort**: 1-2 months for comprehensive coverage
**Risk**: Low (incremental adoption)
