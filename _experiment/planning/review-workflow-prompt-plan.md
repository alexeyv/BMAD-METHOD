# Planning Prompt: review-workflow-prompt Skill

Design a BMAD skill called `review-workflow-prompt` (or similar) that adversarially reviews agentic workflow step files — the kind of prompt files that tell LLMs what to do in a multi-step workflow.

The skill runs three review agents in parallel against a target step file, then aggregates and deduplicates their findings. The three perspectives are:

**1. Context Asymmetric** — The agent receives ONLY the target step file with zero surrounding context (no workflow.md, no config, no conversation history). It reports every point where it would be confused, stuck, or forced to guess. Finds comprehension gaps, undefined references, and implicit dependencies that break when a fresh agent encounters the file.

**2. Edge Cases & Failure Modes** — The agent receives the target step file WITH full codebase access. It walks every branching path and finds scenarios where instructions break down, loop infinitely, deadlock, produce undefined behavior, or silently corrupt state. It checks cross-file consistency (variable definitions, handoffs between steps, schema mismatches).

**3. Fit for Purpose** — The agent receives the target step file WITH full codebase access and evaluates holistically: Does it achieve its stated goal? Is it token-efficient (no waste, no under-investment)? Are there ambiguities where two frontier LLMs would diverge? Are there internal contradictions (e.g., rules that conflict with instructions)? Does it comply with the workflow's own declared standards and principles?

All three agents operate under the constraint: **find problems only, do not suggest improvements.**

The aggregation step (run by the orchestrator, not a sub-agent) should:
- Deduplicate across the three perspectives
- Classify each unique finding by severity (critical / high / medium / low)
- Present only findings worth acting on, with a short rationale for each
- Report noise rate per agent for calibration

The skill should work within the existing BMAD skill/task architecture. Consider: how it's invoked, what inputs it needs (target file, optional context files), output format, and where it fits in the workflow lifecycle (standalone tool vs. integrated into a specific step like step-04-review).

Reference the existing `bmad-review-adversarial-general` skill/task for architectural patterns. The new skill should complement, not replace, the existing adversarial review.
