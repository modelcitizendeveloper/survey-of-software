# Use Case: Complex Forms (Multi-Step Wizards)

**Last Updated**: 2026-01-16
**Complexity**: Medium-High
**Target**: Enterprise apps, onboarding flows, checkout processes

## Scenario

Multi-step form wizard with:
- 3-5 steps with conditional logic
- Cross-field validation
- Async validation (server-side)
- Draft persistence (resume later)
- Progress tracking
- Error handling with field-level feedback

**Team**: 2-5 developers, validation-heavy requirements
**Timeline**: 2-4 weeks
**Performance**: Medium priority (desktop focus)

## Requirements

### State Structure
```typescript
interface FormState {
  currentStep: number
  formData: {
    personal: { name, email, phone }
    address: { street, city, zip, country }
    payment: { cardNumber, cvv, expiry }
  }
  validationErrors: Record<string, string>
  touched: Record<string, boolean>
  isSubmitting: boolean
}
```

### Key Challenges
- Conditional fields (step 2 depends on step 1 choices)
- Async validation (check email availability)
- Complex validation rules (credit card Luhn algorithm)
- Draft auto-save every 30s
- Progress indicator

## Top Library Recommendations

### 1. Zustand + React Hook Form (Best Combination)

**Zustand**: Form-wide state (currentStep, draft save)
**React Hook Form**: Field-level state (values, validation)

```typescript
// Form store (Zustand)
const useFormWizardStore = create((set) => ({
  currentStep: 0,
  draftData: null,
  nextStep: () => set((s) => ({ currentStep: s.currentStep + 1 })),
  prevStep: () => set((s) => ({ currentStep: s.currentStep - 1 })),
  saveDraft: (data) => {
    localStorage.setItem('draft', JSON.stringify(data))
    set({ draftData: data })
  },
}))

// Step 1 Component (React Hook Form)
function PersonalInfoStep() {
  const { register, formState: { errors }, handleSubmit } = useForm()
  const nextStep = useFormWizardStore((s) => s.nextStep)
  const saveDraft = useFormWizardStore((s) => s.saveDraft)

  const onSubmit = (data) => {
    saveDraft(data)
    nextStep()
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register('name', { required: 'Name required' })} />
      {errors.name && <span>{errors.name.message}</span>}

      <input
        {...register('email', {
          required: 'Email required',
          validate: async (email) => {
            const available = await checkEmailAvailability(email)
            return available || 'Email already taken'
          },
        })}
      />
      {errors.email && <span>{errors.email.message}</span>}

      <button type="submit">Next</button>
    </form>
  )
}
```

**Pros**: Clean separation (wizard state vs form state), excellent validation DX
**Bundle**: 3KB (Zustand) + 8KB (RHF) = 11KB total

---

### 2. Jotai + jotai-form

```typescript
// Atoms for each step
const personalInfoAtom = atom({ name: '', email: '', phone: '' })
const addressInfoAtom = atom({ street: '', city: '', zip: '', country: '' })
const paymentInfoAtom = atom({ cardNumber: '', cvv: '', expiry: '' })

// Form state
const currentStepAtom = atom(0)
const formValidAtom = atom((get) => {
  const personal = get(personalInfoAtom)
  return personal.name && personal.email.includes('@')
})

// Validation atoms
const emailValidationAtom = atom(async (get) => {
  const email = get(personalInfoAtom).email
  if (!email) return null

  const available = await checkEmailAvailability(email)
  return available ? null : 'Email already taken'
})

// Component
function PersonalInfoStep() {
  const [personal, setPersonal] = useAtom(personalInfoAtom)
  const [, nextStep] = useAtom(currentStepAtom)
  const emailError = useAtomValue(emailValidationAtom)

  return (
    <div>
      <input
        value={personal.name}
        onChange={(e) => setPersonal({ ...personal, name: e.target.value })}
      />
      <input
        value={personal.email}
        onChange={(e) => setPersonal({ ...personal, email: e.target.value })}
      />
      {emailError && <span>{emailError}</span>}
      <button onClick={() => nextStep((s) => s + 1)}>Next</button>
    </div>
  )
}
```

**Pros**: Atomic composition, automatic async handling
**Cons**: Manual validation logic (no schema validation out-of-box)
**Bundle**: 2.9KB

---

### 3. Redux Toolkit (Enterprise Option)

```typescript
const formSlice = createSlice({
  name: 'form',
  initialState: {
    currentStep: 0,
    formData: {},
    validationErrors: {},
  },
  reducers: {
    updateField: (state, action) => {
      const { step, field, value } = action.payload
      state.formData[step][field] = value
    },
    setValidationError: (state, action) => {
      state.validationErrors[action.payload.field] = action.payload.error
    },
    nextStep: (state) => { state.currentStep += 1 },
  },
})

const validateEmailAsync = createAsyncThunk(
  'form/validateEmail',
  async (email: string) => {
    const available = await checkEmailAvailability(email)
    if (!available) throw new Error('Email taken')
  }
)
```

**Pros**: Centralized logging (audit trail for enterprise), strict patterns
**Cons**: Heavy boilerplate, 33KB bundle
**When to use**: Enterprise with audit requirements

## Recommendation

**Primary: Zustand + React Hook Form**

**Rationale**:
- Best-in-class form validation (RHF)
- Clean state separation
- Excellent async validation handling
- Schema validation (Zod/Yup integration)
- Moderate bundle size (11KB)

**Alternative**: Jotai (if already using for global state)

## Anti-Patterns

❌ Don't use useState for complex forms (validation nightmare)
❌ Don't mix form libraries (e.g., Formik + Zustand for same form)
❌ Don't skip draft persistence for long forms
❌ Don't block UI during async validation (use debounce)

**Last Updated**: 2026-01-16
