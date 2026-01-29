# S3 Need-Driven: Generic Use Case Patterns

**Status**: Discovery research (no code execution)
**Created**: 2026-01-28
**Purpose**: Generic use case patterns for character decomposition (NOT application-specific)

---

## Pattern Philosophy

Per DISCOVERY_VS_IMPLEMENTATION.md guidance:
- ✅ Generic patterns applicable to any developer
- ✅ Technology-neutral descriptions
- ❌ NO application-specific requirements ("for our app...")
- ❌ NO implementation plans ("install and test...")

---

## Pattern 1: Character Decomposition Lookup

**Generic Need**: Given a Chinese character, retrieve its structural components

**Input**: Single character (e.g., 花)
**Output**: Structural decomposition with spatial relationship

**Data Requirements**:
- IDS sequence (⿱艹化)
- Component list ([艹, 化])
- Spatial operator (top-bottom arrangement)

**Example Variations**:
- Flat decomposition: 花 → [艹, 化]
- Hierarchical decomposition: 花 → [艹, [亻, 匕]] (recursive)
- IDS string representation: "⿱艹化"

**Data Sources**:
- Primary: CJKVI-IDS `ids.txt`
- Fallback: cjklib database, makemeahanzi JSON

**Complexity Considerations**:
- Single valid decomposition vs. multiple valid partitions
- Unencoded components (exist only within larger characters)
- Variant forms (simplified vs. traditional differences)

**Generic Use Cases**:
- Dictionary lookup enhancement (show components)
- Educational tools (character structure visualization)
- Font rendering (construct missing glyphs)
- Mnemonic generation (break into memorable parts)

---

## Pattern 2: Radical-Based Character Search

**Generic Need**: Find all characters containing a specific radical

**Input**: Radical (e.g., 土 "earth")
**Output**: List of characters containing that radical

**Data Requirements**:
- Radical-to-character index
- Optional: stroke count for sub-filtering
- Optional: character frequency for sorting

**Example Queries**:
- All characters with radical 土: [地, 坐, 场, 城, ...]
- Characters with 土 + 5 total strokes: [地, 圾, ...]
- Top 100 most frequent characters with 土: sorted by usage

**Data Sources**:
- Primary: Unihan `kRSUnicode` field
- Enhancement: Character frequency data (Unihan `kFrequency` or external corpus)
- Alternative: Reverse index from CJKVI-IDS (parse components)

**Radical System Considerations**:
- Kangxi radicals (214) vs. Simplified radicals (189)
- Radical variants (讠 vs. 言)
- Unicode radical characters vs. component characters

**Generic Use Cases**:
- Dictionary browsing (traditional radical index navigation)
- Character learning (study characters by semantic category)
- Input method optimization (radical-based typing)
- Corpus analysis (semantic field distribution)

---

## Pattern 3: Phonetic Series Identification

**Generic Need**: Find characters sharing the same phonetic component

**Input**: Phonetic component (e.g., 青 "qing")
**Output**: List of characters using that phonetic component with readings

**Data Requirements**:
- Phonetic-semantic compound classification
- Phonetic component extraction
- Pronunciation data for validation

**Example Queries**:
- Characters with phonetic 青: [清 qīng, 情 qíng, 请 qǐng, 晴 qíng, ...]
- Show semantic radical for each: [清(氵), 情(忄), 请(讠), 晴(日)]
- Pronunciation similarity analysis: all share "qing" pronunciation

**Data Sources**:
- Primary: makemeahanzi etymology fields (phonetic/semantic)
- Research: Hsiao & Shillcock phonetic compound database
- Validation: Unihan `kPhonetic` field + pronunciation data

**Pattern Insights**:
- ~80% of Chinese characters are phonetic-semantic compounds
- Phonetic component often indicates pronunciation (not always exact)
- Same phonetic in different semantic contexts = different meanings

**Generic Use Cases**:
- Mnemonic generation (learn pronunciation from phonetic)
- Character learning (phonetic family grouping)
- Historical linguistics (phonetic evolution study)
- OCR validation (phonetic similarity for error correction)

---

## Pattern 4: Etymology Tree Generation

**Generic Need**: Trace a character's historical development and component relationships

**Input**: Target character (e.g., 森)
**Output**: Etymology tree showing component hierarchy

**Decomposition Levels**:
1. **Level 0**: Target character (森)
2. **Level 1**: Direct components (木 + 木 + 木)
3. **Level 2**: Component components (if applicable)
4. **Level N**: Minimal strokes or radicals

**Data Requirements**:
- Recursive IDS parsing
- Etymology type classification (pictographic/ideographic/pictophonetic)
- Historical form variants (oracle bone → seal script → modern)

**Example Tree** (simplified):
```
森 (forest)
├─ 木 (tree) [pictographic]
├─ 木 (tree) [pictographic]
└─ 木 (tree) [pictographic]
└─ Etymology type: ideographic compound (multiple trees = forest)
```

