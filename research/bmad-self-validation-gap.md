# BMAD Methodology Gap: Missing Self-Validation Before Handoff

**Date:** 2025-12-03
**Context:** Discovered during LLM PR Review tracer bullet implementation

---

## What Triggered This

During implementation of a GitHub Actions workflow (Phase 0a/0b of LLM PR Review tech spec), two simple bugs made it all the way to remote testing before being caught:

1. **Python slice syntax error:**

   ```python
   # Wrong - slice outside print(), returns None
   print('text ' * n)[:size]

   # Correct
   print(('text ' * n)[:size])
   ```

2. **Bash quoting issue:**

   ```bash
   # Wrong - variable substitution breaks multiline string
   COMMENT="...
   ${{ steps.llm.outputs.summary }}
   ..."

   # Correct - use heredoc + env vars
   gh pr comment --body "$(cat <<EOF
   ...
   $SUMMARY
   ...
   EOF
   )"
   ```

Both could have been caught with 2-second local tests before committing.

---

## The Reasoning Chain

### Initial Diagnosis: "Quick Dev needs self-checks"

First thought was that the `quick-dev` workflow should include validation before committing.

### Deeper Look: "The tech spec didn't include validation steps"

Looking at the tech spec phases:

**Phase 0a Tasks:**

- Create workflow file
- Add trigger
- Set permissions
- Fetch PR
- Call LLM
- Post comment
- _(no validation step)_

**Acceptance Criteria:**

- Given valid PR, comment appears
- Given invalid PR, fails gracefully
- Works with both auth methods

The AC are designed for _human verification after running_, not _implementer validation before pushing_.

### Even Deeper: "This is a methodology-level gap"

The BMAD workflow pattern at every handoff:

```
Agent does work → Shows to human → Human approves/rejects
```

There's no:

```
Agent does work → Agent validates → Shows to human
```

This applies across all BMAD workflows:

| Agent     | Produces     | Handed to         |
| --------- | ------------ | ----------------- |
| Analyst   | Brief        | PM reviews        |
| PM        | PRD          | Architect reviews |
| Architect | Architecture | Dev implements    |
| Dev       | Code         | Human tests       |
| SM        | Stories      | Dev implements    |

At every checkpoint, the agent shows work without self-validating first.

---

## The Architectural Concern

The `workflow.xml` core (the engine that runs all BMAD workflows) has:

- `<step>` - do work
- `<template-output>` - show to human, wait for approval

Missing concept: `<validate-before-output>` or similar.

The methodology assumes humans catch mistakes. This works for high-level artifacts (PRD, architecture) where validation is subjective. But for code and structured outputs, there are objective checks that should run before bothering the human.

---

## Possible Solutions (Not Decided)

### Option A: Workflow Engine Level

Add validation hook to `workflow.xml` before any `<template-output>`. Each workflow defines what validation means for its artifact type.

### Option B: Per-Workflow Level

Each workflow's instructions include explicit validation steps. Create-tech-spec generates validation tasks for code phases.

### Option C: Agent Level

Agents understand they should self-check. Part of agent persona/principles.

### Option D: Project Context Level

`project-context.md` defines available validation commands. Agents discover and run them.

---

## Open Questions

1. Is validation the agent's responsibility or the workflow's?
2. What's the right granularity? Per-step? Per-phase? Per-output?
3. How do we handle artifacts where validation is subjective (PRD quality)?
4. Should validation failures block handoff or just warn?

---

## For Now

Added a `### Local Validation` section to the specific tech spec being worked on. This is a band-aid, not a fix.

The real fix requires architectural decision about where validation belongs in BMAD.
