# create-prd-cc: Pyramidal Synthesis Design

## The Idea

Replace the current create-prd's "load all upstream docs into one context and hope for the best" with a multi-agent architecture where:

- Each upstream artifact gets its own Haiku agent that **owns** it as source of truth
- A Sonnet lead agent **synthesizes** across them by asking precise questions
- No single agent holds everything — the lead works from summaries + targeted queries

## Reality Check: What Claude Code Teams Actually Support

### What exists

| Primitive | How it works |
|-----------|-------------|
| `TeamCreate` | Creates team + shared task list. JSON config at `~/.claude/teams/{name}/config.json` |
| `Agent` tool with `team_name` | Spawns a teammate. Goes idle after initial work. Wakes on message. |
| `SendMessage` type: "message" | DM to a specific teammate by name |
| `SendMessage` type: "broadcast" | Message all teammates (expensive) |
| `TaskCreate/TaskUpdate/TaskList` | Shared task list all teammates can read/write |
| `Agent` `model` param | `"haiku"`, `"sonnet"`, `"opus"` — per-agent model selection |

### What doesn't exist

- Declarative YAML team configs (no `load:`, no `memory:` directives)
- `/team` slash commands
- Auto-loading documents into agent context
- Token budget introspection or reporting
- Mailbox abstraction or @-tagging
- Content hashing

## Architecture: How It Actually Works

### Phase 0: Pyramid Preprocessing (before team launch)

Before the team spins up, each upstream artifact needs pyramidal structure.
This is a **batch preprocessing step** — run once per artifact.

**Input:** Raw upstream docs (research reports, brainstorming outputs, competitive analysis, etc.)

**Output:** Pyramid-structured versions with frontmatter:

```yaml
---
artifact_type: competitive-analysis
governing_insight: "One sentence — the single most important takeaway"
key_claims:
  - claim: "Claim text"
    evidence_strength: strong|moderate|anecdotal
    section: "## Section Name"
  - claim: "..."
tensions:
  - "Tension or contradiction within this artifact"
sections:
  - id: "s1"
    heading: "## Market Leaders"
    summary: "10-word summary of this section"
  - id: "s2"
    heading: "## Emerging Competitors"
    summary: "10-word summary"
---

# Competitive Analysis (Pyramid)

## Governing Insight
{the single most important takeaway — reader who stops here gets the gist}

## Key Claims
{numbered, each with evidence strength}

## Tensions & Contradictions
{explicitly surfaced — never summarized away}

---

{full original content, organized by section with stable IDs}
```

**How to run it:** A simple Haiku agent per artifact. Embarrassingly parallel.

```
Agent(
  subagent_type="general-purpose",
  model="haiku",
  prompt="""Read {path/to/raw-artifact.md}.
  Restructure it into pyramid format:
  1. Extract the single governing insight
  2. List key claims with evidence strength
  3. Surface any internal tensions or contradictions
  4. Add section-level TOC with 10-word summaries
  5. Preserve ALL original content — restructure, don't summarize
  Write output to {path/to/upstream/artifact-pyramid.md}"""
)
```

### Phase 1: Team Launch

```
TeamCreate(team_name="prd-synthesis")
```

### Phase 2: Spawn Artifact Owners (Haiku teammates)

One agent per upstream pyramid. Each gets a prompt that:
1. Reads its artifact fully
2. Announces readiness with its governing insight
3. Goes idle, waiting for queries

```
Agent(
  subagent_type="general-purpose",
  team_name="prd-synthesis",
  name="comp-analysis",
  model="haiku",
  prompt="""You OWN the competitive analysis pyramid.
  You are the single source of truth for it.

  FIRST ACTION: Read /path/to/upstream/comp-analysis-pyramid.md completely.

  Core rules (never break):
  - Answer ONLY from your owned artifact.
  - Every answer must end with exact citation: [section-id] or "NOT_FOUND".
  - If nuance or tension exists, surface both sides explicitly.
  - Never summarize away contradictions.
  - If you detect a conflict with what another teammate claims,
    use TaskCreate to log it as a tension.

  After reading, send a message to Synthesizer confirming you're ready,
  including your artifact's governing insight.

  Then wait for queries."""
)
```

Repeat for each upstream artifact: `user-research`, `market-sizing`, `domain-research`, `brainstorming`, etc.

### Phase 3: Spawn the Lead Synthesizer

