# OmegaT: Open Source CAT Tool

## Overview

OmegaT is a free, open-source Computer-Assisted Translation (CAT) tool for professional translators, written in Java and available on all major platforms (Windows, macOS, Linux).

**License:** GPL (Free and open source)
**Language:** Java
**Latest Info:** Active development as of 2026
**Website:** https://omegat.org/

## Key Features

### Translation Memory

**Automatic TM Management:**
- OmegaT creates one TM per project automatically
- No manual TM creation or association needed
- The project itself IS the translation memory

**TMX Format (Native):**
- Saves TM databases in TMX format by default
- Every autosave exports to THREE TMX files:
  - Native OmegaT TMX
  - Level 1 TMX (plain text, maximum compatibility)
  - Level 2 TMX (preserves formatting)
- Automatic export ensures TM is always available for other tools

**Multiple Reference TMs:**
- No limit on number of reference TMs
- Easy priority assignment for multiple TMs
- Flexible memory reuse across projects

### Fuzzy Matching

- Matches from translation memories with percentage scoring
- Highlights differences visually
- Keyword search across TM
- Concordance searching (find where terms appear in TM)

### Glossaries

- Glossary lookup during translation
- Term base management
- Reference searching

### Multi-User Projects

- Shared TMX translation memory
- Read/write access for team members
- Collaborative translation workflows

## Architecture

OmegaT projects are folder-based with this structure:

```
project/
├── source/          # Source files to translate
├── target/          # Generated translated files
├── tm/              # Translation memory files (TMX)
│   ├── auto/        # Automatically added TMs
│   └── enforce/     # Enforced TMs (exact matches only)
├── glossary/        # Glossary files
├── dictionary/      # Dictionary files
└── omegat/          # Project metadata
    └── project_save.tmx  # Main TM
```

## File Format Support

OmegaT handles numerous file formats:
- Plain text
- HTML/XML
- Microsoft Office (DOCX, XLSX, PPTX)
- OpenDocument (ODT, ODS, ODP)
- PDF (extract text for translation)
- PO (gettext)
- Java properties files
- Many others via filters

## Institutional Use

**European Commission (DGT):**
The Directorate-General for Translation uses OmegaT as an official alternative CAT tool alongside commercial options. This demonstrates enterprise-level viability.

## Strengths

**Cost:**
- Free and open source (no licensing fees)
- No subscription costs
- Full features available to everyone

**Flexibility:**
- Runs on Windows, macOS, Linux
- Java-based = cross-platform consistency
- Extensible via plugins

**Standards Compliance:**
- Native TMX support
- Open file formats
- No vendor lock-in

**Control:**
- Self-hosted (data stays on your systems)
- No cloud dependency
- Privacy-sensitive work (legal, medical, confidential)

**Community:**
- Active open-source community
- Extensive documentation
- Free support via forums/mailing lists

## Limitations

**User Interface:**
- Less polished than commercial CAT tools
- Steeper learning curve for non-technical users
- Java UI may feel dated compared to modern web-based tools

**No Built-in TMS:**
- Primarily a translator's tool, not a full translation management system
- Project management features are basic
- No built-in invoicing, client management, vendor management

**Machine Translation:**
- MT integration exists but less seamless than commercial tools
- Requires configuration for cloud MT services

**Enterprise Features:**
- No built-in reporting/analytics
- Basic team collaboration (vs. enterprise TMS)
- Limited workflow automation

## Ideal Use Cases

**Individual Translators:**
- Freelancers who own their TM assets
- Translators with privacy/security requirements
- Budget-conscious professionals

**Small Translation Teams:**
- Teams that can share folders/files directly
- Projects not requiring complex workflow orchestration

**Open Source Projects:**
- Software localization (gettext, properties files)
- Community translation efforts

**Academic/Educational:**
- Teaching CAT tool concepts
- University translation programs

**Confidential Work:**
- Legal, medical, government translation
- When data cannot leave internal systems

## Sources

- [OmegaT - multiplatform CAT tool download | SourceForge.net](https://sourceforge.net/projects/omegat/)
- [OmegaT - Wikipedia](https://en.wikipedia.org/wiki/OmegaT)
- [Multi-user translation and open-source CAT software: OmegaT in action - EMT Blog](https://european-masters-translation-blog.ec.europa.eu/articles-emt-blog/multi-user-translation-and-open-source-cat-software-omegat-action-2022-05-10_en)
- [OmegaT - The Free Translation Memory Tool](https://omegat.org/)
- [Introduction to OmegaT](https://omegat.sourceforge.io/manual-standard/en/chapter.instant.start.guide.html)
- [OmegaT CAT Tool - A free Translation Memory (TM) tool](https://www.l10nsoftware.com/omegat-cat-tool/)
