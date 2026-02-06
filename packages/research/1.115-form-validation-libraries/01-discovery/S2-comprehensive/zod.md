# Zod - Technical Deep-Dive

## Architecture

### Schema-First Design

Zod's core innovation is treating **schemas as the single source of truth** for both validation and TypeScript types.

**Traditional approach** (types and validation separate):
```tsx
// 1. Define types
type User = { email: string; age: number }

// 2. Define validation (can drift!)
const validate = (data: unknown): User => {
  if (typeof data.email !== 'string') throw new Error()
  if (typeof data.age !== 'number') throw new Error()
  return data as User
}
```

**Zod approach** (single schema = types + validation):
```tsx
const UserSchema = z.object({
  email: z.string(),
  age: z.number(),
})

type User = z.infer<typeof UserSchema>
// Types automatically derived from schema - no drift possible
```

### Parser Architecture

Zod uses a **parser pattern** with composable validators:

```tsx
abstract class ZodType<Output, Input = Output> {
  parse(data: unknown): Output
  safeParse(data: unknown): SafeParseReturnType<Input, Output>
  _parse(ctx: ParseContext): ParseResult<Output>
}
```

Each schema type (`string()`, `number()`, `object()`) extends this base class with specific parsing logic.

### Type Inference Engine

Zod's type inference is built on TypeScript's **conditional types** and **mapped types**:

```tsx
type infer<T extends ZodType<any, any>> = T extends ZodType<infer Output, any>
  ? Output
  : never

// Example:
const schema = z.object({ name: z.string() })
type Inferred = z.infer<typeof schema>
// TypeScript infers: { name: string }
```

This enables **bidirectional type flow**: schema → types AND types → runtime validation.

## Performance Characteristics

### Bundle Size Breakdown

**~45KB gzipped (core):**
- Type classes: 15KB
- Parsing engine: 10KB
- Error handling: 8KB
- Type inference utilities: 7KB
- Object/array utilities: 5KB

**No dependencies** - fully self-contained.

**Tree-shaking**: Unused validators are eliminated in production builds.

### Runtime Performance

**Validation speed** (1000 iterations):

| Schema Complexity | Zod Time | Yup Time |
|------------------|----------|----------|
| Simple (3 fields) | 2ms | 3ms |
| Medium (10 fields) | 8ms | 15ms |
| Complex (nested + arrays) | 25ms | 50ms |

**Key insight**: Zod is faster because it's **synchronous by default** and has fewer abstraction layers.

### Memory Footprint

- Schema definition: ~100 bytes per field
- Validation context: ~500 bytes per parse call
- Error object: ~1KB per validation failure

