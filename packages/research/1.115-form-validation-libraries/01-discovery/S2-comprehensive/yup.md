# Yup - Technical Deep-Dive

## Architecture

### Schema Builder Pattern

Yup uses a **fluent builder API** for schema construction, predating Zod by several years.

**Builder approach**:
```tsx
const schema = yup.object({
  email: yup.string().required().email(),
  age: yup.number().positive().integer(),
})

// Each method returns a new schema instance
const base = yup.string()
const required = base.required() // New instance
const email = required.email()   // New instance
```

Unlike Zod's class-based approach, Yup uses **prototype chain manipulation** for schema construction:

```tsx
class Schema {
  constructor(spec) {
    this._spec = spec
  }

  clone(spec) {
    // Creates new instance with merged spec
    return new this.constructor({
      ...this._spec,
      ...spec,
    })
  }

  required(message) {
    return this.clone({
      required: true,
      message: message || 'Required',
    })
  }
}
```

### Async-First Validation

Yup was designed for **asynchronous validation from the ground up**:

```tsx
// All validation returns promises
schema.validate(data)      // Promise<T>
schema.validateSync(data)  // Synchronous (limited features)

// Async validators are first-class:
yup.string().test('checkDB', 'Already exists', async (value) => {
  return !(await checkDatabase(value))
})
```

**Key difference from Zod**: Yup's async-first design means better support for async validators but slower performance for synchronous validation.

### Context-Based Validation

Yup uses **validation context** for cross-field validation:

```tsx
const schema = yup.object({
  password: yup.string().required(),
  confirmPassword: yup.string()
    .required()
    .test('passwords-match', 'Passwords must match', function(value) {
      return value === this.parent.password
    })
})

// Access to parent, root, options:
.test('custom', function(value) {
  this.parent    // Parent object
  this.root      // Root value
  this.options   // Validation options
  this.path      // Current field path
})
```

## Performance Characteristics

### Bundle Size Breakdown

**60KB gzipped (core):**
- Schema classes: 18KB
- Validation engine: 15KB
- Error handling: 10KB
- Type coercion: 8KB
- Locale/messages: 6KB
- Utilities: 3KB

**Dependencies**: 4 small packages (~5KB total)
- property-expr (path parsing)
- toposort (dependency ordering)
- tiny-case (string utilities)
- type-fest (TypeScript types)

**Tree-shaking**: Limited - schema methods are prototype-based, harder to eliminate.

### Runtime Performance

**Validation speed** (1000 iterations, simple schema):

| Library | Sync Time | Async Time |
|---------|-----------|------------|
| Yup | 15ms | 40ms |
| Zod | 8ms | 30ms |
| Valibot | 3ms | 25ms |

**Why slower than Zod**:
1. Async-by-default overhead
2. More abstraction layers
3. Prototype chain traversal
4. Type coercion on every validation

**Why slower async than Zod**:
Yup creates promise chains even for sync validators, while Zod only uses promises for explicit async refinements.

### Memory Footprint

- Schema definition: ~200 bytes per field (2x Zod)
- Validation context: ~1KB per validate call
- Error object: ~1.5KB per validation failure

**Memory issue**: Yup clones schemas frequently (every method call), creating more GC pressure than Zod's immutable approach.

## API Design Patterns

### Primitive Types

```tsx
yup.string()
yup.number()
yup.boolean()
yup.date()
yup.array()
yup.object()
yup.mixed()   // any type (like Zod's any())
```

**Notable**: No separate `undefined`, `null`, or `never` types - use `.nullable()`, `.required()` modifiers instead.

### String Validators

```tsx
yup.string()
  .required('Email is required')
  .email('Must be valid email')
  .min(5, 'Too short')
  .max(100, 'Too long')
  .matches(/^[A-Z]/, 'Must start with capital')
  .url('Must be URL')
  .lowercase('Must be lowercase')
  .uppercase('Must be uppercase')
  .trim('Must not have whitespace')
```

