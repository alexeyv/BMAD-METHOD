# Task 07: Spec Loop Guardrails & Positive Preservation (Step 4)

## Prerequisite

Task 06.

## Intent

Bound the autonomous spec-class finding loop to prevent infinite oscillation and preserve good code via KEEP instructions.

## Method

Modify `src/bmm/workflows/bmad-quick-flow/quick-dev2/steps/step-04-review.md` and `tech-spec-template.md` to:
1. Append a **Change Log** to the spec tracking what finding triggered the change and what known-bad state it avoids.
2. Enforce **Positive Preservation**: Extract successful patterns from the discarded code and explicitly record them as KEEP instructions for the next derivation.
3. Include instructions to consult the Change Log prior to amending the spec to avoid regression.

## Output

Modified `step-04-review.md` and `tech-spec-template.md`.
