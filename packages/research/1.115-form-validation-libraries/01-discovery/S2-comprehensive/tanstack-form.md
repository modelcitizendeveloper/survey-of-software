# TanStack Form - Technical Deep-Dive

## Architecture

### Signal-Based Reactivity

TanStack Form uses **signals** (fine-grained reactivity) instead of React state, similar to Solid.js and Preact Signals.

**Traditional React approach** (Formik):
```tsx
// Every change: setState → re-render entire tree
const [values, setValues] = useState({})
<input value={values.email} onChange={e => setValues({...values, email: e.target.value})} />
```

**TanStack Form's signal approach**:
```tsx
// Only subscribed components re-render
const form = useForm()
<form.Field name="email">
  {(field) => <input {...field.getInputProps()} />}
</form.Field>
// Only this field re-renders when email changes
```

### Store Architecture

TanStack Form uses a **store-based architecture** with granular subscriptions:

```tsx
class FormStore<TFormData> {
  state: FormState<TFormData>
  fieldMeta: Map<string, FieldMeta>
  listeners: Set<Listener>

  subscribe(listener: Listener) {
    // Subscribe to specific field changes
    this.listeners.add(listener)
    return () => this.listeners.delete(listener)
  }

  notify(fieldName: string) {
    // Only notify listeners for this specific field
    this.listeners.forEach(listener => {
      if (listener.shouldUpdate(fieldName)) {
        listener.update()
      }
    })
  }
}
```

**Key insight**: Unlike React Hook Form (refs) or Formik (state), TanStack uses **observable store pattern** for surgical re-renders.

### Framework Agnostic Core

TanStack Form is **headless** with adapters for each framework:

```
@tanstack/form-core        (~5KB, framework-agnostic logic)
  ├── @tanstack/react-form      (~3KB, React adapter)
  ├── @tanstack/vue-form        (~3KB, Vue adapter)
  ├── @tanstack/solid-form      (~3KB, Solid adapter)
  ├── @tanstack/angular-form    (~3KB, Angular adapter)
  └── @tanstack/lit-form        (~3KB, Lit adapter)
```

**Total bundle**: ~8-10KB for React (core + React adapter).

### Field Registration

TanStack uses **declarative field components**:

```tsx
const form = useForm({
  defaultValues: { email: '' }
})

<form.Field name="email">
  {(field) => (
    <input
      value={field.state.value}
      onChange={(e) => field.handleChange(e.target.value)}
      onBlur={field.handleBlur}
    />
  )}
</form.Field>
```

**Key difference**:
- React Hook Form: `{...register('email')}` (imperative)
- TanStack Form: `<form.Field name="email">` (declarative)

## Performance Characteristics

### Bundle Size Breakdown

**~10KB gzipped total:**
- Core logic: 5KB
- React adapter: 3KB
- Type utilities: 1KB
- Dev warnings: 1KB

**Zero dependencies** - fully self-contained.

**Tree-shaking**: Excellent - unused features eliminated.

### Runtime Performance

**Benchmark: 20-field form, typing in single field**

| Library | Re-renders per keystroke | Memory overhead |
|---------|-------------------------|-----------------|
| TanStack Form | 1 (only changed field) | ~1KB per form |
| React Hook Form | 0 (ref updates) | ~2KB per form |
| Formik | 20 (entire form) | ~5KB per form |

**Why only 1 re-render**:
- Signal-based subscription (only field component re-renders)
- Form state lives outside React state
- No parent component re-renders

**Why not 0 like RHF**:
- TanStack re-renders the field component to update value
- RHF skips React entirely (DOM updates directly)

**Trade-off**: TanStack is slightly slower than RHF but faster than Formik, with better ergonomics than RHF for complex forms.

### Memory Footprint

- Form instance: ~500 bytes
- Field registration: ~50 bytes per field
- Validation state: ~100 bytes per validator
- Total: ~1KB for typical form

**Comparison**: Smallest memory footprint of all libraries.

## API Design Patterns

### Form Creation

