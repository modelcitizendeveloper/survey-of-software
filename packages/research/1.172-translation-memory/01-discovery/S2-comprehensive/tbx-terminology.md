# TBX: TermBase eXchange for Terminology Management

## What is TBX?

TBX (TermBase eXchange) is an international standard (ISO 30042:2019) for representing and exchanging structured, concept-oriented terminological data.

**Purpose:** Share glossaries and termbases between different tools and organizations in a standardized format.

## Current Standard

**ISO 30042:2019** (published April 2019)
- **Official Site:** https://www.tbxinfo.net/
- **Format:** XML-based
- **License:** Open standard

**History:**
- Originally developed by LISA (Localization Industry Standards Association)
- Co-published by ISO and LISA
- Like TMX, maintained as open standard after LISA's closure

## TBX vs. TMX vs. XLIFF

| Format | Purpose | Typical Data |
|--------|---------|--------------|
| **TBX** | Terminology exchange | Glossary entries, term definitions |
| **TMX** | Translation memory exchange | Sentence/segment pairs |
| **XLIFF** | Localization workflow | Source files + translations |

**Analogy:**
- **XLIFF** = Document being translated (the work in progress)
- **TMX** = Archive of completed translations (the memory)
- **TBX** = Dictionary of approved terms (the reference)

## What is Terminology Management?

**Terminology** = Approved vocabulary for specific domains, products, or organizations

**Example: Software Product**
- **Preferred Term:** "sign in" (not "login" or "log in")
- **Rationale:** Consistency across UI and documentation
- **Context:** Used as verb phrase ("Click here to sign in")
- **Prohibited Terms:** "authenticate", "login"

**Why It Matters:**
- **Brand consistency:** Same terms across all materials
- **User experience:** Predictable interface language
- **Translator guidance:** Clear term choices
- **Quality assurance:** Automated checks for unapproved terms

## TBX Structure (Simplified)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<tbx type="TBX-Basic" style="dca" xml:lang="en" xmlns="urn:iso:std:iso:30042:ed-2">
  <tbxHeader>
    <fileDesc>
      <titleStmt>
        <title>Software Product Terminology</title>
      </titleStmt>
      <sourceDesc>
        <p>Created by: Terminology Team</p>
      </sourceDesc>
    </fileDesc>
  </tbxHeader>
  <text>
    <body>
      <conceptEntry id="c1">
        <langSec xml:lang="en">
          <termSec>
            <term>sign in</term>
            <termNote type="partOfSpeech">verb</termNote>
            <termNote type="termType">preferredTerm-admn-sts</termNote>
          </termSec>
          <descrip type="definition">Process of authenticating user credentials</descrip>
        </langSec>
        <langSec xml:lang="fr">
          <termSec>
            <term>se connecter</term>
            <termNote type="partOfSpeech">verb</termNote>
            <termNote type="termType">preferredTerm-admn-sts</termNote>
          </termSec>
        </langSec>
        <langSec xml:lang="de">
          <termSec>
            <term>anmelden</term>
            <termNote type="partOfSpeech">verb</termNote>
            <termNote type="termType">preferredTerm-admn-sts</termNote>
          </termSec>
        </langSec>
      </conceptEntry>
    </body>
  </text>
