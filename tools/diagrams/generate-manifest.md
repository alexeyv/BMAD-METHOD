# Generate BMM Workflow Manifest

This prompt generates a YAML manifest of BMM and core workflows/agents by discovering what actually exists in source. It uses a three-part architecture (Domain + Inventory + Annotations) with git-anchored change validation to eliminate LLM variance.

---

## Domain Context (Static Knowledge)

Before executing any phase, absorb this stable structure knowledge. This is your frame of reference - workflows and agents within are DISCOVERED, not assumed.

```yaml
# Domain Context - Provided knowledge, not discovered
modules:
  # Core module - foundational workflows/agents available to all modules
  core:
    description: |
      Foundation module with base agents and workflows used across all modules.
      Core workflows have no phase - they are utilities invoked by other workflows.
    source_root: 'src/core'
    agents_path: 'src/core/agents'
    workflows_path: 'src/core/workflows'
    manifest_rules:
      exclude_agents:
        - bmad-master  # Orchestrator only - has no workflow ownership
      workflow_agent_assignment: |
        Core workflows are generic utilities, not owned by any agent.
        - Set `agent: null` for all core workflows
        - Populate `alternate_agents` with any BMM agents that claim the
          workflow in their menu (exec or workflow trigger)

  # BMM module - the BMad Method with phased workflows
  bmm:
    description: |
      BMM (BMad Method) is a 4-phase software development methodology.
      Phases are sequential, but Phase 1 (Discovery) is optional.
      Quick-flow is a parallel fast-track for experienced teams.
    source_root: 'src/bmm'
    agents_path: 'src/bmm/agents'
    workflows_path: 'src/bmm/workflows'

bmm_structure:
  source_root: 'src/bmm/workflows'

  phases:
    - key: discovery
      label: 'PHASE 1: DISCOVERY'
      directory: '1-analysis'
      behavior: parallel # Workflows can run in any order
      optional: true

    - key: planning
      label: 'PHASE 2: PLANNING'
      directory: '2-plan-workflows'
      behavior: sequential

    - key: solutioning
      label: 'PHASE 3: SOLUTIONING'
      directory: '3-solutioning'
      behavior: sequential

    - key: implementation
      label: 'PHASE 4: IMPLEMENTATION'
      directory: '4-implementation'
      behavior: iterative # Has feedback loops

  quick_flow:
    directory: 'bmad-quick-flow'
    description: 'Fast-track path bypassing full discovery/planning'

  scan_rules:
    include:
      - '1-analysis/*'
      - '2-plan-workflows/*'
      - '3-solutioning/*'
      - '4-implementation/*'
      - 'bmad-quick-flow/*'
    exclude:
      - 'excalidraw-diagrams/*' # Diagram generation, not BMM phases
      - 'testarch/*' # Test architecture, separate concern
      - 'document-project/*' # Utility workflow

  tracking_systems:
    # Note: workflow_status tracking removed - see help.md task for current approach

    sprint_status:
      file: '@sprint-status.yaml'
      covers: [implementation]
      description: 'Per-story iterative tracking with explicit state machine'
      entities:
        epic:
          states:
            - backlog # Epic not yet started
            - in-progress # Epic actively being worked on
            - done # All stories in epic completed
        story:
          states:
            - backlog # Story only exists in epic file
            - drafted # Story file created
            - ready-for-dev # Draft approved, ready for implementation
            - in-progress # Developer actively working
            - review # Ready for code review
            - done # Completed
        retrospective:
          states:
            - optional # Can be completed but not required
            - completed # Retrospective done
```

**Migration Note (v6.0.0-alpha.23):** The `workflow-status` tracking system was removed in commit `e29a1273` (Jan 2026). If running against a manifest generated before this change, manually remove:
- `domain.entry` section (workflow-init no longer exists)
- `tracking_systems.workflow_status` block
- `tracking_systems.handoff` block
- `workflow-init` from `inventory.workflows`
- `@bmm-workflow-status.yaml` from `inventory.legend`

**Critical understanding:**

