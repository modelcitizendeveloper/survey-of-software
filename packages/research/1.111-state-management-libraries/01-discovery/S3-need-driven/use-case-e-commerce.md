# Use Case: E-Commerce (Shopping Cart + Checkout)

**Last Updated**: 2026-01-16
**Complexity**: Medium
**Target**: Online stores, marketplace apps

## Scenario

E-commerce app with:
- Product catalog (100-1000 items)
- Shopping cart (add/remove/update quantity)
- Checkout flow (multi-step)
- Inventory sync (real-time stock updates)
- Price calculations (subtotal, tax, shipping)
- Payment processing integration
- Order history

## Top Recommendations

### 1. Zustand (Best Overall)

```typescript
interface CartStore {
  items: CartItem[]
  addItem: (product) => void
  updateQuantity: (id, qty) => void
  removeItem: (id) => void
  clearCart: () => void
  total: number
  checkout: () => Promise<void>
}

const useCartStore = create<CartStore>((set, get) => ({
  items: [],

  addItem: (product) => set((state) => {
    const existing = state.items.find(i => i.id === product.id)
    if (existing) {
      return {
        items: state.items.map(i =>
          i.id === product.id ? { ...i, quantity: i.quantity + 1 } : i
        )
      }
    }
    return { items: [...state.items, { ...product, quantity: 1 }] }
  }),

  updateQuantity: (id, qty) => set((state) => ({
    items: qty > 0
      ? state.items.map(i => i.id === id ? { ...i, quantity: qty } : i)
      : state.items.filter(i => i.id !== id)
  })),

  get total() {
    return get().items.reduce((sum, item) => sum + item.price * item.quantity, 0)
  },

  checkout: async () => {
    const items = get().items
    const response = await fetch('/api/checkout', {
      method: 'POST',
      body: JSON.stringify({ items })
    })
    if (response.ok) {
      set({ items: [] })
    }
  },
}))
```

**Pros**: Simple, efficient, good for transactional flows
**Bundle**: 3KB

### 2. Redux Toolkit (Enterprise with Audit)

Use if need:
- Audit trail (all add-to-cart actions logged)
- Complex inventory sync
- Multiple payment integrations
- Regulatory compliance (order tracking)

**Bundle**: 33KB (but includes RTK Query for API calls)

## Recommendation

**Primary: Zustand**

- Simple cart operations
- Persistent middleware for cart recovery
- Easy checkout integration

**Use Redux Toolkit if**: Enterprise with audit/compliance needs

**Last Updated**: 2026-01-16
