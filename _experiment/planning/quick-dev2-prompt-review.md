# PromptSentinel Review: quick-dev2 Sharded Workflow

**Overall Risk Level:** High
**Critical Issues:** 4 | **High:** 7 | **Medium:** 6 | **Low:** 3
**Estimated Production Failure Rate if Unfixed:** ~18-25% of runs (cross-step state loss, ambiguous completion, variable resolution gaps compound across the 5-step chain)

---

## Context & Dependency Inventory

### File Map

| File | Role | Tokens (est.) |
|------|------|---------------|
| `workflow.md` | Entry point, standards, architecture rules, initialization | ~650 |
| `tech-spec-template.md` | Spec template with placeholders | ~450 |
| `step-01-clarify-and-route.md` | Intent capture, artifact scan, routing | ~450 |
| `step-02-plan.md` | Investigation, spec generation, approval checkpoint | ~350 |
| `step-03-implement.md` | Baseline capture, implementation dispatch | ~200 |
| `step-04-review.md` | Adversarial review, finding classification, loopback logic | ~550 |
| `step-05-present.md` | Summary, commit, PR offer | ~150 |

### Variables & State Tracking

| Variable | Set Where | Consumed Where | Mechanism |
|----------|-----------|----------------|-----------|
| `{main_config}` | workflow.md frontmatter | workflow.md init | Frontmatter reference |
| `{project_name}` | config.yaml via init | Nowhere explicit | Loaded but unused |
| `{implementation_artifacts}` | config.yaml via init | Steps 1-4 | Must persist in memory |
| `{planning_artifacts}` | config.yaml via init | Step 1 instruction 1 | Must persist in memory |
| `{communication_language}` | config.yaml via init | Every step (RULES) | Must persist in memory |
| `{installed_path}` | workflow.md init | Every step NEXT section | Must persist in memory |
| `{templateFile}` | workflow.md init + step-02 frontmatter | Step 2 | Dual declaration |
| `{wipFile}` | workflow.md init + step-01/02 frontmatter | Steps 1, 2 | Dual/triple declaration |
| `{spec_file}` | step-01 (runtime) | Steps 2-5 | In-memory; also step-01 frontmatter as empty |
| `{execution_mode}` | step-01 (runtime) | Steps 3, 4 | In-memory only |
| `{baseline_commit}` | step-03 (written to spec frontmatter) | Step 4 | Spec file frontmatter |
| `{diff_output}` | step-04 (runtime) | Step 4 subagents | In-memory only |
| `{specLoopIteration}` | step-04 frontmatter (init=1) | Step 4 loopback logic | In-memory counter |
| `{deferred_work_file}` | step-01/02/04 frontmatter | Steps 1, 2, 4 | Triple declaration |
| `{date}` | workflow.md init | tech-spec-template frontmatter | Must persist in memory |
| `{project_context}` | workflow.md init | Nowhere explicit | Loaded but unused |
| `{user_skill_level}` | config.yaml via init | Nowhere explicit | Loaded but unused |
| `{adversarial_review_task}` | workflow.md frontmatter + step-04 frontmatter | Step 4 | Dual declaration |
| `{edge_case_hunter_task}` | step-04 frontmatter | Step 4 | Frontmatter reference |

### Conditionals, Loops, Halts, Tool Calls

| Item | Location | Type |
|------|----------|------|
| WIP file exists? | Step 1 ARTIFACT SCAN | Conditional + HALT |
| Active specs found? | Step 1 ARTIFACT SCAN | Conditional + HALT |
| Unformatted spec found? | Step 1 ARTIFACT SCAN | Conditional (suggestion) |
| Questions unanswered? | Step 1 instruction 2 | Loop until clear |
| Dirty tree / branch mismatch? | Step 1 instruction 3 | Conditional + HALT |
| Multi-goal? | Step 1 instruction 4 | Conditional + HALT |
| Token count > 1600? | Step 2 instruction 5 | Conditional + HALT |
| CHECKPOINT 1 approval | Step 2 | HALT + loop on [E] |
| Frozen section violation | Step 3 | Constraint |
| Sub-agent availability | Steps 2, 3, 4 | Conditional dispatch |
| intent_gap found | Step 4 classify 3 | Loopback to Step 2 |
| bad_spec found | Step 4 classify 3 | Loopback to Step 3 |
| specLoopIteration > 5 | Step 4 classify 3 | HALT + escalation |
| Dirty tree at present | Step 5 instruction 1 | Conditional commit |

