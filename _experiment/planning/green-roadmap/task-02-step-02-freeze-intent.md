# Task 02: Enforce Frozen Intent Sections (Step 2)

## Prerequisite

None.

## Intent

Technically enforce the rigidity of the frozen sections of the tech spec (Problem, Solution, Scope, Non-Goals) to prevent downstream agents from altering the core intent.

## Method

Modify `src/bmm/workflows/bmad-quick-flow/quick-dev2/steps/step-02-plan.md` and the `tech-spec-template.md` to explicitly format the spec so that the frozen sections are clearly demarcated (e.g., a "DO NOT MODIFY" or "FROZEN AFTER CHECKPOINT 1" header for these sections). Ensure that downstream instructions in step 3 and 4 explicitly respect this rigid boundary.

## Output

Modified `step-02-plan.md` and `tech-spec-template.md`.
