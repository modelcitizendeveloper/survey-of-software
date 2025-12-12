# Valibot

> "The modular and type safe schema library for validating structural data."

## Quick Facts

| Metric | Value |
|--------|-------|
| GitHub Stars | ~6,000 |
| npm Weekly Downloads | ~500K |
| Bundle Size | **1-2KB** (vs 45KB Zod) |
| Dependencies | Zero |
| License | MIT |
| Version | v1.0 (stable) |

## Why Valibot Matters

Valibot is the **bundle-size champion**:
- **90%+ smaller** than Zod for equivalent schemas
- Login form: Zod 13.5KB → Valibot 1.37KB
- Same TypeScript-first approach as Zod

## How It Achieves Small Size

Valibot uses **modular, tree-shakeable architecture**:

```tsx
// Zod - methods chained on objects
import { z } from 'zod'
const schema = z.string().email().min(5)

// Valibot - functions composed in pipelines
import * as v from 'valibot'
const schema = v.pipe(v.string(), v.email(), v.minLength(5))
```

Only imported functions are bundled. Unused validators are tree-shaken away.

## Basic Usage

```tsx
import * as v from 'valibot'

// Primitives
const str = v.string()
const num = v.number()
const bool = v.boolean()

// With validations (using pipe)
const email = v.pipe(v.string(), v.email())
const age = v.pipe(v.number(), v.minValue(0), v.maxValue(120))

// Objects
const UserSchema = v.object({
  name: v.pipe(v.string(), v.minLength(1)),
  email: v.pipe(v.string(), v.email()),
  age: v.optional(v.number()),
})

// Type inference (same as Zod)
type User = v.InferOutput<typeof UserSchema>
```

## Validation

```tsx
// Parse (throws on error)
const user = v.parse(UserSchema, data)

// SafeParse (never throws)
const result = v.safeParse(UserSchema, data)
if (result.success) {
  console.log(result.output)
} else {
  console.log(result.issues)
}
```

## Key Differences from Zod

| Aspect | Zod | Valibot |
|--------|-----|---------|
| API style | Method chaining | Function pipelines |
| Bundle | ~45KB | 1-2KB |
| Tree-shaking | Partial | Full |
| Performance | Good | 2x faster |
| Ecosystem | Larger | Growing |

### Syntax Comparison

```tsx
// Zod
const schema = z.object({
  email: z.string().email().min(5),
  age: z.number().min(0).optional(),
})

// Valibot
const schema = v.object({
  email: v.pipe(v.string(), v.email(), v.minLength(5)),
  age: v.optional(v.pipe(v.number(), v.minValue(0))),
})
```

## Integration with React Hook Form

```tsx
import { useForm } from 'react-hook-form'
import { valibotResolver } from '@hookform/resolvers/valibot'
import * as v from 'valibot'

const schema = v.object({
  email: v.pipe(v.string(), v.email()),
  password: v.pipe(v.string(), v.minLength(8)),
})

type FormData = v.InferOutput<typeof schema>

function Form() {
  const { register, handleSubmit } = useForm<FormData>({
    resolver: valibotResolver(schema),
  })
  // ...
}
```

## When to Choose Valibot

**Choose Valibot when:**
- Bundle size is critical
- Building for mobile/slow networks
- Simple to medium complexity schemas
- Willing to learn slightly different API

**Choose Zod instead when:**
- Bundle size isn't critical
- Want larger ecosystem
- Team already knows Zod
- Need more complex transformations

## Migration from Zod

Valibot provides a [migration guide](https://valibot.dev/guides/migrate-from-zod/) and codemod.

Key changes:
- `z.string().email()` → `v.pipe(v.string(), v.email())`
- `z.infer<>` → `v.InferOutput<>`
- `z.optional()` → `v.optional()`

## Who Uses Valibot

- The Guardian
- React Router
- Rolldown
- 50,000+ dependent GitHub repos

## Resources

- [Official Docs](https://valibot.dev/)
- [GitHub](https://github.com/fabian-hiller/valibot)
- [Comparison with Zod](https://valibot.dev/guides/comparison/)
- [Migration from Zod](https://valibot.dev/guides/migrate-from-zod/)
