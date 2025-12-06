# CodeRabbit Research: Conclusions

## 1. Pilot Decision
Proceed with a scoped POC on the `bmad` repo using the "chill" profile (verify exact YAML key, commonly `reviews.profile: chill`).

## 2. Implementation Strategy

## 2. Implementation Strategy

### 2.1 The "Automated Gatekeeper" Model
*   **Philosophy:** CodeRabbit acts as the **First Line of Defense**. The Contributor must address bot findings *before* the Maintainer spends time reviewing.
*   **The "No Bullshit" Guardrail:** To prevent the "wall of bullshit" (Actionable Rate < 20%) without a human filter, we must aggressively tune for **High Precision**.
    *   **High Confidence Threshold:** We will configure the bot to suppress low-confidence "nitpicks."
    *   **Summaries Over Spam:** We prioritize "High Level Summaries" and "Walkthroughs" over line-by-line comments for subjective issues.
*   **Workflow:**
    1.  Contributor opens PR.
    2.  Bot automatically runs (via Label or Monitor).
    3.  Contributor resolves Bot feedback (fix or dismiss).
    4.  **Only then** does the Maintainer review the final state.

### 2.2 Configuration Strategy
*   **Profile:** **"Chill"** (`reviews.profile: chill`) to minimize volume.
*   **Non-Blocking:** `reviews.request_changes_workflow: false`. The bot provides *counsel*, not *blockers*. We don't want a dumb bot blocking a smart human.
*   **Assessment:** `reviews.review_status: true`. The contributor *needs* to see the bot's status to know they are being reviewed.
*   **Customization:** We will use `path_filters` and `suppress_low_confidence` settings to ensure only high-signal comments get through.

## 3. Success Criteria
*   **Workflow:** Contributor acts as the first filter (filtering false positives) before Maintainer review.
*   **Actionable Rate:** **Target: ~50%**.
    *   *Pivot Trigger:* If the pilot data shows we are closer to 20% (1-in-5), we will **PIVOT** the workflow. The "Automated Gatekeeper" model fails at low precision. We will not speculate further until we have real data from the calibration phase.
*   **Quality:** Must catch at least 1 severe issue per 10 PRs.

## 4. Risk Awareness
*   **Downtime:** Monitoring shows frequent outages (e.g., 12 in Nov 2025) and throttling issues.
*   **Security (RCE) mitigation:**
    *   **Reality Check:** We likely cannot "Deny" specific permissions (like `Contents: Write`) if the GitHub App manifest requires them for installation.
    *   **Mitigation:** We must rely on **Strict Branch Protection Rules**. The bot user must be treated as untrusted; it must **not** be allowed to bypass branch protection or merge to `main` without human approval.
*   **Noise:** We view "noise" as a configuration problem we own. We will treat out-of-the-box defaults as "mostly bad/irrelevant ideas" and rely on our own custom configuration to signal.
*   **Support:** Slow response times are an acknowledged trade-off we accept for the pilot.

## 5. System Limitations (Static vs. Dynamic)
*   **Static-Focused:** CodeRabbit is a **Static Analysis + LLM** wrapper. It runs standard linters (ESLint, Biome) and analyzes code text.
*   **No Custom Builds:** It is **NOT** a CI runner. We cannot ask it to "build this Dockerfile" or "compile this CMake target" within its own environment.
*   **Future Bridge (MCP):** The "Static" limitation may be mitigated in the future by the **Model Context Protocol (MCP)**, which could allow the bot to query our own local context servers, though this is out of scope for the initial POC.

## 6. Deep Reasoning Limitation
*   **Not an Adversarial Auditor:** CodeRabbit is optimized for **Diff Analysis** (RAG + Context). It is likely **underpowered** for "Deep Whole-Repo Adversarial Reasoning".
*   **Context Slicing:** It slices the repo to fit token limits, which may prevent it from seeing deep connections between untouched modules.

## 7. Compute Bottleneck: The Prompt Validation Reality
*   **Problem:** Validating prompts (Meta-Review) requires massive compute (regression testing, eval loops against test sets).
*   **Classification:**
    1.  **CodeRabbit Tasks:** "Soft Critique" (Heuristic style checks, safety).
    2.  **CI/CD Tasks:** "Hard Evals" (Regression testing, promptfoo).
*   **Plan:** Use CodeRabbit for style/safety, use CI for logic.

## 8. Shift-Left / CLI Workflow (The Orthogonal Loop)
*   **Concept:** CodeRabbit offers a **CLI** that can run reviews locally on staged changes.
*   **Agentic Integration:** This enables a powerful "Private Loop" where your local agent (Claude Code, Cursor, etc.) can:
    1.  Write code.
    2.  Run `coderabbit review --diff` locally.
    3.  Ingest the feedback and fix issues *before* pushing to the shared repo.
*   **Value:** This completely bypasses the "Contributor Shielding" and "Public Noise" risks. It turns CodeRabbit into a private linter for the agent.
*   **Action:** We will test this CLI workflow as part of the POC. If it works, it might be *more* valuable than the PR bot for core maintainers.

## 9. Prior Art & Inspiration Sources
*   **Mature Config Examples:** We will mine `calcom/cal.com` and `NVIDIA-NeMo` for best practices.
*   **Validation Step:** We must **verify every config key** sourced from these examples against the official CodeRabbit schema options to prevent invalid configuration errors.
*   **Tooling:** `Promptfoo` (Open Source) for the hard evals.
*   **Concepts:** LLM-as-a-Judge (arXiv:2306.05685).

## 10. Assumptions
*   **Measurement Hypothesis:** We assume we can effectively measure success by prompting an LLM to analyze the PR threads at the end of the pilot.
