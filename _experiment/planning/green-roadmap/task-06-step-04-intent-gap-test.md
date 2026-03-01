# Task 06: INTENT_GAP Two-Question Test (Step 4)

## Prerequisite

None.

## Intent

Prevent false escalations to the user by requiring a strict two-question test to classify an issue as `intent_gap`.

## Method

Modify `src/bmm/workflows/bmad-quick-flow/quick-dev2/steps/step-04-review.md` to redefine `intent_gap` classification using the formal 2-question test:
1. Can this issue be resolved using only info in the original request + spec?
2. Does fixing it require an uncaptured user-specific decision?

Only if Question 2 is YES does the issue genuinely become an `intent_gap`. Everything else is a `bad_spec`.

## Output

Modified `step-04-review.md`.
