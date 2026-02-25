# Tech-Spec Template Review: Evolved Template vs Gemini & Grok Research

**Date:** 2026-02-24
**Template under review:** `src/bmm/workflows/bmad-quick-flow/quick-dev2/tech-spec-template.md`
**Research inputs:**
- `_experiment/ideal-spec-gemini.md` — 199-line deep-dive, 96/100 confidence score
- `_experiment/ideal-spec-grok.md` — 67-line concise analysis

**Review method:** 4-agent parallel analysis across 18 aspects, each agent specializing in a domain (YAML/metadata, core sections, supplementary sections, structural concerns).

---

## Summary Recommendation Table

| # | Aspect | Verdict | Action Required |
|---|--------|---------|-----------------|
| 1 | Word count guidance | **ADD** | Add 400–1,000 word target as HTML comment |
| 2 | YAML frontmatter basics | **ADD + FIX** | Add `type` field, change status default to `draft` |
| 3 | target_models in YAML | **SKIP** | Do not add — over-engineering |
| 4 | context_dependencies vs Code Map | **ADD + KEEP** | Add `context` YAML array for standards docs; keep body Code Map for source files |
| 5 | Intent / Problem framing | **KEEP** | "Problem" framing is superior for granular stories |
| 6 | Standalone Solution section | **KEEP** | Bridges Problem→Boundaries, minimal word cost |
| 7 | Boundaries & Constraints | **KEEP** | Strongest section — no changes |
| 8 | Context & Code Map structure | **CHANGE** | Annotate paths with roles: `` `file` -- relevance `` |
| 9 | I/O & Edge-Case Matrix | **KEEP + TWEAK** | Rename column "Expected Outcome" → "Expected Output / Behavior" |
| 10 | Tasks format (file-anchored) | **KEEP + SOFTEN** | Soften "one task per file" to a preference |
| 11 | Acceptance Criteria section | **KEEP + CLARIFY** | Add anti-redundancy guidance vs I/O Matrix |
| 12 | Technical Decisions | **RENAME + OPTIONAL** | → "Design Rationale", mark optional |
| 13 | Golden Examples | **KEEP + CONSTRAIN** | Make optional, add 5–10 line size limit |
| 14 | Verification | **MAKE MANDATORY** | Broaden to include manual-check fallback |
| 15 | Spec Change Log | **DISPUTED** | supplementary-analyst: keep; structural-analyst: remove |
| 16 | Notes section | **REMOVE** | Catch-all undermines structural discipline |
| 17 | Over-specification guardrails | **CHANGE** | Comments insufficient — needs structural enforcement |
| 18 | Total section count (12 vs 6) | **RESTRUCTURE** | Proposed: 12 → 7 sections (3 conditional). Depends on open decisions. |

## Cross-Report Comparison Table