**Coercion built-in**: `.trim()` transforms value, not just validates.

### Number Validators

```tsx
yup.number()
  .required()
  .positive('Must be positive')
  .negative('Must be negative')
  .min(0, 'Min is 0')
  .max(100, 'Max is 100')
  .lessThan(50, 'Less than 50')
  .moreThan(10, 'More than 10')
  .integer('Must be integer')
  .round('floor')  // Transform: round value
```

### Array Schemas

```tsx
yup.array()
  .of(yup.string())  // Array items schema
  .min(1, 'Need at least one')
  .max(10, 'Max 10 items')
  .compact()  // Remove falsy values
  .ensure()   // Always return array (even if undefined)
```

**Key difference from Zod**: `.ensure()` coerces undefined → [], Zod requires explicit default.

### Object Schemas

```tsx
const schema = yup.object({
  name: yup.string().required(),
  age: yup.number(),
})

// Or with explicit shape:
const schema = yup.object().shape({
  name: yup.string(),
})

// Nested objects:
yup.object({
  user: yup.object({
    address: yup.object({
      street: yup.string(),
    }),
  }),
})
```

## Advanced Features

### Conditional Validation

**when() for conditional schemas**:

```tsx
const schema = yup.object({
  role: yup.string().oneOf(['user', 'admin']),
  permissions: yup.array()
    .when('role', {
      is: 'admin',
      then: (schema) => schema.required().min(1),
      otherwise: (schema) => schema.notRequired(),
    })
})

// Multiple conditions:
yup.string()
  .when(['field1', 'field2'], {
    is: (val1, val2) => val1 && val2,
    then: (schema) => schema.required(),
  })

// Function form for complex logic:
yup.string().when('other', (other, schema) => {
  if (other > 10) return schema.required()
  return schema
})
```

**Key insight**: Yup's `.when()` is more powerful than Zod's unions for conditional validation.

### Cross-Field Validation

```tsx
const schema = yup.object({
  startDate: yup.date().required(),
  endDate: yup.date()
    .min(yup.ref('startDate'), 'End must be after start'),
})

// Using refs:
yup.number().lessThan(yup.ref('max'))
yup.string().oneOf([yup.ref('password')], 'Passwords must match')
```

**ref() syntax**: Access other fields in the schema.

### Transforms

```tsx
// Transform before validation
yup.string()
  .transform((value, originalValue) => {
    return originalValue ? originalValue.trim() : value
  })
  .required()

// Common pattern: normalize input
yup.string()
  .transform((v) => v?.toLowerCase())
  .email()
```

**Key difference from Zod**: Transforms run **before** validation in Yup, **after** in Zod.

### Lazy Schemas

For recursive/circular structures:

```tsx
const CategorySchema = yup.object({
  name: yup.string(),
  children: yup.lazy(() =>
    yup.array().of(CategorySchema)
  ),
})

// With type annotation:
type Category = {
  name: string
  children?: Category[]
}

const schema: yup.Schema<Category> = yup.object({
  name: yup.string().required(),
  children: yup.lazy(() => yup.array().of(schema)),
})
```

### Default Values

```tsx
// Provide default when value is undefined
yup.string().default('N/A')
yup.number().default(0)
yup.array().default([])

// Function defaults:
yup.date().default(() => new Date())

// Apply defaults on validation:
schema.validateSync(data, { stripUnknown: true })
```

**Key feature**: Defaults are applied during validation, not schema construction (unlike Zod).

### Type Casting

Yup performs **automatic type coercion**:

```tsx
const schema = yup.object({
  age: yup.number(),
  active: yup.boolean(),
})

schema.cast({ age: '42', active: 'true' })
// { age: 42, active: true }

// Control casting:
yup.number().cast('42')          // 42
yup.number().cast('invalid')     // NaN
yup.number().strict().cast('42') // '42' (no coercion)
```

**Trade-off**: Convenient but can mask bugs (Zod requires explicit `.coerce`).

## TypeScript Integration