- The phase structure (4 phases + quick-flow) IS the frame
- Workflows within each phase are DISCOVERED from source
- NEVER assume a workflow exists - only report what you find
- `typical_workflows` would be hints; we don't use them to avoid confirmation bias

---

## Phase 1: Verify Domain Context (Rot Check)

**Objective:** Confirm the domain context above still matches reality. If structure changed, STOP.

### Checks to Perform

1. **Directory Existence**

   ```
   # Core module
   [ ] src/core/ exists
   [ ] src/core/agents/ exists
   [ ] src/core/workflows/ exists

   # BMM module
   [ ] src/bmm/ exists
   [ ] src/bmm/agents/ exists
   [ ] src/bmm/workflows/ exists
   [ ] 1-analysis/ exists
   [ ] 2-plan-workflows/ exists
   [ ] 3-solutioning/ exists
   [ ] 4-implementation/ exists
   [ ] bmad-quick-flow/ exists
   ```

2. **No Unexpected Structure**
   - List all top-level directories in `src/bmm/workflows/`
   - Compare against: `1-analysis`, `2-plan-workflows`, `3-solutioning`, `4-implementation`, `bmad-quick-flow`, plus excluded dirs (`excalidraw-diagrams`, `testarch`, `document-project`)
   - If ANY directory exists that is NOT in this list → **HARD STOP**
   - Report: "Unexpected directory found: `<dirname>`. Domain context may be stale."

3. **Excluded Directories Still Excluded**
   - Verify excluded dirs (`excalidraw-diagrams/`, `testarch/`, `document-project/`) are NOT inside phase directories
   - If any appear inside a phase dir → **HARD STOP**

### Outcomes

- **ALL CHECKS PASS** → Proceed to Phase 2
- **ANY CHECK FAILS** → **HARD STOP**
  - Report exactly what failed
  - Instruction: "Update the prompt's domain context section, then re-run"

---

## Phase 2: Guided Discovery

**Objective:** Scan source directories and extract what actually exists. No assumptions.

### Step 2.1: Gather Metadata

```bash
# Get current git commit
git rev-parse --short HEAD

# Get BMAD version from package.json
# Extract "version" field

# Get current ISO timestamp
```

### Step 2.2: Discover Agents

**Objective:** Build agent roster and agent-to-workflows map for later assignment.

1. **Scan agent files from all modules**

   ```
   Glob: src/core/agents/*.agent.yaml        → module: core
   Glob: src/bmm/agents/*.agent.yaml → module: bmm
   ```

2. **For each agent file:**
   - Determine `module` from path (`src/core/` → `core`, `src/bmm/` → `bmm`)
   - Extract `id` from filename (e.g., `sm.agent.yaml` → `sm`)
   - Read `agent.metadata.name` → `name`
   - Read `agent.metadata.title` → `title`
   - Read `agent.metadata.icon` → `icon`
   - Read `agent.menu[]` → collect all workflow triggers
   - Build agent roster entry and agent-to-workflows mapping

3. **Build inventory.agents roster**

   ```yaml
   agents:
     - id: <agent-id> # From filename
       module: <module> # core or bmm
       name: <name> # From agent.metadata.name
       title: <title> # From agent.metadata.title
       icon: <icon> # From agent.metadata.icon
   ```

4. **Build agent-to-workflows map** (internal, for Step 2.3)

   ```yaml
   agent_workflows:
     <agent-id>: [<workflow-id>, <workflow-id>, ...]
     # Collected from agent.menu[] entries
   ```

5. **Report agent discovery**

   ```
   Discovered N agents:
     - core: [list core agent ids]
     - bmm: [list bmm agent ids]
   ```

### Step 2.3: Discover Phase Workflows

For EACH phase directory (`1-analysis`, `2-plan-workflows`, `3-solutioning`, `4-implementation`):

1. **List subdirectories** - each is a potential workflow
2. **For each subdirectory:**
   - Look for `workflow.yaml` OR `workflow.md`
   - If neither exists → skip (not a workflow)
   - Extract from config:
     - `id`: directory name
     - `name`: from config `name` field, prefix with `/`
     - `outputs`: extract using the rules below

