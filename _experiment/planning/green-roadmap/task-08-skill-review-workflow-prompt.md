# Task 08: Standalone Tooling - review-workflow-prompt

## Prerequisite

End-to-End workflow is functional.

## Intent

Create the `review-workflow-prompt` skill to iteratively and adversarially review workflow step files.

## Method

Implement the `review-workflow-prompt` skill in the `_bmad/core/skills/` following the existing `bmad-review-adversarial-general` subagent patterns, using 3 parallel agents:
1. Context Asymmetric 
2. Edge Cases 
3. Fit for Purpose
This will be used to find flaws in workflow step prompts.

## Output

A new skill added to the BMAD source tree.
