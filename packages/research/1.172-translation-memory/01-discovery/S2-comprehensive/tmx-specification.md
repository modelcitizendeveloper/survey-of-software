# TMX 1.4b Specification: Technical Deep Dive

## Standard Status

**Current Version:** TMX 1.4b (2005)
**Status:** Active, widely adopted, no planned updates
**Specification:** https://www.ttt.org/oscarStandards/tmx/tmx14b.html
**ISO Status:** Specification 1.4b remained current as of 2020

## XML Document Structure

### Root Element Hierarchy

```xml
<tmx version="1.4">
  <header>
    <!-- Metadata about the translation memory -->
  </header>
  <body>
    <!-- Collection of translation units -->
  </body>
</tmx>
```

### The `<header>` Element

Contains metadata about the TM document:

```xml
<header
  creationtool="ToolName"
  creationtoolversion="1.0"
  datatype="plaintext"
  segtype="sentence"
  adminlang="en-US"
  srclang="en-US"
  o-tmf="OmegaT TMX"
  creationdate="20260129T120000Z"
  creationid="user@example.com"
  changedate="20260129T150000Z"
  changeid="reviewer@example.com">
  <note>Optional description of the TM</note>
  <prop type="custom-property">Custom metadata</prop>
</header>
```

**Key Attributes:**
- **creationtool** (required): Tool that created the TMX
- **creationtoolversion** (required): Tool version
- **datatype** (required): Content type (plaintext, html, xml, etc.)
- **segtype** (required): Segmentation type (sentence, paragraph, block, phrase)
- **adminlang** (required): Administrative language (for notes/properties)
- **srclang** (required): Source language code (BCP 47 format)
- **o-tmf** (optional): Original TM format (proprietary format identifier)

**Child Elements:**
- **`<note>`**: Human-readable description
- **`<prop>`**: Custom properties (key-value pairs)

### The `<body>` Element

Container for all translation units:

```xml
<body>
  <tu tuid="12345" creationdate="20260129T120000Z" creationid="translator1">
    <prop type="domain">technical</prop>
    <tuv xml:lang="en-US">
      <seg>Source segment text</seg>
    </tuv>
    <tuv xml:lang="fr-FR">
      <seg>Texte du segment traduit</seg>
    </tuv>
    <tuv xml:lang="de-DE">
      <seg>Übersetzter Segmenttext</seg>
    </tuv>
  </tu>
</body>
```

**Translation Unit (`<tu>`) Attributes:**
- **tuid**: Unique identifier for the translation unit (optional but recommended)
- **creationdate**: When TU was created
- **creationid**: Who created it
- **changedate**: Last modification date
- **changeid**: Who last modified it
- **usagecount**: How many times TU has been reused
- **lastusagedate**: When TU was last used

**Translation Unit Variant (`<tuv>`) Attributes:**
- **xml:lang** (required): Language code (BCP 47 format, e.g., en-US, zh-CN, pt-BR)
- **creationdate**: When this variant was created
- **creationid**: Who created it
- **changedate**: Last modification date
- **changeid**: Who modified it

**Segment (`<seg>`) Element:**
- Contains the actual translated text
- May include inline codes for formatting (Level 2 compliance)

## Compliance Levels

TMX defines three compliance levels for content markup:

### Level 1: Plain Text Only

**Requirements:**
- Support for `<tmx>`, `<header>`, `<body>`, `<tu>`, `<tuv>`, `<seg>` elements
- **Content:** Plain text only inside `<seg>` elements
- **No inline codes** for formatting

**Use Cases:**
- Software UI strings
- Simple messages
- Content without formatting requirements

**Example:**
```xml
<seg>Click the button to continue.</seg>
```

**Advantages:**
- Maximum compatibility
- Simplest to implement
- No formatting information to lose

### Level 2: Inline Formatting

**Requirements:**
- All Level 1 requirements
- Support for inline codes within `<seg>` elements
- Preserves formatting (bold, italic, links, etc.)

**Use Cases:**
- Documentation with formatting
- Marketing materials
- Help files
- Web content