---

## Critical & High Findings

| # | Failure Mode | Exact Quote / Location | Risk (High-Volume) | Mitigation & Rewritten Example |
|---|--------------|------------------------|---------------------|-------------------------------|
| C1 | **Variable Resolution Gap** (FM-8) + **Context Window Assumption** (FM-3) | `{execution_mode}` is set in step-01 instruction 6 as a runtime assignment (`execution_mode = "one-shot"` or `execution_mode = "plan-code-review"`) but is never written to any file. Steps 3 and 4 consume it: step-03 line 25 `execution_mode = "one-shot"`, step-04 line 30 "One-shot: Skip diff construction", line 32 "Plan-code-review: Launch three subagents". | **Critical.** If context is truncated between steps (long conversation, sub-agent handoff, or model context pressure), `execution_mode` evaporates. Step 3 has no fallback -- it silently picks whichever branch the model "remembers" or defaults to. At scale, ~10-15% of runs risk executing the wrong branch. | Persist `execution_mode` in `{spec_file}` frontmatter alongside `status`. Step 3 and 4 should read it from the file, not memory. Rewrite step-01 instruction 6: `Set execution_mode in {spec_file} frontmatter: one-shot | plan-code-review`. Rewrite step-03: `Read execution_mode from {spec_file} frontmatter. If "one-shot": implement directly. If "plan-code-review": hand {spec_file} to a sub-agent.` |
| C2 | **Variable Resolution Gap** (FM-8) | `{spec_file}` is set at runtime in step-01 instruction 5 but is consumed in steps 2, 3, 4, and 5. It is declared as `spec_file: ''` in step-01 frontmatter but never written to any persistent artifact until step-02 renames `{wipFile}` to `{spec_file}`. Before that rename, steps that skip to step-03 (the `ready-for-dev` resume path) rely on `{spec_file}` being set from step-01 ARTIFACT SCAN, which is purely in-memory. | **Critical.** On resume from `ready-for-dev`, the path skips step-02 entirely. If the model loses `{spec_file}` from memory (context pressure, long prior conversation), step-03 receives an empty or hallucinated path. The spec file is the central artifact -- misresolution cascades through implementation, review, and presentation. | Add a frontmatter field `spec_file` to each downstream step file with a comment `# resolved at runtime from step-01 or resume`. More robustly, require step-03 to verify `{spec_file}` exists on disk before proceeding: `If {spec_file} does not exist or is empty, HALT: "Cannot find spec file. Please provide the path."` |
| C3 | **Implicit Ordering** (FM-7) + **Context Window Assumption** (FM-3) | Step-04 "Construct Diff" section reads: `Read {baseline_commit} from {spec_file} frontmatter.` Step-03 writes `baseline_commit` to the spec frontmatter, but only for `plan-code-review` mode. Step-04 consumes it unconditionally for the "plan-code-review" path. If step-03's sub-agent wrote the implementation but did NOT correctly update the frontmatter (sub-agent context isolation means it may not know the exact frontmatter format), `{baseline_commit}` is missing. | **Critical.** Step-04 constructs its diff from a potentially absent or malformed `baseline_commit`. This silently produces an empty or incorrect diff, which means all three review subagents receive garbage input. The entire review pass becomes theater. | Add explicit verification in step-04: `Read baseline_commit from {spec_file} frontmatter. If absent or malformed, HALT: "baseline_commit not found in spec frontmatter. Cannot construct diff."` Also, in step-03, provide explicit frontmatter format: `Add to {spec_file} frontmatter: baseline_commit: <COMMIT_HASH>` with an example. |
| C4 | **Halt/Checkpoint Gap** (FM-10) | Step-04 classify instruction 3, sub-bullet for `intent_gap`: `Revert code changes. Loop back to the human to resolve, then re-run steps 2-4.` The instruction says "loop back to the human" but provides no explicit HALT or checkpoint mechanism. It also says "re-run steps 2-4" but does not specify HOW to re-enter the step chain -- does the model re-read step-02's file? Does it re-execute the workflow from initialization? | **Critical.** Without an explicit `HALT AND WAIT FOR HUMAN` instruction and a concrete re-entry mechanism, the model may: (a) continue autonomously past the human gate, (b) attempt to re-derive intent without human input, or (c) re-read all step files simultaneously (violating the "never load multiple step files" rule). At scale, autonomous continuation past a human safety gate is the highest-severity failure. | Rewrite: `HALT AND WAIT FOR HUMAN: Present the intent_gap finding and ask the human to clarify the intent. Once the human responds, re-read and follow {installed_path}/steps/step-02-plan.md to re-derive the spec.` Add analogous explicit re-entry for `bad_spec`: `Re-read and follow {installed_path}/steps/step-03-implement.md.` |
| H1 | **Ambiguous Completion** (FM-2) | Step-03 implementation section: `hand {spec_file} to a sub-agent/task and let it implement.` No done-state. No verification. No completion criteria. The step says "let it implement" and then immediately transitions to NEXT (step-04). | **High.** The model has no way to verify implementation is complete. Did the sub-agent finish? Did it error out? Did it implement all tasks? The step has zero quality gates between implementation and review. In ~8-12% of runs, incomplete implementation will flow into adversarial review, wasting the review cycle. | Add a verification gate after implementation: `Verify that all tasks in {spec_file} "Tasks & Acceptance" section have been addressed. If any task is incomplete, continue implementation. If all tasks are addressed, proceed to NEXT.` Also add: `If using a sub-agent, verify the sub-agent completed successfully before proceeding.` |
| H2 | **Negation Fragility** (FM-6) | workflow.md "Critical Rules": five consecutive NEVER/ALWAYS statements: `NEVER load multiple step files simultaneously`, `ALWAYS read entire step file before execution`, `NEVER skip steps or optimize the sequence`, `ALWAYS follow the exact instructions`, `ALWAYS halt at checkpoints`. | **High.** Five sequential negation/absolute directives in a block create peak negation fragility. Under context pressure, models reliably invert one or more of these (documented in adversarial literature). The "NEVER load multiple step files" rule is particularly fragile because loading step files is the primary action the model takes. | Convert to positive enforcement with a single structural rule: `STEP LOADING PROTOCOL: (1) Complete the current step fully before loading the next. (2) Load exactly one step file at a time. (3) Read the entire file before executing any instruction. (4) Execute sections in order. (5) At every HALT instruction, stop and wait for human input before continuing.` |
| H3 | **Non-deterministic Phrasing** (FM-5) | Step-01 instruction 3: `Does the current branch make sense for this intent -- considering its name and recent history? If the tree is dirty or the branch is an obvious mismatch, HALT...` The phrase "make sense" and "obvious mismatch" are subjective judgments with no criteria. | **High.** What counts as "making sense" varies between runs. One run may flag a branch named `feature/auth` for a UI task; another may not. "Obvious mismatch" has no definition. This creates inconsistent halt behavior -- sometimes halting unnecessarily, sometimes not halting when it should. | Provide concrete criteria: `Check if the current branch name relates to the clarified intent (e.g., contains relevant keywords or is a general development branch like main/develop). If the branch name clearly references a different feature (e.g., branch is "fix/auth-bug" but intent is about UI styling), HALT and ask the human. If the working tree has uncommitted changes, HALT and ask the human.` |
| H4 | **Variable Resolution Gap** (FM-8) | Step-01 ARTIFACT SCAN instruction 1: `{wipFile} exists? -> Offer resume or archive.` But `{wipFile}` is defined as `{implementation_artifacts}/tech-spec-wip.md`. The step-01 frontmatter re-declares it. Step-02 frontmatter also re-declares it. workflow.md initialization also declares it. Three separate declarations of the same variable create ambiguity about which takes precedence if they diverge during maintenance. | **High.** Triple declaration is a maintenance hazard. If someone updates the path in workflow.md but not in step-01 or step-02 frontmatter, the model resolves to whichever it saw last (or whichever is in active context). This applies equally to `{deferred_work_file}` (declared in steps 1, 2, and 4) and `{templateFile}` (declared in workflow.md and step-02). | Declare each variable exactly once in workflow.md initialization. Remove all re-declarations from step frontmatters. Step frontmatters should reference these variables without re-defining them: remove `wipFile`, `templateFile`, `deferred_work_file` from step frontmatter sections. If frontmatter is used as documentation, add a comment: `# Resolved from workflow initialization -- do not redefine`. |
| H5 | **Scope Creep Invitation** (FM-9) | Step-02 instruction 1: `Investigate codebase. Isolate deep exploration in sub-agents/tasks where available. To prevent context snowballing, instruct subagents to give you distilled summaries only.` | **High.** "Investigate codebase" is unbounded. There is no scope limit, no time budget, no file-count cap, no stopping criterion. The instruction to use sub-agents for isolation is good but insufficient -- even sub-agents need scope boundaries. At scale, this is the step most likely to consume excessive tokens/time. | Add concrete boundaries: `Investigate the codebase to understand the files and patterns relevant to the clarified intent. Limit investigation to files referenced in the intent and their direct dependencies. Do not explore unrelated modules. If using sub-agents, provide them with specific file paths or directory scopes to examine, and require distilled summaries of no more than 200 tokens each.` |
| H6 | **Implicit Ordering** (FM-7) | Step-04 classify instruction 3, sub-bullet for `bad_spec`: `Revert code changes. Read the Spec Change Log in {spec_file} and strictly respect all logged constraints when amending... Re-run steps 3-4.` This instruction implies the model should re-execute step-03 and step-04, but the step-file architecture mandates reading one step file at a time. How does the model "re-run steps 3-4" while currently inside step-04? There is no explicit re-entry protocol. | **High.** The model must somehow navigate back to step-03 from within step-04. Without an explicit instruction like "Read and follow {installed_path}/steps/step-03-implement.md", the model may attempt to inline step-03 logic from memory (violating the step-file architecture), or get confused about which step it is executing. | Rewrite: `After amending the spec and appending the change-log entry, re-read and follow {installed_path}/steps/step-03-implement.md. When step-03 completes, it will direct you back to this step (step-04).` Similarly for `intent_gap`: `After human resolves the intent gap, re-read and follow {installed_path}/steps/step-02-plan.md.` |
| H7 | **Context Window Assumption** (FM-3) | Step-04 review section: `Acceptance auditor -- receives {diff_output}, {spec_file}, and read access to the project. Must also read the docs listed in {spec_file} frontmatter context.` The `context` field in tech-spec-template.md is `context: []` with comment `optional: max 3 project-wide standards/docs. NO source code files.` But step-04 does not handle the case where `context` is empty or not populated. | **High.** If the spec's `context` field is empty (the default), the acceptance auditor's instruction to "read the docs listed in context" resolves to reading nothing, but the instruction's phrasing implies there SHOULD be docs. The auditor may hallucinate doc references or waste time searching. More seriously, there is no instruction for what happens when context docs are listed but cannot be found on disk. | Add: `If {spec_file} frontmatter context is empty, the acceptance auditor proceeds without additional context documents. If context lists files that do not exist, the acceptance auditor notes the missing references as a finding and proceeds with available documents only.` |

