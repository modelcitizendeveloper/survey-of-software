# Stroke Order Implementation Guide

**Research ID**: research-k6iy
**Date**: 2026-01-29
**Pass**: S3 (Need-Driven Application)
**Purpose**: Practical guidance for implementing stroke order features in educational platforms

---

## 1. Implementation Considerations

### 1.1 Licensing

**Open Licenses**:
- **Make Me a Hanzi**: Mixed licenses (check repository)
- **KanjiVG**: CC BY-SA 3.0 (attribution + share-alike)
- **animCJK**: Open-source (verify specific license)
- **KRADFILE**: EDRDG License (check restrictions)

**Action Items**:
- Review license terms before commercial use
- Provide proper attribution
- Comply with share-alike requirements where applicable

---

### 1.2 Data Formats

**SVG** (Recommended for stroke order):
- Scalable without quality loss
- Embeddable in web/mobile apps
- Supports animation paths
- Lightweight

**JSON** (Recommended for metadata):
- Easy to parse
- Works with all modern platforms
- Suitable for APIs

**GIF** (Legacy, limited use):
- Pre-rendered animations
- No customization
- Larger file sizes

---

### 1.3 Technical Integration

**For Web Applications**:
```javascript
// Example: Hanzi Writer
import HanziWriter from 'hanzi-writer';

const writer = HanziWriter.create('character-target-div', '你', {
  width: 100,
  height: 100,
  padding: 5
});

writer.animateCharacter();
```

**For Mobile Applications**:
- Embed SVG files directly
- Use native SVG rendering libraries
- Pre-cache common characters for offline use

**For Backend Systems**:
- cjklib (Python) for character analysis
- Chinese Character Web API for stroke counts
- PostgreSQL with Unihan data for lookups

---

### 1.4 Performance Optimization

**Strategies**:
1. **Lazy Loading**: Load stroke data only when character is displayed
2. **Caching**: Pre-cache common characters (top 3,000)
3. **CDN**: Serve SVG files from CDN for faster delivery
4. **Progressive Enhancement**: Show static character first, animate on interaction

**Estimated Data Sizes**:
- Per-character SVG: 2-10 KB
- 1,000 characters: 2-10 MB
- Full dataset (9,000+): 18-90 MB

---

## 2. Use Cases for Learning Applications

### 2.1 Stroke Order Practice

**Features**:
- Display stroke-by-stroke animation
- User traces character with finger/stylus
- Real-time validation of stroke direction and order
- Feedback on accuracy

**Data Required**:
- SVG stroke paths (from Make Me a Hanzi or KanjiVG)
- Stroke sequence metadata
- Direction vectors

---

### 2.2 Dictionary Lookup by Stroke Count

**Features**:
- Filter characters by total stroke count
- Combine with radical lookup
- Progressive narrowing (radical + stroke count)

**Data Required**:
- Stroke count database (Unihan or ChineseStrokes)
- Radical decomposition (KRADFILE)

**Example Lookup**:
```
User: "Radical 水 (water) + 7 strokes"
Result: 汰, 汲, 汴, 汾 (candidates)
```

---

### 2.3 Handwriting Recognition Training

**Features**:
- Collect user stroke data
- Train ML models for character recognition
- Validate correct stroke order

**Data Required**:
- Labeled stroke order sequences
- Variant forms (different handwriting styles)
- Stroke direction and timing

---

### 2.4 Gamified Learning

**Features**:
- "Draw the character" challenges
- Timed stroke order races
- Achievement badges for stroke accuracy

**Engagement Mechanics**:
- Progress tracking (characters mastered)
- Leaderboards (speed + accuracy)
- Unlock levels based on stroke complexity

---

### 2.5 Adaptive Learning Paths

**Features**:
- Start with simple characters (few strokes)
- Progress to complex characters
- Focus on commonly confused characters

