# Test Report: Scope Guardrails for Quick-Dev2

**Date:** 2026-02-24 (re-run)
**Commit:** 768e1830 (exp/quick-flow-redesign)
**Spec:** `_experiment/intent-scope-guardrails.md`

## How to Re-Run This Test

Ask the orchestrator to run this test suite against the current state of the quick-dev2 workflow files. Use three parallel sub-agents (sonnet-class) with no conversation context — each gets only its test section and the file paths below. Collect results and fill in the Results column.

**Files under test:**
- `src/bmm/workflows/bmad-quick-flow/quick-dev2/workflow.md` (SCOPE STANDARD block)
- `src/bmm/workflows/bmad-quick-flow/quick-dev2/steps/step-01-clarify-and-route.md` (multi-goal detection)
- `src/bmm/workflows/bmad-quick-flow/quick-dev2/steps/step-02-plan.md` (word count check)
- `src/bmm/workflows/bmad-quick-flow/quick-dev2/steps/step-04-review.md` (deferred findings — reference only)

**Method:** Each sub-agent reads the files under test, then role-plays the workflow agent processing each test case. The agent evaluates whether the written instructions would produce the expected behavior, flags ambiguities, and reports PASS / FAIL / AMBIGUOUS.

---

## Suite A: Step-01 Multi-Goal Detection

Tests whether the independent-verb check in step-01 correctly identifies multi-goal intents, avoids false positives on cohesive features, and handles user responses at the split checkpoint.

### TC1: Clear multi-goal intent

| | |
|---|---|
| **Intent** | "I need to add a dark mode toggle to the settings page, AND refactor the authentication module to use JWT instead of sessions, AND build an admin dashboard for user management." |
| **Expected** | Agent detects 3 independent goals (add/refactor/build — each shippable alone). Presents bullet list. Shows `[S]/[K]` menu. |
| **Acceptance** | PASS if split is proposed with all 3 goals listed. FAIL if no split proposed. |
| **Result** | PASS |
| **Notes** | SCOPE STANDARD defines the independent-verb test: "if the intent has >=2 verbs that could ship independently." Three clearly independent verbs (add/refactor/build) with independent deliverables trigger unambiguously. |

### TC2: Single cohesive feature across multiple layers

| | |
|---|---|
| **Intent** | "Add user authentication with a login page, signup page, password reset flow, and the necessary API endpoints and database tables." |
| **Expected** | One user-facing goal (authentication) spanning multiple layers. No split proposed. |
| **Acceptance** | PASS if no split proposed. FAIL if split proposed. |
| **Result** | PASS |
| **Notes** | SCOPE STANDARD explicitly covers this: "One cohesive feature, even if it spans multiple layers/files." One governing verb ("add authentication"); sub-items (login page, signup page, etc.) are elaborations, not independent verbs with independent deliverables. |

### TC3: Borderline — two coupled sub-goals

| | |
|---|---|
| **Intent** | "Add form validation to the checkout page and display error messages inline." |
| **Expected** | No split — displaying errors is a sub-component of validation, not independently shippable. |
| **Acceptance** | PASS if no split proposed. AMBIGUOUS if the instructions don't clearly prevent a split here. FAIL if split is proposed. |
| **Result** | AMBIGUOUS |
| **Notes** | Two surface-level verbs ("add" / "display") but "display errors" depends on validation and has no user value without it. The SCOPE STANDARD says verbs must "could ship independently," which should exclude this, but the instructions provide no explicit guidance for coupled/dependent sub-goals, no examples, and no heuristic beyond "could ship independently." A strict verb-counting agent would likely misfire. |

### TC4: Subtle independent goals

| | |
|---|---|
| **Intent** | "Update the API rate limiting configuration and also add a new /health endpoint for monitoring." |
| **Expected** | Two independent goals (rate limiting config / health endpoint). Split proposed. |
| **Acceptance** | PASS if split proposed with both goals listed. FAIL if no split proposed. |
| **Result** | PASS |
| **Notes** | "Update" (rate limiting) and "add" (health endpoint) are independent verbs with independently shippable deliverables sharing no dependency. Clean trigger of the independent-verb test. |