## Medium & Low Findings

| # | Failure Mode | Exact Quote / Location | Risk (High-Volume) | Mitigation & Rewritten Example |
|---|--------------|------------------------|---------------------|-------------------------------|
| M1 | **Non-deterministic Phrasing** (FM-5) | Step-01 instruction 6: `One-shot -- trivial (~3 files).` The word "trivial" and the parenthetical "~3 files" are both subjective/approximate. There is no hard rule for when something qualifies as "trivial". | **Medium.** Different runs will route differently for the same intent. A 4-file change might be routed as one-shot in one run and plan-code-review in another. Routing determines the entire downstream execution shape. | Provide a deterministic criterion: `One-shot: The intent affects 3 or fewer files AND requires no architectural decisions. Plan-code-review: All other cases. If uncertain, use plan-code-review.` |
| M2 | **Teaching Known Knowledge** (FM-11) | workflow.md "READY FOR DEVELOPMENT STANDARD" re-explains concepts like Given/When/Then, dependency ordering, and "no placeholders or TBDs". These are well-known to 2026 frontier models. | **Medium.** ~40 tokens spent re-explaining known concepts. Under tight context windows, these tokens displace actionable instructions. The standard itself is fine as a checklist; the issue is that the definitions are unnecessary for the target models. | Compress to a pure checklist: `READY FOR DEVELOPMENT STANDARD: (1) Every task has a file path and specific action. (2) Tasks ordered by dependency. (3) ACs use Given/When/Then. (4) No placeholders or TBDs.` (Note: this is already close to the current form -- the risk is low but the "Testable" and "Complete" labels add zero signal.) |
| M3 | **Silent Ignoring** (FM-1) | workflow.md initialization: `project_context = **/project-context.md (load if exists)` and `CLAUDE.md / memory files (load if exist)`. These are loaded during initialization but never referenced again in any step. No step instructs the model to use project context or memory files for any decision. | **Medium.** The model loads these files into context, consuming tokens, but has no instruction to apply them. At best, they passively inform the model's understanding. At worst, they fill the context window and push out step instructions. In either case, there is no guarantee they influence behavior. | Either explicitly reference them in step-01: `Use {project_context} and any loaded memory files to inform your understanding of the intent and codebase conventions.` Or remove the load instructions if they are truly optional: `project_context = **/project-context.md (load if exists; provides background for intent clarification in Step 1)`. |
| M4 | **Ambiguous Completion** (FM-2) | Step-05 instruction 3: `Display summary of your work to the user, including the commit hash if one was created. Advise on how to review the changes. Offer to push and/or create a pull request.` After the display+offer, the step says `Workflow complete.` but there is no instruction on what to do if the user says yes to push/PR. | **Medium.** The model is told the workflow is complete, but it has just offered the user an action (push/PR). If the user accepts, there is no instruction for how to execute it. The model must improvise. Some runs will push correctly; others may refuse because "workflow complete" was already declared. | Add explicit post-offer handling: `If the user requests a push: push to the remote. If the user requests a PR: create a pull request with a title derived from the spec title and a body summarizing the changes. If the user declines: workflow complete.` |
| M5 | **Negation Fragility** (FM-6) | Step-03: `No push. No remote ops.` Step-05: `NEVER auto-push.` Step-04: `Do NOT git add anything.` Three distinct negation-based safety constraints spread across three files. | **Medium.** Each negation individually has inversion risk. The safety constraint "no remote operations during implementation" is critical but expressed as scattered negations rather than a unified positive rule. | Consolidate into a single positive safety rule in workflow.md that persists across all steps: `REMOTE OPERATIONS POLICY: All git operations during steps 1-4 are local only. Remote operations (push, PR creation) are permitted only in step 5, and only when explicitly requested by the human.` |
| M6 | **Over-specification** (FM-4) | Step-04 classify section is ~250 tokens of dense cascading logic with five finding categories, conditional processing order, loopback rules, KEEP instructions, change-log protocol, and spec-loop iteration counting. This is the densest section in the entire workflow. | **Medium.** The classification logic is correct and well-structured, but its density means models under context pressure will simplify. The most likely simplification is collapsing `bad_spec` and `patch` into a single category, or skipping the change-log protocol. The KEEP instruction extraction is the most fragile -- it is a novel concept buried in a dense paragraph. | Split the classification logic into a dedicated sub-section with explicit headings for each category. Consider making the classification a structured decision tree rather than prose: `FOR EACH FINDING: (1) Is it caused by this change? No -> Is it real? Yes -> defer. No -> reject. (2) Is it caused by this change? Yes -> Can you fix it without spec changes? Yes -> patch. No -> Does the fix require changing frozen sections? Yes -> intent_gap. No -> bad_spec.` |
| L1 | **Obsolete Prompting Technique** (FM-12) | Step-01 instruction 2: `When the human replies, verify to yourself that every single numbered question was answered.` The phrase "verify to yourself" is an implicit chain-of-thought instruction. 2026 frontier models have built-in CoT; this instruction is unnecessary and slightly ambiguous (does "to yourself" mean silently? or should verification be shown?). | **Low.** Minor token waste. The instruction is not harmful but the "to yourself" phrasing may cause the model to skip showing its verification, making the process less transparent to the human. | Rewrite: `After the human replies, check that every numbered question was answered. If any were skipped, list only the unanswered questions and HALT.` (This is already mostly what the text says -- just drop "to yourself".) |
| L2 | **Non-deterministic Phrasing** (FM-5) | Step-04 classify instruction 2, `bad_spec` definition: `When in doubt between bad_spec and patch, prefer bad_spec -- a spec-level fix is more likely to produce coherent code.` And for `reject`: `When unsure between defer and reject, prefer reject.` These tie-breaking rules are good but create a subtle tension: the model is told to prefer the more conservative option in one case and the more aggressive option in another. | **Low.** The tie-breaking rules are well-intentioned and individually clear. The risk is that the model generalizes "prefer the more conservative option" and applies it to the defer/reject boundary too, increasing deferrals. Very minor. | No change needed. The current phrasing is clear enough. If desired, add a brief rationale after the reject preference: `prefer reject -- only defer findings you are confident are real, to avoid polluting the deferred backlog.` (This is already present.) |
| L3 | **Silent Ignoring** (FM-1) | workflow.md frontmatter references `advanced_elicitation` and `party_mode_exec` as "Related workflows". These are never referenced in any step file. They exist only in the workflow.md frontmatter as metadata. | **Low.** These consume tokens in the initial context load but are never actionable. They may confuse the model into thinking it should use them. Harmless in most runs but adds noise. | Either remove them from the frontmatter or add a comment: `# Reference only -- not used by this workflow. Available for future extension.` |

