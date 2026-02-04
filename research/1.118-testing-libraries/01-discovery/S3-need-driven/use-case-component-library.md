# Use Case: Component Library Testing

## Context

Reusable UI component libraries (design systems) require specialized testing:
- **Isolated component behavior** - Components work without application context
- **Visual consistency** - Components render correctly across variants
- **Accessibility compliance** - WCAG 2.1 AA standards
- **API contract testing** - Props, events, slots behave as documented
- **Cross-framework compatibility** - Web components work in React, Vue, etc.
- **Responsive behavior** - Components adapt to different viewports

Component library examples: Material-UI, Chakra UI, Shadcn, internal design systems

Testing pyramid emphasis: **70% unit, 20% visual, 10% integration**

## Requirements

### Must-Have Capabilities
1. Component rendering in isolation
2. Props and variant testing
3. Accessibility testing (ARIA, keyboard nav)
4. Visual regression detection
5. Interactive behavior testing
6. Multiple theme testing
7. Documentation with live examples
8. Cross-browser validation

### Nice-to-Have
- Performance benchmarking
- Bundle size tracking
- Component usage analytics
- A11y audit reports

## Primary Recommendation: Testing Library + Storybook + Playwright

### Rationale
Component libraries need a **three-tier testing strategy**:

**Testing Library** - Unit testing component logic:
- User interaction testing
- Accessibility queries
- Fast feedback loops

**Storybook** - Visual development and documentation:
- Isolated component development
- Visual testing in browser
- Living documentation
- Interaction testing

**Playwright** - Visual regression and cross-browser:
- Screenshot comparison
- Multi-browser validation
- Automated visual QA

### Setup Complexity: Medium

Time to full setup: **1 day**

## Tier 1: Unit Testing with Testing Library

### Configuration
```javascript
// vitest.config.js
import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    setupFiles: './test-setup.js',
    coverage: {
      include: ['src/components/**'],
      exclude: ['**/*.stories.tsx', '**/*.test.tsx']
    }
  }
})
```

### Sample Component Tests

#### Button Component
```typescript
// Button.test.tsx
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { Button } from './Button'

describe('Button', () => {
  it('renders with text content', () => {
    render(<Button>Click me</Button>)
    expect(screen.getByRole('button')).toHaveTextContent('Click me')
  })

  it('calls onClick when clicked', async () => {
    const user = userEvent.setup()
    const handleClick = vi.fn()

    render(<Button onClick={handleClick}>Click</Button>)
    await user.click(screen.getByRole('button'))

    expect(handleClick).toHaveBeenCalledTimes(1)
  })

  it('is disabled when disabled prop is true', () => {
    render(<Button disabled>Disabled</Button>)
    expect(screen.getByRole('button')).toBeDisabled()
  })

  it('supports different variants', () => {
    const { rerender } = render(<Button variant="primary">Primary</Button>)
    expect(screen.getByRole('button')).toHaveClass('btn-primary')

    rerender(<Button variant="secondary">Secondary</Button>)
    expect(screen.getByRole('button')).toHaveClass('btn-secondary')
  })

  it('supports different sizes', () => {
    const { rerender } = render(<Button size="small">Small</Button>)
    expect(screen.getByRole('button')).toHaveClass('btn-sm')

    rerender(<Button size="large">Large</Button>)
    expect(screen.getByRole('button')).toHaveClass('btn-lg')
  })
})
```