3. **Output Extraction Rules** (in priority order):

   **For YAML configs (`workflow.yaml`):**
   - Look for `default_output_file` field → use that value
   - If not found → `outputs: []`

   **For Markdown configs (`workflow.md`):**
   - Look for `default_output_file` in frontmatter or `### Paths` section
   - Extract any additional output files listed (e.g., HTML files)
   - If found → use those values
   - If NOT found → check for sharded workflow (below)

   **For Sharded workflows (`workflow.md` + `steps/` directory):**
   - Check if `steps/` subdirectory exists
   - If yes, scan `steps/step-01*.md` files (init steps declare outputs)
   - Look for `outputFile:` in YAML frontmatter
   - Extract the filename from the path pattern:
     - `'{planning_artifacts}/prd.md'` → `@prd.md`
     - `'{planning_artifacts}/implementation-readiness-report-{{date}}.md'` → `@implementation-readiness-report.md` (strip template vars)
   - Normalize: strip path placeholders, strip `{{...}}` template variables, prefix with `@`
   - If multiple step-01 files exist (e.g., step-01-init.md, step-01b-continue.md), use the first one with `outputFile:`
   - If no `outputFile:` found in step files → `outputs: []`

   **Filename Normalization Rules:**
   - Remove path prefix: `{planning_artifacts}/`, `{implementation_artifacts}/`, etc.
   - Remove template variables: `{{date}}`, `{{project_name}}`, etc. (and surrounding hyphens/underscores)
   - Prefix with `@`
   - Examples:
     - `'{planning_artifacts}/implementation-readiness-report-{{date}}.md'` → `@implementation-readiness-report.md`
     - `'{planning_artifacts}/product-brief-{{project_name}}-{{date}}.md'` → `@product-brief.md`
     - `'{planning_artifacts}/prd.md'` → `@prd.md`

   Note: Output _descriptions_ for the legend come from annotations, not discovery.

4. **Read instructions** to find connections:
   - Look in `instructions.md`, `workflow.md`, or `steps/*.md` files
   - Search for these patterns:
     - `` `workflow <name>` `` - explicit workflow command reference
     - `/workflow-name` - slash command reference
     - `workflow: <name>` - YAML reference
     - `{*_workflow}` - placeholder variable (e.g., `{quick_dev_workflow}`) → extract workflow name from variable name
     - Narrative: "proceed to", "next step", "→", "then run"
   - For placeholder variables like `{quick_dev_workflow}`:
     - Extract the workflow name: `quick_dev_workflow` → `quick-dev`
     - Record connection to that workflow
   - Record as `next_steps` with evidence: `"line N: '<quoted text>'"` or `"file.md:N: '<quoted text>'"`

5. **Assign agent to workflow** (using data from Step 2.2):

   a. **Check agent files for workflow**
   - Search agent-to-workflows map from Step 2.2 for this workflow
   - Collect all agents that claim this workflow in their menu
   - Use first claiming agent as `agent`
   - Remaining agents → `alternate_agents`

   b. **Handle no agent found**
   - IF no agent found in any agent menu:
     - Set `agent: null`
     - No warning (agentless workflows are valid)

   c. **Build workflow entry with agent**

   ```yaml
   - id: <workflow-id>
     module: bmm
     phase: <phase>
     name: /<workflow-name>
     agent: <agent-id>
     alternate_agents: [...]
     outputs: [...]
     next_steps: [...]
   ```

   Note: `agent_source` is NOT written to manifest - it's only used for Discovery Report output.

### Step 2.4: Discover Quick Flow Workflows

Apply same process to `bmad-quick-flow/`:

- Use `module: bmm` and `phase: quick_flow` to indicate these are quick-flow workflows

### Step 2.4a: Discover Core Workflows

Scan `src/core/workflows/`:

