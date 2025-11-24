# ankipandas - Anki Database Analysis

**PyPI Package**: `ankipandas`
**GitHub**: klieret/AnkiPandas
**Purpose**: Analyze Anki databases using pandas DataFrames

## Popularity Metrics

- **Downloads**: 357/week (~1,548/month)
- **GitHub Stars**: (part of klieret repos)
- **Maintenance**: Active (scanned July 2024)
- **Latest Version**: 0.3.15
- **License**: Not specified

## Quick Assessment

**Pros**:
- ✅ **Pandas integration** - Load Anki DB as DataFrame
- ✅ **Analysis tools** - Visualize, select, manipulate cards
- ✅ **Export capabilities** - CSV, Excel, HTML, JSON

**Cons**:
- ❌ **Writing DISABLED** - Cannot modify Anki database (issue #137)
- ❌ **Read-only** - Analysis tool, not creation tool
- ❌ **Low popularity** - 1,548 downloads/month (vs 33,970 for genanki)
- ❌ **Not for card generation** - Wrong tool for creating flashcards

## Use Case Fit

**Scenario 1 (Create flashcards for existing Anki users)**: ❌ **NOT APPLICABLE**
- Cannot create cards (write functionality disabled)
- Only for analyzing existing Anki databases

**Scenario 2 (Build software with custom interface)**: ❌ **NOT APPLICABLE**
- Analysis tool, not flashcard delivery system

## Potential Use

**Only useful for**: Research/analytics on Anki usage patterns
- Example: "Which cards are most difficult?"
- Example: "What's average retention rate?"

**Not useful for**: Creating or delivering flashcards

## Basic Usage

```python
from ankipandas import Collection

# Load Anki collection
col = Collection()

# Analyze as DataFrame
notes_df = col.notes.fields_as_columns()
cards_df = col.cards.merge_notes()

# Export analysis
cards_df.to_csv('analysis.csv')
```

## Confidence for Language Learning App

**LOW** - Wrong tool. Use genanki for card creation.

**Verdict**: Skip for flashcard generation use case.

## Sources
- [ankipandas PyPI](https://pypi.org/project/ankipandas/)
- [AnkiPandas GitHub](https://github.com/klieret/AnkiPandas)
- [ankipandas docs](https://ankipandas.readthedocs.io/)
