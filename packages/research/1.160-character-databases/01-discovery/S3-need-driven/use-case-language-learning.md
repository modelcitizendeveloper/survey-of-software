# Use Case: Language Learning Application

## Context

**Application:** Chinese character learning app (e.g., Duolingo, HelloChinese)

**User scenario:**
- Student learns 漢 (Han, Chinese)
- App shows: Etymology (water + 堇), historical forms (oracle bone → modern), mnemonic (water people = Chinese)
- Student retains character better (visual + semantic understanding)

**Educational requirements:**
- Rich explanations (not just glosses)
- Visual mnemonics (component meanings)
- Historical context (character evolution)

## Requirements

### Must-Have (P0)

- **[P0-1] Etymology:** Historical forms (oracle bone, bronze, seal → modern)
  - Critical for advanced learners
  - Builds cultural understanding

- **[P0-2] Component semantics:** What do 氵 and 堇 mean in 漢?
  -氵= water (semantic radical)
  - 堇 = (phonetic component, also means violet plant)

- **[P0-3] Visual decomposition:** Show character structure clearly
  - Hierarchical breakdown
  - Stroke order guidance (if available)

### Nice-to-Have (P1)

- **[P1-1] Semantic relationships:** Find related characters
  - "Characters about water": 江, 河, 海, 湖, ...
  - Thematic learning

- **[P1-2] Multiple pronunciations:** Context-dependent readings

### Constraints

- **Latency:** <500ms (offline use acceptable, not real-time)
- **Coverage:** 3,000 common characters (HSK 1-6 vocabulary)
- **Quality:** Accuracy > speed (education-critical)

## Database Fit Analysis

| Database | P0-1 (Etymology) | P0-2 (Semantics) | P0-3 (Structure) | Fit Score |
|----------|----------------|-----------------|-----------------|-----------|
| **Unihan** | ❌ | ❌ (Glosses only) | ⚠️ (kIDS field) | 30% |
| **CHISE** | ✅ (Extensive) | ✅ (Ontology) | ✅ (Full tree) | 95% |
| **IDS** | ❌ | ❌ | ✅ (Standard) | 40% |
| **CJKVI** | ❌ | ❌ | ❌ | 0% |

## Recommended Stack

**Optimal:** Unihan + CHISE + IDS

**Rationale:**
- CHISE provides etymology (P0-1) and semantic ontology (P0-2, P1-1)
- IDS adds standard structural notation
- Unihan covers pronunciation, stroke count, basic properties
- Performance acceptable (100-200ms queries OK for learning context)

**Mitigation for CHISE complexity:**
- Extract etymology/semantics to JSON (one-time export)
- Pre-compute common character explanations
- Avoid runtime RDF queries (bundle pre-rendered content)

**Real-World:** Skritter, Pleco use CHISE-derived data
- Pleco: Licensed etymology content (CHISE-based)
- Skritter: Visual mnemonics from component semantics
- Performance: 200-500ms initial load, then cached

**Must include:** CHISE (irreplaceable for etymology)
**Optional:** Full CHISE RDF (extract subsets instead)

## Confidence: 85%** - CHISE essential but complexity manageable via extraction
