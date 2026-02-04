# genanki - Programmatic Anki Deck Generation

**PyPI Package**: `genanki`
**GitHub**: kerrickstaley/genanki
**Purpose**: Generate Anki .apkg files without Anki installation

## Popularity Metrics

- **Downloads**: 33,970/month (PyPI)
- **GitHub Stars**: 1,492
- **Maintenance**: Last release Nov 2023 (14 months ago)
- **Latest Version**: 0.13.1
- **License**: MIT

## Quick Assessment

**Pros**:
- ✅ **No Anki dependency** - generates .apkg files standalone
- ✅ **Simple API** - Create Note → Card → Deck → Package → write_to_file()
- ✅ **Media support** - Images, audio embedded in .apkg
- ✅ **GUID management** - Stable IDs for updates
- ✅ **Most popular** Anki generation library (34K downloads/month)
- ✅ **MIT license** - permissive

**Cons**:
- ⚠️ **Maintenance concern** - No releases in 14 months (last: Nov 2023)
- ⚠️ **Not official** - "Not affiliated with main Anki project"
- ⚠️ **No scheduling** - Only creates decks, doesn't handle reviews
- ⚠️ **User must have Anki** - .apkg files require Anki to use

## Use Case Fit

**Scenario 1 (Create flashcards for existing Anki users)**: ✅ **PERFECT FIT**
- Generates .apkg files users import into Anki
- No custom UI needed - leverages Anki ecosystem
- Minimal development: ~5-10 hours to generate decks

**Scenario 2 (Build software with custom interface)**: ❌ **NOT APPLICABLE**
- Only generates export files, no flashcard delivery
- Users still need Anki installed

## Basic Usage

```python
import genanki

# Create model (card template)
model = genanki.Model(...)

# Create notes
note = genanki.Note(model=model, fields=['Latin', 'English'])

# Create deck
deck = genanki.Deck(deck_id=123, name='Latin Vocabulary')
deck.add_note(note)

# Export to .apkg
genanki.Package(deck).write_to_file('output.apkg')
```

## Confidence for Language Learning App

**HIGH** - If targeting existing Anki users (Scenario 1)
**N/A** - If building custom interface (Scenario 2)

## Sources
- [genanki PyPI](https://pypi.org/project/genanki/)
- [genanki GitHub](https://github.com/kerrickstaley/genanki)
- [PyPI Stats](https://pypistats.org/packages/genanki) - 33,970 downloads/month