1. **List subdirectories** - each is a potential workflow
2. **For each subdirectory:**
   - Look for `workflow.yaml` OR `workflow.md`
   - If neither exists → skip (not a workflow)
   - Extract from config:
     - `id`: directory name
     - `name`: from config `name` field, prefix with `/`
     - `outputs`: extract using output extraction rules
3. **Tag with module, no phase:**
   - `module: core`
   - No `phase` field (core workflows are not part of BMM phases)
4. **Agent assignment:** Apply same agent assignment logic from Step 2.3.5

### Step 2.5: Build Inventory Section

Compile all discovered data into the inventory structure:

1. **Include agents roster** (from Step 2.2)

   ```yaml
   inventory:
     agents:
       - id: <agent-id> # From filename
         module: <module> # core or bmm
         name: <agent-name> # From agent.metadata.name
         title: <agent-title> # From agent.metadata.title
         icon: <agent-icon> # From agent.metadata.icon
   ```

2. **Include workflows with agent assignments** (from Steps 2.3, 2.4, and 2.4a)

   ```yaml
   workflows:
     # BMM workflow (has phase)
     - id: <workflow-id>
       module: bmm
       phase: <phase_key> # From parent directory (BMM only)
       name: /<workflow-name>
       agent: <agent-id> # From Step 2.3.5 (or null if agentless)
       alternate_agents: [] # From Step 2.3.5b
       outputs:
         - '@filename.md' # Just the file, no description
       next_steps: # From instructions
         - workflow: <target-id>
           evidence: "line N: '...'"

     # Core workflow (no phase)
     - id: <workflow-id>
       module: core
       name: /<workflow-name>
       agent: <agent-id>
       alternate_agents: []
       outputs: [...]
       next_steps: [...]
   ```

### Step 2.6: Derive Connections

From all `next_steps`, build connections array:

```yaml
connections:
  - from: <source-id>
    to: <target-id>
    type: sequential|converge
    scope: within-phase|cross-phase
```

### Step 2.7: Build Legend

Aggregate all unique output files, pulling descriptions from `annotations.output_descriptions`:

```yaml
legend:
  - file: '@filename.md'
    description: '...' # From annotations.output_descriptions
```

If an output file has no entry in `output_descriptions`, use an empty description or flag for human review.

### Step 2.8: Agent Consistency Validation

**Objective:** Cross-validate agent assignments and emit warnings for inconsistencies.

1. **Validate agent menu claims against inventory**

   For each agent in roster:
   - For each workflow in agent's menu:
     - Check if workflow exists in discovered inventory
     - IF NOT → **WARN:** `"Agent '{agent}' claims '{workflow}' but workflow not found in inventory"`

2. **Track warning counts**
   - Count orphan claim warnings
   - Store totals for Discovery Report

**Important:** Warnings do NOT block manifest generation. Always generate manifest, surface issues for humans to fix.

### Discovery Report

After completing discovery, report:

```
Discovered:
  Agents:
    - core: N agents [list ids]
    - bmm: N agents [list ids]

  Workflows:
    - core: N workflows [list ids]
    - bmm Phase 1 (discovery): N workflows [list ids]
    - bmm Phase 2 (planning): N workflows [list ids]
    - bmm Phase 3 (solutioning): N workflows [list ids]
    - bmm Phase 4 (implementation): N workflows [list ids]
    - bmm Quick Flow: N workflows [list ids]

  Total: N agents, M workflows, P output files

Agent Assignments:
  ✓ <workflow>: agent=<agent>
  ... (list all workflows with agent assignments)

Warnings:
  ⚠️ Agent '<agent>' claims '<workflow>' but workflow not found in inventory
  ... (list all warnings from Step 2.8)

Summary: N workflows assigned, Y inconsistencies
```

---

## Phase 3: Git-Anchored Diff

**Objective:** Compare discovered inventory against existing manifest. Validate changes via git.

### Step 3.1: Load Existing Manifest

- Path: `docs/diagrams/workflow-manifest.yaml`
- If doesn't exist → skip diff phase (first run)
- Extract `source_commit` from existing manifest

### Step 3.2: Compare Inventories

For each difference found, classify:

