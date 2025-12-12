# Form & Validation Libraries: Domain Explainer

## What Problem Do They Solve?

Forms are deceptively complex. A simple login form requires:
- Tracking input values
- Validation (email format, password length)
- Error messages
- Submit handling
- Loading states
- Preventing double submits
- Accessibility (labels, error announcements)

Multiply by dozens of forms in a real application, and complexity explodes.

## Two Separate Concerns

### 1. Form State Management
Tracking values, dirty state, touched fields, submission status.

Libraries: React Hook Form, Formik, TanStack Form

### 2. Schema Validation
Defining rules (email format, required fields) and checking data against them.

Libraries: Zod, Yup, Valibot

These concerns are **separate but work together**:
```tsx
// Form library handles state
const { register, handleSubmit } = useForm({
  // Validation library handles rules
  resolver: zodResolver(schema)
})
```

## Key Concepts

### Controlled vs Uncontrolled Components

**Controlled**: React state drives the input
```tsx
const [value, setValue] = useState('')
<input value={value} onChange={e => setValue(e.target.value)} />
// Every keystroke: setState → re-render
```

**Uncontrolled**: DOM holds the value, React reads via ref
```tsx
const inputRef = useRef()
<input ref={inputRef} />
// Read value: inputRef.current.value
// No re-renders during typing
```

**Why it matters**: Controlled forms re-render on every keystroke. With 20 fields, that's 20 re-renders per character typed. Uncontrolled is faster.

### Schema Validation

Instead of inline validation:
```tsx
// Inline (hard to reuse, test, maintain)
if (!email.includes('@')) {
  setError('Invalid email')
}
if (password.length < 8) {
  setError('Too short')
}
```

Use declarative schemas:
```tsx
// Schema (reusable, testable, type-safe)
const schema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
})
```

### Type Inference

Modern validation libraries can **derive TypeScript types from schemas**:

```tsx
const schema = z.object({
  email: z.string(),
  age: z.number(),
})

// Automatically: { email: string; age: number }
type FormData = z.infer<typeof schema>
```

This is powerful: define once, get both validation AND types.

### Validation Timing

When to validate?

| Timing | Description | UX |
|--------|-------------|-----|
| onChange | Every keystroke | Annoying for users |
| onBlur | When leaving field | Good balance |
| onSubmit | On form submit | Delayed feedback |
| onTouched | After first interaction + onChange | Common pattern |

Most libraries let you configure this per-field or globally.

### Error Handling Patterns

**Field-level errors**: Each field shows its own error
```tsx
<input {...register('email')} />
{errors.email && <span>{errors.email.message}</span>}
```

**Form-level errors**: Errors shown together (less common)
```tsx
{Object.values(errors).map(err => <li>{err.message}</li>)}
```

**Server errors**: Returned from API, mapped to fields
```tsx
// After API call fails
setError('email', { message: 'Email already exists' })
```

### Field Arrays

Dynamic lists of fields (add/remove items):

```tsx
// Tasks list with add/remove
const { fields, append, remove } = useFieldArray({ name: 'tasks' })

{fields.map((field, index) => (
  <div key={field.id}>
    <input {...register(`tasks.${index}.name`)} />
    <button onClick={() => remove(index)}>Remove</button>
  </div>
))}
<button onClick={() => append({ name: '' })}>Add Task</button>
```

### Nested Objects

Forms often map to nested data structures:

```tsx
const schema = z.object({
  user: z.object({
    name: z.string(),
    address: z.object({
      street: z.string(),
      city: z.string(),
    }),
  }),
})

// Access nested fields
register('user.name')
register('user.address.street')
```

## Common Patterns

### Resolver Pattern

Form libraries use "resolvers" to integrate with any validation library:

```tsx
import { zodResolver } from '@hookform/resolvers/zod'
import { yupResolver } from '@hookform/resolvers/yup'
import { valibotResolver } from '@hookform/resolvers/valibot'

useForm({ resolver: zodResolver(schema) })
useForm({ resolver: yupResolver(schema) })
useForm({ resolver: valibotResolver(schema) })
```

This decouples form state from validation logic.

### Default Values

Initialize forms with existing data (edit forms):

```tsx
const { register } = useForm({
  defaultValues: {
    name: user.name,
    email: user.email,
  },
})
```

### Async Validation

Some validations require API calls:

```tsx
const schema = z.object({
  username: z.string().refine(
    async (val) => {
      const exists = await checkUsernameExists(val)
      return !exists
    },
    { message: 'Username taken' }
  ),
})
```

### Transformations

Modify data during validation:

```tsx
const schema = z.object({
  email: z.string().email().transform(val => val.toLowerCase()),
  age: z.string().transform(val => parseInt(val, 10)),
})
```

## Bundle Size Considerations

Forms add significant JavaScript:

| Combination | Size |
|-------------|------|
| No library (manual) | 0KB |
| React Hook Form only | 12KB |
| RHF + Zod | 57KB |
| RHF + Valibot | 14KB |
| Formik + Yup | 104KB |

For bundle-critical applications, consider:
- Valibot (90% smaller than Zod)
- Lazy loading form-heavy routes
- Server-side validation only for simple forms

## Server vs Client Validation

**Client-side**: Fast feedback, better UX
```tsx
// Immediate feedback as user types
{errors.email && <span>Invalid email</span>}
```

**Server-side**: Security, authoritative
```tsx
// After submit, server checks
const result = await api.submit(data)
if (result.errors) {
  setServerErrors(result.errors)
}
```

**Best practice**: Do both. Client for UX, server for security. Never trust client-only validation for sensitive data.

## Accessibility

Form libraries should handle:
- `aria-invalid` on fields with errors
- `aria-describedby` linking fields to error messages
- Error announcements for screen readers
- Focus management (focus first error on submit)

Most modern libraries handle this automatically.

## Common Misconceptions

### "Forms are simple"
Forms are deceptively complex. Validation, accessibility, async operations, nested data, arrays, error handling - each adds complexity.

### "I can build my own"
You can, but you'll reinvent solutions to solved problems. Libraries encode years of edge cases and best practices.

### "More features = better library"
Sometimes simpler is better. React Hook Form wins partly because it does less (uncontrolled) and performs better.

### "Validation belongs in the form library"
They're separate concerns. Form = state. Validation = rules. The resolver pattern lets you mix and match.

## Evolution of the Space

### 2015-2018: Manual forms, redux-form
Every project rolled their own. Redux-form tried to solve it with Redux.

### 2018-2020: Formik + Yup era
Formik simplified form state. Yup became the default validation. This combo dominated.

### 2020-2022: React Hook Form rises
Performance-focused, uncontrolled approach. Smaller bundle. Overtook Formik.

### 2022-Present: Zod takes over
TypeScript-first validation with type inference. Zod overtook Yup in downloads.

### 2025 Trend
- React Hook Form + Zod is the standard
- Valibot for bundle-sensitive apps
- Formik is abandoned
- TanStack Form emerging

---

**Last Updated**: 2025-12-12
**Related Research**: 1.111 (State Management), 1.113 (UI Components)
