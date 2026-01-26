# Generate BMM Workflow Diagram

This prompt generates a D2 diagram showing the BMad Method (BMM) workflow phases and their workflows.

## Instructions

Read workflow structure from the manifest and generate a D2 diagram with the following specifications:

### 1. Load Workflow Manifest

Read `tools/diagrams/workflow-manifest.yaml` to get:

- **Version info**: `bmad_version` for the diagram title
- **Domain context** (`domain`):
  - `phases`: All 4 phases with labels, directories, optional flags, parallel flags
  - `quick_flow`: Quick-flow path info
  - `tracking_systems`: Sprint status tracking info
- **Inventory** (`inventory`):
  - `agents`: List of agents (id, module, name, title, icon)
  - `workflows`: All workflows with id, module, phase, name, agent, outputs, next_steps
  - `connections`: Cross-phase connections (if any)
  - `legend`: Output documents with descriptions
- **Annotations** (`annotations`):
  - `decisions`: Decision points (e.g., "Has UI?" after prd)
  - `standalone_workflows`: Workflows that run ad-hoc (e.g., correct-course)
  - `optional_workflows`: Workflows not required in main flow (e.g., quick-spec)
  - `feedback_loops`: Phase 4 loops (code-review→dev-story, retrospective→sprint-planning)
  - `output_descriptions`: Human-readable descriptions of output files
  - `agent_descriptions`: Human-readable descriptions of agent roles

**Do NOT scan the codebase** - all workflow information is in the manifest.

### 2. Diagram Structure

```
direction: down

# Top-level vertical layout
grid-rows: 4
grid-columns: 1
grid-gap: 20

# Row 1: Title (Left aligned)
title-row: "" {
  style.fill: transparent
  style.stroke: transparent
  grid-rows: 1
  grid-columns: 1
  horizontal-gap: 0

  title: "BMAD METHOD V{VERSION}" {
    style.fill: transparent
    style.stroke: transparent
    style.font-size: 48
    style.bold: true
    style.font-color: "#1a3a5c"
    label.near: top-left
  }
}

vars: {
  d2-config: {
    layout-engine: elk
  }
}

# Row 2: Legend Placeholder
legend-row: "" {
  style.fill: transparent
  style.stroke: transparent
  height: 250
  width: 1200
  grid-rows: 1
  grid-columns: 1
}

# Row 3: Lanes container
lanes with grid-columns: 4

# Row 4: Footer
footer-row: "" {
  style.fill: transparent
  style.stroke: transparent
  footer: "DRAFTED: {DATE} • REPOSITORY: github.com/bmad-code-org/BMAD-METHOD • LICENSE: MIT • UNCLASSIFIED • DISTRIBUTION: UNLIMITED • SUPERSEDES: ALL PREVIOUS EDITIONS" {
    style.fill: transparent
    style.stroke: transparent
    style.font-size: 21
    style.font-color: "#555"
    style.italic: true
    label.near: bottom-left
  }
}
```

### 3. Phase Layout

Each phase is a colored container:

- **Phase 1 (Discovery)**: Teal/cyan (#e8f4f8), dashed border
  - Filter `inventory.workflows` where `phase: discovery`
  - Group activities (brainstorming, research) in a generic "Activities" box
  - Feed into `product-brief`
- **Phase 2 (Planning)**: Purple/lavender (#f0e8f8)
  - Filter `inventory.workflows` where `phase: planning`
  - **EXCLUDE**: `quick-spec` (part of quick flow, not main diagram)
  - Workflows: `/prd`, `/create-ux-design`
  - "Has UI?" decision logic
- **Phase 3 (Solutioning)**: Gold/amber (#f8f0e8)
  - Filter `inventory.workflows` where `phase: solutioning`
  - Workflows: `/create-architecture`, `/create-epics-and-stories`, `/check-implementation-readiness`
- **Phase 4 (Implementation)**: Green/mint (#e8f8f0)
  - Filter `inventory.workflows` where `phase: implementation`
  - Workflows: `/sprint-planning`, `/create-story`, `/dev-story`, `/code-review`, `/retrospective`
  - Include `/correct-course` as standalone utility at bottom
  - Show feedback loops

### 4. Naming Convention

- Forward slash prefix: `/workflow-name`
- Workflows with outputs show `@filename` on second line

### 5. Styling Classes

Use explicit `style` blocks:

```d2
classes: {
  phase1-box: {
    style: {
      fill: "#e8f4f8"
      stroke: "#2d7d9a"
      stroke-width: 3
      border-radius: 12
      font-size: 27
      bold: true
      font-color: "#1a5568"
    }
  }
  # phase2-box (purple), phase3-box (gold), phase4-box (green) follow similar pattern
  
  n1: {
    style: {
      fill: "#fff"
      stroke: "#2d7d9a"
      stroke-width: 2
      border-radius: 4
      font-size: 27
    }
  }
  # n2, n3, n4 follow similar pattern matching phase colors
  
  decision: {
    shape: diamond
    style: {
      fill: "#fff8e8"
      stroke: "#7d2d9a"
      stroke-width: 2
      font-size: 27
    }
  }
}
```

### 6. Post-Processing

1. **Shrink Output Labels**: Make `@*.md` labels smaller and gray.
2. **Outline Title**: Apply hollow effect to title.
3. **Left Align Title**: Ensure title is left-aligned.
4. **Inject Legend**: Inject into `legend-row` area (approx Y=180).
5. **Inject Stamp**: Inject red herring stamp **if file exists**. Skip if missing.

### 7. Output Generation

1. `d2 ... bmm-workflow.d2 bmm-workflow-technical.svg`
2. `python3 post-process-svg.py`
3. `rsvg-convert ...`

### 8. Self-Check

- [ ] Legend does not overlap content (height=250px placeholder)
- [ ] `quick-spec` is excluded
- [ ] Diagram starts with Discovery/Planning (no "Sprint Status" init box)
- [ ] Fonts are consistent (ShareTechMono)
- [ ] Stamp injection is skipped if file missing without error
