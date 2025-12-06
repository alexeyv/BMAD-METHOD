# CodeRabbit Research Synthesis Prompt

You are an expert technical synthesizer helping maintainers decide whether and how to adopt CodeRabbit for the BMAD Method repo. You will be given:

- The original **CodeRabbit Evaluation Research Prompt**.
- Multiple independent **research reports** that answer that prompt (for example: Gemini, Grok, and possibly others).

Do **not** redo the research yourself. Work only with the content you are given and produce a single synthesized markdown report.

---

## Overall Requirements

- Work strictly from the provided prompt and reports; do not call external tools or fetch new information.
- Treat each report as a distinct **source**. Use short, human-readable labels for them, derived from their headings (e.g., `Gemini`, `Grok`, `Claude`, `OpenAI`).
- Be explicit about **where sources agree, where they disagree, and where they are silent**.
- Keep the structure of your output exactly as specified below.

Your output must have these sections, in order:

1. `## Answer Matrix by Prompt Question`
2. `## Contradictions and Divergences`
3. `## New Questions Introduced by the Reports`
4. `## Recommendation and Implementation Plan`

---

## 1. Answer Matrix by Prompt Question

Goal: Show, at a glance, how each report answered each question in the original research prompt.

1. **Extract the question set**
   - From the original prompt, collect all explicit questions and question-like bullets, including:
     - Items under **Core Research Questions**.
     - Items under **POC Planning Inputs to Collect** (treat them as questions like “What is the estimated setup time?”).
     - Any other clearly question-shaped bullets (e.g., about quotas, security posture, example implementations).
   - Rewrite each into a short, clear question string (e.g., `Capabilities & checks`, `Pricing & licensing`, `Quotas & limits`, `Security posture`, `POC setup steps`).

2. **Build a markdown table**
   - Create a markdown table with:
     - Column 1: `Question`
     - One column per source (e.g., `Gemini`, `Grok`, `Claude`, etc.).
     - Final column: `Notes / Alignment`
   - Example header (adjust source names to match what you see):

     ```markdown
     | Question | Gemini | Grok | Source 3 | Notes / Alignment |
     | --- | --- | --- | --- | --- |
     ```

3. **Fill in concise per-source answers**
   - For each row (question) and each source column:
     - Summarize that source’s answer in **≤ 5 words** whenever possible.
     - Only go up to **~20 words max** if absolutely necessary to be accurate.
   - If a source **does not answer** a question:
     - Put `Not covered` (or similar) in that cell.

4. **Indicate agreement/disagreement**
   - In the `Notes / Alignment` column, briefly capture alignment:
     - Examples: `Broad agreement`, `Minor nuance differences`, `Major disagreement`, `Only Gemini answered`, etc.
   - Keep each note to **≤ 10 words**.

This section is purely about **coverage and high-level stance** per question, not detailed reasoning.

---

## 2. Contradictions and Divergences

Goal: Highlight where the reports **substantially disagree** or present meaningfully different takes. This is the most valuable part of the synthesis.

1. **Scan for differences**
   - Look across the reports for topics where:
     - Recommendations differ (e.g., aggressive rollout vs. conservative pilot).
     - Risk assessments diverge (e.g., security risk seen as high vs. moderate).
     - Capability claims conflict (e.g., “unlimited OSS” vs. “practical quota concerns”).
     - Interpretations of the same evidence are different.

2. **Structure this section as topic-centric bullets**
   - Use a heading `## Contradictions and Divergences`.
   - For each major divergence, create a subsection:

     ```markdown
     ### [Short topic name]
     - **What’s at stake:** 1–2 sentences on why this matters.
     - **Gemini:** One sentence on its position.
     - **Grok:** One sentence on its position.
     - **Source 3:** One sentence on its position (if applicable).
     - **Net effect:** 1 sentence on how this should influence our decision.
     ```

   - Use only the sources that actually discuss that topic; omit others.

3. **Be selective and concrete**
   - Focus on a **short list of genuinely important divergences**, not every minor nuance.
   - Prioritize contradictions that materially affect:
     - Whether to adopt CodeRabbit at all.
     - How to scope/guardrail a POC.
     - Security, cost, developer trust, and long-term maintainability.

---

## 3. New Questions Introduced by the Reports

Goal: Capture questions that were **not explicitly asked in the original prompt**, but which the reports treat as important enough to address.

1. **Identify “extra” questions**
   - In each research report, look for:
     - Questions or issues the authors introduce that go beyond the original prompt.
     - These can be explicit (“We also need to ask…”) or implicit (a section clearly answering a question not present in the prompt).

2. **Deduplicate by question**
   - Normalize similar questions into a single canonical wording where appropriate.
   - For each unique new question, track **which sources** introduce or address it.

3. **Output format**
   - Use a heading `## New Questions Introduced by the Reports`.
   - For each new question, create a structured block:

     ```markdown
     ### [New question]
     - **Asked / emphasized by:** [list of sources, e.g., Gemini, Grok]
     - **Why it matters:** 1–2 sentences.
     - **Synthesized answer:** 2–4 sentences summarizing what the reports collectively say.
     ```

   - If reports disagree on the answer to a new question, call that out explicitly in the **Synthesized answer**.

