# JavaScript/TypeScript String Algorithm Libraries

## Built-in: `String` and `RegExp`
- **Native**: JavaScript standard library
- **Capabilities**: Basic string operations, regex matching
- **Performance**: Varies by JS engine (V8, SpiderMonkey, JavaScriptCore)
- **Unicode**: ES6+ has good Unicode support via `/u` flag

## `fuse.js` - Fuzzy Search
- **npm**: `fuse.js`
- **Purpose**: Lightweight fuzzy-search library
- **Algorithm**: Bitap algorithm (approximate string matching)
- **Features**: Threshold tuning, location/distance scoring, key-based search
- **Use case**: Client-side search, autocomplete
- **Bundle size**: ~12KB minified

## `string-similarity` - String Comparison
- **npm**: `string-similarity`
- **Purpose**: Dice coefficient-based string similarity
- **Algorithm**: Sørensen-Dice coefficient
- **Features**: Best match finding, rating comparisons
- **Use case**: Finding closest match from a list

## `fast-levenshtein` - Edit Distance
- **npm**: `fast-levenshtein`
- **Purpose**: Fast Levenshtein distance calculation
- **Performance**: Pure JS, optimized with memoization
- **Use case**: Computing edit distance without native dependencies

## `minimatch` - Glob Matching
- **npm**: `minimatch`
- **Purpose**: Glob pattern matching
- **Features**: Full glob syntax support, used by npm
- **Use case**: File path matching, .gitignore-style patterns

## `xregexp` - Extended Regular Expressions
- **npm**: `xregexp`
- **Purpose**: Extended regex features beyond standard JS
- **Features**: Named capture groups, Unicode categories, free-spacing mode
- **Use case**: Complex regex patterns with better readability

## `natural` - NLP & String Processing
- **npm**: `natural`
- **Purpose**: Natural language processing toolkit
- **String features**: Tokenization, stemming, phonetics (Soundex, Metaphone)
- **Use case**: Text analysis, search indexing, name matching
