# Survey of Software - Claude Skill

Systematic software library research using the Four-Pass Survey (4PS) methodology.

## What It Does

This skill connects Claude to the Survey of Software research library at https://research.modelcitizendeveloper.com/

**When you ask about library/framework selection:**
- Fetches relevant completed surveys (135+ topics covered)
- Synthesizes recommendations with trade-offs
- When topics aren't covered yet, runs rapid discovery research live
- Tailors recommendations to your specific requirements

## Installation

### Option 1: Upload to Claude.ai
1. Package this folder as a ZIP file: `zip -r survey-of-software.zip survey-of-software/`
2. In Claude.ai, go to **Settings → Skills**
3. Click **Upload skill**
4. Upload the ZIP file

### Option 2: Use in Claude Code
Place this folder in your `~/.claude/skills/` directory (or wherever your Claude Code skills are configured)

## Example Queries

Try asking Claude:
- "What's the best graph analysis library for Python?"
- "Compare LLM orchestration frameworks for a RAG pipeline"
- "What should I use for fuzzy search?"
- "Which frontend framework should I choose for a new project?"

## How It Works

The skill uses two strategies:

### For Covered Topics (135+ surveys)
1. Maps your question to the taxonomy
2. Fetches the relevant survey from the research site
3. Synthesizes a recommendation with decision frameworks and trade-offs

### For Uncovered Topics
1. Identifies the gap in the research
2. Offers to run S1 (Rapid Discovery) research live
3. Performs web research, evaluates options, presents findings
4. Invites contribution back to the open research project

## Scope

Currently covers **1.xxx series (libraries)** including:
- Algorithms & Data Structures (1.001-1.049)
- Compression, Encoding, Crypto (1.050-1.069)
- Machine Learning (1.070-1.079)
- Image Processing & Geometry (1.080-1.099)
- Text & Document Processing (1.100-1.109)
- Frontend & UI (1.110-1.119)
- Simulation & Business (1.120-1.139)
- Language Learning & CJK (1.140-1.169)
- Translation (1.170-1.179)
- LLM & AI Stack (1.200-1.219)
- Calendar, Social, Messaging (1.220-1.239)
- Civic & Government Data (1.300-1.309)

Future: Standards (2.xxx) and Applications (3.xxx) series

## Attribution

Survey of Software by Model Citizen Developer
Four-Pass Survey (4PS) methodology
Licensed under CC BY 4.0

Research site: https://research.modelcitizendeveloper.com/
GitHub: https://github.com/modelcitizendeveloper/survey-of-software