**Data-Driven Approach**:
- Sort characters by stroke count (ascending)
- Track user errors (confusion matrix)
- Recommend practice based on weak points

---

## 3. Integration with Educational Platforms

### 3.1 Docusaurus Integration

**Approach**:
- Create MDX components for stroke order display
- Embed Hanzi Writer or animCJK SVGs
- Add interactive quizzes

**Example MDX**:
```mdx
import StrokeOrder from '@site/src/components/StrokeOrder';

<StrokeOrder character="学" />
```

---

### 3.2 QRCards Certificate Integration

**Certificate Fields**:
```json
{
  "certification_info": {
    "type": "competency_badge",
    "name": "Hanzi Writing Fundamentals",
    "issued_date": "2026-XX-XX",
    "level": 1
  },
  "skills": {
    "characters_mastered": 500,
    "stroke_accuracy": "95%",
    "writing_speed": "15 chars/min"
  },
  "portfolio_evidence": [
    {
      "name": "Stroke Order Video",
      "url": "example.com/demo"
    }
  ]
}
```

---

### 3.3 Learning Path Design

**Beginner Path** (8 weeks):
- Week 1-2: Basic strokes (8 types)
- Week 3-4: Simple characters (1-4 strokes)
- Week 5-6: Radicals (214 traditional)
- Week 7-8: Common characters (200 most frequent)

**Intermediate Path** (12 weeks):
- Compound characters (5-12 strokes)
- Stroke order rules and exceptions
- Handwriting speed optimization
- Character variants (simplified vs. traditional)

**Advanced Path** (16 weeks):
- Complex characters (13+ strokes)
- Calligraphy styles (kaishu, xingshu)
- Historical forms
- Error correction (common mistakes)

---

## 4. Recommended Tech Stack

### 4.1 For Web-Based Learning Apps

**Frontend**:
- React/Next.js for UI
- Hanzi Writer for character animations
- SVG.js for custom stroke rendering

**Backend**:
- Node.js API for character data
- PostgreSQL with Unihan data
- Redis for caching common characters

**Data Storage**:
- CDN for SVG files (Cloudflare)
- JSON API for metadata
- User progress in database

---

### 4.2 For Mobile Apps

**iOS**:
- SwiftUI for UI
- Core Graphics for SVG rendering
- Local SQLite database with stroke data

**Android**:
- Jetpack Compose for UI
- AndroidX SVG libraries
- Room database for offline data

**Cross-Platform**:
- React Native + react-native-svg
- Flutter + flutter_svg

---

## 5. Example Implementations

### 5.1 Web Component (React)

```jsx
import React, { useEffect, useRef } from 'react';
import HanziWriter from 'hanzi-writer';

const StrokeOrderDisplay = ({ character }) => {
  const targetRef = useRef(null);
  const writerRef = useRef(null);

  useEffect(() => {
    if (targetRef.current) {
      writerRef.current = HanziWriter.create(targetRef.current, character, {
        width: 200,
        height: 200,
        padding: 10,
        showOutline: true,
        strokeAnimationSpeed: 1,
        delayBetweenStrokes: 300
      });
    }

    return () => {
      if (writerRef.current) {
        writerRef.current = null;
      }
    };
  }, [character]);

  const handleAnimate = () => {
    writerRef.current?.animateCharacter();
  };

  const handleQuiz = () => {
    writerRef.current?.quiz();
  };

  return (
    <div>
      <div ref={targetRef} />
      <button onClick={handleAnimate}>Animate</button>
      <button onClick={handleQuiz}>Practice</button>
    </div>
  );
};

export default StrokeOrderDisplay;
```

---

### 5.2 Backend API (Node.js + Express)

