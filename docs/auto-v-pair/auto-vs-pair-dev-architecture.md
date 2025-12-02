# Auto vs Pair Dev: Architecture Design Document

## Executive Summary

**Two Story Creation Modes:**

- `/create-story-pair` - Flexible stories with strategic checkpoint markers for human validation at design moments
- `/create-story-auto` - Detailed prescriptive stories for autonomous execution

**Single Execution Workflow:**

- `/dev-story` reads checkpoint markers and pauses where marked
- Split happens at story creation, not execution

**Default Recommendation:**

- Pair-mode for most work (information emerges during coding that cannot be known upfront)
- Auto-mode for truly routine stories

**Guidance Mechanism:**

- High-confidence complexity warnings when stories show obvious design density (multiple classes, algorithms, integrations)

## Problem Statement

Users coming to BMad Method expect autonomous story execution ("auto-dev") - they want to feed stories to an AI agent and get a PR at the end with no human intervention. However, real-world software development on non-trivial problems generates technical debt when executed this way because **critical information emerges during coding that cannot be known upfront**.

The current workflow (dev-story) defaults to continuous autonomous execution, which works poorly when stories are under-specified or when implementation reveals unexpected complexity. This creates a mismatch between user expectations and what actually produces quality results.

## Core Insight: Information Emergence

**You cannot front-load what you don't know yet.**

During implementation, information emerges that wasn't predictable during planning:

- "This conflicts with the existing auth pattern"
- "We need to handle this edge case that wasn't obvious"
- "The validation rules interact in unexpected ways"

This emergence happens regardless of story quality. Even comprehensive stories hit reality during implementation and discover gaps, conflicts, or better approaches.

### Why Story Enhancement Tools Have Diminishing Returns

The initial hypothesis was to build tools that help users write better stories upfront (`/story-quality-check`, `/enhance-story`). However, this doesn't solve the fundamental problem:

**Information emerges during coding, especially in early stages.** The story is already as good as it can be before implementation starts. You can't predict what you'll discover when code meets existing codebase.

Research confirms this limitation: "How can you tell whether the specification is complete without knowing what the complete requirement specification is?" Requirements patterns and some upfront work (domain model, architecture basics) provide value, but there are diminishing returns on elaboration—you cannot eliminate emergence through better specifications.

Therefore, **strategic human checkpoints during development are essential** for anything bigger than trivial problems. These checkpoints capture emerging information in real-time before it turns into technical debt.

## The Mental Model

### Pair-Dev (Human in the Loop)

- Agent discovers issue → shows user → decides together → continues
- Story gets implicitly enhanced through conversation
- Human intuition prevents going down wrong paths
- **Value:** Captures emerging information before consequences cascade

### Auto-Dev (Autonomous)

- Agent discovers issue → makes best guess → continues
- No opportunity for course-correction
- **Works for:** Truly routine stories where nothing emerges (rare in real projects)
- **Fails when:** Implementation reveals complexity, conflicts, or better approaches

## Design Decision: Two Story Creation Modes

The key architectural insight: **The split happens at story creation, not execution.**

Rather than having one story format with a runtime mode toggle, we provide two distinct story creation workflows that produce different story structures.

### `/create-story-pair` - Freedom with Checkpoints

**Philosophy:** Leave implementation approach open, mark strategic validation points.

**Story Structure:**

```markdown
## Tasks

- [ ] **[CHECKPOINT]** Design and implement user creation (validation, storage, notifications)
- [ ] Implement authentication flow
- [ ] **[CHECKPOINT]** Add session management
- [ ] **[CHECKPOINT - FINAL]** All ACs verified, tests passing
```

**Characteristics:**

- Acceptance criteria clear, implementation approach flexible
- Checkpoints explicitly marked in task list
- Room to discover and adapt during execution
- **Resilient:** Course-corrections don't invalidate the story
- **Best for:** Most real-world development work

### `/create-story-auto` - Big Design Up-Front

**Philosophy:** Prescribe implementation details upfront for autonomous execution.