**Example Tree** (compound):
```
想 (think)
├─ 相 (mutual/appearance) [phonetic component]
│   ├─ 木 (tree) [radical]
│   └─ 目 (eye) [component]
└─ 心 (heart) [semantic radical]
└─ Etymology type: phonetic-semantic (heart + appearance → thinking)
```

**Data Sources**:
- Structure: CJKVI-IDS (recursive parsing)
- Etymology type: makemeahanzi `etymology.type` field
- Historical forms: Specialized databases (Shuowen Jiezi, oracle bone scripts)

**Termination Conditions**:
- Reach minimal stroke components (一, 丨, etc.)
- Reach pictographic radicals (no further decomposition)
- Reach unencoded component (no Unicode codepoint)

**Generic Use Cases**:
- Educational tools (visualize character structure)
- Mnemonic storytelling (understand meaning from components)
- Historical linguistics research (trace character evolution)
- Character learning curriculum (teach simple before complex)

---

## Pattern 5: Mnemonic Component Extraction

**Generic Need**: Extract semantically meaningful components for memory aids

**Input**: Character + desired mnemonic style
**Output**: Components with semantic hints

**Mnemonic Types**:
1. **Semantic decomposition**: 好 = 女 (woman) + 子 (child) → "woman with child = good"
2. **Phonetic hint**: 清 = 氵(water) + 青 (qing) → "water that sounds like 'qing'"
3. **Pictographic story**: 森 = 木+木+木 → "many trees = forest"

**Component Filtering**:
- Prioritize semantically meaningful components (radicals)
- De-emphasize phonetic components for semantic mnemonics
- Identify pictographic components for visual mnemonics

**Data Requirements**:
- IDS decomposition (structure)
- Etymology type (phonetic vs. semantic vs. pictographic)
- Radical semantic category (Kangxi radical meanings)
- Component meanings (individual character definitions)

**Example Processing**:
```
Character: 想 (think)
├─ Decomposition: ⿱相心
├─ Components: [相, 心]
├─ Etymology: phonetic-semantic
├─ Semantic radical: 心 (heart)
├─ Phonetic component: 相 (xiāng → xiǎng)
└─ Mnemonic: "Thinking (xiǎng) comes from the heart (心), using mutual (相) understanding"
```

**Data Sources**:
- Structure: CJKVI-IDS
- Etymology: makemeahanzi
- Radical meanings: Kangxi radical semantic categories
- Component definitions: Dictionary database (CEDICT, CC-CEDICT)

**Generic Use Cases**:
- Flashcard apps (auto-generate memory aids)
- Character learning books (etymology explanations)
- Educational games (story-based character teaching)
- Spaced repetition systems (memorable hints)

---

## Pattern 6: Learning Progression Sequencing

**Generic Need**: Order characters from simple to complex for curriculum design

**Input**: Set of characters to learn
**Output**: Ordered sequence from simple components to complex compounds

**Complexity Metrics**:
1. **Stroke count**: Fewer strokes = simpler
2. **Component count**: Fewer components = simpler
3. **Decomposition depth**: Shallow hierarchy = simpler
4. **Component frequency**: Common components taught first

**Sequencing Algorithm** (generic pseudo-logic):
```
1. Identify all unique components across character set
2. Build dependency graph (character depends on its components)
3. Topological sort: teach components before compounds
4. Within same level, sort by stroke count (ascending)
5. Within same stroke count, sort by frequency (descending)
```

**Example Sequence**:
```
Level 0 (Radicals/Simple):
  一 (1 stroke) → 二 (2) → 三 (3) → 十 (2) → 人 (2) → 木 (4) → 水 (4)

Level 1 (Simple Compounds):
  好 (女+子, 6 strokes) → 休 (人+木, 6) → 林 (木+木, 8)

Level 2 (Complex Compounds):
  森 (木+木+木, 12) → 想 (相+心, 13)
```

**Data Requirements**:
- IDS decomposition (dependency graph)
- Stroke count data (Unihan `kTotalStrokes`)
- Character frequency (Unihan `kFrequency` or corpus data)
- Component reusability (how many characters use this component)

**Data Sources**:
- Structure: CJKVI-IDS
- Stroke count: Unihan `kTotalStrokes` or `ucs-strokes.txt`
- Frequency: Unihan `kFrequency`, SUBTLEX-CH, or web corpus
- HSK/TOCFL levels (for educational sequencing)

**Generic Use Cases**:
- Textbook curriculum design (character introduction order)
- Adaptive learning systems (personalized progression)
- Character workbook generation (practice sheets)
- Font subset optimization (include components first)

---

## Pattern 7: Character Similarity Analysis

**Generic Need**: Find characters with similar structure or components