```tsx
import { useForm } from '@tanstack/react-form'

const form = useForm({
  defaultValues: {
    email: '',
    age: 0,
  },
  onSubmit: async ({ value, formApi }) => {
    // value: validated form data
    // formApi: form instance for actions
    await submitToAPI(value)
  },
})
```

**Returns form instance** with methods:
```tsx
form.Field        // Field component
form.Subscribe    // Subscription component
form.handleSubmit // Submit handler
form.reset        // Reset form
form.setFieldValue // Imperative API
form.validateAllFields // Trigger validation
form.state        // Current form state
```

### Field Component

**Basic usage**:
```tsx
<form.Field name="email">
  {(field) => (
    <div>
      <input
        value={field.state.value}
        onChange={(e) => field.handleChange(e.target.value)}
        onBlur={field.handleBlur}
      />
      {field.state.meta.errors && (
        <div>{field.state.meta.errors[0]}</div>
      )}
    </div>
  )}
</form.Field>
```

**Field API**:
```tsx
field.name              // Field name
field.state.value       // Current value
field.state.meta.errors // Validation errors
field.state.meta.isTouched  // User interacted
field.state.meta.isDirty    // Modified since init
field.state.meta.isValidating  // Validation running
field.handleChange      // Update value
field.handleBlur        // Mark touched
field.validate          // Trigger validation
field.getInputProps()   // Spread props for inputs
```

**getInputProps() helper**:
```tsx
<form.Field name="email">
  {(field) => (
    <input {...field.getInputProps()} />
    // Automatically wires: value, onChange, onBlur, name
  )}
</form.Field>
```

### Validators

**Inline validation**:
```tsx
<form.Field
  name="email"
  validators={{
    onChange: ({ value }) => {
      if (!value) return 'Email is required'
      if (!value.includes('@')) return 'Invalid email'
      return undefined
    },
    onBlur: ({ value }) => {
      // Validate on blur
    },
    onSubmit: async ({ value }) => {
      // Async validation on submit
      const exists = await checkEmail(value)
      if (exists) return 'Email already registered'
    },
  }}
>
  {(field) => <input {...field.getInputProps()} />}
</form.Field>
```

**Validator timing**:
- `onChange`: Runs on every value change (immediate feedback)
- `onBlur`: Runs when field loses focus (common pattern)
- `onSubmit`: Runs during form submission (async safe)
- `onMount`: Runs when field mounts
- `onChangeAsync`: Debounced async validation on change

### Schema Validation

TanStack Form integrates with **any** validation library via adapters:

**Zod integration**:
```tsx
import { zodValidator } from '@tanstack/zod-form-adapter'
import { z } from 'zod'

const schema = z.object({
  email: z.string().email(),
  age: z.number().min(18),
})

const form = useForm({
  defaultValues: { email: '', age: 0 },
  validators: {
    onChange: schema,
  },
  validatorAdapter: zodValidator,
})
```

**Yup integration**:
```tsx
import { yupValidator } from '@tanstack/yup-form-adapter'
import * as yup from 'yup'

const schema = yup.object({
  email: yup.string().email().required(),
})

const form = useForm({
  validatorAdapter: yupValidator,
  validators: { onChange: schema },
})
```

**Valibot integration**:
```tsx
import { valibotValidator } from '@tanstack/valibot-form-adapter'
import * as v from 'valibot'

const schema = v.object({
  email: v.string([v.email()]),
})

const form = useForm({
  validatorAdapter: valibotValidator,
  validators: { onChange: schema },
})
```

## Advanced Features

### Field Arrays

Dynamic lists with efficient updates:

```tsx
const form = useForm({
  defaultValues: {
    tasks: [{ name: '', done: false }],
  },
})

<form.Field name="tasks">
  {(field) => (
    <div>
      {field.state.value.map((_, index) => (
        <form.Field key={index} name={`tasks[${index}].name`}>
          {(subField) => (
            <input {...subField.getInputProps()} />
          )}
        </form.Field>
      ))}

      <button
        type="button"
        onClick={() => {
          field.pushValue({ name: '', done: false })
        }}
      >
        Add Task
      </button>
    </div>
  )}
</form.Field>
```