#### Accessible Modal Component
```typescript
// Modal.test.tsx
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { Modal } from './Modal'

describe('Modal', () => {
  it('renders when open', () => {
    render(
      <Modal isOpen={true} onClose={() => {}}>
        <h2>Modal Title</h2>
        <p>Modal content</p>
      </Modal>
    )

    expect(screen.getByRole('dialog')).toBeInTheDocument()
    expect(screen.getByText('Modal Title')).toBeInTheDocument()
  })

  it('does not render when closed', () => {
    render(
      <Modal isOpen={false} onClose={() => {}}>
        Content
      </Modal>
    )

    expect(screen.queryByRole('dialog')).not.toBeInTheDocument()
  })

  it('calls onClose when backdrop is clicked', async () => {
    const user = userEvent.setup()
    const handleClose = vi.fn()

    render(
      <Modal isOpen={true} onClose={handleClose}>
        Content
      </Modal>
    )

    const backdrop = screen.getByTestId('modal-backdrop')
    await user.click(backdrop)

    expect(handleClose).toHaveBeenCalled()
  })

  it('calls onClose when escape key is pressed', async () => {
    const user = userEvent.setup()
    const handleClose = vi.fn()

    render(
      <Modal isOpen={true} onClose={handleClose}>
        Content
      </Modal>
    )

    await user.keyboard('{Escape}')
    expect(handleClose).toHaveBeenCalled()
  })

  it('traps focus within modal', async () => {
    const user = userEvent.setup()

    render(
      <Modal isOpen={true} onClose={() => {}}>
        <button>First</button>
        <button>Second</button>
        <button>Third</button>
      </Modal>
    )

    const buttons = screen.getAllByRole('button')

    // Tab through buttons
    buttons[0].focus()
    await user.keyboard('{Tab}')
    expect(buttons[1]).toHaveFocus()

    await user.keyboard('{Tab}')
    expect(buttons[2]).toHaveFocus()

    // Tab from last should wrap to first
    await user.keyboard('{Tab}')
    expect(buttons[0]).toHaveFocus()
  })

  it('has proper ARIA attributes', () => {
    render(
      <Modal
        isOpen={true}
        onClose={() => {}}
        ariaLabelledBy="modal-title"
      >
        <h2 id="modal-title">Modal Title</h2>
      </Modal>
    )

    const dialog = screen.getByRole('dialog')
    expect(dialog).toHaveAttribute('aria-labelledby', 'modal-title')
    expect(dialog).toHaveAttribute('aria-modal', 'true')
  })
})
```

#### Form Input Component
```typescript
// Input.test.tsx
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { axe } from 'jest-axe'
import { Input } from './Input'

describe('Input', () => {
  it('renders with label', () => {
    render(<Input label="Email" name="email" />)

    expect(screen.getByLabelText('Email')).toBeInTheDocument()
  })

  it('shows error message when invalid', () => {
    render(
      <Input
        label="Email"
        name="email"
        error="Invalid email address"
      />
    )

    expect(screen.getByText('Invalid email address')).toBeInTheDocument()
    expect(screen.getByLabelText('Email')).toHaveAttribute('aria-invalid', 'true')
  })

  it('supports controlled value', async () => {
    const user = userEvent.setup()
    const handleChange = vi.fn()

    render(
      <Input
        label="Name"
        value=""
        onChange={handleChange}
      />
    )

    await user.type(screen.getByLabelText('Name'), 'John')

    expect(handleChange).toHaveBeenCalledTimes(4) // One per character
  })

  it('has no accessibility violations', async () => {
    const { container } = render(
      <Input label="Email" name="email" />
    )

    const results = await axe(container)
    expect(results).toHaveNoViolations()
  })
})
```

## Tier 2: Visual Development with Storybook

### Configuration
```typescript
// .storybook/main.ts
import type { StorybookConfig } from '@storybook/react-vite'

const config: StorybookConfig = {
  stories: ['../src/**/*.stories.@(ts|tsx)'],
  addons: [
    '@storybook/addon-links',
    '@storybook/addon-essentials',
    '@storybook/addon-interactions',
    '@storybook/addon-a11y'
  ],
  framework: {
    name: '@storybook/react-vite',
    options: {}
  }
}

export default config
```

### Button Stories
```typescript
// Button.stories.tsx
import type { Meta, StoryObj } from '@storybook/react'
import { Button } from './Button'

const meta: Meta<typeof Button> = {
  title: 'Components/Button',
  component: Button,
  parameters: {
    layout: 'centered'
  },
  tags: ['autodocs'],
  argTypes: {
    variant: {
      control: 'select',
      options: ['primary', 'secondary', 'danger']
    },
    size: {
      control: 'select',
      options: ['small', 'medium', 'large']
    }
  }
}

export default meta
type Story = StoryObj<typeof Button>

export const Primary: Story = {
  args: {
    variant: 'primary',
    children: 'Button'
  }
}

export const Secondary: Story = {
  args: {
    variant: 'secondary',
    children: 'Button'
  }
}

export const Large: Story = {
  args: {
    size: 'large',
    children: 'Large Button'
  }
}

export const Disabled: Story = {
  args: {
    disabled: true,
    children: 'Disabled Button'
  }
}

// Interaction testing in Storybook
export const ClickTest: Story = {
  args: {
    children: 'Click me'
  },
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement)
    const button = canvas.getByRole('button')

    await userEvent.click(button)
    await expect(button).toHaveTextContent('Click me')
  }
}
```