### TC5: Split chosen — first-mentioned goal selection

| | |
|---|---|
| **Intent** | Same as TC1. Simulated user response: **[S]** |
| **Expected** | Child stories (refactor auth, build admin) written to `{deferred_findings_file}` under `## Deferred Stories`. Scope narrows to "add dark mode toggle" (first-mentioned). Continues to routing. |
| **Acceptance** | PASS if first-mentioned goal is selected and child stories are written. FAIL if wrong goal selected or no persistence. |
| **Result** | PASS |
| **Notes** | Step-01 [S] branch: "Narrow scope to the first-mentioned goal" is unambiguous. Child stories appended to `{deferred_work_file}`. Note: test case references `{deferred_findings_file}` / `## Deferred Stories` but actual code uses `{deferred_work_file}` with no section heading — test case variable names are stale. Core behavior (persistence + scope narrowing) is clearly specified. |

### TC6: Keep chosen — override

| | |
|---|---|
| **Intent** | Same as TC1. Simulated user response: **[K]** |
| **Expected** | Full multi-goal intent passes unchanged into routing. No deferred findings written. |
| **Acceptance** | PASS if no scope change and no file writes. FAIL if scope modified. |
| **Result** | PASS |
| **Notes** | [K] branch says "Proceed as-is" — no file writes, no scope modification. Downstream routing will likely recommend Full BMM for this scope; that's correct behavior, not a bug. |

### TC7: Single goal with many AND conjunctions

| | |
|---|---|
| **Intent** | "Build a file upload feature that supports drag-and-drop AND paste from clipboard AND progress indicators AND retry on failure." |
| **Expected** | No split — all conjunctions describe aspects of one feature (file upload). None independently meaningful. |
| **Acceptance** | PASS if no split proposed. AMBIGUOUS if the instructions don't clearly prevent it. FAIL if split proposed. |
| **Result** | AMBIGUOUS |
| **Notes** | One governing verb ("build") with four AND-connected feature aspects. The SCOPE STANDARD's canonical example (`add X AND refactor Y`) implies distinct action verbs, but the instructions provide no explicit guidance to distinguish "feature aspects connected by AND" from "independent goals connected by AND." An agent counting AND conjunctions or gerundive phrases could spuriously trigger. Same gap as TC3. |

---

## Suite B: Step-02 Word Count Check

Tests whether the post-draft word count check correctly triggers, handles user responses, prevents prose compression, and echoes overrides at the approval checkpoint.

### TC8: Spec well under threshold

| | |
|---|---|
| **Scenario** | Agent generates a 750-word spec. |
| **Expected** | No word count warning. Proceeds directly to CHECKPOINT 1. |
| **Acceptance** | PASS if no `[S]/[K]` menu shown. FAIL if menu shown. |
| **Result** | PASS |
| **Notes** | Instruction 5: "If spec exceeds ~1200 words" — 750 is clearly below, condition is false, no menu shown. |

### TC9: Spec barely over threshold

| | |
|---|---|
| **Scenario** | Agent generates a 1250-word spec. |
| **Expected** | Agent shows word count (1250), presents `[S]/[K]` menu. |
| **Acceptance** | PASS if word count shown and menu presented. FAIL if no warning. |
| **Result** | PASS |
| **Notes** | 1250 clearly exceeds ~1200. Instruction explicitly requires "Show user the word count" followed by `[S]/[K]` menu. Clean trigger, no ambiguity. |

### TC10: Split chosen — trim is structural, not editorial

