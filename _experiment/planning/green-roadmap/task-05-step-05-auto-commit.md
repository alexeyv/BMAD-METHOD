# Task 05: Auto-commit Before Handoff (Step 5)

## Prerequisite

None.

## Intent

Ensure that all work is safely committed locally before presenting results to the human, so the handoff starts from a clean, recoverable state.

## Method

Modify `src/bmm/workflows/bmad-quick-flow/quick-dev2/steps/step-05-present.md` to:
1. Automatically create a Git commit with a conventional commit message summarizing what was done.
2. Present the commit hash and summary to the user as part of the handoff.

## Output

Modified `step-05-present.md`.
