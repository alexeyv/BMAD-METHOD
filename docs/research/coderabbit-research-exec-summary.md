## Executive Recommendation

- **Use, but only via a tightly scoped POC.** CodeRabbit is likely valuable enough to test on BMAD, but security history, unclear quotas, and unproven signal quality mean it should **not** be broadly adopted or made merge‑blocking yet.
- Treat the POC as a **decision experiment**: if it clears a high bar (actionable comments, unique bugs found, no security/regression issues), expand; otherwise keep it opt‑in or turn it off.

## Implementation Plan (Short Version)

- **Phase 0 – Preconditions**
  - Name a POC owner + 2–3 maintainers.
  - Agree on success bars **up front** (e.g., ≥60–70% comments actionable, at least one non‑trivial bug caught, no incidents).

- **Phase 1 – Secure Setup**
  - Security/legal review: Trust Center + full Kudelski RCE write‑up; decide acceptable risk.
  - Install GitHub App on **BMAD repo only**, document all requested scopes.
  - Add conservative `.coderabbit.yaml`: `profile: "chill"`, `request_changes_workflow: false`, path filters excluding generated code and `.github/workflows/**`, and username‑based skips for bots.

- **Phase 2 – Scoped Pilot**
  - Run CodeRabbit on **3–5 chosen PRs** (feature, docs, bugfix, ideally one touching “interesting” logic).
  - Prefer **label‑gated** reviews (e.g., `coderabbit-review`); if unavailable, use `@coderabbitai` or a dedicated test branch.
  - Keep all checks **non‑blocking**; humans review first, then compare with CodeRabbit.
  - Optionally add 1–2 **advisory** agentic pre‑merge checks (secrets/TODOs/docs) to see how they behave.

- **Phase 3 – Evaluate & Decide**
  - Measure: comment volume, % of comments leading to changes, % obviously wrong/noisy, overlap with existing CI, rough review time.
  - Capture qualitative sentiment (usefulness, trust, cognitive load).
  - Confirm no anomalous bot actions or outages.
  - Decide:
    - **Expand cautiously** if it meets the higher bar.
    - **Keep opt‑in** if only mildly useful.
    - **Disable and document** if noisy, risky, or fragile.

## Key Contradictions to Beware Of

- **Quotas & limits**
  - Gemini gives specific limits and “summary only” behavior for large PRs; Codex says **no concrete numbers are visible** in public static docs.
  - Treat Gemini’s numbers as **hypotheses**, and **explicitly test** large‑ish PRs and higher usage during the POC instead of trusting them.

- **Security posture after the 2025 exploit**
  - Gemini: RCE incident is remediated via sandboxing, scoped write, zero retention → **risk is manageable** with good config.
  - Codex: details of the exploit, fixes, and validation are **not fully visible**; treats it as **high‑severity** until verified.
  - Operate under Codex’s **more conservative** model: least privilege, strong branch protection, explicit monitoring of the bot, and readiness to disable immediately.

- **Label gating and triggers**
  - Gemini treats label‑based auto‑review as a **first‑class, documented** control.
  - Codex couldn’t confirm label gating from static docs; assumes manual commands/branch scoping may be required.
  - Plan to use labels, but design the POC so it **still works** with manual `@coderabbitai` triggers or test branches if label support is weaker than expected.

- **Success thresholds**
  - Gemini’s bar: **>20% actionable**, **<10% false positives** is “good”.
  - Codex’s bar: **60–70% actionable** plus at least one non‑trivial bug/design issue caught to justify broader rollout.
  - Use Gemini’s bar as **“worth continuing to experiment”**, and Codex’s bar as the gate for any **real adoption or merge‑gating**.

- **Depth of agentic integration**
  - Gemini focuses on CodeRabbit as a smart PR reviewer with context engineering and local learnings.
  - Codex emphasizes **MCP + CLI/IDE + multi‑agent** workflows where CodeRabbit is a central backend.
  - For BMAD’s first step, keep CodeRabbit **PR‑only and advisory**; do **not** wire it deeply into your agentic stack until it has proven safe, stable, and genuinely valuable in the pilot.