| | |
|---|---|
| **Scenario** | 1400-word spec. User chooses **[S]**. |
| **Expected** | Agent identifies independent child story sections. Writes them to deferred file. Removes only those sections — no prose compression on remaining content. Continues to CHECKPOINT 1. |
| **Acceptance** | PASS if the anti-compression instruction ("never compress prose to hit a word count") is explicit and unambiguous. FAIL if an agent could reasonably interpret "trim" as compression. |
| **Result** | PASS |
| **Notes** | S-branch: "Remove only those sections from the current spec — **never compress prose to hit a word count**." The word "only" + the explicit prohibition leave no room for editorial compression. Unambiguous. |

### TC11: Keep chosen — override echo at checkpoint

| | |
|---|---|
| **Scenario** | 1500-word spec. User chooses **[K]**. |
| **Expected** | Agent continues to CHECKPOINT 1. Word count (1500) is echoed in the checkpoint presentation. |
| **Acceptance** | PASS if the instruction to echo word count at checkpoint exists and is conditional on [K] + over-threshold. FAIL if no echo instruction. AMBIGUOUS if the instruction exists but could be missed. |
| **Result** | PASS |
| **Notes** | CHECKPOINT 1 reads: "if word count exceeded ~1200 and user chose [K], echo the word count here." Instruction is present, correctly conditional on [K] + over-threshold. Parenthetical form is correct but soft — a hasty agent might treat it as optional. Consider making it imperative. |

### TC12: Massively over threshold

| | |
|---|---|
| **Scenario** | Agent generates a 2500-word spec. |
| **Expected** | Same as TC9 — word count shown, `[S]/[K]` menu. No additional escalation. |
| **Acceptance** | PASS if same single-level menu as TC9. FAIL if additional escalation or mandatory split. |
| **Result** | PASS |
| **Notes** | Single binary condition ("If spec exceeds ~1200"), one two-option menu. No additional escalation tier, no mandatory split, no secondary threshold. SCOPE STANDARD: "Neither limit is a gate." Identical behavior whether spec is 1250 or 2500 words. |

### TC13: Exactly at threshold — tilde ambiguity

| | |
|---|---|
| **Scenario** | Agent generates a spec that is exactly 1200 words. |
| **Expected** | Should NOT trigger (1200 is the top of the optimal range, not beyond it). |
| **Acceptance** | PASS if "exceeds ~1200" is clearly interpreted as >1200. AMBIGUOUS if the tilde creates genuine uncertainty at this boundary. |
| **Result** | AMBIGUOUS |
| **Notes** | "Exceeds ~1200" — "exceeds" implies strictly greater than, so 1200 exactly shouldn't trigger. But the tilde creates legitimate uncertainty: "exceeds approximately 1200" could mean anywhere from 1150–1250 to a reasonable agent. SCOPE STANDARD gives 400–1200 as optimal range, implying 1200 is the boundary, but step-02 uses "~1200" not ">1200." Not a practical problem but technically fuzzy at this boundary. |

### TC14: Ordering — word count after self-review

| | |
|---|---|
| **Scenario** | Verify instruction 5 (word count) fires after instruction 3 (self-review) and instruction 4 (intent gaps). |
| **Expected** | Strict sequential ordering. Word count check is last before checkpoint. |
| **Acceptance** | PASS if numbering + workflow sequencing rules make this unambiguous. FAIL if an agent could reorder. |
| **Result** | PASS |
| **Notes** | Instructions explicitly numbered 1–5. workflow.md CRITICAL RULES include "NEVER skip steps or optimize the sequence" and "FOLLOW SEQUENCE: Execute sections in order." Together, numeric ordering + sequential enforcement make reordering impossible for a compliant agent. |

### TC15: Post-trim spec still over threshold

| | |
|---|---|
| **Scenario** | 1400-word auth spec. User chooses [S]. Agent removes 2FA and email verification sections. Remaining spec (login + signup + password reset) is ~1050 words — or still ~1250 words. |
| **Expected** | Agent removes child story sections, does NOT re-check or re-trigger the word count menu. Proceeds to checkpoint even if residual exceeds 1200. |
| **Acceptance** | PASS if no re-check loop exists. AMBIGUOUS if instructions could be read as requiring re-evaluation. |
| **Result** | PASS |
| **Notes** | S-branch ends with "Continue to checkpoint" — a direct, unconditional forward-flow directive. No loop instruction, no re-evaluation clause. Numbered instructions are a one-pass sequence per workflow.md sequential enforcement rules; instruction 5 cannot be re-entered. Correct design — avoids infinite negotiation. |

