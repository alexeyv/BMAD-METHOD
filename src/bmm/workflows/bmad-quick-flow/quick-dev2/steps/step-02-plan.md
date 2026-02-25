---
name: 'step-02-plan'
description: 'Investigate, generate spec, present for approval'

slug: kebab-cased strings are valid as a file name, based on the intent
wipFile: '{implementation_artifacts}/tech-spec-[slug].md'
templateFile: '{installed_path}/tech-spec-template.md'
deferred_findings_file: '{output_dir}/deferred-findings.md'
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
5. Word count check (SCOPE STANDARD). If spec exceeds ~1200 words:
   - Show user the word count.
   - `[S] Split — carve off child stories  [K] Keep as-is`
   - **S**: Identify sections corresponding to independent child stories. Write them to `{deferred_findings_file}` under `## Deferred Stories`. Remove only those sections from the current spec — never compress prose to hit a word count. Continue to checkpoint.
   - **K**: Continue to checkpoint with full spec.

### CHECKPOINT 1

Present summary (if word count exceeded ~1200 and user chose [K], echo the word count here). `[A] Approve  [E] Edit  [F] Full BMM`. HALT.

- **A**: Rename to `tech-spec-{slug}.md`, status `ready-for-dev`, freeze Problem/Solution/Boundaries/Golden Examples. → Step 3.
- **E**: Apply changes, re-present.
- **F**: Exit to full BMM.

---

## NEXT

`{installed_path}/steps/step-03-implement.md`
