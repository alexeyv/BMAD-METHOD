---
name: 'step-02-plan'
description: 'Investigate, generate spec, present for approval'

slug: kebab-cased strings are valid as a file name, based on the intent
wipFile: '{implementation_artifacts}/tech-spec-[slug].md'
templateFile: '{installed_path}/tech-spec-template.md'
deferred_work_file: '{implementation_artifacts}/deferred-work.md'
---

# Step 2: Plan

**Step 2 of 5 — Autonomous until checkpoint**

## RULES

- No intermediate approvals.
- YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`

---

## INSTRUCTIONS

1. Investigate codebase.
2. Generate spec from `{templateFile}` into `{wipFile}`.
3. Self-review against READY FOR DEVELOPMENT standard.
4. If intent gaps exist, do not fantasize, do not leave open questions, ask the human.
5. Token count check (see SCOPE STANDARD). If spec exceeds 1600 tokens:
   - Show user the token count.
   - HALT and ask human: `[S] Split — carve off secondary goals` | `[K] Keep as-is`
   - On **S**: Propose the split — name each secondary goal. Append deferred goals to `{deferred_work_file}`. Rewrite the current spec to cover only the main goal — do not surgically carve sections out; regenerate the spec for the narrowed scope. Continue to checkpoint.
   - On **K**: Continue to checkpoint with full spec.

### CHECKPOINT 1

Present summary. If token count exceeded 1600 and user chose [K], include the token count in the summary. HALT and ask human: `[A] Approve` | `[E] Edit`

- **A**: Rename to `tech-spec-{slug}.md`, status `ready-for-dev`, freeze Intent/Boundaries/Design Notes. → Step 3.
- **E**: Apply changes, re-present.

---

## NEXT

`{installed_path}/steps/step-03-implement.md`
