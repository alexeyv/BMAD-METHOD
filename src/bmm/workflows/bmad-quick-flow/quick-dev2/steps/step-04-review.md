---
name: 'step-04-review'
description: 'Adversarial review, classify findings, optional spec loop'

adversarial_review_task: '{project-root}/_bmad/core/tasks/review-adversarial-general.xml'
deferred_work_file: '{implementation_artifacts}/deferred-work.md'
specLoopCap: 5
---

# Step 4: Review

**Step 4 of 5 — Autonomous**

## RULES

- Review subagents get NO conversation context.
- YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`

---

## INSTRUCTIONS

1. Review in context-free subagents: intent audit (skip for one-shot) + adversarial code review via `{adversarial_review_task}`.
2. Deduplicate findings across both reviews.
3. Classify each finding. The first three categories are **this story's problem** — caused or exposed by the current change. The last two are **not this story's problem**. When in doubt between bad_spec and patch, prefer bad_spec — a spec-level fix produces coherent code, a code-level patch produces a patchwork quilt.
   - **intent_gap** — caused by the change; wouldn't happen if intent was clear. Intent is expensive to patch — loop back to the human.
   - **bad_spec** — caused by the change, including direct deviations from spec. The spec should have been clear enough to prevent it. When torn between bad_spec and patch, prefer bad_spec.
   - **patch** — caused by the change; trivially fixable without human input. Just part of the diff.
   - **defer** — pre-existing issue not caused by this story, surfaced incidentally by the review. Collect for later focused attention.
   - **reject** — noise. Drop silently. Accept occasional false negatives to keep the deferred work file from bloating.
4. Process findings in cascading order. Each loopback discards all findings and restarts the pipeline. Max `{specLoopCap}` iterations across all loopbacks. If the cap is reached and loopback-worthy findings remain, HALT and escalate to the human.
   - **intent_gap** — Do not fantasize, ask the user. Discard all findings. Loop back: re-clarify intent, amend spec, re-run step 3 and step 4 from scratch.
   - **bad_spec** — Discard all findings. Amend spec, re-run step 3 and step 4 from scratch.
   - **patch** — Auto-fix. These are the only findings that survive loopbacks.
   - **defer** — Append to `{deferred_work_file}`.
   - **reject** — Drop silently.
5. Commit.

---

## NEXT

Read fully and follow `{installed_path}/steps/step-05-present.md`
