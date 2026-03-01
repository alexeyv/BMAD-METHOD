---
name: 'step-04-review'
description: 'Adversarial review, classify findings, optional spec loop'

adversarial_review_task: '{project-root}/_bmad/core/tasks/review-adversarial-general.xml'
deferred_work_file: '{implementation_artifacts}/deferred-work.md'
specLoopIteration: 1
---

# Step 4: Review

## RULES

- YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- Review subagents get NO conversation context.

## INSTRUCTIONS

Change `{spec_file}` status to `in-review` in the frontmatter before continuing.

### Construct Diff (plan-code-review only)

Read `{baseline_commit}` and `{baseline_untracked}` from `{spec_file}` frontmatter.

If `{baseline_commit}` is a git commit hash:

- `{diff_output}` = `git diff {baseline_commit}` for tracked files.
- Run `git ls-files --others --exclude-standard` and compare against `{baseline_untracked}`. Any files not in the baseline list are new — include their full content in `{diff_output}`.

If a proper diff cannot be constructed, use best effort to determine what changed.

Do NOT `git add` anything — this is read-only inspection.

### Review

**One-shot:** Skip diff construction. Still invoke `{adversarial_review_task}` in a subagent with the changed files — inline review invites anchoring bias.

**Plan-code-review:** Launch three subagents without conversation context.

- **Blind hunter** — receives `{diff_output}` only. No spec, no context docs, no project access. Invoke via `{adversarial_review_task}`.
- **Edge case hunter** — receives `{diff_output}` and read access to the project. Traces through the logic paths in the changed code and finds edge cases that are not addressed.
- **Acceptance auditor** — receives `{diff_output}`, `{spec_file}`, and read access to the project. Must also read the docs listed in `{spec_file}` frontmatter `context`. Checks for violations of acceptance criteria, rules, and principles from the spec and context docs.

### Classify

1. Deduplicate all review findings.
2. Classify each finding. The first three categories are **this story's problem** — caused or exposed by the current change. The last two are **not this story's problem**. When in doubt between bad_spec and patch, prefer bad_spec — a spec-level fix produces coherent code, a code-level patch produces a patchwork quilt.
   - **intent_gap** — caused by the change; wouldn't happen if intent was clear. Intent is expensive to patch — loop back to the human.
   - **bad_spec** — caused by the change, including direct deviations from spec. The spec should have been clear enough to prevent it. When torn between bad_spec and patch, prefer bad_spec.
   - **patch** — caused by the change; trivially fixable without human input. Just part of the diff.
   - **defer** — pre-existing issue not caused by this story, surfaced incidentally by the review. Collect for later focused attention.
   - **reject** — noise. Drop silently. When unsure between defer and reject, prefer reject — only defer findings you are confident are real.
3. Process findings in cascading order. If intent_gap or bad_spec findings exist, they trigger a loopback — code and spec are discarded anyway, so lower findings are moot. If neither exists, process patch and defer normally. Increment `{specLoopIteration}` on each loopback. If it exceeds 5, HALT and escalate to the human.
   - **intent_gap** — Revert code changes, discard the spec. Loop back to step 1, then re-run steps 2–4.
   - **bad_spec** — Revert code changes, discard the spec. Loop back to step 2, then re-run steps 3–4.
   - **patch** — Auto-fix. These are the only findings that survive loopbacks.
   - **defer** — Append to `{deferred_work_file}`.
   - **reject** — Drop silently.
4. Commit.

## NEXT

Read fully and follow `{installed_path}/steps/step-05-present.md`