**Array methods**:
```tsx
field.pushValue(item)          // Add to end
field.insertValue(index, item) // Insert at index
field.removeValue(index)       // Remove at index
field.swapValues(indexA, indexB) // Swap positions
field.moveValue(from, to)      // Move item
```

**Performance**: Only modified field re-renders, not entire array.

### Nested Objects

```tsx
const form = useForm({
  defaultValues: {
    user: {
      profile: {
        name: '',
        bio: '',
      },
      settings: {
        theme: 'light',
      },
    },
  },
})

<form.Field name="user.profile.name">
  {(field) => <input {...field.getInputProps()} />}
</form.Field>

<form.Field name="user.settings.theme">
  {(field) => <select {...field.getInputProps()}>...</select>}
</form.Field>
```

### Cross-Field Validation

**Access parent form values**:

```tsx
<form.Field
  name="confirmPassword"
  validators={{
    onChange: ({ value, fieldApi }) => {
      const password = fieldApi.form.getFieldValue('password')
      if (value !== password) {
        return 'Passwords must match'
      }
    },
  }}
>
  {(field) => <input {...field.getInputProps()} />}
</form.Field>
```

**Validate multiple fields**:

```tsx
<form.Field
  name="endDate"
  validators={{
    onChange: ({ value, fieldApi }) => {
      const startDate = fieldApi.form.getFieldValue('startDate')
      if (new Date(value) < new Date(startDate)) {
        return 'End date must be after start date'
      }
    },
  }}
>
  {(field) => <input {...field.getInputProps()} />}
</form.Field>
```

### Subscribe to Form State

React to specific form state changes:

```tsx
<form.Subscribe
  selector={(state) => ({
    canSubmit: state.canSubmit,
    isSubmitting: state.isSubmitting,
  })}
>
  {(state) => (
    <button disabled={!state.canSubmit || state.isSubmitting}>
      {state.isSubmitting ? 'Submitting...' : 'Submit'}
    </button>
  )}
</form.Subscribe>
```

**Selector pattern**: Only re-render when selected state changes.

**Available state**:
```tsx
state.values          // Current values
state.errors          // All errors
state.canSubmit       // Form is valid + not submitting
state.isSubmitting    // Submit in progress
state.isValidating    // Validation running
state.isDirty         // Modified since init
state.isTouched       // User interacted
state.submitCount     // Number of submit attempts
state.validationMetaMap // Validation metadata per field
```

### Transformations

**Transform on submit**:

```tsx
const form = useForm({
  defaultValues: { name: '' },
  onSubmit: async ({ value }) => {
    const transformed = {
      ...value,
      name: value.name.trim().toUpperCase(),
    }
    await submitToAPI(transformed)
  },
})
```

**Transform on change**:

```tsx
<form.Field
  name="phone"
  validators={{
    onChange: ({ value }) => {
      // Validate
      if (!/^\d{10}$/.test(value)) return 'Invalid phone'
    },
  }}
>
  {(field) => (
    <input
      {...field.getInputProps()}
      onChange={(e) => {
        // Transform then validate
        const cleaned = e.target.value.replace(/\D/g, '')
        field.handleChange(cleaned)
      }}
    />
  )}
</form.Field>
```

### Async Validation with Debounce

```tsx
<form.Field
  name="username"
  validators={{
    onChangeAsyncDebounceMs: 500,
    onChangeAsync: async ({ value }) => {
      const exists = await checkUsername(value)
      if (exists) return 'Username already taken'
    },
  }}
>
  {(field) => (
    <div>
      <input {...field.getInputProps()} />
      {field.state.meta.isValidating && <span>Checking...</span>}
    </div>
  )}
</form.Field>
```

**Built-in debouncing**: No need for external libraries.

### Reset Form

```tsx
// Reset to default values
form.reset()

// Reset to new values
form.reset({
  email: 'new@example.com',
  age: 25,
})

// Reset in submit handler
onSubmit: async ({ value, formApi }) => {
  await submitToAPI(value)
  formApi.reset() // Clear form after success
}
```

## TypeScript Integration

### Generic Type Support