**Best practice**: Reuse schemas across validations (don't recreate schemas in loops).

## API Design Patterns

### Primitive Types

```tsx
z.string()    // string
z.number()    // number
z.boolean()   // boolean
z.date()      // Date instance
z.bigint()    // bigint
z.undefined() // undefined
z.null()      // null
z.void()      // void (for functions)
z.any()       // any (escape hatch)
z.unknown()   // unknown (type-safe any)
z.never()     // never
```

### Refinements (Custom Validation)

```tsx
const schema = z.string().refine(
  (val) => val.length % 2 === 0,
  { message: 'Must have even length' }
)

// Async refinement:
const schema = z.string().refine(
  async (val) => {
    const exists = await checkDB(val)
    return !exists
  },
  { message: 'Already exists' }
)
```

### Transformations

```tsx
// Parse then transform
const schema = z.string().transform((val) => val.toUpperCase())
schema.parse('hello') // 'HELLO'

// Chaining transformations
const schema = z.string()
  .transform((s) => s.trim())
  .transform((s) => parseInt(s, 10))
  .refine((n) => n > 0, 'Must be positive')

schema.parse('  42  ') // 42
```

**Key insight**: Transformations run **after** validation, so you can safely assume valid input.

### Union Types

```tsx
// Union: string OR number
const IdSchema = z.union([z.string(), z.number()])
// or shorthand:
const IdSchema = z.string().or(z.number())

// Discriminated union (tagged union):
const EventSchema = z.discriminatedUnion('type', [
  z.object({ type: z.literal('click'), x: z.number(), y: z.number() }),
  z.object({ type: z.literal('keypress'), key: z.string() }),
])
```

Discriminated unions enable **efficient parsing** (checks discriminator first).

## Advanced Features

### Object Manipulation

```tsx
const UserSchema = z.object({
  id: z.string(),
  email: z.string(),
  password: z.string(),
  role: z.enum(['admin', 'user']),
})

// Pick subset
const PublicUser = UserSchema.pick({ id: true, email: true })

// Omit fields
const CreateUser = UserSchema.omit({ id: true })

// Make all optional
const PartialUser = UserSchema.partial()

// Make all required
const RequiredUser = PartialUser.required()

// Extend with new fields
const AdminUser = UserSchema.extend({
  permissions: z.array(z.string()),
})

// Merge schemas
const MergedSchema = UserSchema.merge(AdminUser)

// Deep partial (nested optionals)
const DeepPartialUser = UserSchema.deepPartial()
```

### Array Schemas

```tsx
// Basic array
const TagsSchema = z.array(z.string())

// Constrained array
const TagsSchema = z.array(z.string())
  .min(1, 'At least one tag')
  .max(10, 'Max 10 tags')

// Non-empty array
const TagsSchema = z.string().array().nonempty()

// Tuple (fixed length + types)
const CoordinateSchema = z.tuple([z.number(), z.number()])
schema.parse([10, 20]) // ✓
schema.parse([10])     // ✗ Too few elements
```

### Record and Map Types

```tsx
// Record: object with dynamic keys
const ConfigSchema = z.record(z.string()) // { [key: string]: string }
const ConfigSchema = z.record(z.string(), z.number()) // { [key: string]: number }

// Map
const MapSchema = z.map(z.string(), z.number())
```

### Lazy and Recursive Schemas

For self-referential data structures:

```tsx
type Category = {
  name: string
  subcategories: Category[]
}

const CategorySchema: z.ZodType<Category> = z.lazy(() =>
  z.object({
    name: z.string(),
    subcategories: z.array(CategorySchema),
  })
)
```

### Error Handling

```tsx
// parse() throws ZodError
try {
  schema.parse(data)
} catch (error) {
  if (error instanceof ZodError) {
    error.issues.forEach((issue) => {
      console.log(issue.path)    // ['email']
      console.log(issue.message)  // 'Invalid email'
      console.log(issue.code)     // 'invalid_string'
    })
  }
}

// safeParse() never throws
const result = schema.safeParse(data)
if (!result.success) {
  result.error.issues // Same as above
} else {
  result.data // Typed correctly
}
```

### Custom Error Messages

```tsx
// Per-field messages
const schema = z.object({
  email: z.string().email({ message: 'Invalid email address' }),
  age: z.number().min(18, { message: 'Must be 18+' }),
})

// Error map (global customization)
z.setErrorMap((issue, ctx) => {
  if (issue.code === 'invalid_type') {
    return { message: `Expected ${issue.expected}, got ${issue.received}` }
  }
  return { message: ctx.defaultError }
})
```

## TypeScript Integration

### Type Inference

```tsx
const schema = z.object({
  name: z.string(),
  age: z.number().optional(),
  tags: z.array(z.string()),
})

// Infer output type (after parsing)
type Output = z.infer<typeof schema>
// { name: string; age?: number; tags: string[] }

// Infer input type (before parsing, with transforms)
const schema2 = z.string().transform((s) => parseInt(s, 10))
type Input = z.input<typeof schema2>   // string
type Output = z.output<typeof schema2> // number
```

### Brand Types

Create nominal types (distinct at type level, same at runtime):

```tsx
const UserId = z.string().brand<'UserId'>()
type UserId = z.infer<typeof UserId> // string & Brand<'UserId'>

const PostId = z.string().brand<'PostId'>()
type PostId = z.infer<typeof PostId>

// Prevents accidental mixing:
function getUser(id: UserId) { }
const postId: PostId = '123' as PostId
getUser(postId) // ✗ Type error: PostId ≠ UserId
```

### Generic Schemas

```tsx
function createSchema<T extends z.ZodTypeAny>(itemSchema: T) {
  return z.object({
    items: z.array(itemSchema),
    count: z.number(),
  })
}

const UserListSchema = createSchema(z.object({ name: z.string() }))
```

## Integration Patterns

### React Hook Form

```tsx
import { zodResolver } from '@hookform/resolvers/zod'

const { register, handleSubmit } = useForm({
  resolver: zodResolver(schema),
})
```

### tRPC

```tsx
import { z } from 'zod'
import { router } from './trpc'

export const appRouter = router({
  createUser: procedure
    .input(z.object({ email: z.string().email() }))
    .mutation(async ({ input }) => {
      // input is typed from schema
    }),
})
```

### Server-Side Validation

```tsx
// Express middleware
app.post('/api/user', (req, res) => {
  const result = UserSchema.safeParse(req.body)
  if (!result.success) {
    return res.status(400).json({ errors: result.error.issues })
  }
  // result.data is validated and typed
})
```

## Architectural Trade-offs

### Advantages

1. **Single source of truth**: Schema = types + validation
2. **Type safety**: TypeScript integration is best-in-class
3. **Composability**: Rich schema manipulation (pick, omit, extend)
4. **Performance**: Faster than Yup, synchronous by default
5. **Ecosystem**: Works with RHF, tRPC, Next.js, etc.

### Disadvantages

1. **Bundle size**: 45KB (vs 1-2KB for Valibot)
2. **Learning curve**: More complex API than Yup
3. **Error messages**: Default messages less friendly than Yup
4. **Tree-shaking**: Not as granular as Valibot
5. **Async validation**: Less intuitive than Yup (uses refine)

## When to Use

**Choose Zod when**:
- Using TypeScript (always)
- Want schema as single source of truth
- Need excellent type inference
- Using React Hook Form, tRPC, or modern TS stack
- Value DX and type safety over bundle size

**Consider alternatives when**:
- Bundle size is critical → Valibot (98% smaller)
- Legacy JavaScript project → Yup (simpler syntax)
- Need friendlier error messages → Yup (better defaults)

## Performance Optimization

### Reuse Schemas

```tsx
// ✗ Bad: creates new schema on every render
function Component() {
  const schema = z.object({ email: z.string() })
  // ...
}

// ✓ Good: schema created once
const schema = z.object({ email: z.string() })
function Component() {
  // use schema
}
```

### Lazy Parsing

Only validate when needed:

```tsx
// Don't validate on every keystroke
// Use safeParse only on submit or blur
```

### Coercion for Performance

```tsx
// Convert types during parsing (faster than separate transform)
const schema = z.object({
  age: z.coerce.number(), // Parses '42' → 42
  active: z.coerce.boolean(), // Parses 'true' → true
})
```

## Resources

- [Official Docs](https://zod.dev/)
- [GitHub](https://github.com/colinhacks/zod)
- [Error Handling Guide](https://zod.dev/ERROR_HANDLING)
- [TypeScript Integration](https://zod.dev/README#type-inference)
- [tRPC Integration](https://trpc.io/docs/server/validators)
