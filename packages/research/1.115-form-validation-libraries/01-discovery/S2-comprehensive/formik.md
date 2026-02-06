# Formik - Technical Deep-Dive

## Architecture

### Controlled Component Strategy

Formik uses **React state** for all form values, the opposite of React Hook Form's uncontrolled approach.

**Formik's controlled approach**:
```tsx
// Every keystroke: setState → re-render
const [values, setValues] = useState({ email: '' })

<input
  value={values.email}
  onChange={(e) => setValues({ ...values, email: e.target.value })}
/>
```

This creates a **single source of truth** in React state, making form values easily accessible but causing re-renders.

### State Management Architecture

Formik maintains complex state internally:

```tsx
type FormikState<Values> = {
  values: Values              // Current form values
  errors: FormikErrors<Values>  // Validation errors
  touched: FormikTouched<Values> // User interaction
  isSubmitting: boolean         // Submit in progress
  isValidating: boolean         // Validation running
  submitCount: number           // Number of submit attempts
  initialValues: Values         // For reset
  initialErrors: FormikErrors<Values>
  initialTouched: FormikTouched<Values>
  initialStatus: any
  status: any                   // Custom status (user-defined)
}
```

**State updates trigger re-renders** of the entire form component tree (unless optimized with `React.memo`).

### Render Props Pattern

Formik pioneered **render props** for form libraries:

```tsx
<Formik
  initialValues={{ email: '' }}
  onSubmit={handleSubmit}
>
  {(formikProps) => (
    <form onSubmit={formikProps.handleSubmit}>
      <input
        name="email"
        value={formikProps.values.email}
        onChange={formikProps.handleChange}
        onBlur={formikProps.handleBlur}
      />
      {formikProps.errors.email && <div>{formikProps.errors.email}</div>}
    </form>
  )}
</Formik>
```

**Alternative**: Hook-based API (added later):

```tsx
function MyForm() {
  const formik = useFormik({
    initialValues: { email: '' },
    onSubmit: handleSubmit,
  })

  return (
    <form onSubmit={formik.handleSubmit}>
      <input
        name="email"
        value={formik.values.email}
        onChange={formik.handleChange}
      />
    </form>
  )
}
```

### Field Registration

Formik uses **name-based registration**:

```tsx
// Formik automatically tracks fields by name attribute
<input name="email" onChange={formik.handleChange} />

// Or use Field component:
<Field name="email" />
// Automatically wires onChange, onBlur, value
```

**Key insight**: Unlike RHF's ref-based registration, Formik relies on `name` attribute and state synchronization.

## Performance Characteristics

### Bundle Size Breakdown

**44KB gzipped (core):**
- Form state management: 15KB
- Validation integration: 10KB
- Field array utilities: 8KB
- Helper components: 6KB
- Context/provider: 3KB
- Utilities: 2KB

**Dependencies**: 8 packages (~12KB total)
- react-fast-compare (deep equality)
- tiny-warning (dev warnings)
- hoist-non-react-statics (HOC utilities)
- Others (lodash methods, etc.)

**Note**: Unmaintained since 2021, dependencies may have security issues.

### Runtime Performance

**Benchmark: 20-field form, typing in single field**

| Library | Re-renders per keystroke | Component updates |
|---------|-------------------------|-------------------|
| Formik | 20 (entire form tree) | All field components |
| React Hook Form | 0 (ref updates) | None |
| TanStack Form | 1 (signal update) | Only changed field |

**Why so many re-renders**:
1. Form values are in state
2. State update triggers re-render
3. All children re-render unless memoized
4. No built-in optimization (user must add `React.memo`)

**Memory footprint**: ~3-5KB per form instance (higher than RHF due to state overhead).

### Optimization Strategies

**Without optimization**:
```tsx
// Every keystroke re-renders ALL fields
<Field name="field1" />
<Field name="field2" />
<Field name="field3" />
// All 3 re-render when field1 changes
```

**With React.memo**:
```tsx
const MemoField = React.memo(Field)

<MemoField name="field1" />
<MemoField name="field2" />
<MemoField name="field3" />
// Only field1 re-renders (if values are compared correctly)
```

**FastField** (built-in optimization):
```tsx
import { FastField } from 'formik'

<FastField name="field1" />
// Only re-renders when field1 value/error/touched changes
// Skips re-renders when other fields change
```

**Trade-off**: `FastField` breaks cross-field dependencies.

## API Design Patterns

### useFormik Hook