| Aspect | Gemini Recommends | Grok Recommends | Template Does | Delta |
|--------|------------------|-----------------|---------------|-------|
| Word count | 400–800 words, strict | 600–1,200 words | No guidance | **Gap.** No ceiling or floor stated. |
| YAML frontmatter | task_id, type, status, target_models, context_dependencies | Not detailed | title, slug, created, status | Missing `type`. Has `slug` instead of `task_id` (better). |
| target_models | Yes — model array for orchestration | Not mentioned | Not present | Gap (minor). Over-engineering for current flow. |
| context_dependencies | YAML field for dynamic RAG injection | RAG mentioned but not in frontmatter | Body-only (Context & Code Map) | **Intentional divergence.** Loses machine-parseable hook. |
| Intent / Problem | "Intent and Business Value" | "Objective anchors intent" | "Problem — what is broken or missing, and why does it matter?" | Template is more concrete for granular stories. |
| Solution | Not a standalone section | Not explicit | Standalone: "the what, not the how" | **Template adds this.** Bridges Problem→Boundaries. |
| Boundaries | Three-tier (Always/Ask First/Never) — "single most critical innovation" | "Non-goals + constraints" (less prescriptive on tiers) | Three tiers with HTML comment explaining each | **Fully aligned with Gemini.** |
| Context & Code Map | Named categories (Entry Point, Schemas, Tests) | "Surface relevant files via RAG" | Flat bullet list, agent-populated | Slightly less structured than Gemini's named categories. |
| I/O & Edge-Case Matrix | Table: Scenario / Input / Expected Output / Error Handling | "Edge matrix kills 80% of hallucinations" | Table: Scenario / Input-State / Expected Outcome / Error Handling | **Fully aligned.** Column names differ trivially. |
| Tasks / Execution Plan | Numbered checklist, no file-path structure | Not detailed | Checklist with `file` — action — rationale | **Template improves on both.** |
| Acceptance Criteria | Not separate (folded into I/O matrix + DoD) | "AC + examples make success verifiable" / "Gherkin AC powerful when embedded" | Separate section, Given/When/Then | **Template adds this.** Grok-endorsed. |
| Technical Decisions | Not present | Not present | "Why this approach, not how to code it" | **Template addition.** |
| Golden Examples | Not mentioned | "Concrete examples reduce hallucination more than any other technique" | Before/after diffs, sample outputs, reference implementations | **Aligned with Grok's spirit.** |
| Verification / DoD | Mandatory — copy-pasteable terminal commands | "Testing/DoD: turns spec into executable contract" | Marked **optional** | **Partial gap.** Both reports treat as essential. |
| Spec Change Log | Not mentioned | Not mentioned | Appended by review loop with KEEP instructions | **Template innovation.** |
| Notes | Not mentioned | Not mentioned | Catch-all for additional context | **Template addition.** Both reports stress every token must earn its place. |
| Over-spec guardrails | Strongest theme — "over-specifying constrains LLM latent space" | "Over-specification hurts more than under-specification once RAG is available" | HTML comments: "the what, not the how" | **Aligned in spirit.** Comments may be insufficient as sole guardrail. |
| Section count | 6 sections | ~6 implied | 12 sections | **Potential concern.** Double the research recommendations. |

---

## Detailed Analysis by Aspect

### #1: Word Count Guidance

**Analyst:** yaml-analyst
**Verdict:** ADD — target 400–1,000 words as HTML comment

**Gemini says:** 400–800 words, strict. Informed by "Context Rot" research and the U-shaped performance curve of transformer architectures. Even with 1–2M token context windows, instruction-following fidelity degrades significantly when parsing dense, unstructured text.

**Grok says:** 600–1,200 words. Below 600 = ambiguity; above 2,000 = context dilution or contradictions.

**Template does:** No explicit guidance anywhere.

**Recommendation detail:**
- 400 lower bound is correct — below that you can't cover intent, boundaries, edge cases, and tasks meaningfully.
- 800 upper bound (Gemini) is too tight for the template's 12-section structure. Even with terse writing, filling Boundaries, I/O Matrix, Tasks, AC, Technical Decisions, and Golden Examples routinely hits 800.
- 1,200 upper bound (Grok) is too generous — at 1,200 words "Lost in the Middle" effects become measurable.
- **1,000 is the sweet spot.** Enough room for all sections; optional sections (Notes, Verification) mean simpler specs land at 500–700 naturally.

**Implementation:** Add an HTML comment below the YAML block:
```markdown
<!-- Target: 400–1,000 words. Below 400 = ambiguous. Above 1,000 = context rot risk. -->
```
Do NOT put in YAML — word count is guidance for the spec-writing agent, not machine-parseable metadata.

