# Launch Sequence (Real Claude Code Primitives)

## Prerequisites

- Upstream artifacts exist in `{planning_artifacts}/upstream/` (or wherever)
- User has reviewed raw artifacts and confirmed they're ready for synthesis

## Phase 0: Pyramid Preprocessing

Run one Haiku agent per upstream artifact. These are independent — launch in parallel.

```
# In Claude Code, call multiple Agent tools in a single message:

Agent(
  subagent_type="general-purpose",
  model="haiku",
  description="Pyramidize comp analysis",
  prompt="<pyramid-preprocessor-prompt.md content, with paths filled in>"
)

Agent(
  subagent_type="general-purpose",
  model="haiku",
  description="Pyramidize user research",
  prompt="<pyramid-preprocessor-prompt.md content, with paths filled in>"
)

# ... one per artifact, all in parallel
```

**Wait for all to complete.** Verify each output has valid frontmatter.

## Phase 1: Create Team

```
TeamCreate(team_name="prd-synthesis")
```

## Phase 2: Spawn Artifact Owners

Launch in parallel — they're independent:

```
Agent(
  subagent_type="general-purpose",
  team_name="prd-synthesis",
  name="comp-analysis",
  model="haiku",
  description="Own comp analysis pyramid",
  prompt="<teammate-prompt.md, with ARTEFACT-NAME and ARTEFACT-PATH filled in>"
)

Agent(
  subagent_type="general-purpose",
  team_name="prd-synthesis",
  name="user-research",
  model="haiku",
  description="Own user research pyramid",
  prompt="<teammate-prompt.md, with ARTEFACT-NAME and ARTEFACT-PATH filled in>"
)

# ... one per pyramid artifact
```

**Wait for ready confirmations** from all teammates (they'll message the Synthesizer).

## Phase 3: Spawn Lead Synthesizer

```
Agent(
  subagent_type="general-purpose",
  team_name="prd-synthesis",
  name="Synthesizer",
  model="sonnet",
  description="Lead PRD synthesis",
  prompt="<synthesizer-prompt.md, with teammate roster and output path filled in>"
)
```

The Synthesizer drives from here — querying teammates, logging tensions, building sections.

## Phase 4: Human Review

After Synthesizer declares complete:

1. Read the generated PRD
2. Check the tension tasks: `TaskList` to see unresolved tensions
3. Run existing BMAD review skills:
   - `bmad-review-adversarial-general` (cynical review)
   - `bmad-editorial-review-structure` (structural integrity)
   - `bmad-editorial-review-prose` (copy quality)
4. Refine as needed

## Phase 5: Cleanup

```
# Shutdown teammates
SendMessage(type="shutdown_request", recipient="comp-analysis", content="Synthesis complete")
SendMessage(type="shutdown_request", recipient="user-research", content="Synthesis complete")
# ... each teammate

# After all confirm shutdown
TeamDelete()
```

## Notes

- Phase 0 can run outside the team — just parallel Haiku agents, no coordination needed
- If an artifact is high-stakes (e.g., regulatory research), promote its owner to `model="sonnet"`
- The Synthesizer may take multiple turns as it queries teammates and waits for responses
- Tensions logged as tasks persist after team cleanup — they're in the task list