**Example:**
```xml
<seg>Click the <bpt i="1">&lt;b&gt;</bpt>Submit<ept i="1">&lt;/b&gt;</ept> button.</seg>
```

**Inline Elements:**
- `<bpt>`: Beginning Paired Tag (e.g., opening `<b>`)
- `<ept>`: Ending Paired Tag (e.g., closing `</b>`)
- `<it>`: Isolated Tag (e.g., `<br/>`)
- `<ph>`: Placeholder (e.g., variable)
- `<hi>`: Highlight (text with special formatting)
- `<ut>`: User-defined Tag

### Level 3: Extended Attributes

**Requirements:**
- All Level 2 requirements
- Additional metadata and context information
- Extended attributes on elements

**Note:** Level 3 is rarely used in practice; most tools use Level 1 or Level 2.

## Compliance Testing

TMX provides a **Compliance Kit** that includes:
- **TMXCheck**: Validation tool for TMX files
- **Test files**: Sample TMX documents for each level
- **Process documentation**: Detailed compliance testing procedures

## Language Codes

TMX uses **BCP 47** (IETF language tags) for language identification:

**Examples:**
- `en` - English (generic)
- `en-US` - English (United States)
- `en-GB` - English (United Kingdom)
- `fr` - French (generic)
- `fr-FR` - French (France)
- `fr-CA` - French (Canada)
- `zh-CN` - Chinese (China, Simplified)
- `zh-TW` - Chinese (Taiwan, Traditional)
- `pt-BR` - Portuguese (Brazil)
- `pt-PT` - Portuguese (Portugal)

**Best Practice:** Use specific locale codes (en-US, not just en) for better context matching.

## Datatype Attribute Values

The `datatype` attribute indicates the original content format:

**Recommended Values:**
- **plaintext**: Plain text files
- **html**: HTML documents
- **xml**: XML documents
- **sgml**: SGML documents
- **rtf**: Rich Text Format
- **winres**: Windows resources
- **po**: gettext PO files
- **java**: Java properties files
- **csharp**: C# resources

## Best Practices

### 1. Always Include Metadata
- Set `creationtool`, `creationtoolversion`, `datatype`, `segtype`
- Include `tuid` for translation units (enables tracking)
- Use `usagecount` and `lastusagedate` for quality metrics

### 2. Use Specific Language Codes
- Prefer `en-US` over `en` for better context matching
- Regional variants matter (fr-FR vs. fr-CA, es-ES vs. es-MX)

### 3. Export Multiple Levels
- Generate Level 1 for maximum compatibility
- Generate Level 2 for formatting preservation
- Some tools (like OmegaT) automatically export all levels

### 4. Validate Before Sharing
- Use TMXCheck or XML validators
- Ensure well-formed XML
- Test import in target tool before client delivery

### 5. Context Matters
- Include adjacent segments where possible (for context matching)
- Use `<prop>` elements for domain/subject metadata
- Consider using `tuid` that references source document structure

## Common Issues and Solutions

**Problem:** Different tools export incompatible TMX files
**Solution:** Stick to Level 1 for interchange; use Level 2 only when formatting is critical

**Problem:** Language code mismatches (en vs. en-US)
**Solution:** Standardize on specific locale codes in your organization

**Problem:** Large TMX files are slow to parse
**Solution:** Split large TMs by domain, project, or year; use incremental updates

**Problem:** Encoding issues with special characters
**Solution:** Always use UTF-8 encoding; specify `encoding="UTF-8"` in XML declaration

## Sources

- [TMX 1.4b Specification](https://www.ttt.org/oscarStandards/tmx/tmx14b.html)
- [TMX Format Specifications - The XML Cover Pages](https://xml.coverpages.org/tmxSpec971212.html)
- [Translation Memory eXchange - Wikipedia](https://en.wikipedia.org/wiki/Translation_Memory_eXchange)
- [Maxprograms - XML in localisation: Reuse translations with TM and TMX](https://www.maxprograms.com/articles/tmx.html)
- [TMX - Okapi Framework](https://okapiframework.org/wiki/index.php/TMX)
