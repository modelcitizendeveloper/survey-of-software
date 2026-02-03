# AnkiConnect - Live Anki Integration API

**Type**: Anki Add-on (not PyPI package)
**GitHub**: FooSoft/anki-connect
**Purpose**: RESTful API for live integration with running Anki desktop

## Popularity Metrics

- **Anki Add-on ID**: 2055492159
- **GitHub Stars**: Not found in search (add-on hosted on AnkiWeb)
- **Maintenance**: Active (maintained by FooSoft)
- **API Port**: localhost:8765
- **Python Client**: `ankiapi` package on PyPI

## Quick Assessment

**Pros**:
- ✅ **Live integration** - Real-time add/update cards while Anki running
- ✅ **Full Anki features** - Access all Anki functionality via API
- ✅ **Bi-directional** - Read AND write (not just export)
- ✅ **Active ecosystem** - Used by many Anki extensions

**Cons**:
- ❌ **Requires Anki running** - Desktop app must be open
- ❌ **User installation** - Must install add-on (extra friction)
- ❌ **Not cross-platform** - Anki desktop only (no mobile API)
- ❌ **More complex** - REST API vs simple .apkg export

## Use Case Fit

**Scenario 1 (Create flashcards for existing Anki users)**: ⚠️ **POSSIBLE BUT COMPLEX**
- Can sync cards to user's Anki
- But requires: Anki running + add-on installed
- More friction than .apkg download

**Scenario 2 (Build software with custom interface)**: ❌ **NOT APPLICABLE**
- Still requires Anki desktop running
- Doesn't provide custom flashcard UI

## API Example

```python
# Install: pip install ankiapi
from ankiapi import AnkiAPI

api = AnkiAPI()  # Connects to localhost:8765

# Create deck
api.create_deck("Latin Vocabulary")

# Add flashcard
api.add_flashcard(
    deck="Latin Vocabulary",
    front="puella",
    back="girl"
)
```

## Confidence for Language Learning App

**MEDIUM** - Adds complexity vs genanki .apkg export
**Best for**: Apps that need real-time sync with Anki desktop
**Not recommended**: If users just want to import decks

## Sources
- [AnkiConnect Add-on](https://ankiweb.net/shared/info/2055492159)
- [FooSoft/anki-connect GitHub](https://github.com/FooSoft/anki-connect)
- [ankiapi PyPI](https://pypi.org/project/ankiapi/)