**Story Structure:**

```markdown
## Tasks

- [ ] Create UserService class with constructor(db, validator, emailService)
- [ ] Implement createUser(email, password) - hash password with bcrypt, validate email format, check uniqueness, send welcome email
- [ ] Implement authenticate(email, password) - lookup user, compare hash, return JWT with 24h expiry
```

**Characteristics:**

- Detailed, prescriptive task breakdown
- Design decisions baked into story during creation
- No checkpoint markers (runs continuously)
- **Fast when right:** If design matches reality, executes quickly
- **Expensive when wrong:** If reality differs, story becomes invalid and implementation needs rework
- **Best for:** Simple, routine stories in well-understood domains

### Single Execution Workflow: `/dev-story`

One execution workflow handles both story types by reading checkpoint markers:

- If checkpoints marked → pauses at those points
- If no checkpoints → runs continuously
- Captures decisions made at checkpoints back into story (Dev Notes, Change Log)

## Strategic Checkpoint Placement

**Not every task needs a checkpoint.** Too many interruptions break flow and feel like babysitting.

### The Checkpoint Rule: Design Moments, Not Mechanical Execution

Checkpoints belong **after design decisions, before implementation consequences**.

This mirrors pair programming best practices: pairing shines when making design choices per unit of time. When doing mechanical work (fixing warnings, writing boilerplate), pairing is waste. Same principle applies here.

### What Triggers Checkpoints

**Design-heavy moments (need checkpoints):**

- Skeleton/interfaces defined → CHECKPOINT → implement methods
- API contract designed → CHECKPOINT → write handlers
- Data flow architecture chosen → CHECKPOINT → wire components
- Error handling strategy decided → CHECKPOINT → add try/catches everywhere

**Mechanical moments (no checkpoint needed):**

- Writing unit tests following established pattern
- Fixing linter warnings
- Implementing CRUD endpoints that match existing pattern
- Adding repetitive validation rules

### The Critical First Checkpoint

**Most important checkpoint: After skeleton code, before any implementation.**

This is the moment where:

- Structure is visible (classes, interfaces, public APIs)
- Nothing's implemented yet (easy to change)
- User can see if agent understood the shape correctly
- Course-correction is cheap

**Why this checkpoint has highest ROI:**

Human pattern-matching and consequence-prediction >> agent's capabilities.

Agent thinks: "This structure satisfies the immediate acceptance criteria"

Human thinks: "This structure means every caller now needs error handling, breaks the existing service layer pattern, and creates inconsistent state management"

**Humans see second and third-order effects** that agents miss. Early structure decisions have cascading consequences - wrong shape requires reworking everything later, right shape makes implementation flow smoothly.

**Research validation:** Boehm's empirical data shows defects cost ~10x more to fix at coding vs design phase, and ~100x more at testing. The first checkpoint sits at the design→coding boundary, making it the highest-leverage intervention point. However, the ROI is conditional: high for design-heavy stories where the checkpoint actually catches misalignment; low for routine stories following established patterns where the checkpoint becomes rubber-stamp overhead. This economic reality justifies the two-mode split—auto-mode isn't just faster, it's economically rational when checkpoint ROI approaches zero.

**Research also validates human superiority in architectural decisions:** AI adoption for architecture decisions is only 36% compared to 67% for coding tasks. Studies explicitly describe AI's architectural role as "auxiliary"—humans provide "experience, intuition, and holistic understanding of context" that AI lacks. Gary Klein's Recognition-Primed Decision research shows experts use pattern recognition from years of experience to see consequences that novices (and AI) miss.

### Checkpoint Presentation: Concrete Code, Not Abstract Discussion

The agent should NOT ask: "I'm thinking of using Strategy pattern here, what do you think?" (too abstract, hard to evaluate)

Instead: Show concrete code structure and let user evaluate in context.

**Checkpoint Flow:**

1. Agent makes design choice
2. Codes the structure (interfaces, classes, function signatures)
3. CHECKPOINT: Shows concrete code
4. User evaluates actual design in situ
5. If good → agent continues with implementation
6. If bad → user sees it early, cheap to change before implementation

