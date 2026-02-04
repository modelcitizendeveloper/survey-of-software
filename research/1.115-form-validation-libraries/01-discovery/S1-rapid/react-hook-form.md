# React Hook Form

> "Performant, flexible and extensible forms with easy-to-use validation."

## Quick Facts

| Metric | Value |
|--------|-------|
| GitHub Stars | 38,700 |
| npm Weekly Downloads | ~5M |
| Bundle Size | 12KB (gzipped) |
| Dependencies | Zero |
| License | MIT |

## Why React Hook Form Dominates

React Hook Form is the **clear winner** for React forms in 2025:

1. **Performance**: Uncontrolled components = minimal re-renders
2. **Bundle size**: 12KB vs 44KB (Formik)
3. **Zero dependencies**: No extra baggage
4. **Active maintenance**: Regular updates
5. **TypeScript first**: Excellent type inference

## Core Concept: Uncontrolled Components

Traditional controlled forms re-render on every keystroke:
```tsx
// Controlled (Formik style) - re-renders on every change
const [value, setValue] = useState('')
<input value={value} onChange={e => setValue(e.target.value)} />
```

React Hook Form uses refs (uncontrolled):
```tsx
// Uncontrolled (RHF style) - no re-renders
const { register } = useForm()
<input {...register('email')} />
```

## Basic Usage

```tsx
import { useForm } from 'react-hook-form'

function LoginForm() {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting }
  } = useForm()

  const onSubmit = (data) => console.log(data)

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register('email', { required: 'Email required' })} />
      {errors.email && <span>{errors.email.message}</span>}

      <input
        type="password"
        {...register('password', { minLength: { value: 8, message: 'Min 8 chars' } })}
      />
      {errors.password && <span>{errors.password.message}</span>}

      <button disabled={isSubmitting}>Submit</button>
    </form>
  )
}
```

## Schema Validation (Zod)

```tsx
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'

const schema = z.object({
  email: z.string().email('Invalid email'),
  password: z.string().min(8, 'Min 8 characters'),
})

type FormData = z.infer<typeof schema>

function LoginForm() {
  const { register, handleSubmit, formState: { errors } } = useForm<FormData>({
    resolver: zodResolver(schema),
  })
  // ...
}
```

## Key Features

### Form State
```tsx
const { formState } = useForm()
// formState.errors - validation errors
// formState.isDirty - form has been modified
// formState.isValid - all validations pass
// formState.isSubmitting - form is submitting
// formState.isSubmitSuccessful - submission succeeded
```

### Watch Values
```tsx
const { watch } = useForm()
const email = watch('email') // Subscribe to single field
const allValues = watch() // Subscribe to all fields
```

### Reset Form
```tsx
const { reset } = useForm()
reset() // Reset to default values
reset({ email: 'new@email.com' }) // Reset with new values
```

### Field Arrays
```tsx
import { useFieldArray } from 'react-hook-form'

const { fields, append, remove } = useFieldArray({
  control,
  name: 'items',
})
```

## Validation Resolvers

React Hook Form supports multiple validation libraries:

```bash
npm install @hookform/resolvers
```

| Library | Resolver |
|---------|----------|
| Zod | `zodResolver` |
| Yup | `yupResolver` |
| Valibot | `valibotResolver` |
| Joi | `joiResolver` |
| Vest | `vestResolver` |

## When to Choose React Hook Form

**Choose RHF when:**
- Building any React form (it's the default)
- Performance matters
- Want smallest bundle
- Using TypeScript
- Need schema validation

**Consider alternatives when:**
- Using TanStack ecosystem → TanStack Form
- Already have large Formik codebase (migrate gradually)

## Resources

- [Official Docs](https://react-hook-form.com/)
- [GitHub](https://github.com/react-hook-form/react-hook-form)
- [Resolvers](https://github.com/react-hook-form/resolvers)
- [DevTools](https://react-hook-form.com/dev-tools)
