# TanStack Form

> "Headless, performant, and type-safe form state management."

## Quick Facts

| Metric | Value |
|--------|-------|
| GitHub Stars | ~4,000 |
| npm Weekly Downloads | ~50K |
| Bundle Size | ~10KB |
| Dependencies | 1 (@tanstack/store) |
| License | MIT |
| TypeScript Requirement | v5.4+ |

## What Is TanStack Form?

TanStack Form is the newest entry in the form library space, from the creators of TanStack Query, Router, and Table. It brings the same philosophy: **headless, performant, and framework-agnostic**.

## Key Differentiators

### 1. Signals-Based Architecture

Built on `@tanstack/store`, each field only re-renders when its specific data changes:

```tsx
// Only re-renders when this specific field changes
<form.Field name="email">
  {(field) => <input value={field.state.value} />}
</form.Field>
```

### 2. First-Class TypeScript

Written 100% in TypeScript with automatic type inference:

```tsx
const form = useForm({
  defaultValues: {
    email: '',
    age: 0,
  },
})

// TypeScript knows: email is string, age is number
form.getFieldValue('email') // string
form.getFieldValue('age') // number
```

### 3. Framework Agnostic

Same API across React, Vue, Angular, Solid, and Lit.

## Basic Usage

```tsx
import { useForm } from '@tanstack/react-form'

function LoginForm() {
  const form = useForm({
    defaultValues: {
      email: '',
      password: '',
    },
    onSubmit: async ({ value }) => {
      console.log(value)
    },
  })

  return (
    <form
      onSubmit={(e) => {
        e.preventDefault()
        form.handleSubmit()
      }}
    >
      <form.Field name="email">
        {(field) => (
          <>
            <input
              value={field.state.value}
              onChange={(e) => field.handleChange(e.target.value)}
              onBlur={field.handleBlur}
            />
            {field.state.meta.errors.length > 0 && (
              <span>{field.state.meta.errors[0]}</span>
            )}
          </>
        )}
      </form.Field>

      <button type="submit">Submit</button>
    </form>
  )
}
```

## Validation with Zod

```tsx
import { useForm } from '@tanstack/react-form'
import { zodValidator } from '@tanstack/zod-form-adapter'
import { z } from 'zod'

const form = useForm({
  validatorAdapter: zodValidator(),
  defaultValues: {
    email: '',
  },
})

<form.Field
  name="email"
  validators={{
    onChange: z.string().email('Invalid email'),
    onBlur: z.string().min(1, 'Required'),
  }}
>
  {(field) => /* ... */}
</form.Field>
```

## When to Choose TanStack Form

**Choose TanStack Form when:**
- Already using TanStack ecosystem (Query, Router, Table)
- Want signals-based reactivity
- Building framework-agnostic forms
- TypeScript v5.4+ is available

**Choose React Hook Form instead when:**
- Want larger ecosystem/community
- Need more third-party integrations
- Want simpler API for basic forms

## Comparison with React Hook Form

| Aspect | TanStack Form | React Hook Form |
|--------|--------------|-----------------|
| Architecture | Signals | Refs/Uncontrolled |
| Bundle | ~10KB | 12KB |
| Community | Growing | Huge |
| Ecosystem | Small | Large |
| TypeScript | v5.4+ required | Any |
| Learning curve | Higher | Lower |

## Current Status

TanStack Form is **actively developed** but still maturing:
- Smaller community than RHF
- Fewer tutorials and resources
- API may evolve

For most projects, React Hook Form is still the safer choice. But TanStack Form is worth watching if you're invested in the TanStack ecosystem.

## Resources

- [Official Docs](https://tanstack.com/form/latest)
- [GitHub](https://github.com/TanStack/form)
- [TypeScript Guide](https://tanstack.com/form/latest/docs/typescript)
