# Formik

> "Build forms in React, without the tears."

## Quick Facts

| Metric | Value |
|--------|-------|
| GitHub Stars | 33,300 |
| npm Weekly Downloads | ~1.9M |
| Bundle Size | 44KB (gzipped) |
| Dependencies | 9 |
| Status | **Maintenance mode** |

## Current Status: Avoid for New Projects

**Important**: Formik is effectively abandoned:
- Last commit: over 1 year ago
- GitHub issues: largely ignored
- No new features or bug fixes
- Creator (Jared Palmer) moved on to other projects

**Recommendation**: Use React Hook Form for new projects. Migrate existing Formik projects when practical.

## Why Formik Was Popular

Formik dominated 2018-2021 because it:
- Simplified form state management
- Integrated well with Yup validation
- Had good documentation
- Was the first major React form library

## How Formik Works

Formik uses **controlled components**:

```tsx
import { Formik, Form, Field, ErrorMessage } from 'formik'
import * as Yup from 'yup'

const schema = Yup.object({
  email: Yup.string().email('Invalid email').required('Required'),
  password: Yup.string().min(8, 'Min 8 chars').required('Required'),
})

function LoginForm() {
  return (
    <Formik
      initialValues={{ email: '', password: '' }}
      validationSchema={schema}
      onSubmit={(values) => console.log(values)}
    >
      <Form>
        <Field name="email" type="email" />
        <ErrorMessage name="email" />

        <Field name="password" type="password" />
        <ErrorMessage name="password" />

        <button type="submit">Submit</button>
      </Form>
    </Formik>
  )
}
```

## Why React Hook Form Is Better

| Aspect | Formik | React Hook Form |
|--------|--------|-----------------|
| Bundle | 44KB | 12KB |
| Dependencies | 9 | 0 |
| Re-renders | Every keystroke | Minimal |
| Maintenance | Abandoned | Active |
| TypeScript | Added later | First-class |
| Performance | Slower | Faster |

### Performance Difference

Formik (controlled):
```
Keystroke → setState → re-render entire form → DOM update
```

React Hook Form (uncontrolled):
```
Keystroke → DOM update only (no React re-render)
```

## Migration Guide

### Basic Form

**Formik:**
```tsx
<Formik initialValues={{ email: '' }} onSubmit={handleSubmit}>
  <Form>
    <Field name="email" />
  </Form>
</Formik>
```

**React Hook Form:**
```tsx
const { register, handleSubmit } = useForm({ defaultValues: { email: '' } })
<form onSubmit={handleSubmit(onSubmit)}>
  <input {...register('email')} />
</form>
```

### With Validation

**Formik + Yup:**
```tsx
<Formik validationSchema={yupSchema}>
```

**React Hook Form + Zod:**
```tsx
useForm({ resolver: zodResolver(zodSchema) })
```

### Accessing Values

**Formik:**
```tsx
<Formik>
  {({ values }) => <span>{values.email}</span>}
</Formik>
```

**React Hook Form:**
```tsx
const { watch } = useForm()
const email = watch('email')
```

## When Formik Might Still Be Used

- Large existing codebase (migration cost too high)
- Team very familiar with Formik
- No performance concerns
- Not actively developing new features

## Resources

- [Official Docs](https://formik.org/)
- [GitHub](https://github.com/jaredpalmer/formik)
- [Migration to RHF](https://react-hook-form.com/get-started#SchemaValidation)