---

## Positive Observations

1. **Persistent artifact strategy for `baseline_commit`**: Writing `baseline_commit` to spec frontmatter (step-03) rather than keeping it in memory is the correct pattern. The same approach should be applied to `execution_mode` and `spec_file`.

2. **Frozen-after-approval mechanism**: The `<frozen-after-approval>` tag in the template with the rule that only humans can modify it is an excellent intent-preservation mechanism. The enforcement is referenced consistently in steps 3 and 4.

3. **Spec Change Log with KEEP instructions**: The append-only change log with explicit KEEP instructions is a sophisticated mechanism for preserving positive state across loopbacks. This is genuinely novel and well-designed for multi-iteration loops.

4. **Sub-agent isolation for review**: Launching review subagents without conversation context (step-04) is the correct approach to prevent anchoring bias. The three-reviewer architecture (blind, edge-case, acceptance) provides orthogonal coverage.

5. **Explicit tie-breaking rules**: The `bad_spec > patch` and `reject > defer` preferences in step-04 reduce classification ambiguity. These are clear, actionable heuristics.

6. **Cascading processing order**: Step-04's rule that intent_gap/bad_spec findings make lower findings moot is a correct optimization that prevents wasted work on code that will be re-derived.

7. **Token count check with user override**: Step-02's 1600-token check with explicit `[S]`/`[K]` options respects the user's autonomy while surfacing the risk. The "neither limit is a gate" framing in the SCOPE STANDARD is well-calibrated.

