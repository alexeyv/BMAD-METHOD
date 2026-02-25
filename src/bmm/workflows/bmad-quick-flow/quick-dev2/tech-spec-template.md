---
title: '{title}'
slug: '{slug}'
type: 'feature' # feature | bugfix | refactor | chore
created: '{date}'
status: 'draft' # draft | ready | in-progress | done
---

<!-- Target: 400–1000 words. Below 400 = ambiguous. Above 1000 = context rot risk. -->

# {title}

## Intent

<!-- What is broken or missing, and why it matters. Then the high-level approach — the "what", not the "how". -->

PROBLEM_AND_WHY_IT_MATTERS

HIGH_LEVEL_APPROACH

## Boundaries & Constraints

<!-- Three tiers: Always = invariant rules. Ask First = human-gated decisions. Never = out of scope + forbidden approaches. -->

**Always:** INVARIANT_RULES

**Ask First:** DECISIONS_REQUIRING_HUMAN_APPROVAL

**Never:** NON_GOALS_AND_FORBIDDEN_APPROACHES

## Context & Code Map

<!-- Agent-populated during planning. Annotated paths prevent blind codebase searching. -->

- `FILE` -- ROLE_OR_RELEVANCE

## I/O & Edge-Case Matrix

<!-- Omit section if task has no meaningful I/O scenarios. Table format exploits LLM attention strengths over prose. -->

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| HAPPY_PATH | INPUT | OUTCOME | N/A |
| ERROR_CASE | INPUT | OUTCOME | ERROR_HANDLING |

## Tasks & Acceptance

<!-- Tasks: backtick-quoted file path -- action -- rationale. Prefer one task per file; group tightly-coupled changes when splitting would be artificial. -->
<!-- AC: Given/When/Then. Covers system-level behaviors not captured by the I/O matrix. Do not duplicate I/O scenarios here. -->

- [ ] `FILE` -- ACTION -- RATIONALE
- [ ] AC: Given PRECONDITION, when ACTION, then EXPECTED_RESULT

## Design Notes

<!-- Optional. Design rationale and golden examples only when the approach is non-obvious. Keep examples to 5–10 lines. If straightforward, omit this section. -->

DESIGN_RATIONALE_AND_EXAMPLES

## Verification

<!-- How the agent confirms its own work. Prefer CLI commands. When no CLI check applies, state what to inspect manually. -->

**Commands:**
- `COMMAND` -- expected: SUCCESS_CRITERIA

**Manual checks (if no CLI):**
- WHAT_TO_INSPECT_AND_EXPECTED_STATE
