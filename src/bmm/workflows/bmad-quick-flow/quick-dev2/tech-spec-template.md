---
title: '{title}'
slug: '{slug}'
created: '{date}'
status: 'in-progress'
---

# {title}

## Problem

<!-- What is broken or missing, and why does it matter? -->

{problem_and_why_it_matters}

## Solution

<!-- High-level approach — the "what", not the "how". -->

{high_level_approach}

## Boundaries & Constraints

<!-- Three tiers: Always = invariant rules. Ask First = human-gated decisions. Never = out of scope + forbidden approaches. -->

**Always:** {must_follow_rules}

**Ask First:** {decisions_requiring_human_approval}

**Never:** {non_goals_and_forbidden_approaches}

## Context & Code Map

<!-- Agent-populated during planning. Concrete file paths prevent blind codebase searching. -->

- {entry_point_or_key_file}
- {related_file}
- {related_file}

## I/O & Edge-Case Matrix

<!-- Tabular edge cases — table format exploits LLM attention strengths over prose. Omit section if task has no meaningful I/O scenarios. -->

| Scenario | Input / State | Expected Outcome | Error Handling |
|----------|--------------|------------------|----------------|
| {happy_path} | {input} | {outcome} | N/A |
| {error_case} | {input} | {outcome} | {error} |

## Tasks

<!-- Each task: backtick-quoted file path -- action to take -- rationale. One task per file change. -->

- [ ] Task 1: `{file}` -- {action} -- {rationale}

## Acceptance Criteria

<!-- Given/When/Then format. Each AC must be independently verifiable. -->

- [ ] AC 1: Given {precondition}, when {action}, then {expected_result}

## Technical Decisions

<!-- Record rationale for design choices, not implementation steps. Why this approach, not how to code it. -->

{technical_decisions}

## Golden Examples

<!-- Before/after diffs, sample outputs, or reference implementations that make the expected result concrete. -->

{golden_examples}

## Verification

<!-- Optional. Include when obvious build/test/lint commands exist. Omit section when not applicable. -->

{verification_commands_and_success_criteria}

## Spec Change Log

<!-- Appended by the review loop. Each entry: what changed, what triggered it, what bad state it avoids, KEEP instructions. Empty until first review cycle. -->

## Notes

<!-- Additional context, open questions resolved during planning, or anything that doesn't fit above. -->

{notes}