### Type Inference

```tsx
const schema = yup.object({
  name: yup.string().required(),
  age: yup.number(),
})

type Inferred = yup.InferType<typeof schema>
// { name: string; age?: number }
```

**Limitations compared to Zod**:
1. Less accurate type inference (optional fields)
2. No input/output type separation
3. Transforms don't update types
4. Generic type parameters less ergonomic

### Type Annotations

```tsx
// Explicit type annotation:
const schema: yup.Schema<User> = yup.object({
  name: yup.string().required(),
  email: yup.string().email().required(),
})

// Validate against type:
const user = schema.validateSync(data) // user: User
```

### Generic Schemas

```tsx
function createPaginatedSchema<T extends yup.Schema>(itemSchema: T) {
  return yup.object({
    items: yup.array().of(itemSchema),
    total: yup.number().required(),
    page: yup.number().required(),
  })
}

const userListSchema = createPaginatedSchema(userSchema)
```

## Error Handling

### ValidationError Structure

```tsx
try {
  await schema.validate(data, { abortEarly: false })
} catch (error) {
  if (error instanceof yup.ValidationError) {
    error.name    // 'ValidationError'
    error.value   // Value that failed
    error.path    // 'user.email'
    error.type    // 'email'
    error.errors  // ['Must be valid email']
    error.inner   // Array of all errors (if abortEarly: false)
  }
}
```

### Error Messages

**Default messages** (friendlier than Zod):

```tsx
yup.string().required()
// 'this is a required field'

yup.string().email()
// 'this must be a valid email'

yup.number().min(5)
// 'this must be greater than or equal to 5'
```

**Custom messages**:

```tsx
// Per-validator:
yup.string().required('Email is required').email('Invalid email')

// Per-field:
yup.string().email().label('Email Address')
// 'Email Address must be a valid email'

// Global overrides:
yup.setLocale({
  mixed: {
    required: 'This field is required',
  },
  string: {
    email: 'Enter a valid email address',
  },
})
```

### Validation Options

```tsx
schema.validate(data, {
  abortEarly: false,      // Return all errors, not just first
  stripUnknown: true,     // Remove unknown keys
  strict: true,           // No type coercion
  context: { user: currentUser }, // Pass context to validators
  recursive: true,        // Validate nested schemas
})
```

## Integration Patterns

### React Hook Form

```tsx
import { yupResolver } from '@hookform/resolvers/yup'

const { register, handleSubmit } = useForm({
  resolver: yupResolver(schema),
})
```

### Formik

Yup was **designed for Formik** (same author originally):

```tsx
import { Formik } from 'formik'

<Formik
  initialValues={{ email: '' }}
  validationSchema={schema}
  onSubmit={handleSubmit}
>
  {/* form */}
</Formik>
```

### Express Middleware

```tsx
function validateBody(schema) {
  return async (req, res, next) => {
    try {
      req.body = await schema.validate(req.body, {
        abortEarly: false,
        stripUnknown: true,
      })
      next()
    } catch (error) {
      res.status(400).json({ errors: error.errors })
    }
  }
}

app.post('/api/user', validateBody(userSchema), handler)
```

## Testing Strategies

### Unit Testing

```tsx
import { describe, it, expect } from 'vitest'

describe('UserSchema', () => {
  it('validates email format', async () => {
    const schema = yup.object({ email: yup.string().email() })

    await expect(schema.validate({ email: 'invalid' }))
      .rejects.toThrow('email must be a valid email')

    await expect(schema.validate({ email: 'test@example.com' }))
      .resolves.toEqual({ email: 'test@example.com' })
  })

  it('handles cross-field validation', async () => {
    const schema = yup.object({
      password: yup.string(),
      confirm: yup.string().oneOf([yup.ref('password')]),
    })

    await expect(schema.validate({
      password: 'pass123',
      confirm: 'different',
    })).rejects.toThrow()
  })
})
```

### Testing Async Validators

