# Form & Validation Libraries - Comparison Matrix

## Form Libraries

### Quantitative Comparison

| Library | Stars | Weekly DL | Bundle | Deps | Approach |
|---------|-------|-----------|--------|------|----------|
| React Hook Form | 38.7K | 5M | 12KB | 0 | Uncontrolled |
| Formik | 33.3K | 1.9M | 44KB | 9 | Controlled |
| React Final Form | 7.3K | 350K | 15KB | 2 | Subscription |
| TanStack Form | 4K | 50K | 10KB | 1 | Signals |

### Feature Comparison

| Feature | RHF | Formik | Final Form | TanStack |
|---------|-----|--------|------------|----------|
| TypeScript | ★★★★★ | ★★★ | ★★★ | ★★★★★ |
| Performance | ★★★★★ | ★★★ | ★★★★ | ★★★★★ |
| Bundle Size | ★★★★★ | ★★ | ★★★★ | ★★★★★ |
| Documentation | ★★★★★ | ★★★★ | ★★★ | ★★★★ |
| Maintenance | ★★★★★ | ★ | ★★ | ★★★★★ |
| Ecosystem | ★★★★★ | ★★★★ | ★★★ | ★★★ |

### Maintenance Status

| Library | Last Commit | Status |
|---------|-------------|--------|
| React Hook Form | Days ago | Active |
| Formik | 1+ year ago | **Abandoned** |
| React Final Form | Months ago | Maintenance |
| TanStack Form | Days ago | Active |

## Validation Libraries

### Quantitative Comparison

| Library | Stars | Weekly DL | Bundle | Deps |
|---------|-------|-----------|--------|------|
| Zod | 35K | 12M | 45KB | 0 |
| Yup | 22K | 8M | 60KB | 4 |
| Valibot | 6K | 500K | 1-2KB | 0 |

### Feature Comparison

| Feature | Zod | Yup | Valibot |
|---------|-----|-----|---------|
| TypeScript | ★★★★★ | ★★★ | ★★★★★ |
| Type Inference | ★★★★★ | ★★★ | ★★★★★ |
| Bundle Size | ★★★ | ★★ | ★★★★★ |
| API Simplicity | ★★★★★ | ★★★★ | ★★★★ |
| Ecosystem | ★★★★★ | ★★★★ | ★★★ |
| Performance | ★★★★ | ★★★ | ★★★★★ |

### TypeScript Integration

| Library | Type Inference | Single Source of Truth |
|---------|---------------|------------------------|
| Zod | Excellent | Yes |
| Valibot | Excellent | Yes |
| Yup | Limited | Partial |

## Recommended Combinations

### Default: React Hook Form + Zod (57KB)
```
Best for: Most projects
TypeScript: Excellent
Ecosystem: Huge
Status: Both actively maintained
```

### Bundle Optimized: React Hook Form + Valibot (14KB)
```
Best for: Mobile, slow networks
TypeScript: Excellent
Trade-off: Smaller Valibot ecosystem
Status: Both actively maintained
```

### TanStack: TanStack Form + Zod (~55KB)
```
Best for: TanStack ecosystem users
TypeScript: Excellent
Status: Both actively maintained
```

### Legacy: Formik + Yup (~104KB)
```
Best for: Existing projects only
Trade-off: Abandoned, large bundle
Status: Both in maintenance mode
```

## Decision Matrix

| Situation | Form Library | Validation |
|-----------|--------------|------------|
| New TypeScript project | RHF | Zod |
| Bundle size critical | RHF | Valibot |
| TanStack ecosystem | TanStack Form | Zod |
| Legacy JavaScript | RHF | Yup |
| Existing Formik project | Migrate to RHF | Migrate to Zod |

## Performance Comparison

### Re-renders (10 field form)

```
Per keystroke re-renders:

Formik (controlled):    ████████████████████ 10 (whole form)
React Final Form:       ████ 2 (field + form)
React Hook Form:        █ 0-1 (just validation)
TanStack Form:          █ 0-1 (signal-based)
```

### Bundle Size (Form + Validation)

```
Formik + Yup:           ████████████████████████████████ 104KB
React Hook Form + Yup:  █████████████████████ 72KB
React Hook Form + Zod:  █████████████████ 57KB
TanStack Form + Zod:    ████████████████ 55KB
React Hook Form + Valibot: ████ 14KB
```

## Migration Paths

### Formik → React Hook Form
- Similar concepts, different API
- Gradual migration possible
- Form-by-form replacement

### Yup → Zod
- Nearly identical syntax
- Can coexist during migration
- Minor API differences

### Zod → Valibot
- Codemod available
- Pipe syntax is main difference
- Good for bundle optimization
