# XLIFF: XML Localization Interchange File Format

## What is XLIFF?

XLIFF (XML Localization Interchange File Format) is an XML-based format for exchanging localizable content between tools during the localization workflow.

**Key Distinction:** While TMX is for **storing and exchanging translation memories**, XLIFF is for **exchanging documents in active translation workflows**.

## Current Status (2026)

**Latest Versions:**
- **XLIFF 2.2** became an OASIS Specification on March 13, 2025
- **XLIFF 2.1** approved as ISO standard (ISO 21720:2024) in July 2024
- **XLIFF 1.2** still widely used (many tools haven't migrated to 2.x yet)

## XLIFF vs. TMX: When to Use Which

| Aspect | XLIFF | TMX |
|--------|-------|-----|
| **Purpose** | Active translation workflow | Translation memory exchange |
| **Use Case** | Extracting/translating/merging files | Sharing completed translations |
| **Languages** | One source + one target | Multiple languages in same file |
| **File Structure** | Preserves original file structure | No structure (just segment pairs) |
| **Workflow Stage** | During translation | After translation (archival/reuse) |
| **Reassembly** | Can rebuild original file | Cannot rebuild original |

### XLIFF Use Case Example

1. Developer creates software with UI strings in JSON
2. Localization tool **extracts** translatable text → XLIFF file
3. Translator receives XLIFF, translates in CAT tool
4. Tool **merges** translations back → localized JSON file

**Why XLIFF?** Translator never sees JSON syntax, only text to translate. Original file structure preserved.

### TMX Use Case Example

1. Translator completes project in CAT tool
2. Tool **exports** translation memory → TMX file
3. Translator sends TMX to client as deliverable
4. Client **imports** TMX into their TM database
5. Future projects reuse these translations

**Why TMX?** Language asset transfer. No specific file format tied to TMX.

## XLIFF Structure (Simplified)

### XLIFF 1.2 Example

```xml
<?xml version="1.0" encoding="UTF-8"?>
<xliff version="1.2" xmlns="urn:oasis:names:tc:xliff:document:1.2">
  <file source-language="en-US" target-language="fr-FR" datatype="plaintext">
    <header>
      <tool tool-id="ExampleTool" tool-name="Example Localization Tool"/>
    </header>
    <body>
      <trans-unit id="1" resname="welcome_message">
        <source>Welcome to our application!</source>
        <target>Bienvenue dans notre application !</target>
        <note>Shown on first app launch</note>
      </trans-unit>
      <trans-unit id="2" resname="submit_button">
        <source>Submit</source>
        <target>Soumettre</target>
      </trans-unit>
    </body>
  </file>
</xliff>
```

### XLIFF 2.x Example

```xml
<?xml version="1.0" encoding="UTF-8"?>
<xliff xmlns="urn:oasis:names:tc:xliff:document:2.0" version="2.0"
       srcLang="en-US" trgLang="fr-FR">
  <file id="f1">
    <unit id="1" name="welcome_message">
      <segment>
        <source>Welcome to our application!</source>
        <target>Bienvenue dans notre application !</target>
      </segment>
    </unit>
    <unit id="2" name="submit_button">
      <segment>
        <source>Submit</source>
        <target>Soumettre</target>
      </segment>
    </unit>
  </file>
</xliff>
```

## Key Differences: XLIFF 1.2 vs. 2.x

| Feature | XLIFF 1.2 | XLIFF 2.x |
|---------|-----------|-----------|
| **Structure** | File > Body > Trans-Unit | File > Unit > Segment |
| **Adoption** | Widely supported | Growing adoption |
| **Complexity** | Simpler | More features, more complex |
| **Modules** | Monolithic | Modular (extensible) |

**Migration:** Many tools still use XLIFF 1.2 because it's battle-tested. XLIFF 2.x adoption is growing but slower than expected.

## Language Handling

**XLIFF Constraint:** One source language + one target language per file

**Multilingual Projects:** Create separate XLIFF files for each language pair:
- `strings_en-US_to_fr-FR.xliff`
- `strings_en-US_to_de-DE.xliff`
- `strings_en-US_to_ja-JP.xliff`

**TMX Advantage:** Single file can contain en-US, fr-FR, de-DE, ja-JP, etc.

## Workflow Integration

### Typical XLIFF Workflow

1. **Extraction:** Source file → XLIFF
   - JSON → XLIFF
   - DOCX → XLIFF
   - HTML → XLIFF
   - PO → XLIFF

2. **Translation:** CAT tool works with XLIFF
   - Translator never sees original file format
   - TM suggestions from previous projects (stored in TMX)
   - Glossary lookups

3. **Merge:** XLIFF → Localized file
   - Translations inserted into original structure
   - Formatting preserved
   - Output: localized JSON/DOCX/HTML/PO

### Benefits

**For Translators:**
- Consistent interface regardless of source format
- No need to learn every file format's syntax
- Focus on translation, not file manipulation

**For Developers:**
- Source files remain untouched during translation
- Automated extraction/merge (continuous localization)
- Version control friendly (XLIFF is text-based XML)

**For Project Managers:**
- Standard format for vendor handoffs
- Tool-agnostic (most CAT tools support XLIFF)
- Metadata for context, notes, deadlines

## XLIFF in Continuous Localization

Modern software development often uses **continuous localization**:

1. Developer adds new UI string to codebase
2. CI/CD pipeline **automatically extracts** XLIFF
3. XLIFF sent to translation management system (TMS)
4. Translators receive notification
5. Translations completed
6. CI/CD **automatically merges** translations
7. Localized build deployed

**XLIFF Role:** Standardized format enables tool interoperability in automated pipelines.

## Complementary Use: XLIFF + TMX

**Best Practice:** Use both formats together:

- **XLIFF:** For active translation projects (source → target)
- **TMX:** For archival and TM sharing (asset building)

**Workflow:**
1. Translate project using XLIFF files
2. Export TM to TMX after project completion
3. Next project: Import previous TMX into TM
4. Use XLIFF for new source files
5. Repeat

This approach combines the structured workflow benefits of XLIFF with the language asset management of TMX.

## Tools Supporting XLIFF

**CAT Tools:**
- OmegaT
- SDL Trados
- MemoQ
- Wordfast
- Smartcat
- Phrase (Memsource)

**Localization Platforms:**
- Crowdin
- Lokalise
- Transifex
- POEditor

**Developer Tools:**
- i18next (JavaScript i18n library)
- gettext utilities
- Android Studio (string export)
- Xcode (string export)

## Common File Formats Converted to XLIFF

- **Android XML** (strings.xml)
- **iOS Strings** (.strings files)
- **gettext PO** files
- **JSON** (i18n resource files)
- **YAML** (Ruby on Rails, etc.)
- **RESX** (.NET resources)
- **Java Properties** files
- **Microsoft Office** (DOCX, XLSX, PPTX via filters)

## Sources

- [Localization file formats - Globalization | Microsoft Learn](https://learn.microsoft.com/en-us/globalization/localization/localization-file-formats)
- [XLIFF vs TMX: Top Differences & Similarities - Doctor Elearning](https://doctorelearning.com/blog/xliff-vs-tmx-top-differences-similarities/)
- [What is an XLIFF file: A Comprehensive Guide](https://www.smartcat.com/blog/xliff-file/)
- [Unlocking the Black Box of Translation Memory Files | TM-Town](https://www.tm-town.com/blog/unlocking-black-box-translation-memory-files)
- [XLIFF - Wikipedia](https://en.wikipedia.org/wiki/XLIFF)
- [FAQ - XLIFF Wiki](https://wiki.oasis-open.org/xliff/FAQ)
