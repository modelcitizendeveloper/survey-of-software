# Survey of Software

A curated research library covering software libraries, algorithms, and development tools across 199 domains.

**🌐 Visit the site:** https://research.modelcitizendeveloper.com/

## What This Is

When choosing a software library, you need answers to practical questions:
- What does this actually do, in plain English?
- What are my alternatives?
- Which one should I use for production?
- Will this still be maintained in 3 years?

This research library answers those questions. Each piece covers a specific domain (sorting algorithms, graph databases, ML frameworks, etc.) with:

- **Concept explanations** for beginners
- **Library comparisons** across alternatives
- **Production readiness** assessments
- **Long-term viability** evaluations

**Current coverage:** 111 of 199 research pieces complete (56%)

## How to Use This

### Option 1: Browse the Website (Easiest)

Visit **https://research.modelcitizendeveloper.com/** for:
- Clean navigation and search
- Organized by category
- Mobile-friendly reading

### Option 2: Work with This Repository

If you prefer working locally or want to contribute:

```bash
# Clone the repo
git clone https://github.com/modelcitizendeveloper/survey-of-software.git
cd survey-of-software

# Install Hugo (one-time setup)
# macOS: brew install hugo
# Linux: https://github.com/gohugoio/hugo/releases (get v0.155.2+ extended)

# Run locally
git submodule update --init --recursive
hugo server -D

# Open http://localhost:1313/
```

## Coverage

Research organized into 13 major categories:

| Category | Topics |
|----------|--------|
| **1.001-009** | Sorting & Searching Algorithms |
| **1.010-019** | Graph & Network Algorithms |
| **1.020-029** | Mathematical & Statistical Algorithms |
| **1.030-039** | String & Text Algorithms |
| **1.040-049** | Data Structure Libraries |
| **1.050-059** | Compression & Encoding |
| **1.060-069** | Cryptographic & Hashing |
| **1.070-079** | Machine Learning Algorithms |
| **1.080-089** | Geometric & Spatial Algorithms |
| **1.100-109** | Text & Document Processing |
| **1.110-119** | User Interface & Frontend |
| **1.200-209** | LLM & AI Stack |
| **1.300-309** | Public Finance & Civic Data |

[Browse the full catalog →](https://research.modelcitizendeveloper.com/survey/)

## Contributing

Contributions welcome! To add or improve research:

1. Fork this repo
2. Add/edit content in `content/survey/`
3. Follow the existing front matter format (see any `1-XXX.md` file)
4. Test locally: `hugo server -D`
5. Submit a pull request

Research pieces follow a structured format:
- Problem/concept explanation
- Available libraries/tools
- Feature comparisons
- Recommendations

See existing pieces for examples.

## Technical Details

- **Generator:** Hugo v0.155.2 (extended)
- **Theme:** [hugo-book](https://github.com/alex-shpak/hugo-book)
- **Deployment:** GitHub Pages via GitHub Actions
- **Auto-deploy:** Pushes to `main` trigger automatic deployment

## License

See [LICENSE](LICENSE) file for details.

Research content is provided for informational purposes. Always verify library compatibility and licensing for your specific use case.

---

**Questions?** Open an issue or visit the [live site](https://research.modelcitizendeveloper.com/).
