# CodeRabbit Research Executive Summary

## Executive Summary
CodeRabbit is a mature, agentic AI code review platform that combines LLM reasoning with AST parsing to provide context-aware feedback. It offers a **free "Pro" tier for public open-source repositories**, making it economically attractive for the BMAD Method project. Key capabilities include deep context retrieval (RAG), intent verification against issue trackers, and automated documentation. However, a significant **Remote Code Execution (RCE) vulnerability in 2025** highlights a non-trivial supply-chain risk that requires strict permission scoping.

## To Use or Not to Use?
**Recommendation: PROCEED WITH A SCOPED PILOT (POC).**

Do not fully adopt immediately. The potential value (automating detailed reviews, catching logic bugs) outweighs the risks *only if* strictly controlled. A 2-week pilot on a targeted subset of PRs will validate the "signal-to-noise" ratio and security comfort level before a broader rollout.

## Implementation Plan

### Phase 1: Secure Setup (Days 1-2)
1.  **Install & Scope**: Install the CodeRabbit GitHub App. **Crucially, limit access to the `bmad` repository only**, reducing the blast radius of any potential compromise.
2.  **Configuration**: Create a `.coderabbit.yaml` file to enforce "Silent Mode":
    *   Set profile to `"chill"` (reduces noise).
    *   **Gating**: Configure `reviews.auto_review.labels: ["coderabbit-review"]` so the bot ignores all PRs by default.
    *   **Path Filters**: Exclude sensitive paths like `.github/workflows` and `dist/`.

### Phase 2: Execution (Days 3-10)
1.  **Select Candidates**: Identify 3-5 active PRs (mix of feature, bugfix, and docs).
2.  **Trigger**: Apply the `coderabbit-review` label to these PRs.
3.  **Train**: Maintainers should reply to bot comments to test its "Learning" capability (e.g., "We prefer snake_case here").

### Phase 3: Evaluation (Days 11-14)
1.  **Measure**: Target an **Actionable Rate > 20%** (comments leading to changes).
2.  **Decide**: If the bot catches non-trivial bugs and maintainers feel reduced load, move to Phase 4 (required non-blocking checks).

## Contradictions to Beware Of

1.  **Security Risk & Remediation**:
    *   *The Conflict:* Reports confirm a 2025 RCE exploit. Gemini and Grok frame it as "resolved/safe" due to new sandboxing. Codex advises treating it as a "high-severity risk" due to limited transparency on the patch.
    *   *Action:* Trust but verify. Use least-privilege installation and do not grant Organization-wide access.

2.  **Performance Accuracy**:
    *   *The Conflict:* Grok cites "95% bug detection" and "46% runtime accuracy." Codex explicitly warns that **no independently verifiable benchmarks exist**.
    *   *Action:* Ignore the marketing numbers. Use the POC to establish your own baseline for false positives.

3.  **Gating Mechanics**:
    *   *The Conflict:* Reports diverge on how to scope the pilot (manual triggers vs. invite-only repos).
    *   *Action:* Gemini’s proposal of **Label-based Gating (`reviews.auto_review.labels`)** is the most robust and least disruptive method for a busy OSS repo.