```tsx
type FormData = {
  email: string
  age: number
  tags: string[]
}

const form = useForm<FormData>({
  defaultValues: {
    email: '',
    age: 0,
    tags: [],
  },
})

// Type-safe field access
<form.Field name="email">      // ✓
<form.Field name="invalid">    // ✗ Type error
```

### Type Inference with Validators

**Zod schema types flow to form**:

```tsx
import { zodValidator } from '@tanstack/zod-form-adapter'

const schema = z.object({
  email: z.string().email(),
  age: z.number(),
})

const form = useForm({
  validatorAdapter: zodValidator,
  validators: { onChange: schema },
  defaultValues: {
    email: '',
    age: 0,
  },
  onSubmit: async ({ value }) => {
    // value is typed as { email: string; age: number }
  },
})
```

### Field-Level Types

```tsx
<form.Field<FormData, 'email'>
  name="email"
  validators={{
    onChange: ({ value }) => {
      // value is typed as string
    },
  }}
>
  {(field) => {
    // field.state.value is typed as string
    return <input {...field.getInputProps()} />
  }}
</form.Field>
```

## Integration Patterns

### With UI Libraries

**Material-UI**:
```tsx
import { TextField } from '@mui/material'

<form.Field name="email">
  {(field) => (
    <TextField
      value={field.state.value}
      onChange={(e) => field.handleChange(e.target.value)}
      error={!!field.state.meta.errors}
      helperText={field.state.meta.errors?.[0]}
    />
  )}
</form.Field>
```

**Chakra UI**:
```tsx
import { Input, FormControl, FormErrorMessage } from '@chakra-ui/react'

<form.Field name="email">
  {(field) => (
    <FormControl isInvalid={!!field.state.meta.errors}>
      <Input {...field.getInputProps()} />
      <FormErrorMessage>{field.state.meta.errors?.[0]}</FormErrorMessage>
    </FormControl>
  )}
</form.Field>
```

### With TanStack Query

**Fetch default values**:

```tsx
import { useQuery } from '@tanstack/react-query'

function EditUserForm({ userId }) {
  const { data: user } = useQuery({
    queryKey: ['user', userId],
    queryFn: () => fetchUser(userId),
  })

  const form = useForm({
    defaultValues: user || { name: '', email: '' },
  })

  // Form updates when query resolves
}
```

**Submit with mutation**:

```tsx
import { useMutation } from '@tanstack/react-query'

const mutation = useMutation({
  mutationFn: (data) => updateUser(data),
})

const form = useForm({
  onSubmit: async ({ value }) => {
    await mutation.mutateAsync(value)
  },
})
```

### With TanStack Router

**Form state in URL**:

```tsx
import { useNavigate } from '@tanstack/react-router'

const form = useForm({
  defaultValues: { search: '' },
  onSubmit: async ({ value }) => {
    navigate({
      search: { q: value.search },
    })
  },
})
```

## Testing Strategies

### Unit Testing

```tsx
import { renderHook, act } from '@testing-library/react'
import { useForm } from '@tanstack/react-form'

test('validates email field', async () => {
  const { result } = renderHook(() =>
    useForm({
      defaultValues: { email: '' },
    })
  )

  const fieldApi = result.current.getFieldMeta('email')

  act(() => {
    result.current.setFieldValue('email', 'invalid')
  })

  await act(async () => {
    await result.current.validateAllFields('change')
  })

  expect(fieldApi.errors).toContain('Invalid email')
})
```

### Integration Testing

```tsx
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'

test('submits form with valid data', async () => {
  const onSubmit = jest.fn()

  render(<MyForm onSubmit={onSubmit} />)

  await userEvent.type(screen.getByLabelText('Email'), 'test@example.com')
  await userEvent.click(screen.getByRole('button', { name: /submit/i }))

  expect(onSubmit).toHaveBeenCalledWith({
    value: { email: 'test@example.com' },
    formApi: expect.anything(),
  })
})
```

### Testing Async Validation

```tsx
test('validates username availability', async () => {
  const checkUsername = jest.fn().mockResolvedValue(true)

  render(<MyForm checkUsername={checkUsername} />)

  const input = screen.getByLabelText('Username')
  await userEvent.type(input, 'taken')

  await waitFor(() => {
    expect(screen.getByText('Username already taken')).toBeInTheDocument()
  })
})
```