**Note:** If the section count is restructured from 12 to 7 (#18), the ceiling could tighten to 800, aligning with Gemini.

---

### #2: YAML Frontmatter Basics

**Analyst:** yaml-analyst
**Verdict:** ADD `type` field, CHANGE `status` default, KEEP everything else

**Current frontmatter:**
```yaml
title: '{title}'
slug: '{slug}'
created: '{date}'
status: 'in-progress'
```

**Gemini's frontmatter:**
```yaml
task_id: "BMAD-402"
type: "feature|bugfix|refactor"
status: "ready_for_dev"
```

**Recommendation detail:**

1. **`slug` vs `task_id` — KEEP `slug`.** `task_id` assumes an external issue tracker. In BMAD Quick Flow, specs are generated conversationally and may not map 1:1 to tickets. `slug` is self-describing (e.g., "jwt-auth-middleware") and doubles as a filename component. If tracker linking is needed later, add an optional `issue:` field.

2. **`type` — ADD it.** Both reports emphasize that the spec should signal work type because the agent's implementation strategy differs:
   - Features need new test files and may scaffold new modules.
   - Bugfixes need regression tests targeting the specific failure.
   - Refactors should preserve behavior and focus on existing test coverage.
   - Recommended values: `feature | bugfix | refactor | chore`. Keep the enum short.

3. **`status` — CHANGE default.** `in-progress` is wrong for a template. A freshly generated spec should be `draft`. Suggested lifecycle: `draft → ready → in-progress → done`.

4. **`title` and `created` — KEEP as-is.**

**Recommended frontmatter:**
```yaml
title: '{title}'
slug: '{slug}'
type: 'feature'  # feature | bugfix | refactor | chore
created: '{date}'
status: 'draft'  # draft | ready | in-progress | done
```

---

### #3: target_models in YAML

**Analyst:** yaml-analyst
**Verdict:** DO NOT ADD

**Gemini proposes:**
```yaml
target_models: ["claude-4-sonnet", "gpt-5.3-codex", "grok-4.20"]
```

**Grok:** Not mentioned.

**Recommendation detail:**

1. **Specs should be model-agnostic.** The structured Markdown format works because it aligns with how ALL transformer attention mechanisms work, not model-specific quirks.
2. **Model versions churn too fast.** "claude-4-sonnet" becomes "claude-4.5-sonnet" next quarter. Every spec becomes stale metadata.
3. **BMAD Quick Flow does not do multi-model routing.** The orchestrator uses whatever model is configured system-wide. The spec doesn't choose its executor.
4. **Grok doesn't mention it.** This is Gemini-only, and even Gemini frames it as "hints."
5. **Trivial to add later.** YAML frontmatter is extensible. If multi-model routing is ever needed, it's a one-line schema change.

Skip it. Keep frontmatter lean. Speculative fields train authors to treat YAML as a dumping ground.

---

### #4: context_dependencies in YAML vs Code Map

**Analyst:** yaml-analyst
**Verdict:** ADD lightweight `context` YAML array AND KEEP body Code Map — they serve different purposes

**Gemini proposes:** Machine-parseable `context_dependencies` in YAML for MCP/RAG dynamic injection.

**Grok says:** "Always surface relevant codebase files via RAG before spec finalization" — but not in frontmatter.

**Template does:** Body-only approach (Context & Code Map section).

**The key insight — these are NOT the same thing:**

| | YAML `context` | Body Code Map |
|---|---|---|
| **Answers** | "What project-wide standards/docs must the orchestrator pre-load?" | "What source files are relevant to THIS task?" |
| **Contains** | Coding standards, API conventions, DB rules, UI guidelines | Entry points, schemas, test files the agent will edit |
| **Read by** | Orchestrator (machine-parsed, before handing off) | Implementation agent (narrative context) |
| **Mutability** | Read-only reference material | Files the agent will modify |

**Recommended YAML addition:**
```yaml
context:           # project docs the orchestrator should pre-load (optional)
  - 'docs/api-standards.md'
  - 'docs/db-conventions.md'
```

**Keep body Code Map unchanged** for task-specific source files.

**Why not body-only:** Without the YAML field, the orchestrator can't automatically pre-load project standards. The agent would need to discover them via search (wasteful tokens, may miss them).

**Why not YAML-only:** Gemini lumps code files and standards together in one array. This conflates two concerns. The orchestrator doesn't need to pre-load `src/auth/types.ts`.

Mark the `context` field as optional — many specs won't need it if CLAUDE.md or rules files already handle standards injection.

---

### #5: Intent / Problem Framing

**Analyst:** core-sections-analyst
**Verdict:** KEEP as-is

**Gemini says:** "Intent and Business Value"
**Grok says:** "Objective anchors intent"
**Template says:** "Problem — what is broken or missing, and why does it matter?"

**Recommendation detail:**

1. **More concrete and scope-constraining.** "Problem" forces articulation of a specific gap or pain point, naturally preventing scope creep. "Intent and Business Value" suits product-level PRDs, not story-level specs.

2. **Already captures intent.** The HTML comment "what is broken or missing, and why does it matter?" covers the "why" dimension without a separate business-value paragraph that would bloat word count.

3. **Better semantic anchor.** "Problem" is direct and action-oriented — the model immediately knows what gap it's filling. "Intent and Business Value" is softer and more ambiguous.

4. **Appropriate audience.** Quick Flow specs are consumed by coding agents, not stakeholders. The agent needs to understand what's wrong and why fixing it matters technically, not the business case.

No changes needed.

**Note:** structural-analyst (#18) proposes merging Problem + Solution into a single "Intent" section. See Open Decisions below.

---

### #6: Standalone Solution Section

**Analyst:** core-sections-analyst
**Verdict:** KEEP

Neither Gemini nor Grok includes a separate Solution section. The template has one with "High-level approach — the 'what', not the 'how'" guidance.

**Recommendation detail:**

1. **Fills the gap left by "Problem" framing.** Since the template uses "Problem" instead of "Intent" (#5), there's no natural place for the high-level approach. Solution bridges "here's what's wrong" → "here's what we're doing about it" in 1–2 sentences.

2. **Top-down comprehension.** Without this, the agent infers the approach bottom-up from Tasks. A brief Solution statement gives the agent a mental model before reading details — aligns with primacy-bias research both reports cite.

3. **Anti-over-specification guardrail.** The "what, not how" comment directly addresses the #1 anti-pattern identified by both reports.

4. **Essential for non-obvious changes.** For refactors, architectural shifts, or multi-file changes, the approach isn't inferable from Problem alone.

5. **Minimal word-count cost.** 1–3 sentences. Doesn't threaten the word budget.

**Note:** structural-analyst (#18) proposes merging this with Problem into "Intent". See Open Decisions below.

---

### #7: Boundaries & Constraints (Always / Ask First / Never)

**Analyst:** core-sections-analyst
**Verdict:** KEEP as-is — this is the template's strongest section

**Both reports converge:** Gemini calls the three-tier system "the single most critical innovation in 2025-2026 spec evolution." Grok confirms constraints and non-goals are top hallucination killers.

**What the template gets right:**

1. **Exact alignment with Osmani's pattern.** Always/Ask First/Never matches the industry-standard boundary system.
2. **Smart consolidation.** Gemini separates "Non-Goals" from "Never Do." Template wisely merges them under "Never" — at granular story level the distinction is academic.
3. **Excellent HTML comment.** "Three tiers: Always = invariant rules. Ask First = human-gated decisions. Never = out of scope + forbidden approaches." Concise, unambiguous.
4. **Compact formatting.** Bold labels instead of sub-headings keeps word count tight. 3–6 bullet points total.
5. **"Ask First" is undervalued by both reports** but arguably the most important tier for agentic workflows — the safety valve preventing high-impact autonomous decisions (new dependencies, schema changes, public API modifications).

**Observation:** Gemini emphasizes negative prompting (telling the model what NOT to do) is empirically more effective than positive prompting. The "Never" tier captures this. No change needed.

---

### #8: Context & Code Map Structure

**Analyst:** core-sections-analyst
**Verdict:** CHANGE — annotate paths with roles

**Gemini uses:** Named categories (Entry Point, Related Schemas, Test Location).
**Template uses:** Flat bullet list.

**Why Gemini's categories are too rigid:** They assume a specific code architecture (handler/schema/test). Many tasks involve config files, migrations, utilities, build scripts that don't fit these buckets.

**Why the flat list undersells the section:** A bare file path tells the agent *which* files matter but not *why*. The agent must open each file to figure out relevance, wasting tokens.

**Proposed change:** Keep flat list, update placeholders to show annotated format:

From:
```markdown
- {entry_point_or_key_file}
- {related_file}
```

To:
```markdown
- `{file_path}` -- {role or relevance}
- `{file_path}` -- {role or relevance}
```

This mirrors the Tasks section format (`file` -- action -- rationale), creating internal consistency. Also update the HTML comment to: "Agent-populated during planning. Annotated file paths prevent blind codebase searching and give the coding agent immediate context."

---

### #9: I/O & Edge-Case Matrix

**Analyst:** core-sections-analyst
**Verdict:** KEEP with one minor column rename

Most universally endorsed section across both reports. Gemini: table format forces consistent attention mapping. Grok: "kills 80% of hallucinations on boundaries."

**What's right:**
1. Table format over prose — both reports emphatic.
2. Four-column structure forces completeness.
3. **The escape hatch ("Omit section if no meaningful I/O scenarios") is excellent** — a critical addition neither report addresses. Many tasks (refactors, config, docs) have no I/O scenarios.

**One change:** Rename "Expected Outcome" → "Expected Output / Behavior":
- "Outcome" is vague — state change? side effect? return value?
- "Output / Behavior" is more precise: "Output" for return values, "Behavior" for observable side effects.
- Helps agent generate more testable assertions.

Updated header:
```
| Scenario | Input / State | Expected Output / Behavior | Error Handling |
```

---

### #10: Tasks Format (File-Anchored)

**Analyst:** supplementary-analyst
**Verdict:** KEEP with minor refinement

**Template does:** Each task structured as `` `{file}` -- {action} -- {rationale} ``, one task per file change.

**Gemini:** Plain checklist with file paths embedded informally in prose.
**Grok:** Doesn't address task format.

**Why the template's format is a genuine innovation:**
1. **Prevents scope creep per task** — one file per task means the agent can't silently modify unrelated files.
2. **Creates an implicit change manifest** — scanning backtick-quoted paths shows blast radius before implementation.
3. **Rationale column forces justification** — the "why this change" that prevents mechanical file-touching.

**Refinement:** Soften the "one task per file change" guidance. Some tasks legitimately touch multiple files (e.g., "add type + update barrel export"). Change the comment to:

"Prefer one task per file change; group tightly-coupled changes (e.g., type + re-export) when splitting would be artificial."

The structured format is strictly superior to Gemini's prose-embedded paths — more parseable by agents and more scannable by humans.

---

### #11: Acceptance Criteria Section

**Analyst:** supplementary-analyst
**Verdict:** KEEP as separate section, add anti-redundancy guidance

**Gemini:** Folds AC into I/O matrix + Verification/DoD. No separate section.
**Grok:** Endorses AC. "Gherkin AC remains powerful when embedded inside broader Markdown spec."

**Key insight — I/O Matrix and AC serve different purposes:**

| | I/O Matrix | Acceptance Criteria |
|---|---|---|
| **Answers** | "Given this input, what is the exact output?" | "What system-level behaviors constitute success?" |
| **Nature** | Data-level, atomic, tabular | Behavioral, spanning components, narrative |
| **Example** | "Valid JWT → 200 OK, { user_id }" | "Given user is logged out, when visiting /dashboard, then redirect to /login with return URL" |

Gemini's approach works for simple function-level stories but breaks for feature-level work where behaviors span multiple components.

**The real risk is redundancy.** Add to the HTML comment: "AC covers system-level behaviors not captured by the I/O matrix. Do not duplicate I/O scenarios here."

**Note:** structural-analyst (#18) proposes merging AC with Tasks into "Tasks & Acceptance". See Open Decisions below.

---

### #12: Technical Decisions

**Analyst:** supplementary-analyst
**Verdict:** KEEP, rename to "Design Rationale", make optional

Neither report includes a dedicated section, but both implicitly require this information. Boundaries absorbs some design rationale; non-goals capture intent through negation. But there's a class of information that doesn't fit elsewhere:

- "We chose WebSocket over SSE because we need bidirectional communication" — not a constraint, not a boundary.
- "Using a denormalized cache table rather than joins because read pattern is 100:1" — critical context preventing the agent from "improving" the design.

**Refinements:**
1. **Rename to "Design Rationale"** — more descriptive, less likely to invite implementation details. (Three agents independently recommended this name.)
2. **Mark as optional** — simple stories (add a field, fix a bug) have no meaningful design decisions.
3. **Add guidance:** "Record only decisions where the agent might reasonably choose a different approach. If there's only one obvious way, don't document it."

**Note:** structural-analyst (#18) proposes merging this with Golden Examples into "Design Notes". See Open Decisions below.

---

### #13: Golden Examples

**Analyst:** supplementary-analyst
**Verdict:** KEEP, make optional, add size constraints

**Grok is emphatic:** "Concrete examples + edge matrices reduce hallucination more than any other single technique." Strongest single endorsement in either report.

**Gemini:** No dedicated section, but I/O Matrix rows with concrete values serve as implicit examples.

**High value, high risk:**
- **High value:** Examples ground the spec in concrete reality. An I/O row says "returns paginated response" — a golden example shows the exact JSON shape. For UI work, a before/after diff is worth 100 words. For data transformations, a sample pair eliminates ambiguity.
- **High risk:** Most likely section to balloon past word count. A 30-line JSON response eats the entire budget. Also most prone to staleness.

**Refinements:**
1. Keep optional — many tasks don't benefit.
2. Add size constraint: "Keep examples minimal — a 5–10 line snippet or diff, not a full file. Point to existing code via file path when a reference implementation already exists."
3. Clarify that only ONE type per spec is typically needed (diff, sample output, or reference — not all three).

**Note:** structural-analyst (#18) proposes merging this with Technical Decisions into "Design Notes". See Open Decisions below.

---

### #14: Verification — Mandatory vs Optional

**Analyst:** supplementary-analyst
**Verdict:** CHANGE to mandatory, with structured fallback

**Gemini:** Unequivocal — Verification is section 6 of 6, not optional. "Explicit, copy-pasteable terminal commands the agent must run to verify its own work before halting its execution loop." Enables "autonomous self-correction loop."

**Grok:** "Testing/DoD: turns spec into executable contract."

**Template:** "Optional. Include when obvious build/test/lint commands exist. Omit section when not applicable."

**Why mandatory matters:** Without verification, the agent writes code, declares success, and halts. The human must manually run everything — defeating the autonomous self-correction loop both reports identify as the key differentiator.

**The template's concern is valid:** Some tasks genuinely lack CLI checks (documentation, config edits, template changes). But "no CLI commands" ≠ "no verification."

**Proposed structure:**
```markdown
## Verification

<!-- How the agent confirms its own work. Prefer CLI commands. When no CLI check applies, state what to inspect manually. -->

**Commands:**
- `{command}` -- expected: {what_success_looks_like}

**Manual checks (if no CLI verification):**
- {what_to_inspect_and_expected_state}
```

Examples:
- Code tasks: `npm run build`, `npm test -- --filter auth`, `npx tsc --noEmit`
- Config/docs: `npx yaml-lint config.yml` or "Open {file} and confirm {condition}"

The "expected" annotation after each command is critical — without it the agent runs the command but can't self-judge the result.

---

### #15: Spec Change Log — DISPUTED

**Analyst:** supplementary-analyst (KEEP) vs structural-analyst (REMOVE)

**Neither report mentions this.** Template innovation.

**Case for KEEP (supplementary-analyst):**

This section solves spec drift during iterative refinement — a problem both reports overlook because they assume linear flow (write → implement). BMAD assumes iterative flow (write → review → revise → review → implement).

Without a change log:
1. **Lost context:** The agent revises the spec, rationale disappears. On next review, human or agent may undo the fix because they don't know why it was made. "What bad state it avoids" is the critical field.
2. **KEEP instructions:** When a review identifies a constraint the agent keeps dropping (e.g., "don't add a dependency — use existing utility"), KEEP creates a persistent instruction surviving future edits. This is in-spec reinforcement learning.

Word count concern: Change Log entries accumulate but sit at the bottom (recency bias zone) and are machine-written audit trail, not prose competing for attention.

**Case for REMOVE (structural-analyst):**

Process metadata, not specification content. Adds zero value to the implementing agent. Can be tracked via git history. Contributes to "Lost in the Middle" by adding non-actionable content. If review changes need to be visible, append a KEEP instruction to the relevant section.

**Unresolved.** See Open Decisions below.

---

### #16: Notes Section

**Analyst:** supplementary-analyst
**Verdict:** REMOVE

Both analysts (supplementary and structural) independently agree: remove it.

**Why:**
1. **Invites lazy authoring.** When info is hard to categorize, Notes lets authors skip the work of figuring out where it belongs.
2. **"Anything that doesn't fit above" means everything fits.** With 11 other sections, if info doesn't fit any of them, it probably doesn't belong in the spec.
3. **Attention sink.** Unstructured prose at the end occupies the recency-bias zone, competing with structured sections.
4. **Stated use cases are already covered:** "Open questions resolved during planning" → Technical Decisions. "Additional context" → Problem or Boundaries.

---

### #17: Over-Specification Guardrails

**Analyst:** structural-analyst
**Verdict:** CHANGE — comments are necessary but insufficient; add structural constraints

Both reports identify over-specification as the #1 anti-pattern. Gemini: "over-specifying the 'how' paralyzes the latent space." Grok: "95% of 2024 mega-prompt templates are now anti-patterns."

**Why comments alone are insufficient:**

1. **The spec author is an AI agent.** HTML comments are weak signals. An LLM filling out the template frequently ignores comment guidance when the heading invites elaboration — "Technical Decisions" practically begs for implementation details.
2. **No enforcement mechanism.** No word budget, no structural constraint, no validation step.
3. **The template's own structure works against brevity.** 12 sections with placeholder prompts creates implicit pressure to fill every section substantially.

**Concrete recommendations:**

1. **Word count target at the top** (not buried in sections): `<!-- TARGET: 400–1,000 words. Over 1,000 = over-specified. -->`
2. **Rename "Technical Decisions" to "Design Rationale"** — reframes away from implementation toward justification.
3. **Agent prompt enforcement (outside template):** The quick-spec agent's system prompt should contain examples of over-specification vs correct specification. Show bad: `"Implement a for-loop iterating over users array, checking each user.role === 'admin'"` vs good: `"Filter users by admin role"`.
4. **Tasks section brevity by design:** Add `<!-- Max 1 sentence per task. If a task needs a paragraph, split it. -->`
5. **Structural validation step in workflow:** After generation, agent self-checks: "Does any section contain pseudocode? Does word count exceed target? Are any tasks longer than one sentence?"

Bottom line: HTML comments are a "please don't speed" sign. Real guardrails need: (a) hard word budget, (b) headings that don't invite elaboration, (c) enforcement in agent prompt and review workflow.

---

### #18: Total Section Count (12 vs 6) — The Meta-Question

**Analyst:** structural-analyst
**Verdict:** RESTRUCTURE from 12 to 7 sections (3 conditional)

Current: 12 sections. Gemini: 6. Grok: ~6. Both cite "Lost in the Middle" and Context Rot.

**Proposed restructured outline:**

```
---
YAML frontmatter (title, slug, type, date, status, context)
---
<!-- Target: 400–1,000 words. Over 1,000 = over-specified. -->

# {title}

## 1. Intent
   What is broken/missing + high-level approach (the what, not the how)

## 2. Boundaries & Constraints
   Always / Ask First / Never

## 3. Context & Code Map
   Agent-populated annotated file paths

## 4. I/O & Edge-Case Matrix          <- conditional: omit if no meaningful I/O
   | Scenario | Input | Output / Behavior | Error |

## 5. Tasks & Acceptance
   - [ ] Task: `file` -- action -- rationale
   - [ ] AC: Given/When/Then

## 6. Design Notes                    <- conditional: omit if straightforward
   Design rationale + golden examples (only when non-obvious)

## 7. Verification                    <- conditional: omit if no build/test commands
   Commands + success criteria
```

**Section dispositions:**

| Current Section | Disposition | Rationale |
|----------------|-------------|-----------|
| Problem | Merge → Intent | Single "what's wrong + what we'll do" section |
| Solution | Merge → Intent | Two headings for framing is overhead at 400–800 words |
| Boundaries & Constraints | Keep as-is | Unanimously the strongest section |
| Context & Code Map | Keep as-is | Both reports endorse |
| I/O & Edge-Case Matrix | Keep, make conditional | Both reports emphatic; not all tasks have I/O |
| Tasks | Merge → Tasks & Acceptance | Same axis: "what to do" + "how we know it's done" |
| Acceptance Criteria | Merge → Tasks & Acceptance | Reduces navigation overhead |
| Technical Decisions | Merge → Design Notes | Empty more often than not for simple stories |
| Golden Examples | Merge → Design Notes | Conditional; only for non-obvious approaches |
| Verification | Keep, make conditional | Already optional; broaden to include manual checks |
| Spec Change Log | Remove | Process metadata — track via git |
| Notes | Remove | Anti-pattern catch-all |

**Word count impact:**
- 12 sections with minimum content: ~1,200–1,800 words (exceeds both reports' ceilings)
- 7 sections (4–5 active): ~400–800 words (hits both reports' sweet spots)

**Effective section count for simple stories:** 4–5 (Intent, Boundaries, Context, Tasks & Acceptance, maybe Verification). Complex stories expand to full 7.

---

## Open Decisions Requiring Human Input

### Decision 1: Problem + Solution — Keep Separate or Merge into "Intent"?

**Keep separate (core-sections-analyst):**
- "Problem" is more concrete than "Intent" for granular stories.
- Solution bridges Problem→Boundaries at minimal word cost (1–3 sentences).
- Reports likely omit Solution because they fold approach into "Intent" — but since we use "Problem" instead, Solution fills that role.

**Merge into "Intent" (structural-analyst):**
- Two top-level headings for problem framing is overhead in a 400–800 word spec.
- A single "Intent" section with "What's wrong / What we'll do" sub-points conveys the same info with one fewer heading.
- Reduces section count from 12 to 11 (or 7 in the full restructure).

### Decision 2: Tasks + AC — Keep Separate or Merge into "Tasks & Acceptance"?

**Keep separate (supplementary-analyst):**
- I/O Matrix is data-level; AC is behavioral/system-level. Different concerns.
- Anti-redundancy guidance resolves the overlap concern.
- Given/When/Then format deserves its own heading for visibility.

**Merge (structural-analyst):**
- Same axis: "what to do" + "how we know it's done."
- Good tasks already imply their ACs; ACs often map 1:1 to tasks.
- Adjacent under one heading reduces navigation overhead.

### Decision 3: Spec Change Log — Keep or Remove?

**Keep (supplementary-analyst):**
- Solves spec drift during iterative refinement.
- KEEP instructions = in-spec reinforcement learning.
- Both reports overlook this because they assume linear flow.
- Git history doesn't capture "what bad state this avoids."

**Remove (structural-analyst):**
- Process metadata, not specification content.
- Zero value to the implementing agent.
- Track via git history instead.
- Contributes to "Lost in the Middle."
