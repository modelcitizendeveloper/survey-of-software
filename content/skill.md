---
title: "Claude Skill"
weight: 9999
---

# Survey of Software - Claude Skill

Let Claude consult this research library directly in your conversations. The skill enables Claude to fetch surveys, synthesize recommendations, and run live research when topics aren't covered yet.

## What It Does

When you ask Claude about library or framework selection:
- **Fetches completed surveys** (135+ topics) from this research library
- **Synthesizes recommendations** with decision frameworks and trade-offs
- **Runs rapid discovery research** live when topics aren't covered yet
- **Tailors recommendations** to your specific requirements and constraints

## Installation

### Option 1: Upload to Claude.ai

1. **Download the skill:**
   - **[⬇️ Download survey-of-software.zip](https://github.com/modelcitizendeveloper/survey-of-software/releases/download/v1.0.0/survey-of-software.zip)** (8.7 KB)

2. **Upload to Claude:**
   - Go to [claude.ai](https://claude.ai) → **Settings → Skills**
   - Click **Upload skill**
   - Upload the downloaded ZIP file

3. **Start using:**
   - Create a new conversation in Claude.ai
   - The skill is now available for Claude to use automatically

<details>
<summary>Alternative: Package from source</summary>

```bash
git clone https://github.com/modelcitizendeveloper/survey-of-software.git
cd survey-of-software/skill
zip -r ../survey-of-software.zip .
```
</details>

### Option 2: Use in Claude Code

If you're using the [Claude Code CLI](https://github.com/anthropics/claude-code):

```bash
# Clone the repository
git clone https://github.com/modelcitizendeveloper/survey-of-software.git
cd survey-of-software

# Copy skill files to Claude Code skills directory
mkdir -p ~/.claude/skills/survey-of-software
cp skill/* ~/.claude/skills/survey-of-software/
```

The skill will be automatically available in all Claude Code sessions.

## Example Queries

Once installed, try asking Claude:

- "What's the best graph analysis library for Python?"
- "Compare LLM orchestration frameworks for a RAG pipeline"
- "What should I use for fuzzy search?"
- "Which frontend framework should I choose for a new project?"
- "I need a Chinese word segmentation library - what are my options?"
- "What's the current state of vector databases?"
- "Compare state management libraries for React"

## How It Works

The skill uses two strategies depending on whether the topic has been researched:

### For Covered Topics (135+ surveys)

1. Maps your question to the research taxonomy
2. Fetches the relevant survey from this site
3. Synthesizes a recommendation with:
   - Decision framework (when to use what)
   - Trade-off analysis (what you gain/lose with each choice)
   - Migration complexity considerations

### For Uncovered Topics

1. Identifies the gap in the research library
2. Offers to run **S1 (Rapid Discovery)** research live in your conversation
3. Performs web research, evaluates options, presents findings following the survey format
4. Invites contribution back to this open research project (CC BY 4.0)

### Collaborative Four-Pass Model

The skill implements the [Four-Pass Survey (4PS) methodology](/survey/method/):

- **S1: Rapid Discovery** - Claude performs this automatically (70-80% confidence)
- **S2: Comprehensive Analysis** - Available via deep research for benchmarks and detailed comparison
- **S3: Need-Driven Discovery** - You provide your specific requirements, Claude evaluates fit
- **S4: Strategic Selection** - You provide strategic context, Claude assesses long-term viability

Together, all four passes produce complete, tailored recommendations for your specific situation.

## What's Covered

The skill currently covers the **1.xxx series (libraries)**:

- **Algorithms & Data Structures** (1.001-1.049): Sorting, searching, graphs, strings, collections
- **Compression & Crypto** (1.050-1.069): Compression, serialization, hashing, encryption
- **Machine Learning** (1.070-1.079): Dimensionality reduction, forecasting, gradient boosting, deep learning
- **Image & Geometry** (1.080-1.099): Image processing, QR codes, spatial algorithms, collision detection
- **Text Processing** (1.100-1.109): PDF generation, document parsing, markdown, code formatting
- **Frontend & UI** (1.110-1.119): Frameworks, state management, CSS, components, build tools, testing
- **Simulation & Business** (1.120-1.139): Discrete event, Monte Carlo, financial simulation, CRM
- **Language Learning & CJK** (1.140-1.169): Classical languages, spaced repetition, Chinese NLP, character databases
- **Translation** (1.170-1.179): Machine translation, alignment, terminology
- **LLM & AI Stack** (1.200-1.219): Orchestration, agents, vector databases, RAG, evaluation, fine-tuning
- **Calendar & Social** (1.220-1.239): CalDAV, open social protocols, bot frameworks
- **Civic & Government** (1.300-1.309): Public finance, government data, budget parsing, procurement

Future series: **Standards** (2.xxx) and **Applications** (3.xxx)

## Source Code

The skill is open source (CC BY 4.0):
- **Skill repository:** [github.com/modelcitizendeveloper/survey-of-software](https://github.com/modelcitizendeveloper/survey-of-software)
- **Research content:** Browse this site or view source in `/content/survey/`

## Attribution

When Claude presents findings using this skill, it will cite:

> Source: [Survey of Software](https://research.modelcitizendeveloper.com/) by Model Citizen Developer. Four-Pass Survey (4PS) methodology. Licensed under CC BY 4.0.

## Questions or Issues?

- **Skill not working?** Check that it's uploaded correctly in Settings → Skills
- **Want to contribute research?** The project is open source - PRs welcome
- **Found an error in a survey?** Open an issue on [GitHub](https://github.com/modelcitizendeveloper/survey-of-software/issues)
