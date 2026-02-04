# S1 Rapid Discovery - Recommendation

**Time Spent**: ~75 minutes
**Confidence Level**: HIGH (for library landscape)

## Anki Integration Libraries Found

| Library | Downloads/Month | Maintenance | Purpose | Verdict |
|---------|----------------|-------------|---------|---------|
| **genanki** | **33,970** | Stable (Nov 2023) | Generate .apkg files | ✅ **USE THIS** |
| AnkiConnect | N/A (add-on) | Active | Live Anki API | ⚠️ Complex, niche |
| ankipandas | 1,548 | Active (Jul 2024) | Analyze Anki DB | ❌ Read-only |

## Clear Winner: **genanki**

**Popularity**: 22× more downloads than ankipandas (33,970 vs 1,548/month)

**Why genanki wins**:
- ✅ Highest popularity by far
- ✅ Simple API (Note → Card → Deck → Package)
- ✅ No Anki installation needed (generates .apkg standalone)
- ✅ MIT license (permissive)
- ✅ Media support (audio, images)
- ✅ Stable (v0.13.1, mature codebase)

**Why skip alternatives**:
- **AnkiConnect**: Requires Anki running + add-on install (more friction)
- **ankipandas**: Read-only, cannot create decks (wrong tool)

## Quick Validation

**Basic Usage** (confirmed from docs):
```python
pip install genanki

import genanki
model = genanki.Model(...)
note = genanki.Note(model=model, fields=['Latin', 'English'])
deck = genanki.Deck(deck_id=123, name='Latin')
deck.add_note(note)
genanki.Package(deck).write_to_file('output.apkg')
```

**Generates**: `.apkg` file users import into Anki

## S1 Library Recommendation

**Use `genanki`** for Anki deck generation.

- Most popular option (33,970 downloads/month)
- Proven stable (1,492 GitHub stars)
- Simple API for programmatic deck creation

## What S1 Did NOT Answer

S1 is **library discovery only**. These questions belong in S2/S3:

**For S2 (Comprehensive)**:
- Detailed genanki features (templates, media, updates)
- Alternative approaches (custom flashcard system architecture)
- API comparison (genanki vs direct Anki DB vs AnkiConnect)

**For S3 (Need-Driven)**:
- Scenario 1: Does genanki .apkg export satisfy existing Anki users?
- Scenario 2: Build custom flashcard interface (no Anki dependency)?
- Implementation effort comparison (Anki export vs custom system)

S1 found the libraries. S2/S3 determine how to use them.

## Sources

- [genanki PyPI](https://pypi.org/project/genanki/) - 33,970 downloads/month
- [genanki GitHub](https://github.com/kerrickstaley/genanki) - 1,492 stars
- [AnkiConnect](https://ankiweb.net/shared/info/2055492159) - Anki add-on
- [ankipandas PyPI](https://pypi.org/project/ankipandas/) - 1,548 downloads/month
- [FSRS PyPI](https://pypi.org/project/fsrs/) - From 1.141 research
- [Awesome FSRS](https://github.com/open-spaced-repetition/awesome-fsrs)
- [Real Python Django Flashcards](https://realpython.com/django-flashcards-app/)
