# Valibot - Technical Deep-Dive

## Architecture

### Modular Design Philosophy

Valibot's innovation is **maximum tree-shakability** through granular modular design.

**Zod approach** (monolithic):
```tsx
import { z } from 'zod' // Imports entire library (~45KB)
const schema = z.string().email()
```

**Valibot approach** (modular):
```tsx
import * as v from 'valibot' // Only imports what you use (~1-2KB)
const schema = v.pipe(v.string(), v.email())
```

### Pipe-Based Composition

Unlike Zod's method chaining, Valibot uses **functional composition**:

```tsx
// Zod (chaining)
z.string().min(5).email()

// Valibot (pipe)
v.pipe(
  v.string(),
  v.minLength(5),
  v.email()
)
```

**Advantages**:
- Each validator is a separate module → better tree-shaking
- Explicit execution order
- Easier to extend with custom validators

**Trade-off**: Slightly more verbose syntax.

### Type Inference

Similar to Zod, but uses pipe type inference:

```tsx
const schema = v.object({
  email: v.pipe(v.string(), v.email()),
  age: v.pipe(v.number(), v.minValue(0)),
})

type Output = v.InferOutput<typeof schema>
// { email: string; age: number }
```

## Performance Characteristics

### Bundle Size

**Comparison for validation-only scenario**:

| Library | Bundle Size |
|---------|-------------|
| Valibot | 1-2KB (depending on validators used) |
| Zod | 45KB |
| Yup | 60KB |

**Example breakdown**:
- String validation: ~300 bytes
- Email validation: ~100 bytes
- Object schema: ~500 bytes
- **Total for simple email + password form: ~1.2KB**

### Runtime Performance

Similar to Zod (synchronous, fast parsing):

| Schema Complexity | Valibot | Zod |
|------------------|---------|-----|
| Simple (3 fields) | 2ms | 2ms |
| Medium (10 fields) | 7ms | 8ms |
| Complex (nested) | 23ms | 25ms |

**Key insight**: Performance is comparable; bundle size is the main differentiator.

## API Design

### Schema Definition

```tsx
import * as v from 'valibot'

// Primitives
const StringSchema = v.string()
const NumberSchema = v.number()
const BooleanSchema = v.boolean()

// With validations (via pipe)
const EmailSchema = v.pipe(v.string(), v.email())
const AgeSchema = v.pipe(v.number(), v.minValue(0), v.maxValue(120))

// Objects
const UserSchema = v.object({
  name: v.pipe(v.string(), v.minLength(1)),
  email: v.pipe(v.string(), v.email()),
  age: v.optional(v.pipe(v.number(), v.minValue(0))),
})

// Arrays
const TagsSchema = v.array(v.string())
const TagsSchema = v.pipe(v.array(v.string()), v.minLength(1))

// Unions
const IdSchema = v.union([v.string(), v.number()])

// Enums
const RoleSchema = v.picklist(['admin', 'user', 'guest'])
```

### Custom Validations

```tsx
const schema = v.pipe(
  v.string(),
  v.custom((val) => val.length % 2 === 0, 'Must be even length')
)

// Async custom validation
const schema = v.pipe(
  v.string(),
  v.customAsync(async (val) => {
    const exists = await checkDB(val)
    return !exists
  }, 'Already exists')
)
```

### Transformations

```tsx
const schema = v.pipe(
  v.string(),
  v.transform((s) => s.toUpperCase())
)

// Type changes with transform
const schema = v.pipe(
  v.string(),           // Input type: string
  v.transform(parseInt) // Output type: number
)
```

## Advanced Features

### Object Manipulation

```tsx
const UserSchema = v.object({
  id: v.string(),
  email: v.string(),
  password: v.string(),
})

// Pick fields
const PublicUser = v.pick(UserSchema, ['id', 'email'])

// Omit fields
const CreateUser = v.omit(UserSchema, ['id'])

// Partial (all optional)
const PartialUser = v.partial(UserSchema)

// Required (all required)
const RequiredUser = v.required(PartialUser)

// Merge schemas
const ExtendedUser = v.merge([UserSchema, v.object({ role: v.string() })])
```

### Variant (Discriminated Union)

```tsx
const EventSchema = v.variant('type', [
  v.object({ type: v.literal('click'), x: v.number(), y: v.number() }),
  v.object({ type: v.literal('keypress'), key: v.string() }),
])
```

### Fallback Values

```tsx
const schema = v.pipe(
  v.string(),
  v.fallback('default value') // Use if validation fails
)
```

### Error Handling

```tsx
// parse() throws ValiError
try {
  const result = v.parse(schema, data)
} catch (error) {
  if (error instanceof v.ValiError) {
    error.issues.forEach((issue) => {
      console.log(issue.path)
      console.log(issue.message)
    })
  }
}

// safeParse() never throws
const result = v.safeParse(schema, data)
if (result.success) {
  result.output // Typed correctly
} else {
  result.issues // Validation errors
}
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

const { register, handleSubmit } = useForm<FormData>({
  resolver: valibotResolver(schema),
})
```

## Architectural Trade-offs

### Advantages

1. **Bundle size**: 95% smaller than Zod (1-2KB vs 45KB)
2. **Tree-shaking**: Granular modular design
3. **Performance**: Fast, comparable to Zod
4. **TypeScript**: Full type inference support
5. **Modern**: Built with latest JS/TS features

### Disadvantages

1. **Ecosystem**: Smaller than Zod (newer library)
2. **Syntax**: Pipe syntax more verbose than chaining
3. **Documentation**: Less comprehensive than Zod
4. **Adoption**: Lower usage (500K/week vs 12M for Zod)
5. **Maturity**: Newer, fewer edge cases covered

## When to Use

**Choose Valibot when**:
- Bundle size is critical (mobile, PWA, performance-sensitive)
- Using TypeScript
- Need schema validation with minimal overhead
- Building public-facing apps where every KB matters

**Choose Zod instead when**:
- Bundle size is not a concern
- Want larger ecosystem and community
- Need more comprehensive documentation
- Prefer method chaining over pipe syntax

## Migration from Zod

Most Zod patterns have Valibot equivalents:

```tsx
// Zod → Valibot
z.string()                      → v.string()
z.string().email()              → v.pipe(v.string(), v.email())
z.string().min(5)               → v.pipe(v.string(), v.minLength(5))
z.number().optional()           → v.optional(v.number())
z.union([z.string(), z.number()]) → v.union([v.string(), v.number()])
z.object({ ... })               → v.object({ ... })
z.array(z.string())             → v.array(v.string())
```

**Migration strategy**:
1. Replace imports: `import { z } from 'zod'` → `import * as v from 'valibot'`
2. Convert chaining to pipes: `.method()` → `v.pipe(v.base(), v.method())`
3. Update type inference: `z.infer` → `v.InferOutput`
4. Test thoroughly (some edge cases differ)

## Bundle Size Example

**Real-world comparison** (login form: email + password):

```tsx
// Zod version: 57KB (RHF 12KB + Zod 45KB)
import { z } from 'zod'
const schema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
})

// Valibot version: 14KB (RHF 12KB + Valibot ~2KB)
import * as v from 'valibot'
const schema = v.object({
  email: v.pipe(v.string(), v.email()),
  password: v.pipe(v.string(), v.minLength(8)),
})

// Savings: 43KB (75% reduction)
```

## Resources

- [Official Docs](https://valibot.dev/)
- [GitHub](https://github.com/fabian-hiller/valibot)
- [Bundle Size Comparison](https://bundlephobia.com/package/valibot)
- [Migration Guide from Zod](https://valibot.dev/guides/migrate-from-zod/)