```tsx
const formik = useFormik({
  initialValues: {
    email: '',
    password: '',
  },
  validationSchema: yupSchema,  // Yup integration
  validate: customValidator,     // Or custom function
  onSubmit: async (values, actions) => {
    await submitForm(values)
    actions.setSubmitting(false)
    actions.resetForm()
  },
  enableReinitialize: false,    // Re-initialize when initialValues change
  validateOnChange: true,       // Validate on every change
  validateOnBlur: true,         // Validate on blur
  validateOnMount: false,       // Validate on mount
})

// Returns object with:
formik.values           // Current values
formik.errors           // Validation errors
formik.touched          // Touched fields
formik.isSubmitting     // Submit state
formik.handleSubmit     // Submit handler
formik.handleChange     // Change handler
formik.handleBlur       // Blur handler
formik.setFieldValue    // Set single field
formik.setValues        // Set all values
formik.setFieldError    // Set single error
formik.setFieldTouched  // Set touched state
formik.resetForm        // Reset to initial
formik.validateForm     // Trigger validation
```

### Field Component

**Basic usage**:
```tsx
import { Field } from 'formik'

<Field name="email" />
// Renders <input> with automatic wiring
```

**Custom component**:
```tsx
<Field name="email" type="email" placeholder="Email" />

// Or with render prop:
<Field name="email">
  {({ field, form, meta }) => (
    <div>
      <input {...field} />
      {meta.touched && meta.error && <div>{meta.error}</div>}
    </div>
  )}
</Field>
```

**Field props**:
```tsx
field: {
  name: string           // Field name
  value: any             // Current value
  onChange: Function     // Change handler
  onBlur: Function       // Blur handler
}

form: FormikProps        // Full formik instance

meta: {
  value: any             // Current value (duplicate of field.value)
  error: string          // Validation error
  touched: boolean       // Has been blurred
  initialValue: any      // Initial value
  initialTouched: boolean
  initialError: string
}
```

### FieldArray Component

For dynamic lists:

```tsx
import { FieldArray } from 'formik'

<FieldArray name="friends">
  {(arrayHelpers) => (
    <div>
      {formik.values.friends.map((friend, index) => (
        <div key={index}>
          <Field name={`friends.${index}.name`} />
          <button onClick={() => arrayHelpers.remove(index)}>Remove</button>
        </div>
      ))}
      <button onClick={() => arrayHelpers.push({ name: '' })}>Add</button>
    </div>
  )}
</FieldArray>

// arrayHelpers provides:
arrayHelpers.push(value)
arrayHelpers.pop()
arrayHelpers.swap(indexA, indexB)
arrayHelpers.move(from, to)
arrayHelpers.insert(index, value)
arrayHelpers.unshift(value)
arrayHelpers.remove(index)
arrayHelpers.replace(index, value)
```

**Performance issue**: Every array operation re-renders entire list (no optimization).

### ErrorMessage Component

```tsx
import { ErrorMessage } from 'formik'

<ErrorMessage name="email" />
// Renders error text if field has error + is touched

// Custom render:
<ErrorMessage name="email">
  {(msg) => <div className="error">{msg}</div>}
</ErrorMessage>

// Component prop:
<ErrorMessage name="email" component="div" className="error" />
```

## Validation Integration

### Yup Integration

Formik was **designed for Yup** (same original author):

```tsx
import * as yup from 'yup'

const schema = yup.object({
  email: yup.string().email().required(),
  age: yup.number().positive().integer(),
})

<Formik validationSchema={schema} {...} />
// Automatic validation on change/blur/submit
```

**How it works**:
1. Formik calls `schema.validate(values, { abortEarly: false })`
2. Converts Yup errors to `{ [field]: error }` format
3. Updates `formik.errors` state
4. Triggers re-render

### Custom Validation

**Function-based validation**:

```tsx
<Formik
  validate={(values) => {
    const errors = {}

    if (!values.email) {
      errors.email = 'Required'
    } else if (!/^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i.test(values.email)) {
      errors.email = 'Invalid email'
    }

    return errors
  }}
/>
```

**Async validation**:

```tsx
<Formik
  validate={async (values) => {
    const errors = {}

    if (values.username) {
      const exists = await checkUsername(values.username)
      if (exists) errors.username = 'Username taken'
    }

    return errors
  }}
/>
```

**Field-level validation**:

```tsx
function validateEmail(value) {
  if (!value) return 'Required'
  if (!/^[A-Z0-9._%+-]+@/.test(value)) return 'Invalid email'
}

<Field name="email" validate={validateEmail} />
```

