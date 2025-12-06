## CodeRabbit Research Capsule

This directory contains a self-contained research capsule for evaluating **CodeRabbit** on the BMAD Method repo.

### Files

| File | Description |
|------|-------------|
| `research-prompt.md` | Original research brief (questions, goals, deliverables) |
| `research-gemini.md` | Research report from Gemini |
| `research-grok.com` | Research report from Grok |
| `research-codex.md` | Research report from Codex |
| `research-synthesis-prompt.md` | Prompt that defines how to synthesize the reports |
| `research-synthesis-adversarial-review-prompt.md` | Prompt for adversarial/critical review of synthesis |
| `exec-summary-prompt.md` | Prompt for generating executive summaries |
| `research-synthesis-codex.md` | Synthesis by Codex (answer matrix, contradictions, POC plan) |
| `research-synthesis-opus.md` | Synthesis by Opus (answer matrix, contradictions, POC plan) |
| `research-exec-summary-codex.md` | Executive summary by Codex |
| `research-exec-summary-opus.md` | Executive summary by Opus |

### Flow

```
research-prompt.md
        ↓
┌───────┼───────┐
↓       ↓       ↓
Gemini  Grok   Codex  (individual reports)
└───────┼───────┘
        ↓
research-synthesis-*.md  (synthesized analysis)
        ↓
research-exec-summary-*.md  (actionable summary)
```

