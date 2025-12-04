# Refactor Proposal: Unified Path Files for All Phases

## Problem

Path files currently exclude Phase 4 workflows (except `sprint-planning`) because "they're tracked by sprint-status, not workflow-status." This creates:

1. **Two sources of truth for agent assignments**
   - Phases 1-3: Path files (primary)
   - Phase 4: Agent menu files (fallback)

2. **Special-case logic everywhere**
   - Manifest generator needs phase-aware agent lookup
   - Documentation (CLAUDE.md) must explain the split
   - Diagram generation must handle the boundary

3. **Confusion and errors**
   - We created a flawed tech-spec (tech-spec-bmm-consistency-fixes.md) trying to "fix" what was actually by-design
   - The design is non-obvious even to people working in the codebase

## Root Cause

The design conflates two distinct concerns:

| Concern        | What it answers                      |
| -------------- | ------------------------------------ |
| **Definition** | What workflows exist? Who owns them? |
| **Tracking**   | How is progress tracked at runtime?  |

Path files should handle **definition**. The `tracked_in` field handles **tracking**.

## Proposed Solution

Add Phase 4 workflows to path files with a `tracked_in` field:

```yaml
- phase: 3
  name: 'Implementation'
  workflows:
    - id: sprint-planning
      agent: sm
      command: sprint-planning
      tracked_in: workflow-status # Last one workflow-status tracks
      creates: sprint-status.yaml # Handoff artifact

    - id: create-story
      agent: sm
      command: create-story
      tracked_in: sprint-status # Tracked per-instance

    - id: dev-story
      agent: dev
      command: dev-story
      tracked_in: sprint-status

    - id: code-review
      agent: dev
      command: code-review
      tracked_in: sprint-status

    - id: retrospective
      agent: sm
      command: retrospective
      tracked_in: sprint-status

    - id: correct-course
      agent: sm
      command: correct-course
      tracked_in: sprint-status
      standalone: true # Ad-hoc, not part of main flow
```

## Changes Required

| Component                | Change                                             | Effort  |
| ------------------------ | -------------------------------------------------- | ------- |
| Path files (4)           | Add Phase 4 workflows with `tracked_in` field      | 30 min  |
| `workflow-status`        | Filter: skip `tracked_in: sprint-status` workflows | 1-2 hrs |
| `generate-manifest.md`   | Remove phase-based special-case logic              | 30 min  |
| `workflow-manifest.yaml` | Add `tracked_in` to schema, regenerate             | 30 min  |

**Total estimate:** Half day to one day

## Benefits

1. **Single source of truth** - Path files define the complete methodology
2. **Simpler manifest generator** - No phase-aware agent lookup needed
3. **Accurate diagrams** - Full picture with clear tracking boundaries
4. **Less confusion** - One place to look for "what workflows exist and who owns them"

## Migration

1. Add `tracked_in: workflow-status` to all existing path file workflows (default behavior)
2. Add Phase 4 workflows with `tracked_in: sprint-status`
3. Update `workflow-status` to filter by `tracked_in`
4. Simplify `generate-manifest.md`
5. Regenerate manifest

Backward compatible - existing path files work unchanged until explicitly updated.

## Decision

- [ ] Approve for implementation
- [ ] Defer to backlog
- [ ] Reject (reason: \_\_\_\_\_\_\_\_\_\_\_\_\_)