## Advanced Features

### Nested Objects

```tsx
const formik = useFormik({
  initialValues: {
    user: {
      name: '',
      address: {
        street: '',
        city: '',
      },
    },
  },
})

// Dot notation for fields:
<Field name="user.name" />
<Field name="user.address.street" />

// Access values:
formik.values.user.address.street

// Set values:
formik.setFieldValue('user.address.street', '123 Main St')
```

### Touched State Management

```tsx
// Track which fields user interacted with
formik.touched.email  // true after blur

// Only show errors for touched fields:
{formik.touched.email && formik.errors.email && (
  <div>{formik.errors.email}</div>
)}

// Set touched programmatically:
formik.setFieldTouched('email', true)
formik.setTouched({ email: true, password: true })
```

### Submit Handling

```tsx
<Formik
  onSubmit={async (values, actions) => {
    // values: form data
    // actions: formik helpers

    try {
      await submitToAPI(values)
      actions.setStatus('success')
      actions.resetForm()
    } catch (error) {
      actions.setErrors({ server: error.message })
      actions.setStatus('error')
    } finally {
      actions.setSubmitting(false)
    }
  }}
/>
```

**Submit helpers**:
```tsx
actions.setSubmitting(false)      // Stop loading state
actions.setStatus(status)          // Set custom status
actions.setErrors({ field: 'error' })  // Set errors
actions.setFieldError('field', 'error')
actions.resetForm()                // Reset to initial
actions.validateForm()             // Trigger validation
```

### Conditional Fields

**Show/hide fields based on values**:

```tsx
<Formik initialValues={{ role: 'user', permissions: [] }}>
  {(formik) => (
    <Form>
      <Field name="role" as="select">
        <option value="user">User</option>
        <option value="admin">Admin</option>
      </Field>

      {formik.values.role === 'admin' && (
        <Field name="permissions" as="select" multiple>
          <option value="read">Read</option>
          <option value="write">Write</option>
        </Field>
      )}
    </Form>
  )}
</Formik>
```

**Validation for conditional fields**:

```tsx
const schema = yup.object({
  role: yup.string().required(),
  permissions: yup.array().when('role', {
    is: 'admin',
    then: (schema) => schema.min(1).required(),
    otherwise: (schema) => schema.notRequired(),
  }),
})
```

### Context API

Share Formik state across components:

```tsx
import { useFormikContext } from 'formik'

function NestedComponent() {
  const formik = useFormikContext()
  // Access formik.values, formik.errors, etc.
  return <div>{formik.values.email}</div>
}

<Formik {...}>
  {() => (
    <Form>
      <NestedComponent />
    </Form>
  )}
</Formik>
```

### Reset Form

```tsx
// Reset to initial values:
formik.resetForm()

// Reset to new values:
formik.resetForm({
  values: { email: 'new@example.com' },
  errors: {},
  touched: {},
})

// Reset button:
<button type="button" onClick={formik.handleReset}>
  Reset
</button>
```

## TypeScript Integration

### Generic Type Support

```tsx
import { useFormik } from 'formik'

interface FormValues {
  email: string
  age: number
}

const formik = useFormik<FormValues>({
  initialValues: {
    email: '',
    age: 0,
  },
  onSubmit: (values) => {
    // values is typed as FormValues
  },
})

// Type-safe access:
formik.values.email   // string
formik.values.age     // number
formik.values.other   // ✗ Type error
```

### Type Inference with Yup

```tsx
import * as yup from 'yup'

const schema = yup.object({
  email: yup.string().required(),
  age: yup.number().required(),
})

type FormValues = yup.InferType<typeof schema>

const formik = useFormik<FormValues>({
  initialValues: {
    email: '',
    age: 0,
  },
  validationSchema: schema,
})
```

**Limitation**: Yup inference less accurate than Zod (optional fields, transforms).

### Field Component Types

```tsx
import { Field, FieldProps } from 'formik'

<Field name="email">
  {({ field, form, meta }: FieldProps<string, FormValues>) => (
    <input {...field} />
  )}
</Field>
```

## Testing Strategies

### Unit Testing