**Input**: Query character
**Output**: Ranked list of structurally similar characters

**Similarity Dimensions**:
1. **Component overlap**: Share N components
2. **Structural similarity**: Same IDS operators (both ⿰ left-right)
3. **Radical similarity**: Same Kangxi radical
4. **Phonetic similarity**: Share phonetic component
5. **Visual similarity**: OCR confusion pairs

**Example Queries**:
- Characters structurally similar to 清: [请, 晴, 情] (all ⿰X青)
- Characters with same radical as 清: [河, 海, 泪] (all 氵)
- Characters visually similar to 大: [太, 犬, 天] (OCR confusion)

**Similarity Scoring** (generic approach):
```
Jaccard similarity: intersection(components) / union(components)
Structural similarity: same IDS operator = +1 point
Radical match: same Kangxi radical = +2 points
Phonetic match: same phonetic component = +1 point
```

**Data Requirements**:
- IDS decomposition (component extraction)
- Radical classification (Kangxi radical)
- Phonetic-semantic classification
- Optional: Stroke-level similarity (for OCR)

**Data Sources**:
- Structure: CJKVI-IDS
- Radicals: Unihan `kRSUnicode`
- Phonetics: makemeahanzi etymology
- Visual confusion: OCR error datasets (research papers)

**Generic Use Cases**:
- OCR post-processing (similar character suggestions)
- Character learning (study confusable pairs)
- Dictionary features (related characters navigation)
- Text correction (typo detection)

---

## Pattern 8: Component Reusability Analysis

**Generic Need**: Identify high-value components (used in many characters)

**Input**: Character database
**Output**: Components ranked by reusability

**Reusability Metrics**:
1. **Character count**: How many characters contain this component
2. **Frequency-weighted**: Weighted by character usage frequency
3. **Pedagogical value**: Appears in HSK 1-6 vocabulary

**Example High-Reusability Components**:
```
口 (mouth): appears in 1000+ characters
  - 吃, 喝, 叫, 唱, 吗, 呢, 哪, 呀, ...
  - High pedagogical value (early HSK levels)

氵(water radical): appears in 800+ characters
  - 水, 河, 海, 洋, 湖, 江, 清, 洗, ...
  - Semantic category: water-related meanings
```

**Analysis Output**:
- Top 100 most reusable components (by character count)
- Components by semantic category (214 Kangxi radicals)
- Components by pedagogical level (HSK 1-6 coverage)

**Data Requirements**:
- Component extraction from all characters
- Character frequency data (usage weighting)
- HSK/TOCFL level data (pedagogical value)

**Data Sources**:
- Components: CJKVI-IDS (parse all IDS)
- Frequency: Web corpus or Unihan `kFrequency`
- HSK levels: HSK vocabulary lists (external)

**Generic Use Cases**:
- Curriculum design (teach high-value components first)
- Font subsetting (prioritize reusable components)
- Input method optimization (frequent component shortcuts)
- Mnemonic generation (focus on common building blocks)

---

## Pattern 9: Traditional ↔ Simplified Mapping

**Generic Need**: Map between traditional and simplified character forms

**Input**: Character (traditional or simplified)
**Output**: Corresponding form(s) in other system

**Complexity Cases**:
1. **One-to-one**: 花 (same in both) → 花
2. **One-to-many**: 發 (trad) → 发 or 髮 (simp, context-dependent)
3. **Many-to-one**: 發/髮 (trad) → 发 (simp, merged)
4. **Component differences**: 國 → 国 (玉 → 王 inside 口)

**Decomposition Impact**:
- Traditional: 國 → ⿴囗或 (囗 + 或)
- Simplified: 国 → ⿴囗玉 (囗 + 玉)
- Component change affects mnemonic/etymology

**Data Requirements**:
- Traditional/simplified variant mappings
- IDS for both forms (structural differences)
- Context rules (for one-to-many mappings)

**Data Sources**:
- Variants: Unihan `kSimplifiedVariant`, `kTraditionalVariant`
- Structure: CJKVI-IDS (includes both forms)
- Context: HanDeDict or CC-CEDICT (word-level distinctions)

**Generic Use Cases**:
- Text conversion (traditional ↔ simplified)
- Dictionary lookup (show both forms)
- Cross-Strait content (Taiwan vs. Mainland)
- Character learning (understand simplification rules)

---

## Pattern 10: Stroke Order & Decomposition Alignment

**Generic Need**: Align component decomposition with stroke writing order

**Input**: Character
**Output**: Components ordered by stroke sequence

**Challenge**: IDS decomposition ≠ stroke order
- IDS: 想 = ⿱相心 (top 相, bottom 心)
- Stroke order: Write partial 木, then 目, then 心, then finish 木

**Alignment Strategy**:
1. Parse IDS decomposition (structural)
2. Parse stroke order sequence (temporal)
3. Map strokes to components (spatial)
4. Reorder components by first stroke