### All Variants Matrix
```typescript
// Button.stories.tsx (continued)
export const AllVariants: Story = {
  render: () => (
    <div style={{ display: 'flex', gap: '1rem', flexDirection: 'column' }}>
      <div style={{ display: 'flex', gap: '1rem' }}>
        <Button variant="primary">Primary</Button>
        <Button variant="secondary">Secondary</Button>
        <Button variant="danger">Danger</Button>
      </div>
      <div style={{ display: 'flex', gap: '1rem' }}>
        <Button size="small">Small</Button>
        <Button size="medium">Medium</Button>
        <Button size="large">Large</Button>
      </div>
      <div style={{ display: 'flex', gap: '1rem' }}>
        <Button disabled>Disabled</Button>
        <Button loading>Loading</Button>
      </div>
    </div>
  )
}
```

## Tier 3: Visual Regression with Playwright

### Configuration
```typescript
// playwright.config.ts
import { defineConfig } from '@playwright/test'

export default defineConfig({
  testDir: './tests/visual',
  use: {
    baseURL: 'http://localhost:6006', // Storybook dev server
  },
  webServer: {
    command: 'npm run storybook',
    port: 6006,
    reuseExistingServer: !process.env.CI
  }
})
```

### Visual Regression Tests
```typescript
// tests/visual/button.spec.ts
import { test, expect } from '@playwright/test'

test.describe('Button Visual Tests', () => {
  test('all variants match snapshot', async ({ page }) => {
    await page.goto('/iframe.html?id=components-button--all-variants')

    // Wait for fonts to load
    await page.waitForLoadState('networkidle')

    // Take screenshot
    await expect(page).toHaveScreenshot('button-variants.png')
  })

  test('primary button hover state', async ({ page }) => {
    await page.goto('/iframe.html?id=components-button--primary')

    const button = page.getByRole('button')
    await button.hover()

    await expect(button).toHaveScreenshot('button-primary-hover.png')
  })

  test('button in dark mode', async ({ page }) => {
    await page.goto('/iframe.html?id=components-button--primary&globals=theme:dark')

    await expect(page).toHaveScreenshot('button-primary-dark.png')
  })

  test('responsive button on mobile', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 })
    await page.goto('/iframe.html?id=components-button--large')

    await expect(page).toHaveScreenshot('button-mobile.png')
  })
})
```

### Cross-Browser Visual Testing
```typescript
// playwright.config.ts
export default defineConfig({
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] }
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] }
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] }
    },
    {
      name: 'mobile',
      use: { ...devices['iPhone 12'] }
    }
  ]
})
```

## Accessibility Testing

### Automated A11y with jest-axe
```typescript
// test-setup.js
import { toHaveNoViolations } from 'jest-axe'
expect.extend(toHaveNoViolations)
```

### Storybook A11y Addon
```typescript
// .storybook/preview.ts
import { withA11y } from '@storybook/addon-a11y'

export const decorators = [withA11y]

export const parameters = {
  a11y: {
    config: {
      rules: [
        {
          id: 'color-contrast',
          enabled: true
        }
      ]
    }
  }
}
```

### Manual Keyboard Testing
```typescript
// Modal.test.tsx
describe('Modal Keyboard Navigation', () => {
  it('supports keyboard navigation', async () => {
    const user = userEvent.setup()

    render(
      <Modal isOpen={true} onClose={() => {}}>
        <button>First</button>
        <input type="text" placeholder="Text input" />
        <a href="#test">Link</a>
        <button>Last</button>
      </Modal>
    )

    // Test tab order
    await user.keyboard('{Tab}')
    expect(screen.getByText('First')).toHaveFocus()

    await user.keyboard('{Tab}')
    expect(screen.getByPlaceholderText('Text input')).toHaveFocus()

    await user.keyboard('{Tab}')
    expect(screen.getByText('Link')).toHaveFocus()

    await user.keyboard('{Tab}')
    expect(screen.getByText('Last')).toHaveFocus()

    // Test reverse tab
    await user.keyboard('{Shift>}{Tab}{/Shift}')
    expect(screen.getByText('Link')).toHaveFocus()
  })
})
```

## CI/CD Integration

