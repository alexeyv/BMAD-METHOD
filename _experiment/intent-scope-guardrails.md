# Intent: Add Scope Guardrails to Quick-Dev2 Workflow

## Problem

Quick-dev2 has no protection against oversized or multi-goal stories. Users dump raw intent that spans independent features or balloons past 1200 words, leading to context-rot in implementation agents.

### Why This Is Hard

Research (Gemini, Grok — see `_experiment/ideal-spec-*.md`) converges on 400–1200 words as the optimal spec size for LLM consumption, but neither explains how to enforce that when you don't control the input. This is a chicken-and-egg problem: the user doesn't know the right scope until the spec exists, but the spec can't be right-sized until the scope is bounded. You can't solve it at either end alone — gate too early and you're guessing without information; gate too late and you've already burned tokens and user time on an oversized draft.

No clean solution exists. The pragmatic answer is two cheap checkpoints — one at routing (semantic, before any writing) and one after drafting (empirical, word count in hand) — with the user making the final call at both. This doesn't solve the wicked problem; it just creates two low-cost moments to course-correct.

## Desired Behavior

### Step 1 (Clarify and Route) — Multi-Goal Detection

During intent clarification, if the request contains ≥2 independent goals that could ship separately (look for independent verbs: "add X AND refactor Y AND build Z"), propose a split:

- Present the detected child stories as a bullet list.
- Checkpoint menu: `[S] Split — pick first story, note the rest  [K] Keep as single spec`
- If split: note child stories for later, narrow scope to the first story, continue into step 2.
- If keep: proceed as-is into step 2.

### Step 2 (Plan) — Post-Draft Word Count Check

After generating the spec, check word count. If it exceeds ~1200 words:

- Show the user the count.
- Checkpoint menu: `[S] Split — carve off child stories, keep current story  [K] Keep as-is`
- If split: save child stories for later, trim current spec, continue into step 3.
- If keep: continue into step 3 with the full spec.

No compression step. Attempting to silently shrink a spec drops details without the user knowing.

### Key Principles

- **One user-facing goal = one spec**, even if it touches DB + backend + UI. Never force-split a cohesive feature just because it touches multiple files/layers.
- **Never block the workflow.** Both checks are proposals with user override. You always continue forward with a story.
- **Explicit criteria over semantic judgment.** Use the independent-verb test, not vibes.

## Where Changes Go

- **`workflow.md`**: Add ~3-line SCOPE STANDARD block next to READY FOR DEVELOPMENT STANDARD.
- **`step-01-clarify-and-route.md`**: Add multi-goal routing branch with checkpoint menu.
- **`step-02-plan.md`**: Add post-draft word-count check after self-review with checkpoint menu.

## Open Questions

- Where do noted child stories get persisted? `{tasksDir}/backlog/`? Inline in the spec? Separate file?
- Does quick-spec (the other flow) get the same treatment, or just quick-dev2 for now?
