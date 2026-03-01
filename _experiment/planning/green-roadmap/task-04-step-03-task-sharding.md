# Task 04: Sequential File-Based Task Sharding (Step 3)

## Prerequisite

Task 03.

## Intent

Replace the generic sub-agent handoff with a disciplined, file-based sharded execution loop to prevent lost-in-the-middle context issues.

## Method

Modify `src/bmm/workflows/bmad-quick-flow/quick-dev2/steps/step-03-implement.md` to:
1. Parse the `{spec_file}` tasks and write them into individual task files (e.g., `_bmad-output/tasks/task-01.md`).
2. Create and maintain a sequence file tracking execution order and status.
3. Have the agent execute tasks strictly sequentially, reading each file fresh, checking ACs, and updating the sequence file on disk to persist state across interruptions.

## Output

Modified `step-03-implement.md` with explicit task sharding instructions.
