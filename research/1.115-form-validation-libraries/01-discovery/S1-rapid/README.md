# 1.115 Form & Validation Libraries - S1 Rapid Discovery

## Quick Decision Guide

| Situation | Recommendation |
|-----------|----------------|
| New React project | **React Hook Form + Zod** |
| TypeScript project | React Hook Form + Zod |
| Bundle size critical | React Hook Form + **Valibot** |
| TanStack ecosystem | **TanStack Form** + Zod |
| Existing Formik project | Consider migration to RHF |
| Legacy JavaScript | React Hook Form + Yup |

## 2025 Landscape

### Form Libraries

```
GitHub Stars:
React Hook Form:  ████████████████████████████  38.7K
Formik:           ██████████████████████        33.3K
React Final Form: █████                         7.3K
TanStack Form:    ███                           4K

Weekly Downloads:
React Hook Form:  ████████████████████████████  5M
Formik:           ███████████                   1.9M
React Final Form: ██                            350K
TanStack Form:    █                             50K
```

### Validation Libraries

```
Weekly Downloads:
Zod:     ████████████████████████████████████  12M
Yup:     ████████████████████████              8M
Valibot: ██                                    500K
```

## The Winning Combination: React Hook Form + Zod

This is the **default choice** for React forms in 2025:

```tsx
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'

const schema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
})

type FormData = z.infer<typeof schema>

function LoginForm() {
  const { register, handleSubmit, formState: { errors } } = useForm<FormData>({
    resolver: zodResolver(schema),
  })

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register('email')} />
      {errors.email && <span>{errors.email.message}</span>}
      <input type="password" {...register('password')} />
      {errors.password && <span>{errors.password.message}</span>}
      <button type="submit">Login</button>
    </form>
  )
}
```

## Why This Combination Wins

| Aspect | React Hook Form + Zod |
|--------|----------------------|
| Bundle | 12KB + 45KB = 57KB |
| Performance | Uncontrolled (minimal re-renders) |
| TypeScript | First-class (infer types from schema) |
| Validation | Schema-based (reusable, testable) |
| Ecosystem | Huge (resolvers for all validators) |
| Maintenance | Both actively maintained |

## Library Summary

### Form Management

| Library | Bundle | Approach | Status | Best For |
|---------|--------|----------|--------|----------|
| React Hook Form | 12KB | Uncontrolled | Active | Default choice |
| Formik | 44KB | Controlled | Dormant | Legacy projects |
| TanStack Form | ~10KB | Signals | Active | TanStack users |
| React Final Form | ~15KB | Subscription | Dormant | Existing users |

### Validation Schema

| Library | Bundle | TypeScript | Best For |
|---------|--------|------------|----------|
| Zod | 45KB | First-class | Default choice |
| Yup | 60KB | Supported | Legacy/JavaScript |
| Valibot | 1-2KB | First-class | Bundle-sensitive |

## Key Insight: Formik is Dead

Formik was the default for years, but:
- Last commit: over 1 year ago
- GitHub issues: ignored
- No new features
- Larger bundle (44KB vs 12KB)
- Controlled = more re-renders

**Recommendation**: Migrate existing Formik projects to React Hook Form.

## Sources

- [React Hook Form vs Formik - LogRocket](https://blog.logrocket.com/react-hook-form-vs-formik-comparison/)
- [Zod vs Yup - Better Stack](https://betterstack.com/community/guides/scaling-nodejs/yup-vs-zod/)
- [Valibot - Lightweight Zod Alternative](https://blog.logrocket.com/valibot-lightweight-zod-alternative/)
- [TanStack Form](https://tanstack.com/form/latest)
