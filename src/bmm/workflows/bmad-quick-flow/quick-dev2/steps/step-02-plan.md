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
5. Word count check (SCOPE STANDARD). If spec exceeds 1200 words:
   - Show user the word count.
   - `[S] Split — carve off child stories  [K] Keep as-is`
   - **S**: Propose the split — name each child story and its goal. Append child stories to `{deferred_work_file}`. Rewrite the current spec to cover only the main goal — do not surgically carve sections out; regenerate the spec for the narrowed scope. Continue to checkpoint.
   - **K**: Continue to checkpoint with full spec.

### CHECKPOINT 1

Present summary. If word count exceeded 1200 and user chose [K], include the word count in the summary. `[A] Approve  [E] Edit  [F] Full BMM`. HALT.

- **A**: Rename to `tech-spec-{slug}.md`, status `ready-for-dev`, freeze Intent/Boundaries/Design Notes. → Step 3.
- **E**: Apply changes, re-present.
- **F**: Exit to full BMM.

---

## NEXT

`{installed_path}/steps/step-03-implement.md`