```tsx
import { renderHook, act } from '@testing-library/react'
import { useFormik } from 'formik'

test('handles form submission', async () => {
  const onSubmit = jest.fn()

  const { result } = renderHook(() =>
    useFormik({
      initialValues: { email: '' },
      onSubmit,
    })
  )

  act(() => {
    result.current.setFieldValue('email', 'test@example.com')
  })

  await act(async () => {
    await result.current.submitForm()
  })

  expect(onSubmit).toHaveBeenCalledWith(
    { email: 'test@example.com' },
    expect.anything()
  )
})
```

### Integration Testing

```tsx
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'

test('validates and submits form', async () => {
  const onSubmit = jest.fn()

  render(<MyFormikForm onSubmit={onSubmit} />)

  const emailInput = screen.getByLabelText('Email')
  await userEvent.type(emailInput, 'test@example.com')

  const submitButton = screen.getByRole('button', { name: /submit/i })
  await userEvent.click(submitButton)

  await waitFor(() => {
    expect(onSubmit).toHaveBeenCalledWith(
      { email: 'test@example.com' },
      expect.anything()
    )
  })
})
```

### Testing Validation

```tsx
test('shows validation errors', async () => {
  render(<MyFormikForm />)

  const submitButton = screen.getByRole('button')
  await userEvent.click(submitButton)

  await waitFor(() => {
    expect(screen.getByText('Email is required')).toBeInTheDocument()
  })
})
```

## Architectural Trade-offs

### Advantages

1. **Simple mental model**: Controlled components, familiar React patterns
2. **Easy debugging**: All state in React DevTools
3. **Yup integration**: Seamless validation with Yup
4. **Rich API**: Comprehensive helper functions
5. **Context support**: Easy to share state across components
6. **Mature ecosystem**: Many examples, tutorials, patterns

### Disadvantages

1. **Performance**: Slow for large forms (many re-renders)
2. **Bundle size**: 44KB (4x larger than RHF)
3. **Maintenance**: Abandoned since 2021 (last commit: Dec 2021)
4. **Re-render overhead**: No built-in optimization
5. **Memory usage**: Higher than uncontrolled alternatives
6. **Security**: Dependencies may have vulnerabilities
7. **TypeScript**: Weaker inference than modern libraries

## Migration Status

**Formik is effectively abandoned**:
- Last commit: December 2021 (1+ year)
- No response to issues/PRs
- Dependencies outdated
- Security vulnerabilities unfixed

**Migration paths**:

**To React Hook Form** (most common):
```tsx
// Formik
const formik = useFormik({ initialValues, onSubmit })
<input {...formik.getFieldProps('email')} />

// React Hook Form
const { register, handleSubmit } = useForm({ defaultValues })
<input {...register('email')} />
```

**To TanStack Form** (modern alternative):
```tsx
// Formik
const formik = useFormik({ initialValues, onSubmit })

// TanStack Form
const form = useForm({ defaultValues, onSubmit })
```

## When to Use

**DO NOT use Formik for new projects** (abandoned).

**If maintaining existing Formik code**:
- Keep using it if it works (stable, no breaking changes)
- Watch for security issues in dependencies
- Plan migration to React Hook Form or TanStack Form

**Historical reasons to have chosen Formik**:
- Wanted controlled components
- Preferred render props pattern
- Using Yup for validation
- Needed simple, familiar API

**Why NOT to use today**:
- Abandoned (no maintenance)
- Performance issues (re-render overhead)
- Better alternatives exist (RHF, TanStack Form)
- Security concerns (outdated dependencies)

## Performance Optimization (Legacy)

If stuck with Formik, optimize with:

### FastField

```tsx
import { FastField } from 'formik'

// Only re-renders when this field changes
<FastField name="email" />
```

### React.memo

```tsx
const MemoField = React.memo(({ name }) => (
  <Field name={name} />
))
```

### Debounce Validation

```tsx
import { debounce } from 'lodash'

const debouncedValidate = debounce((values) => {
  // validation logic
}, 300)

<Formik validate={debouncedValidate} />
```

### Disable Validation on Change

```tsx
<Formik
  validateOnChange={false}  // Only validate on blur/submit
  validateOnBlur={true}
/>
```

## Resources

- [GitHub Repository](https://github.com/jaredpalmer/formik) (⚠️ unmaintained)
- [Documentation](https://formik.org/docs/overview) (archived)
- [Tutorial](https://formik.org/docs/tutorial)
- [Yup Integration](https://formik.org/docs/guides/validation#validationschema)
- [Migration Guide to RHF](https://react-hook-form.com/migrate-v6-to-v7) (community)

**Note**: Since Formik is abandoned, rely on community resources and plan migration to actively maintained alternatives.
