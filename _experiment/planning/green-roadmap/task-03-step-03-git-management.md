# Task 03: Git Management & Clean Tree Assertion (Step 3)

## Prerequisite

Task 01 and Task 02.

## Intent

Implement the safety checks and git state management required before implementation begins, to prevent losing work or mixing feature code.

## Method

Modify `src/bmm/workflows/bmad-quick-flow/quick-dev2/steps/step-03-implement.md` to:
1. Assert a clean working tree before starting. If dirty and fresh start, halt. If dirty and resume, apply the resume policy (identify if changes are from an interrupted task, continue or revert).
2. Automate feature branch and worktree creation based on the spec slug. 
3. Ensure this step is idempotent (reuse existing branch/worktree if already present).

## Output

Modified `step-03-implement.md`.