```
Agent(
  subagent_type="general-purpose",
  team_name="prd-synthesis",
  name="Synthesizer",
  model="sonnet",
  prompt="""You are the Lead Synthesizer building a PRD from upstream artifacts.

  You do NOT hold the upstream artifacts yourself.
  You work by querying your teammates, who each own one artifact.

  Your teammates (each owns one pyramid):
  - comp-analysis: competitive analysis
  - user-research: user research findings
  - market-sizing: market sizing data
  - domain-research: domain/industry research
  - brainstorming: brainstorming session outputs

  ## Your Protocol

  You may only do these things:
  1. QUERY a teammate: SendMessage to ask a precise question
  2. LOG A TENSION: TaskCreate when you find cross-artifact contradictions
  3. DRAFT A PRD SECTION: write a section of the PRD
  4. DECLARE SYNTHESIS COMPLETE: when all sections are drafted

  ## Your Process

  ### Step 1: Collect Governing Insights
  Message each teammate asking for their governing insight and key claims.
  Wait for all responses.

  ### Step 2: Identify the Governing Insight for the PRD
  From the collected insights, synthesize the ONE governing insight
  for the product. This is the pyramid peak — everything else supports it.
  Log any tensions between artifacts.

  ### Step 3: Build PRD Sections
  For each PRD section, query the relevant teammates for supporting evidence.
  Always cite which teammate + section-id the evidence comes from.

  PRD sections to build:
  - Executive Summary (governing insight + what makes this special)
  - Target Users & Journeys
  - Success Criteria & Metrics
  - Domain Considerations
  - Scope & MVP Definition
  - Functional Requirements
  - Non-Functional Requirements

  ### Step 4: Adversarial Self-Review
  Before declaring complete, review each section:
  - Does the evidence actually support the claims?
  - Are there tensions that were smoothed over instead of preserved?
  - Would a skeptic find gaps?
  Log any issues as tasks.

  ### Step 5: Write Output
  Write the complete PRD to {planning_artifacts}/prd.md
  Include all citations and unresolved tensions.

  ## Rules
  - NEVER fabricate evidence. If no teammate can support a claim, say so.
  - Preserve tensions — they are features, not bugs.
  - Every claim in the PRD must trace to a teammate + section-id.
  - When teammates contradict each other, include both perspectives."""
)
```

### Phase 4: Human Review & Refinement

After synthesis completes, the PRD goes through:

1. **Structural editorial review** — pyramid integrity check
   (does the executive summary actually govern? do sections support it?)
2. **Adversarial review** — existing BMAD cynical review skill
3. **Prose editorial review** — existing BMAD editorial skill
4. **Human approval** — the user reviews and refines

## What Changes vs. Current create-prd

| Current | create-prd-cc |
|---------|--------------|
| Single agent loads ALL upstream docs | Each doc gets its own Haiku agent |
| 13-step sequential conversation | Preprocessing → team synthesis → review |
| User drives every step interactively | Synthesis is automated; human reviews output |
| Upstream docs are flat/unstructured | Upstream docs are pyramidally preprocessed |
| Tensions between docs are invisible | Tensions are explicitly surfaced and preserved |
| No citation/traceability | Every claim traces to source artifact + section |

## What This Doesn't Replace

- The **collaborative discovery** steps (2, 2b) — when there ARE no upstream artifacts
  and the user needs to articulate vision through conversation. That's a different mode.
- The **product brief** — but it shrinks from a full workflow to a single pyramidal
  assertion (governing insight) that gets stress-tested before PRD construction.
- **Advanced Elicitation / Party Mode** — these remain as refinement tools on the output.

## Open Questions

1. **Hybrid mode?** What if you have SOME upstream artifacts but also need interactive
   discovery? The current workflow handles greenfield well. This redesign handles
   artifact-rich scenarios well. Need a router.

2. **How many teammates is practical?** Each Haiku agent costs a spawn + stays in memory.
   With 3-5 upstream artifacts, this is fine. With 15, it might get unwieldy.
   Consider: merge related artifacts (e.g., all research into one agent).

3. **The brief question.** Current design has a full product-brief workflow
   (6 interactive steps). The proposed redesign replaces this with a synthesized
   governing insight. Is that enough? Or does the human need the forcing function
   of the brief workflow to actually make decisions?

4. **Step-file architecture compatibility.** The current PRD steps expect to run in
   a single long conversation with one agent. The team-based approach is fundamentally
   different. This is a parallel workflow, not a sequential replacement. Both should exist.