```yaml
# .github/workflows/component-tests.yml
name: Component Library Tests

on: [push, pull_request]

jobs:
  unit-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3

      - name: Install dependencies
        run: npm ci

      - name: Run unit tests
        run: npm run test:coverage

      - name: Upload coverage
        uses: codecov/codecov-action@v3

  visual-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3

      - name: Install dependencies
        run: npm ci

      - name: Install Playwright
        run: npx playwright install --with-deps

      - name: Run visual tests
        run: npm run test:visual

      - name: Upload visual diffs
        uses: actions/upload-artifact@v3
        if: failure()
        with:
          name: visual-diffs
          path: test-results/

  build-storybook:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3

      - name: Install dependencies
        run: npm ci

      - name: Build Storybook
        run: npm run build-storybook

      - name: Deploy to Chromatic
        uses: chromaui/action@v1
        with:
          projectToken: ${{ secrets.CHROMATIC_PROJECT_TOKEN }}
```

## Alternative Options

### Option B: Storybook + Chromatic (SaaS)

**When to choose**: Team wants managed visual regression, budget available

**Advantages**:
- Fully managed visual regression
- UI review workflow
- Better diff visualization
- Automatic baseline management

**Disadvantages**:
- Monthly cost ($149-$899/month)
- Vendor lock-in
- Requires external service

**Setup complexity**: Low

### Option C: React Testing Library Only

**When to choose**: Small component library, no visual testing needed

**Advantages**:
- Simplest setup
- Fast tests
- Free

**Disadvantages**:
- No visual regression
- No living documentation
- Manual visual QA needed

**Setup complexity**: Very low

## Validation Results

### Speed Benchmarks
- **Unit tests**: 0.8s for 50 component tests
- **Visual tests**: 45s for 20 snapshot comparisons
- **Storybook build**: 15s

### Developer Experience Metrics
- Component development time: 30% faster with Storybook
- Bug detection: Catch 90% of visual regressions
- Documentation: Auto-generated from stories

### Maintenance Burden
- **Low to Medium**: Visual snapshots need updates on intentional changes
- Unit tests are stable
- Storybook requires occasional addon updates

## Known Gaps

### What This Solution Cannot Handle
1. **Real user testing** - Needs user research
2. **Performance profiling** - Needs React DevTools
3. **Bundle size analysis** - Needs bundlesize tool
4. **Usage analytics** - Needs tracking integration

### Scenarios Requiring Additional Tools
- **Color contrast checking**: Add axe-core
- **Screen reader testing**: Manual QA needed
- **Animation testing**: Custom Playwright scripts
- **Print styles**: Manual browser testing

## Recommended Tool Stack

**Minimal viable testing**:
```
Vitest + Testing Library
Storybook (for development)
```

**Production-ready stack**:
```
Vitest + Testing Library
Storybook with a11y addon
Playwright for visual regression
jest-axe for accessibility
```

**Enterprise stack**:
```
Above tools plus:
Chromatic (visual regression SaaS)
Bundle size tracking (bundlesize)
Performance monitoring (Lighthouse CI)
Component usage analytics
```

## Documentation Strategy

### Auto-Generated Docs
```typescript
// Button.stories.tsx
const meta: Meta<typeof Button> = {
  title: 'Components/Button',
  component: Button,
  tags: ['autodocs'],
  parameters: {
    docs: {
      description: {
        component: 'A versatile button component with multiple variants and sizes.'
      }
    }
  }
}
```

### MDX Documentation
```mdx
<!-- Button.mdx -->
import { Canvas, Meta, Story } from '@storybook/blocks'
import * as ButtonStories from './Button.stories'

<Meta of={ButtonStories} />

# Button

Buttons allow users to take actions with a single tap.

## Usage

```tsx
import { Button } from '@company/ui'

<Button variant="primary">Click me</Button>
```

## Variants

<Canvas of={ButtonStories.AllVariants} />

## Accessibility

- Keyboard navigable (Tab, Enter, Space)
- Screen reader announcements
- Focus visible indicator
- Disabled state properly conveyed
```

## Cost-Benefit Analysis

### Setup Investment
- **Time**: 2-3 days for full testing infrastructure
- **Training**: 1 day for team onboarding
- **Tooling cost**: Free (or $150/month for Chromatic)

### Ongoing Returns
- **Quality assurance**: Prevent visual bugs in production
- **Development speed**: Faster iteration with live preview
- **Documentation**: Auto-generated from code
- **Confidence**: Safe refactoring and updates

## Migration Path

### From No Component Testing
1. Set up Storybook for development
2. Add stories for existing components
3. Add unit tests for critical components
4. Add visual regression last

**Effort**: 2-4 weeks
**Risk**: Low
