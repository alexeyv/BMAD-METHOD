---
title: Fix Documentation References
description: Corrects workflow, agent, and command references in BMad documentation
---

# Fix Documentation References

## Purpose

Fix incorrect references to workflows, agents, and commands in BMad documentation files.

## Step 1: Establish Target Audience

Before fixing references, determine who the document is for:

| Audience | Indicators | Style |
|----------|------------|-------|
| **Newbies** | tutorials/, getting-started, "What You'll Learn" | Keep "workflow", include platform hints |
| **Experienced** | reference/, how-to/, explanation/ | Drop "workflow", no platform hints |

**If unclear**: Ask the user "Who is the target audience for this document — new users learning BMad, or experienced users who know the system?"

This determines whether helper words like "workflow" and platform hints are helpful context or just noise.

## Reference Patterns to Fix

### Always Wrong

| Pattern | Example | Problem |
|---------|---------|---------|
| `*workflow` | `*prd` | Obsolete menu shortcut notation |
| `/workflow` | `/workflow-init` | Platform-specific slash command |
| `bmad_bmm_*` | `bmad_bmm_workflow-init` | Internal slash command name, platform-specific |

### Correct Format

Use backticks with plain workflow name:
- **Wrong**: Run `/workflow-init`
- **Wrong**: Run `*prd`

**When to say "workflow"**:
- **Newbie docs** (getting-started): "Run the `prd` workflow" — helps them learn what it is
- **Other docs**: "Run `prd`" — they already know, so "workflow" is noise

**Platform hint**: Only in getting-started/newbie docs, first mention can include hint:
- Run the `help` workflow (`/bmad-help` on most platforms)

In all other docs, the hint is noise — just use the workflow name.

### Workflow Name Changes

| Old Name | New Name | Notes |
|----------|----------|-------|
| `workflow-init` | `bmad-help` | DEPRECATED - help system replaces initialization |
| `workflow-status` | `bmad-help` | DEPRECATED - help system replaces status checking |

### The Help System

The `bmad-help` workflow is the modern replacement for both `workflow-init` and `workflow-status`:
- **Universal**: Works regardless of workflow state or module
- **Contextual**: Infers completion from artifacts and conversation
- **Adaptive**: Guides users through workflows based on phase ordering
- **Anytime**: Can be run at any point, no pre-initialization needed

Users can run `bmad-help` to get guidance on what to do next. It detects:
- What workflows have been completed (by checking for output artifacts)
- What module is active
- What the next recommended/required step is

## Lessons Learned

1. **Platform-agnostic**: Docs should never include platform-specific invocation patterns (slashes, prefixes)
2. **Backtick the name**: Use backticks around workflow names: `workflow-name`
3. **Simple names**: Just the workflow name, no `bmad_bmm_` prefix, no `/` prefix