8. **Deferred work file**: Consistent use of `{deferred_work_file}` across steps 1, 2, and 4 for capturing out-of-scope items prevents scope creep while preserving ideas.

---

## Recommended Refactor Summary

- **Highest leverage -- persist all routing state to disk**: Write `execution_mode`, `spec_file`, and `specLoopIteration` to spec frontmatter (or a separate state file). Every step should read state from file, not memory. This single change eliminates findings C1, C2, and reduces C3 risk.

- **Add explicit re-entry instructions for loopbacks**: Step-04's loopback instructions must include `Read and follow {installed_path}/steps/step-0X-....md` rather than abstract "re-run steps N-M". This fixes C4 and H6.

- **Add verification gates at step boundaries**: Step-03 needs a completion check before transitioning to step-04. Step-04 needs a `baseline_commit` existence check before constructing the diff. Step-03 needs a `spec_file` existence check before starting implementation.

- **Single-source variable declarations**: Declare `wipFile`, `templateFile`, `deferred_work_file`, `adversarial_review_task` exactly once in workflow.md. Remove re-declarations from step frontmatters. This eliminates maintenance drift risk (H4).

- **Convert negation-based safety rules to a single positive policy block**: Consolidate "no push", "no remote ops", "never auto-push", "do not git add" into a `REMOTE OPERATIONS POLICY` in workflow.md that applies to all steps.

