# 23: Research Value Case Study - Factumerit Platform Decision

**Date**: 2025-12-22
**Type**: Meta-analysis
**Theme**: Why research before building

---

## The Question

"Which SDK should I use for my Vikunja bot?"

## What We Would Have Done Without Research

Built on Slack (existing POC), fought with:
- Mobile UX issues
- TOS restrictions
- Gated admin API
- Per-user costs at scale
- "Join my workspace" friction for new users

## What Research Revealed

**3.023 Team Chat** → Matrix exists, has bridges, E2EE, self-hostable

**1.230 Open Social Networks** → Matrix is federated protocol, not just a product

**1.234 Bot SDK Frameworks** → matrix-nio is mature, Python, async

**Hands-on exploration** → Vikunja community already on Matrix

## The Unlock: Federation as Distribution

Without research: "Sign up for my Slack workspace to try my bot"

With research: "DM @taskbot:factumerit.com from wherever you are"

**Zero friction distribution to an existing community already on Matrix.**

The Vikunja Matrix room becomes a distribution channel, not a support burden.

## Research ROI

| Investment | Return |
|------------|--------|
| ~4 hours research | Distribution model change |
| 9 documents | Platform decision with confidence |
| $0 | Avoided $100/mo Element Cloud (wrong path) |

## Lesson

The valuable output wasn't "use matrix-nio" (the SDK choice).

It was "Matrix federation means your target community can try your product without leaving their existing platform."

Research answers questions you didn't know to ask.

---

## Related

- [1.230 Open Social Networks Research](../../research/1.230-open-social-networks/)
- [1.234 Bot SDK Frameworks Research](../../research/1.234-bot-sdk-frameworks/)
- [3.023 Team Chat Research](../../research/3.023-team-chat/)
- [21-MATRIX_PLATFORM_RECOMMENDATION.md](21-MATRIX_PLATFORM_RECOMMENDATION.md)
