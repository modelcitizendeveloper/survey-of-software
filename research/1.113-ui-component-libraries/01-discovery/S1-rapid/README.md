# 1.113 UI Component Libraries - S1 Rapid Discovery

## Quick Decision Guide

| Situation | Recommendation |
|-----------|----------------|
| New React project (default) | **shadcn/ui** |
| Already using Tailwind | shadcn/ui or Headless UI |
| Enterprise with Material Design | MUI |
| Data-heavy admin panels | Ant Design |
| Building custom design system | Radix UI + Tailwind |
| Want full-featured + modern DX | Mantine |
| Prop-based styling preference | Chakra UI |
| Need Vue support | Headless UI |

## 2025 Landscape Summary

### By GitHub Stars (March 2025)
```
MUI:           ████████████████████████████████████  95K
Ant Design:    ███████████████████████████████████   94K
shadcn/ui:     █████████████████████████████████     85K
Chakra UI:     ███████████████                       39K
Mantine:       ███████████                           28K
Headless UI:   ██████████                            26K
Radix UI:      ███████                               17K
```

### By npm Weekly Downloads
```
MUI:           ████████████████████████████████████  4.1M
Ant Design:    ████████████████                      1.4M
Headless UI:   █████████                             800K
Chakra UI:     ██████                                587K
Mantine:       █████                                 500K
Radix UI:      ██                                    226K
```

Note: shadcn/ui uses copy-paste model (no npm downloads tracked).

## Library Categories

### 1. Pre-Styled Complete Libraries
Full component sets with design system baked in.

| Library | Design System | Customization | Best For |
|---------|---------------|---------------|----------|
| MUI | Material Design | Moderate | Consumer apps, dashboards |
| Ant Design | Enterprise | Limited | Admin panels, data apps |
| Chakra UI | Minimalist | Excellent | Custom branded apps |

### 2. Headless/Unstyled Primitives
Accessibility and behavior only - you add styles.

| Library | Maintainer | Framework | Use Case |
|---------|------------|-----------|----------|
| Radix UI | WorkOS | React | Building design systems |
| Headless UI | Tailwind Labs | React, Vue | Tailwind projects |

### 3. Copy-Paste Model
Components you own (copied into your codebase).

| Library | Foundation | Styling | Ownership |
|---------|------------|---------|-----------|
| shadcn/ui | Radix UI | Tailwind | Full code ownership |

### 4. Full-Featured Modern
Rich ecosystem with components + hooks.

| Library | Components | Hooks | Strength |
|---------|------------|-------|----------|
| Mantine | 120+ | 70+ | Best balance of features + DX |

## Decision Tree

```
Are you using Tailwind CSS?
├── Yes
│   ├── Want pre-built components? → shadcn/ui
│   └── Building from scratch? → Headless UI or Radix UI
└── No
    ├── Need Material Design look? → MUI
    ├── Building admin/data dashboard? → Ant Design
    ├── Want prop-based styling? → Chakra UI
    └── Want modern full-featured? → Mantine
```

## Quick Comparison

| Aspect | shadcn/ui | MUI | Ant Design | Chakra | Mantine | Radix |
|--------|-----------|-----|------------|--------|---------|-------|
| Stars | 85K | 95K | 94K | 39K | 28K | 17K |
| Styling | Tailwind | CSS-in-JS | Less/CSS | Props | CSS-in-JS | None |
| Bundle | 0 (copy) | Large | Large | Medium | Medium | Small |
| Customization | Full | Moderate | Limited | Excellent | High | Full |
| Learning Curve | Low | Medium | Medium | Low | Low | Medium |
| Accessibility | Excellent | Good | Good | Excellent | Excellent | Excellent |

## 2025 Trends

1. **shadcn/ui dominance**: Copy-paste model wins - developers want code ownership
2. **Headless foundation**: Radix powers shadcn/ui, others build on primitives
3. **Tailwind integration**: Most new libraries assume Tailwind
4. **Accessibility first**: All major libraries now WAI-ARIA compliant
5. **Smaller bundles**: Tree-shaking, modular imports standard

## Sources

- [React UI Libraries 2025 - Makers Den](https://makersden.io/blog/react-ui-libs-2025-comparing-shadcn-radix-mantine-mui-chakra)
- [Best React UI Component Libraries - Croct](https://blog.croct.com/post/best-react-ui-component-libraries)
- [Radix Primitives](https://www.radix-ui.com/primitives)
- [Headless UI](https://headlessui.com/)
- [Mantine](https://mantine.dev/)