**Why concrete is better:**

- Easier to evaluate actual code than abstract concepts
- Agent's best guess is often right (no wasted discussion when correct)
- When wrong, user sees it in structure before it's buried in implementation
- Sometimes reveals upstream issues (story planning mistakes become obvious)

**Example checkpoint:**

```
Created User model structure:

class User {
  constructor(email, password) {}
  async validate() {}
  async hashPassword() {}
  async save() {}
}

Interface matches existing pattern in src/models/Product.js

Ready to implement the methods? Or adjust the structure first?
```

User can:

- Approve → continue
- Adjust → "add a role field", "use async constructor pattern instead"
- Redirect → "wrong - we use a UserService, not methods on model"

### Mid-Flight Checkpoints

Beyond the critical first checkpoint, additional checkpoints appear when:

- Agent makes architectural choice mid-implementation (data flow strategy, error handling pattern)
- Integration point reached (connecting to external API, database schema changes)
- Always at completion (final review before marking ready for review)

Typical story has **2-4 total checkpoints**:

1. After skeleton (always)
2. At integration point (if applicable)
3. At completion (always)
4. Occasionally mid-flight if architectural choice emerges

**Why 2-4 is the right range:** Story complexity is bounded by epic planning—stories needing >4 checkpoints should have been split. The lower bound is effectively 1 (final verification for auto-mode) or 2 if counting human review of the story file before execution. Research on flow state shows programmers need 10-15 minutes to resume after interruption, and frequent IT-mediated interruptions negatively impact both flow and task accuracy. Strategic placement at design moments preserves productivity while capturing value.

### Capturing Decisions in the Story

When user provides direction at a checkpoint, that decision gets captured back into the story:

```markdown
## Dev Notes

**Design Decisions (from checkpoints):**

- Task 1: Extended existing AuthService rather than creating UserService
  (integrates with existing session management)
- Task 3: Changed from JWT to session-based auth after discovering
  existing middleware incompatibility
```

This keeps the story as living documentation of actual implementation choices, not just original plan.

### Course Correction Converts to Pair Mode

**Key insight:** If a user interrupts an auto-mode story mid-flight to correct course, that story has proven it needed human intervention. From that point forward, treat it as pair-mode.

**Behavior:**

- User interrupts auto-mode execution with `/correct-course`
- Some tasks are fait accompli (already implemented)
- Remaining tasks may be reordered or expanded
- `/correct-course` adds checkpoint markers to revised remaining tasks
- Story now executes as pair-mode from this point forward

**Rationale:**

- Self-correcting classification: story that "should have been pair-mode" becomes pair-mode
- No prediction needed: reality reveals complexity rather than heuristics guessing it
- Fail-safe: auto-mode stories that are truly simple never get interrupted

**Implementation:** The checkpoint placement logic used by `/create-story-pair` must also be available to `/correct-course` for re-placing checkpoints on revised tasks.

**Metric opportunity:** Auto-mode stories that get interrupted indicate complexity detection heuristics are missing cases. Track this to improve warnings over time.

## Tradeoffs: Auto vs Pair

### Auto-Style Stories (Detailed/Prescriptive)

**Advantages:**

- Fast execution when design is correct
- Works well for routine, well-understood work
- Less human attention required
- Good for batch processing simple stories

**Disadvantages:**

- Rigid - course corrections require story rewrite
- Fails when implementation reveals unexpected complexity
- Wrong design choices get baked into hundreds of lines before user sees result
- Generates technical debt when agent makes assumptions

**When it works:**

- Simple CRUD operations
- Following established patterns exactly
- Routine refactoring with clear scope
- Stories where nothing unexpected can emerge

### Pair-Style Stories (Flexible with Checkpoints)

**Advantages:**

- Resilient to discovery - adapts as information emerges
- Leverages human intuition at critical decision points
- Prevents wrong paths before consequences cascade
- Stories stay valid even when implementation approach changes
- Captures actual decisions as documentation