**Data Requirements**:
- IDS decomposition (spatial structure)
- Stroke order sequences (temporal order)
- Stroke-to-component mapping

**Data Sources**:
- IDS: CJKVI-IDS
- Stroke order: makemeahanzi `strokes` array
- Graphics: SVG stroke paths (for visualization)

**Generic Use Cases**:
- Handwriting teaching apps (component-aware practice)
- Stroke order animations (show components correctly)
- Calligraphy tools (component-based guidance)
- Character tracing worksheets (pedagogical materials)

---

## Cross-Pattern Dependencies

**Foundation Patterns** (required by others):
1. Character Decomposition Lookup (Pattern 1)
   - Used by: Etymology Tree (4), Mnemonic Extraction (5), Learning Progression (6)

**Enhancement Patterns** (add value to foundation):
2. Radical-Based Search (2) + Phonetic Series (3)
   - Enables: Comprehensive similarity analysis (7)

**Advanced Patterns** (combine multiple patterns):
6. Learning Progression = Decomposition (1) + Frequency + Stroke Count
7. Similarity Analysis = Decomposition (1) + Radical (2) + Phonetic (3)

---

## Data Source Coverage Matrix

| Pattern | CJKVI-IDS | Unihan | makemeahanzi | pypinyin | External |
|---------|-----------|--------|--------------|----------|----------|
| 1. Decomposition | ✅ Primary | 🟨 Fallback | 🟨 Fallback | ❌ | ❌ |
| 2. Radical Search | 🟨 Reverse | ✅ Primary | 🟨 Enhancement | ❌ | 🟨 Frequency |
| 3. Phonetic Series | 🟨 Structure | 🟨 kPhonetic | ✅ Primary | ✅ Validation | ❌ |
| 4. Etymology Tree | ✅ Primary | ❌ | 🟨 Type | ❌ | 🟨 Historical |
| 5. Mnemonic Extract | ✅ Structure | 🟨 Radicals | ✅ Etymology | ❌ | 🟨 Definitions |
| 6. Learning Progress | ✅ Structure | ✅ Strokes | 🟨 Data | ❌ | ✅ HSK levels |
| 7. Similarity | ✅ Primary | 🟨 Radicals | 🟨 Phonetic | ❌ | ❌ |
| 8. Reusability | ✅ Primary | 🟨 Frequency | ❌ | ❌ | 🟨 HSK |
| 9. Trad ↔ Simp | ✅ Both forms | ✅ Variants | ❌ | ❌ | 🟨 Context |
| 10. Stroke Order | 🟨 Structure | ❌ | ✅ Primary | ❌ | ❌ |

Legend:
- ✅ Primary data source (best fit)
- 🟨 Enhancement or fallback
- ❌ Not applicable

---

## Identified Data Gaps

**Gap 1**: No comprehensive phonetic-semantic database
- CJKVI-IDS: Structure only (no phonetic classification)
- makemeahanzi: Limited coverage (common chars only)
- Hsiao & Shillcock: Limited availability (academic dataset)

**Gap 2**: Traditional vs. Simplified decomposition differences
- CJKVI-IDS includes both forms BUT no explicit mapping
- Must parse both and compare programmatically

**Gap 3**: Stroke order integration
- makemeahanzi has stroke order but limited coverage
- No standard format linking stroke order to IDS decomposition

**Gap 4**: Historical forms
- Oracle bone → seal script → modern evolution
- Requires specialized databases (Shuowen Jiezi, etc.)
- Not covered by Unicode Unihan or CJKVI-IDS

---

## Next Steps for S4 (Strategic)

**Technology Evolution**:
- Unicode roadmap for CJK extensions (Ext-G, Ext-H)
- Python ecosystem health (cjklib inactive, alternatives?)
- Modern NLP integration (transformers, embeddings)

**Maintenance & Governance**:
- CJKVI-IDS: Why no releases since 2018 despite commits?
- pypinyin: Active maintenance trajectory
- Data quality assurance across multiple sources

**Variant Handling**:
- CJK unification implications (China/Taiwan/Japan/Korea/Vietnam)
- Regional glyph differences in decomposition
- Font rendering vs. semantic decomposition

---

**Sources**:
- [CJKVI-IDS GitHub](https://github.com/cjkvi/cjkvi-ids)
- [Unihan Database (UAX #38)](https://www.unicode.org/reports/tr38/)
- [makemeahanzi GitHub](https://github.com/skishore/makemeahanzi)
- [Hsiao & Shillcock (2006)](https://link.springer.com/article/10.1007/s10936-006-9022-y)
- [Hacking Chinese: Phonetic Components](https://www.hackingchinese.com/phonetic-components-part-1-the-key-to-80-of-all-chinese-characters/)