| Change Type         | Examples                                     |
| ------------------- | -------------------------------------------- |
| WORKFLOW_ADDED      | New workflow directory discovered            |
| WORKFLOW_REMOVED    | Workflow in old manifest not found in source |
| OUTPUT_CHANGED      | Output files differ                          |
| CONNECTION_CHANGED  | Connections differ                           |
| DESCRIPTION_CHANGED | Only description text differs                |

### Step 3.3: Git Validation

For EACH change:

```bash
OLD_COMMIT="<from existing manifest>"
CURRENT_COMMIT=$(git rev-parse --short HEAD)

# Check if workflow source actually changed
git diff --name-only $OLD_COMMIT..$CURRENT_COMMIT -- src/bmm/workflows/<affected-path>/
```

**Classify result:**

| Git Diff Result  | Classification  | Action                            |
| ---------------- | --------------- | --------------------------------- |
| Files listed     | `GIT_CONFIRMED` | Real change - include in report   |
| Empty (no files) | `LLM_VARIANCE`  | Non-determinism - suppress change |

### Step 3.4: Handle LLM Variance

For `LLM_VARIANCE` changes:

- Default: KEEP old manifest value
- Do NOT include in change report
- Track count for summary: "Suppressed N variance artifacts"

### Step 3.5: Generate Change Report

```
Changes Detected:

GIT_CONFIRMED (require review):
  - WORKFLOW_ADDED: <id>
    Evidence: git diff shows new directory created
  - WORKFLOW_REMOVED: <id>
    Evidence: git diff shows directory deleted

LLM_VARIANCE (suppressed):
  - DESCRIPTION_CHANGED: <id> (no git changes in source)

Summary: N real changes, M variances suppressed
```

---

## Phase 4: Human Gate

**Objective:** Present changes for approval. Handle different change types appropriately.

### Decision Tree

```
IF no existing manifest:
    → First run, write manifest directly
    → Report: "Initial manifest created with N workflows"

ELSE IF all changes are LLM_VARIANCE:
    → Keep old manifest unchanged
    → Update only: generated timestamp, source_commit
    → Report: "No real changes detected (N variances suppressed)"

ELSE IF GIT_CONFIRMED changes exist:
    → Present change report (from Phase 3)
    → Proceed to approval flow
```

### Approval Flow

**For Quick Flow Changes:**

```
⚠️  QUICK FLOW CHANGES DETECTED

The following changes affect the fast-track development path:
<list changes>

Evidence:
<git diff summary>

This is a SIGNIFICANT change affecting Quick Flow users.

Options:
  [1] Accept changes and update manifest
  [2] Reject changes and keep existing manifest
  [3] Show detailed diff

Choose (1/2/3):
```

**For Main Workflow Changes:**

```
📋 WORKFLOW CHANGES DETECTED

Changes:
<list changes>

Evidence:
<git diff summary>

Accept changes? (y/n):
```

### On Approval

Write new manifest with:

1. **Metadata section** - Updated timestamp, commit, version
2. **Domain section** - Copy EXACTLY from this prompt's Domain Context
3. **Inventory section** - From discovery
4. **Annotations section** - Preserve from old manifest (see Annotation Rules below)

### On Rejection

- Keep old manifest unchanged
- Optionally offer: "Update only metadata (timestamp, commit)? (y/n)"

---

## Annotation Preservation Rules

The annotations section contains human-maintained edge cases not encoded in source.

### Preservation Policy

1. **Default: PRESERVE** - Copy annotations unchanged from old manifest
2. **Exception: Workflow Removed** - If annotated workflow no longer exists:
   - Flag for review: "Annotation references removed workflow: `<id>`"
   - Ask: "Remove this annotation? (y/n)"
3. **Never auto-generate** - Annotations come from humans, not discovery

### Standard Annotations (preserve these)

