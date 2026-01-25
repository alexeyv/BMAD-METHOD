# Validate Manifest

Validate `tools/diagrams/workflow-manifest.yaml` against the source code in `src/`. The manifest makes factual claims—entities exist, have properties, stand in relationships. Find evidence for each claim.

## Intentional Exclusions

The following directories exist in `src/modules/bmm/workflows/` but are **intentionally excluded** from the manifest. Do NOT flag these as "unclaimed":

```yaml
excluded_directories:
  - excalidraw-diagrams/  # Diagram generation utilities, not BMM phase workflows
  - testarch/             # Test architecture workflows, separate concern from BMM
  - document-project/     # Brownfield documentation utility, not part of BMM flow
```

These are documented in `generate-manifest.md` under `scan_rules.exclude`.

## Instructions

### Step 1: Read the Manifest

Read `tools/diagrams/workflow-manifest.yaml`. Extract all claims:
- Phase directories exist
- Agents exist with specific properties (name, title, icon, module)
- Workflows exist in specific phases
- Workflows have specific agents and alternate_agents
- Workflows produce specific outputs
- Feedback loops connect specific workflows

### Step 2: Validate Phase Directories

Use Glob to check `src/modules/bmm/workflows/*/` exists.

For each phase in `domain.phases`:
1. Check the claimed directory exists
2. List any directories that exist but are NOT in the manifest

Report format:
```
| Phase | Claimed Dir | Exists | Status |
```

### Step 3: Validate Agents

For each agent in `inventory.agents`:

1. Use Read on `src/modules/bmm/agents/{id}.agent.yaml`
2. Verify these properties match exactly:
   - `name`
   - `title`
   - `icon`
   - `module`
3. Record the line number for each property

Report format:
```
| Agent ID | Property | Manifest Value | Actual Value | Line | Status |
```

### Step 4: Validate Workflows Exist

For each workflow in `inventory.workflows`:

1. Determine expected path from `phase` and `id`:
   - Phase 1 → `src/modules/bmm/workflows/1-analysis/{id}/`
   - Phase 2 → `src/modules/bmm/workflows/2-plan-workflows/{id}/`
   - Phase 3 → `src/modules/bmm/workflows/3-solutioning/{id}/`
   - Phase 4 → `src/modules/bmm/workflows/4-implementation/{id}/`
   - quick_flow → `src/modules/bmm/workflows/bmad-quick-flow/{id}/`
   - core → `src/core/workflows/{id}/`

2. Use Glob to verify directory exists
3. Check for `workflow.yaml` or `workflow.md`

Report format:
```
| Workflow | Phase | Directory Exists | Config File | Status |
```

### Step 5: Validate Workflow-Agent Relationships

For each workflow with `agent` not null:

1. Read the agent's `.agent.yaml` file
2. Search the `menu` section for a reference to this workflow
3. Record the line number where the workflow path appears
4. If `alternate_agents` is claimed, verify each alternate agent also references the workflow

Report format:
```
| Workflow | Claimed Agent | Agent References It | Line | Status |
```

### Step 6: Validate Output Artifacts

For each workflow with non-empty `outputs`:

1. Read the workflow's template files and step files
2. Search for the output filename pattern
3. Note any differences (e.g., date templates, path variations)

Report format:
```
| Workflow | Claimed Output | Found In | Actual Pattern | Status |
```

### Step 7: Find Unclaimed Entities

1. Glob for all directories in `src/modules/bmm/workflows/*/`
2. Glob for all `.agent.yaml` files in `src/modules/bmm/agents/`
3. **Filter out intentional exclusions** (see "Intentional Exclusions" section above):
   - `excalidraw-diagrams/`
   - `testarch/`
   - `document-project/`
4. Compare remaining directories against manifest claims
5. List anything in source but NOT in manifest AND not in exclusions

### Step 8: Compile Final Report

Produce a summary:

```
## Validation Summary

| Category | Claims | Verified | Issues |
|----------|--------|----------|--------|
| Phase Directories | N | N | N |
| Agent Properties | N | N | N |
| Workflow Locations | N | N | N |
| Agent Relationships | N | N | N |
| Output Artifacts | N | N | N |

## Issues Found

### Critical (entity missing)
- [list]

### Medium (property mismatch)
- [list]

### Low (inconsistency)
- [list]

## Unclaimed in Source
- [directories/files that exist but manifest doesn't mention]
- Note: Intentionally excluded directories (excalidraw-diagrams, testarch, document-project) are NOT listed here

## Verdict
[PASS | PASS WITH WARNINGS | FAIL]
```

## Rules

- **Only `src/` is evidence.** Ignore `docs/`, `tools/`, other directories.
- **Line numbers required** for property verifications.
- **Exact match** - `name: Mary` must match `name: Mary`.
- **Flag all mismatches** - even minor ones like filename patterns.

## Parallelization

Run these in parallel for speed:
- Phase directory validation
- Agent validation (can split by agent)
- Workflow validation by phase (Phase 1-2, Phase 3, Phase 4, Core+QuickFlow)

Use the Task tool with Explore subagents for each parallel validation.
