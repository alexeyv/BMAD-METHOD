# CodeRabbit Research: Conclusions

## 1. Pilot Decision
Proceed with a scoped POC on the `bmad` repo using the "chill" profile.

## 2. Implementation Strategy
*   **Silent Calibration Phase:** The first few PRs will be processed silently. The bot should NOT post comments publicly.
*   **Validation Gate:** We only expose the bot to contributors after verifying it achieves a decent actionable rate (approx. 50%) internally. We will not burden contributors with noise during the calibration phase.
*   **Trigger:** Manual label triggers (`coderabbit-review`).
*   **Configuration:** We will **not** rely on defaults. Success correlates with heavy customization using `.coderabbit.yaml`, specific `path_filters`, and contextual instructions (e.g., extracting rules from `CLAUDE.md`).

## 3. Success Criteria
*   **Workflow:** Contributor acts as the first filter (filtering false positives) before Maintainer review.
*   **Actionable Rate:** Target ~50%. (20% is too low).
*   **Quality:** Must catch at least 1 severe issue per 10 PRs.

## 4. Risk Awareness
*   **Downtime:** Monitoring shows frequent outages (e.g., 12 in Nov 2025) and throttling issues.
*   **Security (RCE) & Mitigation:** The 2025 RCE (Rubocop sandbox escape) is considered a "past tense" lesson, but highlights the risk of the large attack surface (40+ tools).
    *   **Mitigation:** We treat this as a signal to **DENY `Contents: Write` permissions**. CodeRabbit will be restricted to **Comments Only** (Read Code + Write PR Comments). It will have NO ability to commit to `main` or push fixes.
*   **Noise:** We view "noise" as a configuration problem we own. We will treat out-of-the-box defaults as "mostly bad/irrelevant ideas" and rely on our own custom configuration to signal.
*   **Support:** Slow response times are an acknowledged trade-off we accept for the pilot.

## 5. System Limitations (Static vs. Dynamic)
*   **Static-Focused:** CodeRabbit is a **Static Analysis + LLM** wrapper. It runs standard linters (ESLint, Biome) and analyzes code text.
*   **No Custom Builds:** It is **NOT** a CI runner. We cannot ask it to "build this Dockerfile" or "compile this CMake target" within its own environment. It cannot run custom dynamic analysis.
*   **CI Integration:** It *can* analyze logs from *our* GitHub Actions failures, but the build execution must happen on our infrastructure, not theirs.

## 6. Deep Reasoning Limitation
*   **Not an Adversarial Auditor:** CodeRabbit is optimized for **Diff Analysis** (RAG + Context). It is likely **underpowered** for "Deep Whole-Repo Adversarial Reasoning" (e.g., "burn 100k tokens to find obscure logic bugs").
*   **Context Slicing:** It slices the repo to fit token limits, which may prevent it from seeing deep connections between untouched modules.

## 7. Compute Bottleneck: The Prompt Validation Reality
*   **Problem:** Validating prompts (Meta-Review) requires massive compute (regression testing, eval loops against test sets).
*   **Classification:**
    1.  **CodeRabbit Tasks:** Static checks, heuristic critique ("Does this look like a prompt?"), safety checks. (Cheap, single-pass).
    2.  **CI/CD Tasks:** Regression evals, golden set validation, iterative optimization. (Expensive, multi-pass).
*   **Plan:** We will use CodeRabbit for the "Soft Critique" and our own CI for the "Hard Evals".

## 8. Prior Art & Inspiration Sources
*   **Mature Config Examples:** We will mine `calcom/cal.com` (App), `NVIDIA-NeMo` (Research), and `Kyverno` (Policy) for best practices.
*   **Tooling:** `Promptfoo` (Open Source) is the industry standard for CLI-based prompt testing (likely candidate for our CI layer).
*   **Concepts:**
    *   **LLM-as-a-Judge:** (arXiv:2306.05685) Validates our measurement hypothesis.
    *   **Constitutional AI:** (Anthropic pattern) Adapting this pattern for our "Prompt Validation" rules.

## 9. Assumptions
*   **Measurement Hypothesis:** We assume we can effectively measure success by prompting an LLM to analyze the PR threads at the end of the pilot. This method is unproven.