</tbx>
```

## Key Concepts

### Concept-Oriented Structure

TBX organizes around **concepts**, not words:

**Example Concept:** "The act of accessing a system with credentials"

**Terms in Different Languages:**
- English: "sign in", "log in" (variants)
- French: "se connecter"
- German: "anmelden"
- Spanish: "iniciar sesión"

**Why Concept-Oriented?**
- One concept may have multiple terms (synonyms, variants)
- Translation is concept-to-concept, not word-to-word
- Different approval status (preferred vs. deprecated terms)

### Metadata Types

**Term-Level Metadata:**
- **Part of Speech:** noun, verb, adjective
- **Term Type:** preferredTerm, admittedTerm, deprecatedTerm
- **Usage:** formal, informal, slang
- **Gender:** (for gendered languages)
- **Number:** singular, plural

**Concept-Level Metadata:**
- **Definition:** Explanation of the concept
- **Subject Field:** Domain (IT, legal, medical)
- **Context:** Example usage
- **Source:** Where term originates (standard, company policy)

## TBX Dialects

The ISO 30042:2019 standard defines a **metamodel** for creating TBX dialects:

### TBX-Basic

**Purpose:** Simple terminology exchange
**Use Case:** Most common dialect for CAT tools
**Complexity:** Minimal metadata

**Example Entry:**
- Term in source language
- Term in target language
- Part of speech
- Definition

### TBX-Default (TBX-Core)

**Purpose:** More detailed terminology management
**Use Case:** Enterprise terminology databases
**Complexity:** Rich metadata (subject fields, usage notes, administrative data)

### TBX-Min

**Purpose:** Absolute minimum for interchange
**Use Case:** When tools have limited TBX support
**Complexity:** Concept + terms only (minimal metadata)

## Integration with CAT Tools

### How TBX Works with TM

**During Translation:**

1. Translator types segment in CAT tool
2. **TM** suggests similar previous translations
3. **Termbase (TBX)** highlights approved terms in segment
4. Tool warns if translator uses non-approved term

**Example:**
- Source: "Click here to login"
- Termbase: "login" is deprecated, use "sign in"
- CAT tool: Highlights "login" in red, suggests "sign in"

### Quality Assurance

**Automated Checks:**
- **Terminology consistency:** Ensure approved terms used
- **Forbidden terms:** Flag deprecated/prohibited terms
- **Stemming:** Detect term variations (account vs. accounts)

**Example Tools with TBX Support:**
- MemoQ (integrated termbase with QA)
- SDL Trados (MultiTerm termbase)
- OmegaT (glossary import/export via TBX)

## TBX vs. Simple Glossaries

| Feature | TBX | Simple Glossary (CSV/Excel) |
|---------|-----|----------------------------|
| **Structure** | Concept-oriented | Flat list |
| **Metadata** | Rich (part of speech, usage, etc.) | Minimal |
| **Multilingual** | Yes (multiple languages per concept) | Usually bilingual |
| **Tool Support** | Standard import/export | Manual entry |
| **QA Integration** | Automated checks | Manual reference |

**When to Use TBX:**
- Large terminology databases
- Multilingual projects (3+ languages)
- Strict terminology governance
- Automated QA requirements

**When Simple Glossary is Enough:**
- Small projects
- Ad-hoc translation
- Single language pair
- No formal terminology management

## Practical Workflow

### Creating a Termbase

1. **Identify Key Terms**
   - Product-specific vocabulary
   - Technical terms
   - Brand names
   - UI strings requiring consistency

2. **Define Concepts**
   - Write clear definitions
   - Identify synonyms/variants
   - Mark preferred vs. deprecated

3. **Translate Terms**
   - Get approved translations for each language
   - Include context/usage notes
   - Specify part of speech

4. **Export to TBX**
   - Use termbase management tool
   - Export TBX-Basic for maximum compatibility
   - Validate XML structure

5. **Import into CAT Tools**
   - Import TBX into each translator's CAT tool
   - Configure QA checks
   - Train team on terminology usage

### Maintaining Termbases

- **Versioning:** Track changes to approved terms
- **Governance:** Define who can add/modify terms
- **Review Cycles:** Periodic terminology audits
- **Feedback Loop:** Translators suggest new terms

## Use Cases

### Software Localization

**Challenge:** UI must use consistent terminology
**Solution:** TBX termbase with approved UI terms
**Benefit:** "Settings" always translates to same term in each language

### Legal Translation

**Challenge:** Legal terms have precise meanings
**Solution:** TBX with legal term definitions and approved translations
**Benefit:** Consistency across contracts, compliance documents

### Medical/Pharmaceutical

**Challenge:** Medical terminology must be accurate
**Solution:** TBX based on medical ontologies and standards
**Benefit:** Patient safety, regulatory compliance

### Enterprise Documentation

**Challenge:** Product names, features must be consistent
**Solution:** Corporate TBX maintained by terminology team
**Benefit:** Brand consistency across all materials

## Tools for TBX Management

**Dedicated Termbase Tools:**
- SDL MultiTerm
- Lingo Systems Termbase
- TermWeb

**CAT Tools with Built-in Termbases:**
- MemoQ (integrated termbase)
- SDL Trados (MultiTerm integration)
- Wordfast (termbase feature)

**Open Source Options:**
- OmegaT (glossary import/export)
- Custom scripts (Python libraries for TBX parsing)

## Sources

- [ISO 30042:2019 - Management of terminology resources — TermBase eXchange (TBX)](https://www.iso.org/standard/62510.html)
- [TermBase eXchange - Wikipedia](https://en.wikipedia.org/wiki/TermBase_eXchange)
- [Introduction to TermBase eXchange (TBX)](https://www.tbxinfo.net/)
- [About TBX – Introduction to TermBase eXchange (TBX)](https://www.tbxinfo.net/tbx-about/)
- [What is TBX?](https://help.wordbee.com/wbt/what-is-tbx)
- [Term Base eXchange (TBX)](https://blog.andovar.com/term-base-exchange-tbx)