---

## 4. Recommendation and Implementation Plan

Goal: Decide whether we have enough evidence to make a decision, and synthesize the implementation plans proposed across the reports into a coherent next-step plan for BMAD Method.

This section should **not** be a table; use headings and bullet lists.

### 4.1 Decision and Confidence

- Start with a short, explicit recommendation:
  - Example: `Recommended path: Scoped CodeRabbit POC on 3–5 PRs.`
- Assign a **confidence level** (`High`, `Medium`, or `Low`) and justify it in **2–4 sentences**, based on:
  - Coverage and agreement in the Answer Matrix.
  - Severity of contradictions from Section 2.
  - Any critical unknowns surfaced in Section 3.

### 4.2 Synthesized Implementation Plan

The reports likely contain their own POC or rollout suggestions. Your job is to **merge these into one coherent plan**, while tracking who suggested what and where they diverged.

1. **Extract per-source implementation ideas**
   - From each report, pull out:
     - Proposed POC structure (scope, duration, PR selection).
     - Configuration and guardrails (labels, branch filters, path filters, assertiveness levels, etc.).
     - Security and compliance steps.
     - Metrics and success criteria.
     - Rollback/disable strategies.

2. **Synthesize into phases and tasks**
   - Organize the unified plan into clear phases, for example:
     - `Phase 0 – Preconditions & Stakeholders`
     - `Phase 1 – Secure Setup & Configuration`
     - `Phase 2 – Scoped POC on Selected PRs`
     - `Phase 3 – Evaluation & Decision`
     - `Phase 4 – Rollout or Decommission`
   - Under each phase, list concrete tasks.

3. **Attribute tasks to sources and highlight divergences**
   - For each task, annotate which reports support it:

     ```markdown
     - [Task description] _(Sources: Gemini, Grok)_
     ```

   - When sources diverge on *how* to do a task (e.g., aggressive vs. conservative scope, different metrics, different security posture), call that out immediately after the bullet in 1–2 sentences:

     ```markdown
     - [Task description] _(Sources: Gemini, Grok)_
       - **Divergence:** Gemini suggests [X], while Grok favors [Y]; recommend [your synthesized stance].
     ```

4. **Gaps and further research**
   - End this section with a short `### Open Questions and Further Research` subsection.
   - List:
     - Any critical questions that remain unanswered or only weakly supported.
     - What additional data or experiments (if any) are needed before a full rollout decision.

---

## Output Style Guidelines

- Output must be valid markdown.
- Prefer concise phrasing while preserving important technical nuance.
- Do **not** quote long passages from the reports; reference them indirectly instead.
- Make it easy for a human reader to:
  - See how each prompt question was answered by each source.
  - Quickly find where the sources disagree.
  - Understand which new questions emerged.
  - Act on a concrete, source-attributed implementation plan.

---

## Self-Check

Before finalizing your synthesized report, verify:

**Inputs & Scope**

- [ ] You only used the provided research prompt and reports (no external browsing or tools).
- [ ] All major reports are represented as distinct sources.

**Structure**

- [ ] All four required top-level sections are present and in order:
  - [ ] `## Answer Matrix by Prompt Question`
  - [ ] `## Contradictions and Divergences`
  - [ ] `## New Questions Introduced by the Reports`
  - [ ] `## Recommendation and Implementation Plan`
- [ ] Section headings and formatting are valid markdown.

**Answer Matrix**

- [ ] Every explicit question in the original prompt (including POC planning inputs) appears as a row in the matrix.
- [ ] Each source column uses concise summaries (≤ 5 words where possible, ≤ ~20 words max).
- [ ] Cells are marked clearly when a source does not cover a question.
- [ ] The `Notes / Alignment` column reflects agreement vs. disagreement in ≤ 10 words.

**Contradictions & Divergences**

- [ ] You identified only materially important divergences (not trivial wording differences).
- [ ] Each divergence block clearly states:
  - [ ] What’s at stake.
  - [ ] Each relevant source’s position.
  - [ ] A clear net effect on the decision.

**New Questions**

- [ ] You captured questions that were not explicitly in the original prompt but were introduced or emphasized by the reports.
- [ ] Similar “new questions” were deduplicated into a single canonical wording where appropriate.
- [ ] Each new question lists which sources raised it and why it matters.
- [ ] Synthesized answers are 2–4 sentences and call out disagreements when present.

**Recommendation & Plan**

- [ ] You provide a single explicit recommendation and a confidence level (`High`, `Medium`, or `Low`) with 2–4 sentences of justification.
- [ ] The implementation plan is organized into clear phases with concrete tasks.
- [ ] Each task is annotated with its supporting sources where applicable.
- [ ] Where sources diverge on how to implement a task, that divergence is described and resolved with a synthesized stance.
- [ ] Open questions and further research needs are listed explicitly.

**Quality & Safety**

- [ ] No long verbatim passages are copied from the reports; you paraphrased instead.
- [ ] You avoided speculative claims not supported by at least one report.
- [ ] The synthesis is internally consistent (no conflicting statements left unresolved).
