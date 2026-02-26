---
name: 'step-03-implement'
description: 'Execute implementation directly or via sub-agent. Local only.'
---

# Step 3: Implement

**Step 3 of 5 — Autonomous. Local only.**

## RULES

- YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- No push. No remote ops.
- Sequential execution only.

---

## INSTRUCTIONS

`execution_mode = "one-shot"` or no sub-agents/tasks available: implement the intent.

Otherwise (`execution_mode = "plan-code-review"`): hand `{spec_file}` to a sub-agent/task and let it implement.

---

## NEXT

Read fully and follow `{installed_path}/steps/step-04-review.md`
