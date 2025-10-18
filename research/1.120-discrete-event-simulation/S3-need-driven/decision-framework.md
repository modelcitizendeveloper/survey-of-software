# Decision Framework: Library Selection Criteria

## Tier 1: Paradigm Match

**Q1: Agent-based or process-based?**

Agent-based (autonomous entities, spatial environment, emergence):
→ **Mesa** (HIGH confidence)

Process-based (entities following defined processes):
→ Continue to Q2

---

## Tier 2: Specialization

**Q2: Is your system primarily a queueing network?**

Yes (queue-server structures, routing, call centers):
→ **Ciw** (HIGH confidence)

No (general processes, complex routing, non-queue logic):
→ Continue to Q3

---

## Tier 3: Usability Needs

**Q3: Do you need built-in animation?**

Yes (stakeholder demos, presentations, education):
→ **salabim** (HIGH confidence - unique feature)

No (analysis-focused, static plots sufficient):
→ Continue to Q4

---

## Tier 4: Scale and Architecture

**Q4: Is your system large-scale and modular?**

Yes (100+ components, hierarchical structure, long-term maintenance):
→ **desmod** (MEDIUM confidence - corporate backing)

No (simple/moderate complexity):
→ Continue to Q5

---

## Tier 5: API Preference

**Q5: Python generator experience?**

Unfamiliar (prefer yieldless API):
→ **salabim** (MEDIUM confidence - smaller community)

Comfortable (want largest ecosystem):
→ **SimPy** (HIGH confidence - industry standard)

---

## Multi-Criteria Scoring Matrix

If decision tree doesn't resolve choice, score each criterion:

| Criterion | Weight | SimPy | salabim | Ciw | Mesa | desmod |
|-----------|--------|-------|---------|-----|------|--------|
| **Maturity** | 20% | 10 | 7 | 7 | 8 | 7 |
| **Documentation** | 20% | 10 | 8 | 7 | 9 | 7 |
| **Community** | 15% | 10 | 5 | 5 | 8 | 4 |
| **Ease of use** | 15% | 7 | 9 | 8 | 6 | 5 |
| **Features** | 15% | 7 | 9 | 6 | 8 | 7 |
| **Performance** | 10% | 8 | 8 | 8 | 6 | 8 |
| **Extensibility** | 5% | 10 | 7 | 6 | 7 | 9 |

**Note**: Scores are research-based estimates, not benchmarks.

---

## Risk Assessment

### Low-Risk Choices:
- **SimPy** (most mature, largest community)
- **Mesa** (if ABM is clear requirement)

### Medium-Risk Choices:
- **salabim** (smaller community, but active development)
- **Ciw** (narrow scope, but well-documented)

### Higher-Risk Choices:
- **desmod** (smallest community, corporate dependency)

---

## Migration Paths

**If you outgrow a library**:

- **Ciw → SimPy**: Rebuild using SimPy's Resource (more flexibility)
- **salabim → SimPy**: Port processes to generator functions
- **SimPy → desmod**: Refactor into component hierarchy

---

## Summary Decision

**Default**: SimPy (80% of use cases)
**Specialized**: Ciw (queues), Mesa (ABM), salabim (animation), desmod (large models)

**Confidence levels based on research evidence**:
- SimPy, Mesa, Ciw: HIGH
- salabim, desmod: MEDIUM (smaller communities, but viable)

See S1-rapid/recommendation.md for detailed guidance and S2-comprehensive/* for technical deep-dives.