## Architectural Trade-offs

### Advantages

1. **Performance**: Signal-based, only changed fields re-render
2. **Bundle size**: Tiny (~10KB), smaller than RHF
3. **Framework agnostic**: Works with React, Vue, Solid, etc.
4. **TypeScript**: Excellent type inference
5. **Modern DX**: Declarative API, built-in async/debounce
6. **TanStack ecosystem**: Integrates with Query, Router, Table
7. **Active development**: Maintained by TanStack team
8. **Validation flexibility**: Works with Zod, Yup, Valibot, custom

### Disadvantages

1. **New/less mature**: Released 2023, smaller ecosystem than RHF
2. **Learning curve**: Different mental model (signals vs state/refs)
3. **Render prop verbosity**: More boilerplate than RHF's spread pattern
4. **Less examples**: Fewer tutorials, Stack Overflow answers
5. **Breaking changes**: Still in v0, API may change
6. **Community size**: Smaller than RHF (but growing)

## When to Use

**Choose TanStack Form when**:
- Using TanStack ecosystem (Query, Router, Table)
- Want modern, signal-based architecture
- Need framework portability (React today, Vue tomorrow)
- Value small bundle size + performance
- Building complex forms with async validation
- Prefer declarative API over imperative

**Consider alternatives when**:
- Using React Hook Form already (migration cost)
- Need battle-tested stability → RHF (7+ years mature)
- Want largest ecosystem → RHF (most tutorials/examples)
- Don't care about bundle size → any library works
- Simple forms → native HTML forms may suffice

## Comparison with React Hook Form

| Aspect | TanStack Form | React Hook Form |
|--------|---------------|-----------------|
| Bundle size | ~10KB | ~12KB |
| Re-renders | 1 per field change | 0 (ref updates) |
| API style | Declarative (components) | Imperative (hooks) |
| Mental model | Signals/observables | Refs/uncontrolled |
| Framework support | React, Vue, Solid, etc. | React only |
| Maturity | New (2023) | Mature (2019) |
| Ecosystem | Growing | Large |
| TypeScript | Excellent | Excellent |
| Validation | Adapter-based | Resolver-based |
| Async validation | Built-in debounce | Manual |

**Migration from RHF to TanStack**:

```tsx
// React Hook Form
const { register, handleSubmit } = useForm()
<input {...register('email')} />

// TanStack Form
const form = useForm()
<form.Field name="email">
  {(field) => <input {...field.getInputProps()} />}
</form.Field>
```

**Trade-off**: TanStack has more boilerplate but better TypeScript inference and framework portability.

## Performance Optimization

### Use Subscribe Selectively

```tsx
// ✗ Bad: Re-renders on any form state change
<form.Subscribe>
  {(state) => <div>{state.values.email}</div>}
</form.Subscribe>

// ✓ Good: Only re-renders when email changes
<form.Subscribe selector={(state) => state.values.email}>
  {(email) => <div>{email}</div>}
</form.Subscribe>
```

### Debounce Async Validation

```tsx
<form.Field
  name="username"
  validators={{
    onChangeAsyncDebounceMs: 500, // Wait 500ms before validating
    onChangeAsync: async ({ value }) => {
      return await checkUsername(value)
    },
  }}
>
```

### Validate on Blur, Not Change

```tsx
<form.Field
  name="email"
  validators={{
    onBlur: ({ value }) => {
      // Only validate when field loses focus
    },
  }}
>
```

## Resources

- [Official Docs](https://tanstack.com/form/latest)
- [GitHub](https://github.com/TanStack/form)
- [Examples](https://tanstack.com/form/latest/docs/examples/react/simple)
- [API Reference](https://tanstack.com/form/latest/docs/reference/formApi)
- [Zod Adapter](https://tanstack.com/form/latest/docs/framework/react/guides/validation#adapter-based-validation-zod)
- [Discord Community](https://discord.com/invite/WrRKjPJ)
- [TanStack Ecosystem](https://tanstack.com)
