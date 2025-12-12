# Zod

> "TypeScript-first schema validation with static type inference."

## Quick Facts

| Metric | Value |
|--------|-------|
| GitHub Stars | ~35,000 |
| npm Weekly Downloads | ~12M |
| Bundle Size | ~45KB |
| Dependencies | Zero |
| License | MIT |
| Creator | Colin McDonnell (2020) |

## Why Zod Dominates

Zod is the **default validation library** for TypeScript projects:

1. **TypeScript-first**: Built for TS from the ground up
2. **Type inference**: `z.infer<typeof schema>` derives types from schema
3. **Single source of truth**: Schema = validation + types
4. **Zero dependencies**: No extra baggage
5. **Ecosystem**: Works with everything (RHF, tRPC, etc.)

## Core Concept: Schema as Types

Traditional approach - duplicate definitions:
```tsx
// Define types
type User = { email: string; age: number }

// Define validation separately (can drift!)
function validate(data: unknown) {
  if (!data.email || !data.age) throw new Error()
}
```

Zod approach - single source of truth:
```tsx
import { z } from 'zod'

// Schema IS the type definition
const UserSchema = z.object({
  email: z.string().email(),
  age: z.number().min(0),
})

// Derive TypeScript type from schema
type User = z.infer<typeof UserSchema>
// { email: string; age: number }

// Validation uses the same schema
const result = UserSchema.safeParse(unknownData)
```

## Basic Usage

```tsx
import { z } from 'zod'

// Primitives
const str = z.string()
const num = z.number()
const bool = z.boolean()
const date = z.date()

// With validations
const email = z.string().email()
const age = z.number().min(0).max(120)
const url = z.string().url()

// Objects
const UserSchema = z.object({
  name: z.string().min(1),
  email: z.string().email(),
  age: z.number().optional(),
})

// Arrays
const TagsSchema = z.array(z.string())

// Enums
const RoleSchema = z.enum(['admin', 'user', 'guest'])

// Union
const IdSchema = z.union([z.string(), z.number()])
// or: z.string().or(z.number())
```

## Validation

```tsx
// Parse (throws on error)
try {
  const user = UserSchema.parse(data)
} catch (error) {
  // ZodError with details
}

// SafeParse (never throws)
const result = UserSchema.safeParse(data)
if (result.success) {
  console.log(result.data) // typed correctly
} else {
  console.log(result.error.issues) // validation errors
}
```

## Key Features

### Custom Error Messages
```tsx
const schema = z.object({
  email: z.string().email({ message: 'Invalid email address' }),
  password: z.string().min(8, { message: 'Password must be at least 8 characters' }),
})
```

### Transformations
```tsx
const schema = z.string().transform((val) => val.toUpperCase())
schema.parse('hello') // 'HELLO'
```

### Refinements
```tsx
const schema = z.string().refine(
  (val) => val.includes('@'),
  { message: 'Must contain @' }
)
```

### Object Manipulation
```tsx
const UserSchema = z.object({
  id: z.string(),
  email: z.string(),
  password: z.string(),
})

// Pick specific fields
const PublicUser = UserSchema.pick({ id: true, email: true })

// Omit fields
const CreateUser = UserSchema.omit({ id: true })

// Make all optional
const PartialUser = UserSchema.partial()

// Extend
const AdminSchema = UserSchema.extend({
  role: z.literal('admin'),
})
```

## Integration with React Hook Form

```tsx
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'

const schema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
})

type FormData = z.infer<typeof schema>

function Form() {
  const { register, handleSubmit, formState: { errors } } = useForm<FormData>({
    resolver: zodResolver(schema),
  })
  // ...
}
```

## When to Choose Zod

**Choose Zod when:**
- Using TypeScript (always)
- Want schema as single source of truth
- Need excellent DX and type inference
- Using React Hook Form, tRPC, etc.

**Consider alternatives when:**
- Bundle size is critical → Valibot (1KB vs 45KB)
- Legacy JavaScript project → Yup (more familiar syntax)

## Resources

- [Official Docs](https://zod.dev/)
- [GitHub](https://github.com/colinhacks/zod)
- [Error Handling](https://zod.dev/ERROR_HANDLING)