```tsx
it('validates async rules', async () => {
  const checkUsername = jest.fn().mockResolvedValue(false)

  const schema = yup.string().test(
    'unique',
    'Username taken',
    async (value) => !(await checkUsername(value))
  )

  await schema.validate('newuser')
  expect(checkUsername).toHaveBeenCalledWith('newuser')
})
```

## Architectural Trade-offs

### Advantages

1. **Friendly API**: Most intuitive syntax of all validators
2. **Error messages**: Best default messages, easier to customize
3. **Async validation**: First-class support, most mature
4. **Conditional logic**: Powerful `.when()` for complex rules
5. **Type coercion**: Automatic (convenient for forms)
6. **Ecosystem**: Works everywhere (Formik, RHF, etc.)
7. **Stability**: Mature, battle-tested (7+ years)

### Disadvantages

1. **Bundle size**: 60KB (33% larger than Zod)
2. **Performance**: Slower than Zod/Valibot (async overhead)
3. **TypeScript**: Weaker type inference than Zod
4. **Memory**: More allocations (clone-heavy API)
5. **Tree-shaking**: Poor (prototype-based architecture)
6. **Type coercion**: Can mask bugs (implicit conversions)
7. **Maintenance**: Less active development than Zod

## When to Use

**Choose Yup when**:
- Using Formik (designed together)
- JavaScript project (not TypeScript-first)
- Need friendliest error messages
- Want automatic type coercion
- Complex conditional validation (`.when()`)
- Team prefers fluent/readable API
- Async validation is primary use case

**Consider alternatives when**:
- TypeScript project → Zod (better types)
- Bundle size critical → Valibot (95% smaller)
- Performance critical → Zod or Valibot
- Want schema as source of truth → Zod
- Need brand types or transformations → Zod

## Migration from Yup to Zod

**Common patterns translated**:

```tsx
// Yup → Zod

// Required field
yup.string().required()
→ z.string()

// Optional field
yup.string()
→ z.string().optional()

// Email validation
yup.string().email()
→ z.string().email()

// Conditional
yup.string().when('role', {
  is: 'admin',
  then: schema => schema.required(),
})
→ z.discriminatedUnion('role', [
  z.object({ role: z.literal('admin'), field: z.string() }),
  z.object({ role: z.literal('user'), field: z.string().optional() }),
])

// Cross-field
yup.string().oneOf([yup.ref('password')])
→ z.string().refine((val, ctx) => val === ctx.parent.password)

// Transform
yup.string().transform(s => s.trim())
→ z.string().transform(s => s.trim())
```

**Key differences**:
- Yup transforms before validation, Zod after
- Yup has built-in coercion, Zod requires `.coerce`
- Zod has better TypeScript, Yup has friendlier API

## Performance Optimization

### Reuse Schemas

```tsx
// ✗ Bad: creates new schema every time
function validate(data) {
  const schema = yup.object({ email: yup.string() })
  return schema.validate(data)
}

// ✓ Good: create once
const schema = yup.object({ email: yup.string() })
function validate(data) {
  return schema.validate(data)
}
```

### Use validateSync for Sync Validators

```tsx
// If no async validators:
try {
  const result = schema.validateSync(data)
} catch (error) {
  // ...
}
// Faster than await schema.validate()
```

### Strip Unknown Fields

```tsx
// Reduce memory usage:
schema.validate(data, { stripUnknown: true })
```

### Abort Early

```tsx
// Stop at first error (faster):
schema.validate(data, { abortEarly: true })

// Show all errors (slower):
schema.validate(data, { abortEarly: false })
```

## Resources

- [Official Docs](https://github.com/jquense/yup)
- [API Reference](https://github.com/jquense/yup#api)
- [Type Inference](https://github.com/jquense/yup#typescript-integration)
- [Conditional Validation](https://github.com/jquense/yup#mixed-whenkeys-string--arraystring-builder-object--value-schema-schema-schema)
- [Error Messages](https://github.com/jquense/yup#customizing-errors)