**Disadvantages:**

- Requires human availability at checkpoint moments
- Slower total execution time
- More cognitive load on user (though strategically placed)

**When it works:**

- Most real-world development (recommended default)
- Complex integrations
- Touching unfamiliar code
- Stories where discovery is expected
- Learning new codebases

## Competency-Aware Checkpoint Design

Pair-mode effectiveness varies significantly based on user expertise level. Research reveals the **expertise inversion problem** in human-AI pairing.

### The Expertise Inversion Problem

**Traditional pair programming (expert + novice):**

- Expert navigates (strategic decisions)
- Novice drives (tactical typing)
- Novice trusts navigator "with incomplete understanding"

**LLM pair programming:**

- LLM drives (generates code)
- Human navigates (validates, steers)

**The problem:** When a novice human is in the navigator seat with an LLM driver, they lack the pattern recognition to catch issues. Research explicitly states: "Copilot can become an asset for experts, but a liability for novice developers who may fail to filter its buggy or non-optimal solutions due to a lack of expertise."

| Competency | Navigator Capability                 | Risk                                          |
| ---------- | ------------------------------------ | --------------------------------------------- |
| **Novice** | Can't recognize architectural issues | Rubber-stamps bad decisions, accumulates debt |
| **Expert** | Sees second/third-order effects      | Over-scaffolding breaks flow, wastes time     |

### Checkpoint Presentation by Competency Level

The installer captures `competency_level`. Checkpoint presentation adapts accordingly.

**For Novice Users - Scaffolded Checkpoints:**

Research on instructional design shows novices benefit from explicit guidance. The "expertise reversal effect" confirms that scaffolding helpful for novices becomes harmful for experts.

```markdown
## CHECKPOINT: Structure Review

I've created this skeleton:
[code block]

**Before approving, consider:**

- [ ] Does this match patterns in existing codebase? (check src/models/)
- [ ] Are there missing error cases?
- [ ] Will this integrate with existing auth/session handling?
- [ ] Any fields that might need validation?

**Questions to ask yourself:**

- "What happens when X fails?"
- "How does this connect to [related component]?"

Ready to continue, or want to discuss?
```

**For Expert Users - Minimal Checkpoints:**

```markdown
## CHECKPOINT: Structure Review

Created User model matching Product.js pattern:
[code block]

Continue? (or redirect)
```

### Design Implications

1. **Checkpoint presentation templates** vary by `competency_level` from installer config

2. **LLM explanation depth** at checkpoints:
   - Novice: Explain _why_ choices were made (the "because" pattern from code review research)
   - Expert: State _what_ was done, assume understanding of _why_

3. **Checkpoint prompts/checklists**:
   - Novice: Include domain-specific checklist items (security? validation? error handling?)
   - Expert: Omit scaffolding (expertise reversal—it becomes noise)