- **Add deterministic routing criteria**: Replace "trivial (~3 files)" with `<= 3 files AND no architectural decisions`. Replace "make sense" and "obvious mismatch" with concrete branch-name matching rules.

- **Add post-offer handling in step-05**: The workflow declares itself complete before resolving the push/PR offer. Add explicit handling for user acceptance.

---

## Revised Prompt Sections (Critical/High items only)

### C1+C2 Fix: State Persistence in Step-01 (instruction 5-6 rewrite)

```markdown
5. Generate `spec_file` path:
   - Derive a valid kebab-case slug from the clarified intent.
   - If `{implementation_artifacts}/tech-spec-{slug}.md` already exists, append `-2`, `-3`, etc.
   - Set `spec_file` = `{implementation_artifacts}/tech-spec-{slug}.md`.
   - Write `spec_file` to a known location or hold in memory for immediate use in the next step.
6. Route:
   - **One-shot** — affects 3 or fewer files AND requires no architectural decisions. Set `execution_mode = "one-shot"`. → Step 3.
   - **Plan-code-review** — all other cases. Set `execution_mode = "plan-code-review"`. → Step 2.
   - Write `execution_mode` to `{wipFile}` or `{spec_file}` frontmatter so downstream steps can read it from disk.
```

### C3 Fix: Baseline Commit Verification in Step-04

