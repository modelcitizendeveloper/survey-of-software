# Form & Validation Library Recommendation Guide

## Quick Decision Tree

```
Start Here
│
├─ What's your priority?
│  │
│  ├─ Standard React project
│  │  └─ React Hook Form + Zod ✓
│  │
│  ├─ Bundle size critical
│  │  └─ React Hook Form + Valibot ✓
│  │
│  ├─ Using TanStack ecosystem
│  │  └─ TanStack Form + Zod ✓
│  │
│  └─ Legacy JavaScript (no TypeScript)
│     └─ React Hook Form + Yup ✓

├─ Have existing Formik codebase?
│  └─ Plan migration to React Hook Form
│     (Formik is abandoned)
```

## The Default Choice: React Hook Form + Zod

For **90% of React projects**, use this combination:

```tsx
npm install react-hook-form @hookform/resolvers zod
```

**Why this wins:**
- React Hook Form: 12KB, zero deps, best performance
- Zod: TypeScript-first, type inference, 12M downloads/week
- Total: ~57KB (vs 104KB for Formik + Yup)
- Both actively maintained

---

## Recommendation by Scenario

### 1. New React + TypeScript Project

**Recommended**: React Hook Form + Zod

```tsx
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'

const schema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
})

type FormData = z.infer<typeof schema>
```

---

### 2. Bundle Size Critical (Mobile, PWA)

**Recommended**: React Hook Form + Valibot

Saves 43KB vs Zod:
- RHF + Zod: 57KB
- RHF + Valibot: 14KB

```tsx
import { useForm } from 'react-hook-form'
import { valibotResolver } from '@hookform/resolvers/valibot'
import * as v from 'valibot'

const schema = v.object({
  email: v.pipe(v.string(), v.email()),
  password: v.pipe(v.string(), v.minLength(8)),
})
```

---

### 3. TanStack Ecosystem User

**Recommended**: TanStack Form + Zod

If you're using TanStack Query, Router, Table:

```tsx
import { useForm } from '@tanstack/react-form'
import { zodValidator } from '@tanstack/zod-form-adapter'

const form = useForm({
  validatorAdapter: zodValidator(),
  // ...
})
```

---

### 4. Legacy JavaScript Project

**Recommended**: React Hook Form + Yup

For non-TypeScript projects where Yup's simpler syntax helps:

```tsx
import { useForm } from 'react-hook-form'
import { yupResolver } from '@hookform/resolvers/yup'
import * as yup from 'yup'

const schema = yup.object({
  email: yup.string().email().required(),
  password: yup.string().min(8).required(),
})
```

---

### 5. Existing Formik Codebase

**Recommended**: Plan migration to React Hook Form

Why migrate:
- Formik is abandoned (no updates in 1+ year)
- 3.6x larger bundle (44KB vs 12KB)
- Worse performance (controlled vs uncontrolled)

Migration strategy:
1. New forms use React Hook Form
2. Migrate existing forms incrementally
3. Replace Yup with Zod as you migrate

---

## What NOT to Do

### Don't Start New Projects with Formik
- Last commit: 1+ year ago
- No bug fixes or features
- Creator moved on

### Don't Use Yup for TypeScript Projects
- Type inference is limited
- Zod does it better
- Smaller bundle

### Don't Build Your Own Validation
- Schema libraries handle edge cases
- Type inference is valuable
- Community-tested

---

## Form vs Validation: Separate Concerns

Form libraries (state management):
- React Hook Form ✓
- TanStack Form
- Formik ✗

Validation libraries (schema + types):
- Zod ✓
- Valibot (bundle-critical)
- Yup (legacy JS)

They work together via **resolvers**:
```tsx
useForm({ resolver: zodResolver(schema) })
useForm({ resolver: valibotResolver(schema) })
useForm({ resolver: yupResolver(schema) })
```

---

## Bundle Size Summary

| Combination | Size | Recommendation |
|-------------|------|----------------|
| RHF + Valibot | 14KB | Bundle-critical |
| TanStack + Zod | 55KB | TanStack users |
| RHF + Zod | 57KB | **Default** |
| RHF + Yup | 72KB | Legacy JS |
| Formik + Yup | 104KB | Avoid |

---

## Final Recommendations

### For Most Projects
**React Hook Form + Zod** - The standard choice

### For Bundle-Sensitive
**React Hook Form + Valibot** - 75% smaller validation

### For TanStack Users
**TanStack Form + Zod** - Ecosystem alignment

### For Legacy JS
**React Hook Form + Yup** - Better than Formik

### Always Avoid
**Formik** - Abandoned, migrate away