```yaml
annotations:
  decisions:
    - id: has-ui
      after: prd
      label: 'Has UI?'
      branches:
        - condition: 'Yes'
          to: create-ux-design
        - condition: 'No'
          to: create-architecture
      reason: 'UI decision affects whether UX design phase is needed'

  standalone_workflows:
    - id: correct-course
      reason: 'Run ad-hoc when issues arise, not part of main flow'

  optional_workflows:
    - id: quick-spec
      reason: 'Part of quick-flow path, not required in main BMM flow'

  feedback_loops:
    - from: code-review
      to: dev-story
      label: 'fixes'
    - from: retrospective
      to: sprint-planning
      label: 'next epic'

  # Human-authored descriptions for legend (not discoverable from configs)
  # Note: @bmm-workflow-status.yaml removed with workflow_status tracking system
  output_descriptions:
    '@product-brief.md': 'Product vision and requirements'
    '@PRD.md': 'Product requirements document'
    '@ux-design-specification.md': 'UX design and wireframes'
    '@architecture.md': 'System architecture and design'
    '@epics.md': 'Epic and story breakdown'
    '@implementation-readiness-report.md': 'Implementation readiness report'
    '@sprint-status.yaml': 'Sprint status and planning'
    '@{epic}-{story}-*.md': 'Story implementation details'
    '@sprint-change-proposal.md': 'Sprint change proposal'
    '@tech-spec.md': 'Technical specification'

  # Human-maintained agent descriptions (for diagrams and docs)
  agent_descriptions:
    analyst: 'Conducts discovery research, competitive analysis, and product briefs'
    pm: 'Manages product requirements, PRD creation, and epic/story breakdown'
    ux-designer: 'Creates UX designs, wireframes, and design specifications'
    architect: 'Designs system architecture and validates implementation readiness'
    sm: 'Manages sprint planning, story creation, and retrospectives'
    dev: 'Implements stories and conducts code reviews'
    quick-flow-solo-dev: 'Fast-track development from spec to implementation'
    tea: 'Test architecture, quality strategy, and test automation'
    tech-writer: 'Documentation, diagrams, and technical writing'
```

---

## Output Manifest Structure

The final manifest has four sections:

```yaml
# ============================================================
# SECTION 1: METADATA (auto-updated each run)
# ============================================================
version: '1.0'
generated: '<ISO timestamp>'
source_commit: '<git short hash>'
bmad_version: '<from package.json>'

# ============================================================
# SECTION 2: DOMAIN CONTEXT (copied from prompt)
# ============================================================
domain:
  phases:
    discovery:
      label: 'PHASE 1: DISCOVERY'
      directory: '1-analysis'
      optional: true
      parallel: true
    planning:
      label: 'PHASE 2: PLANNING'
      directory: '2-plan-workflows'
      optional: false
      parallel: false
    solutioning:
      label: 'PHASE 3: SOLUTIONING'
      directory: '3-solutioning'
      optional: false
      parallel: false
    implementation:
      label: 'PHASE 4: IMPLEMENTATION'
      directory: '4-implementation'
      optional: false
      parallel: false
      has_feedback_loops: true

  quick_flow:
    directory: 'bmad-quick-flow'
    description: 'Fast-track path for experienced teams'

  tracking_systems:
    # Note: workflow_status tracking removed - see help.md task for current approach

    sprint_status:
      file: '@sprint-status.yaml'
      covers: [implementation]
      description: 'Per-story iterative tracking with explicit state machine'
      entities:
        epic:
          states: [backlog, in-progress, done]
        story:
          states: [backlog, drafted, ready-for-dev, in-progress, review, done]
        retrospective:
          states: [optional, completed]

# ============================================================
# SECTION 3: INVENTORY (discovered from source)
# ============================================================
inventory:
  # Agent roster (discovered from agent files - Step 2.2)
  agents:
    - id: <agent-id> # From filename
      module: <module> # core or bmm
      name: <name> # From agent.metadata.name
      title: <title> # From agent.metadata.title
      icon: <icon> # From agent.metadata.icon
    # ... all discovered agents

  # Workflows (discovered from Steps 2.3, 2.4, 2.4a)
  workflows:
    # BMM workflow example (has module + phase)
    - id: <workflow-id>
      module: bmm
      phase: <phase_key> # BMM only: discovery|planning|solutioning|implementation|quick_flow
      name: /<workflow-name>
      agent: <agent-id> # Primary agent (or null if agentless)
      alternate_agents: [] # Other agents that can run this workflow
      outputs:
        - '@filename.md' # Just file paths, descriptions in annotations
      next_steps:
        - workflow: <target-id>
          evidence: "line N: '...'"

    # Core workflow example (has module, no phase)
    - id: <workflow-id>
      module: core
      name: /<workflow-name>
      agent: <agent-id>
      alternate_agents: []
      outputs: []
      next_steps: []
    # ... all discovered workflows

  connections:
    - from: <id>
      to: <id>
      type: sequential|converge
      scope: within-phase|cross-phase

  legend:
    - file: '@filename.md'
      description: '...' # Pulled from annotations.output_descriptions

# ============================================================
# SECTION 4: ANNOTATIONS (human-maintained)
# ============================================================
annotations:
  decisions:
    - id: has-ui
      after: prd
      label: 'Has UI?'
      branches:
        - condition: 'Yes'
          to: create-ux-design
        - condition: 'No'
          to: create-architecture
      reason: '...'

  standalone_workflows:
    - id: correct-course
      reason: '...'

  optional_workflows:
    - id: quick-spec
      reason: '...'

  feedback_loops:
    - from: code-review
      to: dev-story
      label: 'fixes'
    # ...

  output_descriptions:
    '@filename.md': 'Human-authored description for legend'
    # ...

  agent_descriptions:
    # See "Standard Annotations" section for canonical values
    # ...
```

