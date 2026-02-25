---
title: '{title}'
slug: '{slug}'
type: 'feature' # feature | bugfix | refactor | chore
created: '{date}'
status: 'draft' # draft | ready | in-progress | done
context: [] # optional: max 3 project-wide standards/docs. NO source code files.
---

<!-- Target: 900–1300 tokens. Above 1600 = high risk of context rot.
     Never over-specify "how" — use boundaries + examples instead.
     Cohesive cross-layer stories (DB+BE+UI) stay in ONE file. -->

# {title}

## Intent

<!-- What is broken or missing, and why it matters. Then the high-level approach — the "what", not the "how". -->

**Problem:** ONE_TO_TWO_SENTENCES

**Approach:** ONE_TO_TWO_SENTENCES

## Boundaries & Constraints

<!-- Three tiers: Always = invariant rules. Ask First = human-gated decisions. Never = out of scope + forbidden approaches. -->

**Always:** INVARIANT_RULES

**Ask First:** DECISIONS_REQUIRING_HUMAN_APPROVAL
<!-- Agent: if any of these trigger during execution, HALT and ask the user before proceeding. -->

**Never:** NON_GOALS_AND_FORBIDDEN_APPROACHES

## Context & Code Map

<!-- Agent-populated during planning. Annotated paths prevent blind codebase searching. -->

- `FILE` -- ROLE_OR_RELEVANCE
- `FILE` -- ROLE_OR_RELEVANCE

## I/O & Edge-Case Matrix

<!-- If no meaningful I/O scenarios exist, DELETE THIS ENTIRE SECTION. Do not write "N/A" or "None". -->

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| HAPPY_PATH | INPUT | OUTCOME | N/A |
| ERROR_CASE | INPUT | OUTCOME | ERROR_HANDLING |

## Tasks & Acceptance

<!-- Tasks: backtick-quoted file path -- action -- rationale. Prefer one task per file; group tightly-coupled changes when splitting would be artificial. -->
<!-- If an I/O Matrix is present, include a task to unit-test its edge cases. -->

**Execution:**
- [ ] `FILE` -- ACTION -- RATIONALE

**Acceptance Criteria:**
- Given PRECONDITION, when ACTION, then EXPECTED_RESULT

## Design Notes

<!-- If the approach is straightforward, DELETE THIS ENTIRE SECTION. Do not write "N/A" or "None". -->
<!-- Design rationale and golden examples only when non-obvious. Keep examples to 5–10 lines. -->

DESIGN_RATIONALE_AND_EXAMPLES

## Verification

<!-- How the agent confirms its own work. Prefer CLI commands. When no CLI check applies, state what to inspect manually. -->

**Commands:**
- `COMMAND` -- expected: SUCCESS_CRITERIA

**Manual checks (if no CLI):**
- WHAT_TO_INSPECT_AND_EXPECTED_STATE
