# C/C++ String Algorithm Libraries

## C Libraries

### `<string.h>` - Standard C String Functions
- **Standard library**: C standard library
- **Functions**: strcpy, strcmp, strlen, strstr, strtok
- **Limitations**: Null-terminated strings, no Unicode, unsafe (buffer overflows)
- **Use case**: Low-level string manipulation, legacy code

### PCRE (Perl Compatible Regular Expressions)
- **Library**: `libpcre` or `libpcre2`
- **Purpose**: Full-featured regex engine
- **Features**: Perl-compatible syntax, backtracking, named groups
- **Performance**: Highly optimized C implementation
- **Use case**: Production regex needs, system utilities

### RE2
- **Library**: `libre2` (C++ but C-callable)
- **Purpose**: Fast, safe regex engine
- **Features**: Guaranteed linear time, no backtracking
- **Safety**: DoS-resistant, no stack overflow on nested patterns
- **Use case**: Untrusted input, security-critical applications

### `libbsd` - String Functions
- **Library**: `libbsd`
- **Purpose**: BSD-style safer string functions
- **Functions**: strlcpy, strlcat (bounds-checked)
- **Use case**: Safer alternatives to strcpy/strcat

## C++ Libraries

### `<regex>` - C++11 Standard Regex
- **Standard library**: C++11 onwards
- **Features**: ECMAScript, POSIX regex syntaxes
- **Performance**: Varies by compiler, generally adequate
- **Use case**: Modern C++ projects, portable regex

### Boost.Regex
- **Library**: Boost C++ Libraries
- **Purpose**: Mature regex implementation
- **Features**: Perl-compatible, Unicode support, flexible API
- **Use case**: Pre-C++11 projects, advanced regex features

### Google RE2 (C++ API)
- **Library**: `re2`
- **Purpose**: Safe, fast regex with rich C++ API
- **Features**: Linear time guarantee, thread-safe, Unicode support
- **Use case**: Production systems, high-performance text processing

### fmtlib (`fmt`)
- **Library**: `fmt` (becoming C++20 `<format>`)
- **Purpose**: Modern string formatting
- **Features**: Type-safe, fast, extensible formatting
- **Use case**: String formatting, text generation

### Boost.String_Algo
- **Library**: Boost C++ Libraries
- **Purpose**: String manipulation algorithms
- **Features**: case conversion, trimming, splitting, joining, predicates
- **Use case**: Rich string processing needs

### ICU (International Components for Unicode)
- **Library**: `libicu`
- **Purpose**: Comprehensive Unicode and i18n support
- **Features**: Normalization, collation, text boundary analysis, transliteration
- **Use case**: Complex Unicode handling, internationalization

### RapidFuzz-cpp
- **Library**: Header-only C++17 library
- **Purpose**: Fast fuzzy string matching
- **Algorithms**: Levenshtein, Jaro-Winkler, token-based matching
- **Performance**: SIMD-accelerated implementations
- **Use case**: High-performance fuzzy matching
