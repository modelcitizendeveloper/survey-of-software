# Latin Noun Declension Pedagogy

## Framework

Latin nouns have 3 defining dimensions:
- **Declension**: 5 types (1st, 2nd, 3rd, 4th, 5th)
- **Case**: 6 types (nominative, genitive, dative, accusative, ablative, vocative)
- **Number**: 2 types (singular, plural)

**Total combinations**: 5 × 6 × 2 = **60 forms**

## Learning Strategy

### Phase 1: Lock 2 dimensions, drill the 3rd (Foundation)

**1.1 Lock DECLENSION (drill case × number)** - 12 forms each
- 01-single_declension_1st.jsonl ✅
- 02-single_declension_2nd.jsonl ✅
- 03-single_declension_3rd.jsonl ✅
- 04-single_declension_4th.jsonl ✅
- 05-single_declension_5th.jsonl ✅

**1.2 Lock NUMBER (drill declension × case)** - 30 forms each
- 06-single_number_singular.jsonl ✅
- 07-single_number_plural.jsonl ✅

**1.3 Lock CASE (drill declension × number)** - 10 forms each
- ❌ single_case_nominative.jsonl (need to create)
- ❌ single_case_genitive.jsonl (need to create)
- ❌ single_case_dative.jsonl (need to create)
- ❌ single_case_accusative.jsonl (need to create)
- ❌ single_case_ablative.jsonl (need to create)
- ❌ single_case_vocative.jsonl (need to create)

### Phase 2: Lock 1 dimension, drill the other 2 (Intermediate)

Could create exercises that lock only ONE dimension:
- Lock declension: drill all case×number (12 forms) - **Already covered in 1.1**
- Lock number: drill all declension×case (30 forms) - **Already covered in 1.2**
- Lock case: drill all declension×number (10 forms) - **Need to create in 1.3**

### Phase 3: Integration (Advanced)

- 08-model_nouns_1st_to_5th.jsonl ✅ - All dimensions mixed
- 09-ambiguous_forms_drill.jsonl ✅ - Edge cases where same form has multiple valid interpretations

## Ambiguous Forms

Many forms are identical across different cases/numbers. These must be marked with arrays:

### Always ambiguous:
- **Dative/Ablative plural**: Identical in ALL declensions
- **Nominative/Accusative plural**: Identical in 3rd, 4th, 5th declensions
- **Vocative**: Identical to nominative except 2nd declension singular (-us → -e)

### Declension-specific:
- **1st declension**: genitive/dative singular (-ae), all plurals
- **2nd declension**: dative/ablative singular (-ō), all plurals
- **5th declension**: genitive/dative singular (-eī or -ī)

## Vocative Case

Vocative is used for direct address ("O Marcus!"). Rules:
- **Identical to nominative** in most cases
- **Exception**: 2nd declension singular masculine -us → -e
  - ventus → vente ("O wind!")
  - Marcus → Marce ("O Marcus!")
- **Exception**: 2nd declension singular -ius → -ī
  - fīlius → fīlī ("O son!")

## Current Status

### Completed ✅
- All 5 single-declension drills (phase 1.1)
- Both single-number drills (phase 1.2)
- Model nouns integration drill (phase 3)
- Ambiguous forms drill (phase 3)

### Missing ❌
- All 6 single-case drills (phase 1.3)
- Vocative case coverage (in all drills)
- Proper ambiguous form marking (many files still need arrays)

### Broken 🔧
- single_case_nominative.jsonl - misnamed, tests ALL cases not just nominative

## Next Steps

1. **Delete** current single_case_nominative.jsonl (misnamed)
2. **Create** 6 proper single-case drill files
3. **Add vocative** to all existing drills
4. **Fix ambiguous forms** throughout (add array notation)
5. **Reorder** exercises in launcher with new pedagogical sequence