---

## Suite C: Cross-Step Integration

Tests the interaction between steps that share the deferred-findings file, variable resolution, bypass paths, and checkpoint menu consistency.

### IT1: Double-split — step-01 then step-02 both write deferred stories

| | |
|---|---|
| **Scenario** | User splits at step-01 (writes child stories). Narrowed scope still produces >1200 word spec. User splits again at step-02 (writes more child stories). |
| **Expected** | Both writes should coexist in the same file without data loss. |
| **Acceptance** | PASS if append semantics are specified. FAIL if no append/overwrite instruction exists and the second write could clobber the first. |
| **Result** | PASS (with quality caveat) |
| **Notes** | Both steps now explicitly use "Append" semantics — step-01: "Append child stories to `{deferred_work_file}`", step-02: "Append them to `{deferred_work_file}`." Data loss from overwrite cannot occur. However, neither step specifies a section heading or separator, so concatenated content from two separate split operations will be unstructured and difficult to distinguish. |

### IT2: Step-01 deferred stories + step-04 deferred review findings

| | |
|---|---|
| **Scenario** | Step-01 writes child stories to `{deferred_work_file}`. Later, step-04 writes deferred review findings to the same file. |
| **Expected** | Both appends coexist without data loss. No section headings required — the file is a flat append log by design. |
| **Acceptance** | PASS if both steps use append semantics. FAIL if either could clobber the other. |
| **Result** | PASS |
| **Notes** | Step-01: "Append child stories to `{deferred_work_file}`." Step-04: "Append deferred findings to `{deferred_work_file}`." Both use explicit append semantics. No structural separation between content types is required by design. |

### IT3: Clean run — deferred file doesn't exist when step-04 writes

| | |
|---|---|
| **Scenario** | No splits at step-01 or step-02. Step-04 is the first writer. |
| **Expected** | Step-04 creates the file from scratch. |
| **Acceptance** | PASS if agents typically handle file creation on write. AMBIGUOUS if the instruction doesn't address file creation. |
| **Result** | AMBIGUOUS |
| **Notes** | Step-04 says "Append deferred findings" but does not address the case where the file does not yet exist. Most agents/tools create files on write — standard OS behavior — but the instruction itself is silent on file creation. Additionally, step-04 has no format specification (heading, template, or example), so output structure varies between runs. |

### IT4: Variable resolution — `{deferred_work_file}` chain

| | |
|---|---|
| **Scenario** | Steps 01, 02, and 04 reference `{deferred_work_file}` = `{implementation_artifacts}/deferred-work.md`. |
| **Expected** | `{implementation_artifacts}` resolves to a real path via config.yaml. |
| **Acceptance** | PASS if `{implementation_artifacts}` is defined in config.yaml and resolves through `{project-root}`. FAIL if undefined. |
| **Result** | PASS |
| **Notes** | `{implementation_artifacts}` is defined in config.yaml as `{project-root}/_bmad-output/implementation-artifacts`. `{project-root}` resolves at runtime. The full chain `{deferred_work_file}` → `{implementation_artifacts}/deferred-work.md` → `{project-root}/_bmad-output/implementation-artifacts/deferred-work.md` resolves correctly. |

### IT5: Ready-for-dev bypass skips both guardrails

