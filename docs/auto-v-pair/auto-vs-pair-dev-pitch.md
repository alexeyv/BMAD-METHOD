# Auto vs Pair Dev: The Pitch

The core insight is: you can't predict what you'll discover when code meets existing codebase. Auto-dev works until it doesn't, and by then you've got 500 lines built on wrong assumptions.

Trying harder and harder to make a story better upfront has diminishing returns because some information that matters emerges _during_ coding, not before.

So we give user a choice at story creation, (not execution):

**`/create-story-pair`** — Freedom with checkpoints. Acceptance criteria are clear, but implementation approach stays flexible. The workflow marks strategic pause points in the task list—after the skeleton is coded, at integration points, at completion. The agent makes its design choice, codes the structure (interfaces, classes, function signatures), then shows you concrete code at the checkpoint. Not abstract discussion ("I'm thinking of using Strategy pattern here")—actual code in context that you can evaluate, approve, adjust, or redirect.

This mirrors pair programming at its best: pairing shines when making design choices, not during mechanical execution. Checkpoints belong after design decisions, before implementation consequences. The critical first checkpoint—after skeleton, before any implementation—has the highest ROI because human pattern recognition catches second and third-order effects that agents miss. You see "this structure means every caller now needs error handling and breaks the existing service layer pattern" while the agent only sees "this satisfies the immediate acceptance criteria."

Typical story has 2-4 checkpoints total. One checkpoint (at the end) is the auto-mode, more than 4 means the story should have been split.

**`/create-story-auto`** — Big design up front. Prescriptive, detailed task breakdown with design decisions baked in during creation. No checkpoint markers, runs continuously to completion. Fast when the design matches reality. Expensive when it doesn't—wrong design choices get baked into hundreds of lines before you see the result, and the story becomes invalid requiring rework.

**`/dev-story`** — Single execution workflow handles both. Reads checkpoint markers in the story file. If checkpoints are marked, pauses at those points. If no checkpoints, runs continuously. Captures decisions made at checkpoints back into the story's Dev Notes section, so the story becomes living documentation of actual implementation choices.

## Steering Without Blocking

Users coming to BMad Method expect autonomous execution—feed stories to an agent, get a PR at the end. We're not going to block that. But we can steer them towards human-in-the-loop without being obnoxious.

Menu verbiage does the first nudge: `/create-story-pair` is "recommended for most stories" while `/create-story-auto` "works well for routine/simple stories." Social proof without gatekeeping.

The second nudge is smarter. When someone runs `/create-story-auto`, we check for obvious complexity signals using fast, cheap heuristics—no expensive LLM reasoning, just text analysis. First pass looks for instant signals: story text over 300 words (normal stories run 150-250), title contains "refactor"/"migrate"/"integrate"/"redesign", or the epic has more than 8 stories. If any of those hit, we do a second pass looking at story content: creates 2+ new classes, involves algorithm implementation, multiple conditional flows in acceptance criteria, data transformations between formats.

If we find at least one fast signal AND one medium signal, we surface a warning:

> Story created for auto-execution.
>
> ⚠️ Heads up: This story looks complex (creates multiple classes, involves algorithm implementation). Pair-mode with checkpoints usually works better for stories like this.
>
> Want to recreate with /create-story-pair instead? (y/n)

The key is high precision, low recall. Only warn on obvious cases—better to under-warn than nag. When warnings prove accurate, users learn to trust the recommendation. When simple stories run through auto-mode without warnings and succeed, that builds trust too. Education through experience, not docs nobody reads.

## The Escape Hatch

If someone interrupts auto-mode mid-flight with `/correct-course`, that story has proven it needed human intervention. From that point forward, it's pair-mode. The `/correct-course` workflow adds checkpoint markers to remaining tasks, and execution continues with strategic pauses.

This is self-correcting classification. Stories that "should have been pair-mode" become pair-mode when reality reveals the complexity. No prediction needed—just a fail-safe that converts on contact with actual difficulty.

## Why This Works

The research backs it up. AI adoption for architecture decisions sits at 36% versus 67% for coding tasks—humans provide experience, intuition, and holistic understanding that AI lacks. Studies show autonomous agent PRs have 35-49% acceptance rates versus humans. AI "struggles with complex tasks, large functions, multiple files" but succeeds with "small function context" and "boilerplate."

Pair-mode captures emerging information before it turns into technical debt. Auto-mode has valid use cases for genuinely routine work. The system nudges toward appropriate choices without forcing, and reality corrects the mistakes.