4. **Default mode recommendation**:
   - Novice: Stronger nudge toward pair-mode (they need checkpoints even if they can't fully evaluate)
   - Expert: Trust their mode selection more

5. **Fading over time**: As user demonstrates competency (successful course-corrections, catching issues), reduce scaffolding

### Is Pair-Mode Even Appropriate for Novices?

Research shows novices benefit most from AI productivity gains but are greatest liability for quality. If a novice can't effectively evaluate at checkpoints, does pair-mode help?

**Yes, but differently:** Pair-mode for novices is still better than auto-mode because:

- Forces them to _look_ (even if they miss things)
- Creates learning opportunities (seeing the skeleton)
- Scaffolding prompts teach them _what_ to look for over time
- At minimum, they can catch obvious mismatches

The scaffolded checkpoints help novices learn what to evaluate, not guarantee they'll catch everything. Over time, this builds the pattern recognition that makes expert-level checkpoints effective.

## User Experience Design

### Goal: Nudge Toward Pair Without Being Annoying

**The Challenge:** Users expect auto-dev but pair-dev works better for most real work. How do we guide them without forcing or nagging?

**Constraint:** We cannot reliably detect story complexity with high accuracy. LLMs can't judge:

- How likely requirements will shift during implementation
- How well design accounts for existing codebase
- Whether edge cases will emerge
- User's risk tolerance

### Strategy: High-Confidence Warnings Only

When user runs `/create-story-auto`, check for **obvious** complexity signals. Only warn when multiple signals present (high precision, low recall).

**High-confidence complexity indicators:**

Evaluation uses short-circuit logic: check fast signals first, only check medium signals if a fast signal is found. Warning triggers when at least one fast AND one medium signal are present.

**Fast signals (check first, instant text analysis):**

- Story + Acceptance Criteria sections combined >300 words (outlier; normal stories are 150-250 words)
- Story title contains: "refactor", "migrate", "integrate", "redesign"
- Epic has >8 stories

**Medium signals (check only if fast signal found, requires story content parsing):**

- Creates 2+ new classes/services
- Introduces complex algorithm (sorting, parsing, validation logic)
- Multiple conditional flows described in ACs
- Data transformations between formats/schemas

**If fast >= 1 AND medium >= 1:**

```
Story created for auto-execution.

⚠️ Heads up: This story looks complex (creates multiple classes,
involves algorithm implementation). Pair-mode with checkpoints
usually works better for stories like this.

Want to recreate with /create-story-pair instead? (y/n)
```

**Key principles:**

- Only warn on obvious cases (better to under-warn than over-warn)
- Make it a suggestion, not a block
- User learns "oh, system was right" when warnings prove accurate
- Builds trust in the recommendation over time
- No warning for simple stories (lets auto-mode succeed, shows it has valid use cases)

### Menu Verbiage (Subtle Steering)

```
Scrum Master Agent Menu:

/create-story-pair
  Create story with human checkpoints (recommended for most stories)

/create-story-auto
  Create detailed story for autonomous execution (works well for routine/simple stories)
```

The description alone steers choice through social proof ("recommended for most") without blocking access to auto-mode.

### What We're NOT Doing

**No post-hoc struggle detection:** Agent can't reliably detect when it's struggling during execution. Hard to distinguish "made assumption" vs "followed obvious pattern" or "backtracked" vs "refactored normally."

**No story quality scoring:** Can't predict what information will emerge during implementation. Story enhancement tools don't solve the fundamental emergence problem.

**No forced mode:** Always let user choose. Education through experience (occasional accurate warnings) > forced guardrails.

**No docs-only education:** Nobody reads docs. Behavior change comes from:

- Default recommendations in menu
- Occasional accurate complexity warnings
- Experiencing pair-mode success on complex stories
- Experiencing auto-mode success on simple stories

## Implementation Architecture

### File Structure

```
4-implementation/
  ├── create-story-pair/
  │   ├── workflow.yaml
  │   └── instructions.md      # Creates flexible stories with checkpoints
  ├── create-story-auto/
  │   ├── workflow.yaml
  │   └── instructions.md      # Creates detailed prescriptive stories
  ├── dev-story/
  │   ├── workflow.yaml
  │   └── instructions.md      # Single execution workflow, checkpoint-aware
  ├── _shared/
  │   ├── dev-standards.md     # TDD protocol, coding standards (referenced by both)
  │   ├── story-loader.xml     # Common: load story from sprint-status
  │   └── completion.xml       # Common: mark review, update sprint-status
  ├── story-context/
  ├── story-done/
  └── code-review/
```

### Scrum Master Agent Updates

```yaml
menu:
  - trigger: create-story-pair
    workflow: '{project-root}/{bmad_folder}/bmm/workflows/4-implementation/create-story-pair/workflow.yaml'
    description: 'Create story with human checkpoints (recommended for most stories)'

  - trigger: create-story-auto
    workflow: '{project-root}/{bmad_folder}/bmm/workflows/4-implementation/create-story-auto/workflow.yaml'
    description: 'Create detailed story for autonomous execution (works well for routine/simple stories)'
```

### Dev Agent Updates

No menu changes needed - `/dev-story` workflow handles both story types by reading checkpoint markers in the story file.

### Story File Format

**Checkpoint markers in Tasks section:**

```markdown
## Tasks

- [ ] Some task description
- [ ] **[CHECKPOINT]** Design-heavy task requiring validation
- [ ] Another task
- [ ] **[CHECKPOINT - FINAL]** Completion validation
```

**Dev Notes section captures checkpoint decisions:**

```markdown
## Dev Notes

### Design Decisions (from checkpoints)

- Task 1 checkpoint: Extended AuthService instead of creating UserService
- Task 3 checkpoint: Switched to session-based auth due to middleware conflict
```

**No mode metadata needed** - presence/absence of checkpoint markers determines execution behavior.

## Out of Scope

### Git Workflow

BMad Method workflows do not concern themselves with commit strategy. That remains entirely user choice:

- When to commit (during checkpoints, at end, never)
- Commit message format
- Branching strategy
- PR creation

Focus is purely on:

- Write code
- Validate with user at design moments
- Mark tasks complete in story file
- Update sprint-status

### Test-Driven Development

TDD is important for both modes but implementation details are separate concern:

- **In auto-dev:** TDD mandatory (only way to verify correctness without human validation)
- **In pair-dev:** TDD strongly encouraged, human can validate other ways if needed

Specific TDD protocols live in `_shared/dev-standards.md` referenced by both workflows.

## Success Metrics

How do we know this architecture is working?

**Qualitative signals:**

- Users naturally graduate from pair-mode to using auto-mode appropriately (simple stories)
- Complexity warnings prove accurate when they fire (builds trust)
- Users report less rework/technical debt from autonomous execution
- Checkpoint conversations surface real design issues early

**Quantitative signals:**

- Pair-mode stories complete with fewer post-review changes
- Auto-mode stories that triggered warnings have higher revision rates (validates warning accuracy)
- Retrospectives show fewer "wrong design choice" problems in pair-mode stories

**Anti-patterns to watch for:**

- Users always choosing auto-mode despite warnings (suggests warnings aren't convincing)
- Users frustrated by checkpoint frequency (suggests poor checkpoint placement heuristics)
- Pair-mode stories taking much longer without quality improvement (suggests checkpoints not adding value)

## Open Questions

### Checkpoint Placement Heuristics

How does `create-story-pair` decide where to place checkpoints in the task list?

**Current thinking:**

- Always after first substantive task (skeleton/interfaces)
- Mark tasks that involve integration points
- Mark tasks with words like "design", "implement [new component]", "add [new pattern]"
- Always mark final task as completion checkpoint

**Needs validation:** Will SM agent reliably identify design-heavy tasks during story creation?

**Note:** This same logic must be shared with `/correct-course` for re-placing checkpoints on revised tasks.

### Checkpoint Presentation Format

What's the optimal way to show checkpoint code to user?

**Options:**

- File diffs in terminal
- File paths + summary of changes
- Code blocks in chat
- Link to files with line numbers

**Needs user testing.**

**Note:** Format should also adapt to competency level—novices may benefit from more context, experts from brevity.

### Auto-Dev Failure Modes

When auto-dev encounters genuine ambiguity mid-flight, should it:

- **A.** Make assumption, log it, continue (current behavior)
- **B.** Pause and ask user (effectively becomes pair-mode)
- **C.** Fail fast: "Cannot proceed without knowing X"

**Current recommendation:** A, but surface all assumptions clearly at completion so user knows what to review carefully.

**Note:** If user does interrupt with `/correct-course`, story converts to pair-mode for remaining tasks (see "Course Correction Converts to Pair Mode" section).

### Workflow Migration

How do existing users transition?

**Options:**

- Keep `/create-story` as alias to pair-mode (recommended default)
- Require explicit choice on first use, remember preference
- Gradual migration with deprecation warnings

**Recommendation:** `/create-story` becomes `/create-story-pair`, add `/create-story-auto` as new option.

### Competency Level Detection

The installer captures `competency_level`, but should this be:

- Self-reported (user selects "novice/intermediate/expert")
- Inferred from behavior over time (fading scaffolding as competency demonstrated)
- Per-project (expert in one codebase, novice in another)

**Current thinking:** Start with self-reported, add behavioral fading as enhancement.

## Conclusion

The architecture splits story creation into two modes (pair vs auto) rather than trying to make one story format work for both execution styles. This acknowledges the fundamental tradeoff:

**Big design up-front** (auto) is fast when right but expensive when wrong, because stories become invalid when implementation reveals different reality.

**Freedom with checkpoints** (pair) is resilient to discovery, leveraging human intuition at strategic moments to prevent cascading consequences of wrong design choices.

Most real-world development benefits from pair-mode because **information emerges during coding that cannot be known upfront**. Auto-mode has valid use cases for truly routine work, but should be opt-in with guidance rather than the default path.

The system nudges users toward appropriate choices through:

- Menu verbiage (social proof)
- High-confidence complexity warnings (education through experience)
- Natural learning (experiencing pair-mode success on complex work, auto-mode success on simple work)

Success comes from making pair-mode checkpoints strategically placed and valuable, not from preventing users from choosing auto-mode.

## Appendix: Academic Validation

This architecture was validated against academic literature and empirical studies. Key claims and their research support:

### Claim: Information Emerges During Implementation

**Status: Strongly Supported**

Research confirms requirements cannot be fully specified upfront. Studies show requirements "evolve quickly and become obsolete even before project completion." Agile RE research identifies "complete understanding and specification of requirements" as among the most difficult tasks in software engineering.

### Claim: Strategic Checkpoint Placement at Design Moments

**Status: Supported**

Pair programming research shows developers spend "on average a third of the session without any computer interaction focusing mainly on communication"—the navigator adds most value at strategic moments, not during mechanical execution. Flow state research shows 10-15 minute recovery time after interruptions, supporting fewer, strategically-placed checkpoints over frequent interruptions.

### Claim: Concrete Code > Abstract Discussion

**Status: Supported**

Code review research shows "code review requires deeper engagement of higher-level cognitive processes than code comprehension alone." Prototype research achieves 91% similarity using concrete skeleton code. Reviewers use strategies like "narrowing down scope" facilitated by concrete artifacts.

### Claim: Human Pattern Recognition > AI for Architecture

**Status: Strongly Supported**

AI adoption for architecture decisions is only 36% vs 67% for coding. Studies describe AI's architectural role as "auxiliary"—humans provide "experience, intuition, and holistic understanding." Gary Klein's Recognition-Primed Decision research shows experts see consequences that novices and AI miss.

### Claim: Auto for Routine, Pair for Complex

**Status: Strongly Supported**

Large-scale study (456,000+ PRs) found autonomous agent PRs have 35-49% acceptance vs humans—"substantial performance gaps suggest systemic limitations." Copilot "struggles with complex tasks, large functions, multiple files" but succeeds with "small function context" and "boilerplate." Human-in-the-loop research confirms automation works in "well-defined contexts" while human intervention is needed in "not yet defined or undefinable contexts."

### Claim: Novice vs Expert Checkpoint Effectiveness

**Status: Supported**

Research shows "Copilot can become an asset for experts, but a liability for novice developers who may fail to filter buggy or non-optimal solutions." The "expertise reversal effect" from cognitive load theory confirms instructional techniques effective for novices can harm experts. This validates competency-aware checkpoint presentation.

### Key Research Sources

- Boehm, B. - Software Engineering Economics (defect cost curves)
- Klein, G. - Recognition-Primed Decision Making
- Dreyfus, H. & Dreyfus, S. - Skill Acquisition Model
- IEEE/ACM studies on pair programming effectiveness
- Stanford HAI - Human-in-the-Loop AI Systems
- AIDev study - 456K PRs from autonomous coding agents
- GitHub Copilot empirical studies (Microsoft Research)
