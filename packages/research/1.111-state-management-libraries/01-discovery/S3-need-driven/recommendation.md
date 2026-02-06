# S3 Need-Driven Recommendations Summary

**Last Updated**: 2026-01-16

## Quick Reference

| Use Case | Primary | Alternative | Avoid |
|----------|---------|-------------|-------|
| Simple SPA | Zustand | Jotai | Redux Toolkit |
| Complex Forms | Zustand + RHF | Jotai | useState alone |
| Real-Time Collab | Valtio | Preact Signals | Redux Toolkit |
| E-Commerce | Zustand | RTK (enterprise) | MobX |
| Dashboard | Preact Signals | Jotai | Redux Toolkit |
| Vue Project | Pinia | Nanostores (multi-FW) | Any React lib |
| Multi-Framework | Nanostores | TanStack Store | Framework-specific |

## Pattern Insights

### Zustand Dominates Simple-to-Medium Complexity

Zustand appears as the primary or alternative in 4 of 6 React use cases.

**Why**: Best balance of simplicity, performance, and flexibility.

### Performance-Critical → Signals

Preact Signals wins for:
- High-frequency updates (dashboards)
- Real-time data streams
- Mobile/low-end devices

### Complex Derived State → Jotai

Jotai excels when:
- Many computed values
- Cross-domain dependencies
- Need automatic optimization

### Enterprise/Audit → Redux Toolkit

Redux Toolkit justified for:
- Regulatory compliance (audit trails)
- Large teams (strict patterns)
- Complex middleware needs

### Vue → Pinia (No Contest)

Pinia is the only serious choice for Vue 3 projects.

## Cross-Cutting Insights

1. **Avoid useState for complex state** (appears in multiple "Avoid" sections)
2. **Combine with React Hook Form** for forms (best practice)
3. **React Query + Zustand** for server + client state separation
4. **Never use Recoil** (archived)

## Decision Shortcuts

**"What should I use?"** → Zustand (if React), Pinia (if Vue)

**"But I need..."**
- Performance → Preact Signals
- Atomic composition → Jotai
- Multi-framework → Nanostores
- Enterprise patterns → Redux Toolkit
- Real-time → Valtio

**Last Updated**: 2026-01-16
