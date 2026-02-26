---
name: 'step-01-clarify-and-route'
description: 'Capture intent, route to execution path'

wipFile: '{implementation_artifacts}/tech-spec-wip.md'
deferred_work_file: '{implementation_artifacts}/deferred-work.md'
---

# Step 1: Clarify and Route

**Step 1 of 5**

## RULES

- YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- The prompt that triggered this workflow IS the intent — not a hint.
- Do NOT assume you start from zero.

## CONTEXT

- `ready-for-dev` spec in `{implementation_artifacts}`? → Confirm, skip to step 3.
- `{wipFile}` exists? → Offer resume or archive.

---

## INSTRUCTIONS

1. Clarify intent. Do not fantasize, do not leave open questions. If you must ask questions, ask them as a numbered list. When the human replies, verify to yourself that every single numbered question was answered. If any were ignored, HALT and re-ask only the missing questions before proceeding. Keep looping until intent is clear enough to implement.
2. Multi-goal check (see SCOPE STANDARD). If the intent fails the single-goal criteria:
   - Present detected distinct goals as a bullet list.
   - HALT and ask human: `[S] Split — pick first goal, defer the rest` | `[K] Keep as-is`
   - On **S**: Append deferred goals to `{deferred_work_file}`. Narrow scope to the first-mentioned goal. Continue routing.
   - On **K**: Proceed as-is.
3. Route:
   - **One-shot** — trivial (~3 files). `{execution_mode}` = "one-shot". → Step 3.
   - **Plan-code-review** — normal. → Step 2.
   - Ambiguous? Default to plan-code-review.

---

## NEXT

- One-shot / ready-for-dev: `{installed_path}/steps/step-03-implement.md`
- Plan-code-review: `{installed_path}/steps/step-02-plan.md`
