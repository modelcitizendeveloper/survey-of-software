# S3 Need-Driven Pass: Practical Implementation Recommendations

## Key Takeaways

### 1. Python Libraries Make TMX Accessible

**PythonTmx** is production-ready for:
- Parsing existing TMX files
- Generating TMX programmatically
- Building custom TM services
- Converting between formats (TMX ↔ Excel ↔ JSON)

**Action:** Use PythonTmx for any programmatic TM manipulation (automation, cleaning, merging)

### 2. TM Cleaning is Essential, Not Optional

**Reality:** 20-45% of typical TM is problematic (duplicates, errors, outdated content)

**Tools Available:**
- **TMOP** (open source, Python) for batch cleaning
- **Commercial services** for professional cleanup
- **DIY scripts** (examples provided) for ongoing maintenance

**Action:** Schedule quarterly TM cleaning. Export cleaned TMX before client delivery.

### 3. Alignment Tools Convert Legacy Translations

**Common Scenario:** You have old translations but no TM

**Solution:**
- **LF Aligner** (GUI, easy for non-technical users)
- **bitext2tmx** (command-line, automation-friendly)
- **TMPotter** (Java-based, PO file support)

**Action:** Recover value from legacy translations by creating TMX. Review output quality.

### 4. MT + TM Hybrid is the 2026 Standard

**Not "MT vs. TM" anymore—it's "MT AND TM"**

**Workflow:**
- 100% context match → TM (no review needed)
- 90-99% fuzzy → TM (light review)
- 70-89% fuzzy → TM or MT (full review)
- <70% match → MT + post-edit

**Action:** Implement threshold-based routing. Store post-edited MT in TM (builds asset over time).

### 5. Continuous Localization is Achievable

**Modern Stack:**
- Git integration (GitHub Actions, GitLab CI)
- XLIFF for file exchange
- TMS with API (Transifex, Lokalise, Smartcat, Phrase)
- TM for reuse, MT for new content

**Action:** Start small (automate XLIFF extraction), add TMS integration, then automate merging.

## Implementation Priorities

### For Individual Developers

**Week 1: Learn TMX Basics**
```bash
pip install pythontmx
# Read/write TMX files, experiment with format
```

**Week 2: Alignment (if you have legacy translations)**
- Install LF Aligner or bitext2tmx
- Align 5-10 document pairs
- Review quality, adjust process

**Week 3: Cleaning**
- Run deduplication script on TM
- Identify source=target segments
- Manual review of flagged items

**Week 4: Integration**
- Add XLIFF extraction to build process
- Test round-trip (extract → translate → merge)

### For Teams/Organizations

**Month 1: Audit Current State**
- Inventory existing TMs (where stored, what quality)
- Document current localization process
- Identify pain points

**Month 2: Clean and Consolidate**
- Clean existing TMs (deduplication, quality checks)
- Merge project TMs into master TM
- Export to TMX, store in version control

**Month 3: Pilot Continuous Localization**
- Choose one project for pilot
- Set up GitHub Actions for XLIFF extraction
- Integrate with TMS (Transifex/Lokalise/Smartcat)
- Test end-to-end workflow

**Month 4-6: Scale**
- Roll out to additional projects
- Add MT integration for low-match segments
- Train team on new workflows
- Measure metrics (time-to-translation, match rates)

## Common Mistakes to Avoid

### Mistake 1: Not Version-Controlling TM

**Problem:** TM lives only in CAT tool, no backup, no history

**Solution:** Export TMX to git regularly. Treat TM as source code asset.

### Mistake 2: Trusting Alignment Output Blindly

**Problem:** Alignment tools make mistakes, garbage in TM

**Solution:** Always review alignment output (at least sample). One bad alignment = many bad matches.

### Mistake 3: Ignoring TM Quality

**Problem:** "More TM is better" → bloated TM with errors

**Solution:** Quality > quantity. Clean TM quarterly. Remove outdated segments.

### Mistake 4: Manual XLIFF Handoffs

**Problem:** Email XLIFF files back and forth, merge manually

**Solution:** Automate. Use TMS with API. Let CI/CD handle extraction and merging.

### Mistake 5: Not Leveraging Post-Edited MT

**Problem:** Use MT, human edits, discard edits

**Solution:** Store post-edited MT in TM. Next project reuses improved translations.

## Tool Recommendations by Use Case

| Use Case | Recommended Tools |
|----------|------------------|
| **Programmatic TM manipulation** | PythonTmx (Python library) |
| **Alignment (GUI)** | LF Aligner |
| **Alignment (CLI/automation)** | bitext2tmx |
| **TM cleaning (open source)** | TMOP or DIY scripts |
| **TM cleaning (professional)** | Inten.to, Custom.MT |
| **Continuous localization (cloud)** | Transifex, Lokalise, Smartcat |
| **Continuous localization (self-hosted)** | Custom scripts + OmegaT |
| **MT integration** | Platform MT (Smartcat, Phrase) or API (DeepL, Google) |

## Next: S4 Strategic

S4 will address:
- **Build vs. buy decisions** for enterprises
- **TM governance** (ownership, quality standards, asset valuation)
- **Long-term vendor strategy** (avoiding lock-in, migration paths)
- **ROI calculations** for CAT tool investments
