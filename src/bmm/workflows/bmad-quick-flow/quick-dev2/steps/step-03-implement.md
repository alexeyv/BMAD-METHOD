---
name: 'step-03-implement'
description: 'Execute implementation directly or via sub-agent. Local only.'
---

# Step 3: Implement

## RULES

- YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- No push. No remote ops.
- Sequential execution only.

## INSTRUCTIONS

### Baseline Snapshot (plan-code-review only)

Before making any changes, capture the baseline into `{spec_file}` frontmatter:

- `baseline_commit` = output of `git rev-parse HEAD`, or `NO_GIT` if not in a git repo.
- `baseline_untracked` = output of `git ls-files --others --exclude-standard`, or empty if `NO_GIT`.

### Implement

Change `{spec_file}` status to `in-progress` in the frontmatter before starting implementation.

`execution_mode = "one-shot"` or no sub-agents/tasks available: implement the intent.

Otherwise (`execution_mode = "plan-code-review"`): hand `{spec_file}` to a sub-agent/task and let it implement.


## NEXT

Read fully and follow `{installed_path}/steps/step-04-review.md`