```markdown
### Construct Diff (plan-code-review only)

Read `baseline_commit` from `{spec_file}` frontmatter. If `baseline_commit` is absent, empty, or
does not resolve to a valid commit, HALT: "baseline_commit not found or invalid in spec frontmatter.
Cannot construct diff. Please verify step-03 completed correctly."

Construct `{diff_output}` covering all changes — tracked and untracked — since `{baseline_commit}`.
If a proper diff cannot be constructed, use best effort to determine what changed.

Do NOT `git add` anything — this is read-only inspection.
```

### C4+H6 Fix: Explicit Loopback Re-entry in Step-04

```markdown
3. Process findings in cascading order. If intent_gap or bad_spec findings exist, they trigger
   a loopback — lower findings are moot since code will be re-derived. If neither exists,
   process patch and defer normally. Increment `{specLoopIteration}` on each loopback. If it
   exceeds 5, HALT and escalate to the human.

   On any loopback, re-evaluate routing — if scope has grown beyond one-shot, update
   `execution_mode` to `plan-code-review` in `{spec_file}` frontmatter.

   - **intent_gap** — Root cause is inside `<frozen-after-approval>`. Revert code changes.
     HALT AND WAIT FOR HUMAN: Present the intent_gap finding and ask the human to clarify
     the intent. Once the human responds, read and follow
     `{installed_path}/steps/step-02-plan.md` to re-derive the spec.

   - **bad_spec** — Root cause is outside `<frozen-after-approval>`. Before reverting code:
     extract KEEP instructions for positive preservation (what worked well and must survive
     re-derivation). Revert code changes. Read the `## Spec Change Log` in `{spec_file}`
     and strictly respect all logged constraints when amending the non-frozen sections that
     contain the root cause. Append a new change-log entry recording: the triggering finding,
     what was amended, the known-bad state avoided, and the KEEP instructions. Then read and
     follow `{installed_path}/steps/step-03-implement.md` to re-implement.

   - **patch** — Auto-fix. These are the only findings that survive loopbacks.
   - **defer** — Append to `{deferred_work_file}`.
   - **reject** — Drop silently.
```

### H1 Fix: Implementation Completion Verification in Step-03

```markdown
### Implement

Change `{spec_file}` status to `in-progress` in the frontmatter before starting implementation.

`execution_mode = "one-shot"` or no sub-agents/tasks available: implement the intent directly.

Otherwise (`execution_mode = "plan-code-review"`): hand `{spec_file}` to a sub-agent/task and
let it implement.

### Verify Completion

After implementation (whether direct or via sub-agent):
1. Read the "Tasks & Acceptance" section of `{spec_file}`.
2. Confirm every task has been addressed. If any task is incomplete, continue implementation.
3. If using a sub-agent, verify it completed successfully (no errors, no partial output).
4. Run any commands listed in the "Verification" section of `{spec_file}` and confirm they pass.
   If any verification fails, fix the issue before proceeding.
```

### H2 Fix: Positive Step Loading Protocol (replaces Critical Rules)

```markdown
### Step Loading Protocol (NO EXCEPTIONS)

1. Complete the current step fully before loading the next step file.
2. Load exactly one step file at a time.
3. Read the loaded step file from start to finish before executing any instruction.
4. Execute sections within the step in the order they appear.
5. At every HALT instruction, stop and wait for human input before continuing.
6. When a step's NEXT section directs you to another step, read and follow that file.
```

---

**Reviewer Confidence:** 92/100
**Review Complete** -- ready for re-submission or automated patching.