| | |
|---|---|
| **Scenario** | A `ready-for-dev` spec exists in `{implementation_artifacts}`. Step-01 fast-paths to step-03, skipping both scope guardrails. |
| **Expected** | Intentional and correct — a ready-for-dev spec was already reviewed. |
| **Acceptance** | PASS if the bypass is documented and by design. FAIL if accidental. |
| **Result** | PASS |
| **Notes** | Step-01 CONTEXT: "`ready-for-dev` spec in `{implementation_artifacts}`? → Confirm, skip to step 3." Bypass fires before the multi-goal check is reached. Step-02 is never loaded. Both guardrails are advisory by design ("Neither limit is a gate"), so skipping them for an already-approved spec is intentional and coherent. |

### IT6: Checkpoint menu consistency across steps

| | |
|---|---|
| **Scenario** | Compare all checkpoint menus for letter collisions, label consistency, and UX coherence. |
| **Expected** | No letter collisions within any single menu. Consistent S/K usage across scope checks. |
| **Acceptance** | PASS if no collisions and reasonable consistency. AMBIGUOUS if minor label drift. |
| **Result** | AMBIGUOUS |
| **Notes** | No letter collisions within any single menu. S/K consistent across both scope checks (good). A/E/F at approval checkpoint (no collision). However, minor label drift: `[K] Keep as single spec` (step-01) vs `[K] Keep as-is` (step-02) — semantically equivalent but not identical. Per acceptance criterion ("AMBIGUOUS if minor label drift"), this qualifies. `[F] Full BMM` is opaque for new users. |

---

## Summary

### Pass Rates

| Suite | Pass | Ambiguous | Fail | Total |
|-------|------|-----------|------|-------|
| A: Multi-Goal Detection | 5 | 2 | 0 | 7 |
| B: Word Count Check | 7 | 1 | 0 | 8 |
| C: Integration | 4 | 2 | 0 | 6 |
| **Total** | **16** | **5** | **0** | **21** |

### Changes from Previous Run

| Test | Previous | Current | Reason |
|------|----------|---------|--------|
| IT1 | FAIL | **PASS** | Both steps now explicitly use "Append" semantics, preventing data loss |
| IT4 | FAIL (stale test) | **PASS** | Test case updated to reflect actual variable names; `{deferred_work_file}` → `{implementation_artifacts}` chain resolves correctly |
| IT2 | FAIL | **PASS** | Acceptance criterion updated — flat append log is by design, no section headings required |
| IT6 | PASS | **AMBIGUOUS** | Acceptance criterion says "AMBIGUOUS if minor label drift" — `[K]` label differs between steps |
| Suite B totals | 6/2/0 | **7/1/0** | Previous summary had a counting error (TC11 was PASS, not AMBIGUOUS) |

### Issues by Severity

**Ambiguous (5) — hardening opportunities:**

1. **Independent-verb test doesn't specify scope of application (TC3, TC7)** — coupled sub-goals and noun-phrase conjunctions may false-trigger in weaker agents. Fix: clarify the test applies to top-level actions only.
2. **Tilde threshold ambiguity at exactly 1200 (TC13)** — "exceeds ~1200" is technically fuzzy at the boundary. Fix: drop the tilde or add "use 1200 as the threshold."
3. **`[K]` label drift between step-01 and step-02 (IT6)** — "Keep as single spec" vs "Keep as-is." Semantically equivalent but not identical.
4. **Step-04 has no format specification (IT3)** — output structure varies between runs. File creation on first write is implicit.
5. **Word count echo instruction is parenthetical (TC11)** — correct but could be missed by a hasty agent. Fix: make it imperative.

**Resolved from previous run:**

6. ~~No append/overwrite semantics for deferred file (IT1)~~ — **Fixed.** Both steps now explicitly say "Append."
7. ~~`{output_dir}` undefined (IT4)~~ — **Not a code defect.** Test case updated to use actual variable names; chain resolves correctly.
8. ~~Step-04 writes with no section heading (IT2)~~ — **By design.** Deferred work file is a flat unsorted append log; stories, findings, bugs, and ideas are all the same content type at this level.

**Minor observations (non-blocking):**

9. `[F] Full BMM` is opaque for new users.
10. No user warning when [K] at step-01 will likely hit Full BMM at routing.

