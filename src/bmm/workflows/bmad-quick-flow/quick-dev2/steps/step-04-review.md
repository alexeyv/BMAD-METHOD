---
name: 'step-04-review'
description: 'Adversarial review, classify findings, optional spec loop'

adversarial_review_task: '{project-root}/_bmad/core/tasks/review-adversarial-general.xml'
edge_case_hunter_task: '{project-root}/_bmad/core/tasks/review-edge-case-hunter.xml'
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

**Plan-code-review:** Launch three subagents without conversation context. If no sub-agents are available, implement directly. 

- **Blind hunter** — receives `{diff_output}` only. No spec, no context docs, no project access. Invoke via `{adversarial_review_task}`.
- **Edge case hunter** — receives `{diff_output}` and read access to the project. Traces through the logic paths in the changed code and finds edge cases that are not addressed.
- **Acceptance auditor** — receives `{diff_output}`, `{spec_file}`, and read access to the project. Must also read the docs listed in `{spec_file}` frontmatter `context`. Checks for violations of acceptance criteria, rules, and principles from the spec and context docs.

### Classify

1. Deduplicate all review findings.
2. Classify each finding. The first three categories are **this story's problem** — caused or exposed by the current change. The last two are **not this story's problem**. 
   - **intent_gap** — caused by the change; cannot be resolved from the spec because the captured intent is incomplete. Do not infer intent unless there is exactly one possible reading.
   - **bad_spec** — caused by the change, including direct deviations from spec. The spec should have been clear enough to prevent it. When in doubt between bad_spec and patch, prefer bad_spec — a spec-level fix is more likely to produce coherent code.
   - **patch** — caused by the change; trivially fixable without human input. Just part of the diff.
   - **defer** — pre-existing issue not caused by this story, surfaced incidentally by the review. Collect for later focused attention.
   - **reject** — noise. Drop silently. When unsure between defer and reject, prefer reject — only defer findings you are confident are real.
3. Process findings in cascading order. If intent_gap or bad_spec findings exist, they trigger a loopback — lower findings are moot since code will be re-derived. If neither exists, process patch and defer normally. Increment `{specLoopIteration}` on each loopback. If it exceeds 5, HALT and escalate to the human.
   - **intent_gap** — Root cause is inside `<frozen-after-approval>`. Revert code changes. Loop back to the human to resolve, then re-run steps 2–4.
   - **bad_spec** — Root cause is outside `<frozen-after-approval>`. Before reverting code: extract positive preservation (KEEP instructions — what worked well and must survive re-derivation). Revert code changes. Read the `## Spec Change Log` in `{spec_file}` and respect all logged constraints. Amend the non-frozen sections where the root cause lives. Append a change log entry recording: the triggering finding, what was amended, what known-bad state the amendment avoids, and the KEEP instructions. Re-run steps 3–4.
   - **patch** — Auto-fix. These are the only findings that survive loopbacks.
   - **defer** — Append to `{deferred_work_file}`.
   - **reject** — Drop silently.
4. Commit.

## NEXT

Read fully and follow `{installed_path}/steps/step-05-present.md`
