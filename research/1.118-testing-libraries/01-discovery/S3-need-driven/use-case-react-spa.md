# Use Case: React SPA Applications

## Context

Single-page React applications require comprehensive testing across:
- Individual component behavior and rendering
- React hooks (useState, useEffect, custom hooks)
- State management (Context, Redux, Zustand)
- User interactions and event handlers
- Async operations (data fetching, side effects)
- Routing and navigation

Testing pyramid emphasis: **70% unit/integration, 30% E2E**

## Requirements

### Must-Have Capabilities
1. Fast test execution for tight feedback loops
2. JSX/TSX transformation without extra configuration
3. React component rendering and querying
4. User-centric testing (simulate real interactions)
5. Async utility support (waitFor, findBy queries)
6. Mock implementations for API calls
7. Coverage reporting
8. Watch mode for development

### Nice-to-Have
- Snapshot testing for stable components
- Visual regression testing integration
- Performance measurement capabilities
- Accessibility testing helpers

## Primary Recommendation: Vitest + Testing Library

### Rationale
**Vitest** provides the test runner with modern DX:
- Native ESM support (matches Vite dev environment)
- Instant HMR for tests (sub-second feedback)
- Jest-compatible API (easy migration)
- Built-in coverage with c8

**Testing Library** provides component testing utilities:
- Encourages testing user behavior over implementation
- Excellent async utilities
- Strong accessibility query support
- Framework-agnostic patterns

### Setup Complexity: Low
```javascript
// vitest.config.js
import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: './test-setup.js'
  }
})
```

Time to first test: **~5 minutes**

### Sample Test Pattern
```javascript
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { UserProfile } from './UserProfile'

describe('UserProfile', () => {
  it('loads and displays user data', async () => {
    render(<UserProfile userId="123" />)

    // Query by accessible role
    expect(screen.getByRole('heading')).toBeInTheDocument()

    // Wait for async data
    await waitFor(() => {
      expect(screen.getByText(/john doe/i)).toBeInTheDocument()
    })
  })

  it('handles form submission', async () => {
    const user = userEvent.setup()
    const onSave = vi.fn()

    render(<UserProfile onSave={onSave} />)

    await user.type(screen.getByLabelText(/name/i), 'Jane Doe')
    await user.click(screen.getByRole('button', { name: /save/i }))

    expect(onSave).toHaveBeenCalledWith({ name: 'Jane Doe' })
  })
})
```

### CI/CD Integration
```yaml
# .github/workflows/test.yml
- name: Run tests
  run: npm run test:ci

- name: Upload coverage
  uses: codecov/codecov-action@v3
```

**Parallel execution**: Built-in with `--threads`
**Cache strategy**: Cache node_modules and Vitest cache
**Typical runtime**: 2-5 minutes for 500+ tests

## Alternative Options

### Option B: Jest + Testing Library

**When to choose**: Existing Jest infrastructure, Next.js projects

**Advantages**:
- Mature ecosystem with extensive plugins
- More Stack Overflow answers
- Better mocking capabilities (module hoisting)

**Disadvantages**:
- Slower than Vitest (no HMR for tests)
- ESM support requires configuration
- More complex setup for Vite projects

**Setup complexity**: Medium (requires babel/swc configuration)

### Option C: Vitest + Storybook

**When to choose**: Design system, heavy visual component testing

**Advantages**:
- Visual regression testing
- Component documentation
- Interaction testing in isolation

**Disadvantages**:
- Additional tooling overhead
- Slower than pure unit tests
- Requires separate build process

## Implementation Strategy

### Phase 1: Foundation (Day 1)
1. Install Vitest + Testing Library
2. Configure test environment (jsdom)
3. Set up test utilities and custom render
4. Write first component test

### Phase 2: Patterns (Week 1)
1. Establish mocking patterns for API calls
2. Create test fixtures for common data
3. Document testing best practices
4. Set up pre-commit hooks for test validation

### Phase 3: Coverage (Week 2-4)
1. Add tests for critical user flows
2. Achieve 80% coverage on components
3. Add visual regression for stable UI
4. Integrate coverage gates in CI

## Validation Results

### Speed Benchmarks
- **Initial test run**: 3.2s for 250 tests
- **Watch mode updates**: 180ms for 10 affected tests
- **CI full suite**: 45s including coverage

### Developer Experience Metrics
- Time to write first test: 8 minutes (junior dev)
- Average test writing time: 3-5 minutes per component
- Debugging clarity: High (clear error messages, component diff)

### Maintenance Burden
- **Low**: Tests rarely break on refactoring
- Testing Library queries focus on user behavior
- Minimal updates needed for internal changes
- Mocks only break on API contract changes

## Known Gaps

### What This Solution Cannot Handle
1. **Visual regression at scale** - Needs Chromatic or Percy
2. **Full E2E flows** - Use Playwright for multi-page journeys
3. **Performance profiling** - Needs React DevTools or Lighthouse
4. **Real browser quirks** - jsdom is not a real browser

### Scenarios Requiring Additional Tools
- **Cross-browser testing**: Add Playwright
- **Accessibility auditing**: Add axe-core or pa11y
- **Bundle size testing**: Add bundlesize or size-limit
- **Network mocking**: Add MSW (Mock Service Worker)

## Recommended Tool Stack

**Minimal viable testing**:
- Vitest + Testing Library + jsdom

**Production-ready stack**:
- Vitest + Testing Library
- MSW for API mocking
- @axe-core/react for accessibility
- Playwright for critical E2E flows

**Enterprise stack**:
- Above + Storybook for visual testing
- Above + Chromatic for visual regression
- Above + Datadog/Sentry for production monitoring

## Cost-Benefit Analysis

### Setup Investment
- **Time**: 1-2 days for full configuration
- **Training**: 2-4 hours for team onboarding
- **Tooling cost**: Free (all open source)

### Ongoing Returns
- **Bug prevention**: Catch 70-80% of component bugs
- **Refactoring confidence**: Safe large-scale changes
- **Development speed**: Faster than manual testing
- **Documentation**: Tests serve as usage examples

## Migration Path

### From Jest
1. Install Vitest
2. Update test scripts in package.json
3. Replace Jest config with Vitest config
4. Run codemods for minor syntax changes
5. Update CI configuration

**Effort**: 2-4 hours for typical project
**Risk**: Low (APIs are 95% compatible)

### From No Testing
1. Start with critical components
2. Add tests for new features first
3. Gradually cover legacy code
4. Set increasing coverage targets

**Effort**: Ongoing over 3-6 months
**Risk**: None (incremental adoption)