---

## Self-Check

Before finalizing, verify:

### Completeness

- [ ] Core module directories scanned (`src/core/agents/`, `src/core/workflows/`)
- [ ] BMM module directories scanned (`src/bmm/agents/`, `src/bmm/workflows/`)
- [ ] All BMM phase directories scanned
- [ ] All subdirectories checked for workflow configs
- [ ] All workflow.yaml/workflow.md files read
- [ ] All output files extracted
- [ ] Version, commit, timestamp included
- [ ] All agent files scanned (`*.agent.yaml`) from both modules

### Accuracy

- [ ] Only workflows with actual config files included
- [ ] NO phantom workflows (verify each id maps to real directory)
- [ ] Output files match what's in configs
- [ ] Connections derived from actual instruction text
- [ ] Agent assignments derived from agent menu claims
- [ ] Agent IDs extracted from filenames, not content
- [ ] All agents have correct `module` field (core or bmm)
- [ ] All workflows have correct `module` field
- [ ] BMM workflows have `phase` field, core workflows do not

### Agent Validation

- [ ] `inventory.agents` section includes all discovered agents
- [ ] Each workflow has `agent` field (primary or null)
- [ ] Each workflow has `alternate_agents` array
- [ ] `annotations.agent_descriptions` section present
- [ ] Warnings emitted for orphan menu claims

### Git Validation

- [ ] Changes validated against git diff
- [ ] LLM variance suppressed for non-git-confirmed changes
- [ ] Evidence recorded for all confirmed changes

### Determinism

- [ ] Running twice on same source produces identical output
- [ ] No description fields that could vary between runs
- [ ] Manifest anchored to specific git commit

---

## Execution Summary

```
Phase 1: Rot Check      → Verify structure matches domain context
Phase 2: Discovery      → Scan source, extract workflows/outputs/connections
Phase 3: Git Diff       → Compare with old manifest, validate via git
Phase 4: Human Gate     → Present changes, get approval, write manifest
```

**Key guarantees:**

1. Only reports workflows that EXIST in source
2. Changes must be GIT_CONFIRMED or they're suppressed
3. Domain structure is static; inventory is dynamic
4. Annotations are preserved unless explicitly removed

---

## Notes

- This is an **agentic prompt** for manifest generation
- The manifest is the **source of truth** for diagram generation
- Quick Flow changes require **hard stop** approval
- Main workflow changes require **user approval**
- LLM variance is **auto-suppressed** via git validation
