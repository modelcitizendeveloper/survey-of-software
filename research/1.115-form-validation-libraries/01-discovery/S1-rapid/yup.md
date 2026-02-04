# Yup

> "Schema validation for JavaScript and TypeScript."

## Quick Facts

| Metric | Value |
|--------|-------|
| GitHub Stars | ~22,000 |
| npm Weekly Downloads | ~8M |
| Bundle Size | ~60KB |
| License | MIT |
| Creator | Jason Quense |

## Current Status

Yup remains widely used but **Zod has overtaken it** for TypeScript projects:
- Yup: 8M downloads/week
- Zod: 12M downloads/week

## Why Yup Was Popular

Yup dominated 2018-2022 because:
- First major schema validation for JS
- Excellent Formik integration
- Chainable API (familiar to JS developers)
- Good documentation

## How Yup Works

```tsx
import * as yup from 'yup'

const schema = yup.object({
  email: yup.string().email('Invalid email').required('Required'),
  age: yup.number().min(0).max(120).required(),
  website: yup.string().url().nullable(),
})

// Validate
try {
  const result = await schema.validate(data)
} catch (error) {
  console.log(error.errors) // Array of error messages
}

// Validate sync
const isValid = schema.isValidSync(data)
```

## Yup vs Zod

| Aspect | Yup | Zod |
|--------|-----|-----|
| Bundle | 60KB | 45KB |
| TypeScript | Added later | First-class |
| Type inference | Limited | Excellent |
| API | Chainable | Chainable + functional |
| Async | Built-in | Built-in |
| Popularity | Declining | Rising |

### TypeScript Difference

**Yup** - Types can drift from schema:
```tsx
// Schema
const schema = yup.object({ name: yup.string() })

// Type might not match exactly
type User = yup.InferType<typeof schema>
// Sometimes has issues with optional/nullable
```

**Zod** - Types always match:
```tsx
const schema = z.object({ name: z.string() })
type User = z.infer<typeof schema>
// Always accurate
```

## When to Choose Yup

**Choose Yup when:**
- Legacy JavaScript project (no TypeScript)
- Team already knows Yup
- Using Formik (historical pairing)
- Don't need strict type inference

**Choose Zod instead when:**
- Using TypeScript (always)
- Starting new project
- Want smaller bundle
- Using React Hook Form

## Migration to Zod

Most Yup patterns have direct Zod equivalents:

```tsx
// Yup
yup.string().required()
yup.number().min(0)
yup.object({ name: yup.string() })
yup.array().of(yup.string())

// Zod
z.string().min(1)  // Note: Zod has no required(), use min(1)
z.number().min(0)
z.object({ name: z.string() })
z.array(z.string())
```

## Resources

- [Official Docs](https://github.com/jquense/yup)
- [GitHub](https://github.com/jquense/yup)
- [API Reference](https://github.com/jquense/yup#api)