```javascript
const express = require('express');
const { Pool } = require('pg');

const app = express();
const pool = new Pool({
  connectionString: process.env.DATABASE_URL
});

// Get stroke count for a character
app.get('/api/strokes/:character', async (req, res) => {
  const { character } = req.params;
  const codepoint = character.codePointAt(0).toString(16).toUpperCase();

  const result = await pool.query(
    'SELECT stroke_count, radical FROM unihan WHERE codepoint = $1',
    [codepoint]
  );

  if (result.rows.length === 0) {
    return res.status(404).json({ error: 'Character not found' });
  }

  res.json(result.rows[0]);
});

// Search characters by stroke count
app.get('/api/search/strokes/:count', async (req, res) => {
  const { count } = req.params;

  const result = await pool.query(
    'SELECT codepoint, character FROM unihan WHERE stroke_count = $1 LIMIT 100',
    [parseInt(count)]
  );

  res.json(result.rows);
});

app.listen(3000, () => {
  console.log('API running on port 3000');
});
```

---

### 5.3 Python Stroke Analysis

```python
from cjklib import characterlookup

cjk = characterlookup.CharacterLookup('C')  # 'C' for Chinese

# Get stroke count
character = '学'
stroke_count = cjk.getStrokeCount(character)
print(f"Stroke count for {character}: {stroke_count}")

# Get radicals
radicals = cjk.getCharacterRadicalResidualStrokeCount(character)
print(f"Radicals: {radicals}")

# Find characters by stroke count
chars_with_5_strokes = cjk.getCharactersForStrokeCount(5)
print(f"Characters with 5 strokes: {chars_with_5_strokes[:10]}")
```

---

## 6. Testing and Validation

### 6.1 Data Quality Checks

**Validation Steps**:
1. Verify stroke count matches across data sources
2. Check SVG files render correctly
3. Validate stroke order follows standard conventions
4. Test on different screen sizes

**Automated Testing**:
```javascript
describe('Stroke Order Data', () => {
  test('SVG files exist for common characters', async () => {
    const commonChars = ['的', '一', '是', '不', '了'];

    for (const char of commonChars) {
      const svg = await loadCharacterSVG(char);
      expect(svg).toBeDefined();
      expect(svg).toContain('<path');
    }
  });

  test('Stroke counts match database', async () => {
    const testCases = [
      { char: '一', expectedStrokes: 1 },
      { char: '二', expectedStrokes: 2 },
      { char: '三', expectedStrokes: 3 }
    ];

    for (const { char, expectedStrokes } of testCases) {
      const count = await getStrokeCount(char);
      expect(count).toBe(expectedStrokes);
    }
  });
});
```

---

### 6.2 User Experience Testing

**Test Scenarios**:
- Stroke animation speed (too fast/slow?)
- Touch responsiveness on mobile
- Accuracy threshold for practice mode
- Feedback clarity (correct/incorrect strokes)

**Metrics to Track**:
- Animation load time
- Practice completion rate
- User accuracy over time
- Session engagement duration

---

## 7. Deployment Checklist

### 7.1 Data Preparation

- [ ] Download required datasets (Make Me a Hanzi, KanjiVG, etc.)
- [ ] Process SVG files for CDN delivery
- [ ] Set up database with Unihan data
- [ ] Create character metadata JSON files
- [ ] Implement caching strategy

### 7.2 Infrastructure

- [ ] Set up CDN for SVG files
- [ ] Configure API endpoints
- [ ] Set up Redis for caching
- [ ] Configure database backups
- [ ] Set up monitoring and logging

### 7.3 Integration

- [ ] Test Hanzi Writer integration
- [ ] Verify mobile responsiveness
- [ ] Test offline functionality
- [ ] Validate cross-browser compatibility
- [ ] Test performance under load

### 7.4 Content

- [ ] Create learning path content
- [ ] Write exercise instructions
- [ ] Prepare quiz questions
- [ ] Create tutorial videos (optional)
- [ ] Design achievement badges

---

**Document Status**: Complete
**Last Updated**: 2026-01-29
**Related**: See S2-comprehensive for data sources, S4-strategic for roadmap
