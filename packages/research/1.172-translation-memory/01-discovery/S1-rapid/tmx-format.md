# TMX: Translation Memory eXchange Format

## What is TMX?

Translation Memory eXchange (TMX) is an XML-based standard for exchanging translation memory data between different CAT tools and localization systems with minimal data loss.

## Current Status

**Latest Version:** TMX 1.4b (released 2005)
- Remains the current specification as of 2026
- No active development of TMX 2.0 (draft released 2007, never finalized)
- Specification available at: https://www.gala-global.org/tmx-14b

## History

- **1997**: First released by OSCAR (Open Standards for Container/Content Allowing Re-use)
- **LISA Era**: Maintained by Localization Industry Standards Association
- **2007**: TMX 2.0 working draft released for public comment
- **2011**: LISA declared insolvent; standards moved under Creative Commons license
- **2005-Present**: TMX 1.4b remains the de facto standard

## Why TMX Matters

### Interoperability
- **Vendor Independence**: Switch CAT tools without losing translation assets
- **Team Collaboration**: Teams using different tools can share TM data
- **Client Handoffs**: Deliver TM to clients in a standard format
- **Archival**: Long-term storage in an open, documented format

### Universal Support
Nearly all CAT tools support TMX import/export:
- OmegaT (native format)
- MemoQ
- SDL Trados
- Wordfast
- Smartcat
- Translation management systems (TMS)

## Technical Structure

TMX files are XML documents with this basic structure:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<tmx version="1.4">
  <header
    creationtool="ToolName"
    creationtoolversion="1.0"
    datatype="plaintext"
    segtype="sentence"
    adminlang="en-US"
    srclang="en-US"
    o-tmf="OmegaT TMX"/>
  <body>
    <tu>
      <tuv xml:lang="en-US">
        <seg>Source segment text</seg>
      </tuv>
      <tuv xml:lang="fr-FR">
        <seg>Texte du segment traduit</seg>
      </tuv>
    </tu>
  </body>
</tmx>
```

### Key Elements

- **`<tmx>`**: Root element, specifies version
- **`<header>`**: Metadata about the TM (tool, language, segmentation type)
- **`<body>`**: Container for all translation units
- **`<tu>`**: Translation Unit (one source + one or more targets)
- **`<tuv>`**: Translation Unit Variant (segment in specific language)
- **`<seg>`**: The actual text segment

## TMX Levels

TMX defines compliance levels:

- **Level 1**: Plain text only (widely supported)
- **Level 2**: Preserves formatting (bold, italic, etc.) and inline codes
- **Level 3**: Includes additional metadata

Most tools export multiple TMX levels to ensure compatibility.

## Practical Use

### Export/Import Workflow
1. Translator completes work in CAT Tool A
2. Export TM to TMX format
3. Send TMX file to client or colleague
4. Import TMX into CAT Tool B
5. Translations available in new tool's TM

### Merging Translation Memories
- Combine TMs from multiple projects
- Consolidate work from different translators
- Build master TM for organization

### Quality Assurance
- TMX files are human-readable XML
- Can be validated, filtered, or cleaned with XML tools
- Scripts can detect duplicate segments or low-quality entries

## Limitations

- No active development (specification from 2005)
- Limited support for modern features:
  - Machine translation integration metadata
  - Neural MT quality scores
  - Version control information
  - Advanced context (beyond adjacent segments)
- But: Wide adoption means TMX remains the interchange lingua franca

## Sources

- [TMX – Smartling Help Center](https://help.smartling.com/hc/en-us/articles/115003184114-TMX)
- [Maxprograms - XML in localisation: Reuse translations with TM and TMX](https://www.maxprograms.com/articles/tmx.html)
- [Translation Memory eXchange - Wikipedia](https://en.wikipedia.org/wiki/Translation_Memory_eXchange)
- [Translation Memory Exchange file (.tmx) - Localizely](https://localizely.com/tmx-file/)
- [TMX Files and Format | Transifex Help Center](https://help.transifex.com/en/articles/6838724-tmx-files-and-format)
- [What is TMX - Translation Memory eXchange format | Localazy Dictionary](https://localazy.com/dictionary/tmx-translation-memory-exchange-format)
