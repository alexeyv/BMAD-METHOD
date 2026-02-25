# Test Report: Scope Guardrails for Quick-Dev2

**Date:** 2026-02-24
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
| **Notes** | Three independent verbs unambiguously trigger the >=2 condition. |

### TC2: Single cohesive feature across multiple layers

| | |
|---|---|
| **Intent** | "Add user authentication with a login page, signup page, password reset flow, and the necessary API endpoints and database tables." |
| **Expected** | One user-facing goal (authentication) spanning multiple layers. No split proposed. |
| **Acceptance** | PASS if no split proposed. FAIL if split proposed. |
| **Result** | PASS |
| **Notes** | SCOPE STANDARD explicitly says "even if it spans multiple layers/files." One top-level verb ("add authentication"), sub-items are nouns not independent verbs. |

### TC3: Borderline — two coupled sub-goals

| | |
|---|---|
| **Intent** | "Add form validation to the checkout page and display error messages inline." |
| **Expected** | No split — displaying errors is a sub-component of validation, not independently shippable. |
| **Acceptance** | PASS if no split proposed. AMBIGUOUS if the instructions don't clearly prevent a split here. FAIL if split is proposed. |
| **Result** | AMBIGUOUS |
| **Notes** | Two surface-level verbs ("add" / "display") but "display errors" depends on validation. The independent-verb test says "could ship separately" which should exclude this, but the instructions don't explicitly say to check whether goal B depends on goal A. A weaker agent could false-trigger. |

### TC4: Subtle independent goals

| | |
|---|---|
| **Intent** | "Update the API rate limiting configuration and also add a new /health endpoint for monitoring." |
| **Expected** | Two independent goals (rate limiting config / health endpoint). Split proposed. |
| **Acceptance** | PASS if split proposed with both goals listed. FAIL if no split proposed. |
| **Result** | PASS |
| **Notes** | "Update" and "add" are independent verbs; either could ship alone. |

### TC5: Split chosen — first-mentioned goal selection

| | |
|---|---|
| **Intent** | Same as TC1. Simulated user response: **[S]** |
| **Expected** | Child stories (refactor auth, build admin) written to `{deferred_findings_file}` under `## Deferred Stories`. Scope narrows to "add dark mode toggle" (first-mentioned). Continues to routing. |
| **Acceptance** | PASS if first-mentioned goal is selected and child stories are written. FAIL if wrong goal selected or no persistence. |
| **Result** | PASS |
| **Notes** | "Narrow scope to the first-mentioned goal" is unambiguous from sentence ordering. |

### TC6: Keep chosen — override

| | |
|---|---|
| **Intent** | Same as TC1. Simulated user response: **[K]** |
| **Expected** | Full multi-goal intent passes unchanged into routing. No deferred findings written. |
| **Acceptance** | PASS if no scope change and no file writes. FAIL if scope modified. |
| **Result** | PASS |
| **Notes** | "[K]: Proceed as-is" is minimal but unambiguous. Downstream routing will likely recommend Full BMM for this scope — that's correct behavior, not a bug. |

### TC7: Single goal with many AND conjunctions

| | |
|---|---|
| **Intent** | "Build a file upload feature that supports drag-and-drop AND paste from clipboard AND progress indicators AND retry on failure." |
| **Expected** | No split — all conjunctions describe aspects of one feature (file upload). None independently meaningful. |
| **Acceptance** | PASS if no split proposed. AMBIGUOUS if the instructions don't clearly prevent it. FAIL if split proposed. |
| **Result** | AMBIGUOUS |
| **Notes** | Same gap as TC3. One top-level verb ("build"), but AND appears 4 times. The instructions don't explicitly say the test applies to top-level verbs only. A careful agent handles this; a conjunction-counting agent may not. |

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
| **Notes** | "If spec exceeds ~1200 words" — 750 clearly does not. |

### TC9: Spec barely over threshold

| | |
|---|---|
| **Scenario** | Agent generates a 1250-word spec. |
| **Expected** | Agent shows word count (1250), presents `[S]/[K]` menu. |
| **Acceptance** | PASS if word count shown and menu presented. FAIL if no warning. |
| **Result** | PASS |
| **Notes** | Clean trigger. |

### TC10: Split chosen — trim is structural, not editorial

| | |
|---|---|
| **Scenario** | 1400-word spec. User chooses **[S]**. |
| **Expected** | Agent identifies independent child story sections. Writes them to deferred file. Removes only those sections — no prose compression on remaining content. Continues to CHECKPOINT 1. |
| **Acceptance** | PASS if the anti-compression instruction ("never compress prose to hit a word count") is explicit and unambiguous. FAIL if an agent could reasonably interpret "trim" as compression. |
| **Result** | PASS |
| **Notes** | The prohibition is named and specific: "Remove only those sections from the current spec — never compress prose to hit a word count." |

### TC11: Keep chosen — override echo at checkpoint

| | |
|---|---|
| **Scenario** | 1500-word spec. User chooses **[K]**. |
| **Expected** | Agent continues to CHECKPOINT 1. Word count (1500) is echoed in the checkpoint presentation. |
| **Acceptance** | PASS if the instruction to echo word count at checkpoint exists and is conditional on [K] + over-threshold. FAIL if no echo instruction. AMBIGUOUS if the instruction exists but could be missed. |
| **Result** | PASS |
| **Notes** | The parenthetical "if word count exceeded ~1200 and user chose [K], echo the word count here" is correct but soft. A hasty agent might treat parenthetical text as optional. Consider making it imperative in a future pass. |

### TC12: Massively over threshold

| | |
|---|---|
| **Scenario** | Agent generates a 2500-word spec. |
| **Expected** | Same as TC9 — word count shown, `[S]/[K]` menu. No additional escalation. |
| **Acceptance** | PASS if same single-level menu as TC9. FAIL if additional escalation or mandatory split. |
| **Result** | PASS |
| **Notes** | SCOPE STANDARD says "Neither limit is a gate." No tiered escalation by design. |

### TC13: Exactly at threshold — tilde ambiguity

| | |
|---|---|
| **Scenario** | Agent generates a spec that is exactly 1200 words. |
| **Expected** | Should NOT trigger (1200 is the top of the optimal range, not beyond it). |
| **Acceptance** | PASS if "exceeds ~1200" is clearly interpreted as >1200. AMBIGUOUS if the tilde creates genuine uncertainty at this boundary. |
| **Result** | AMBIGUOUS |
| **Notes** | "Exceeds ~1200" — most natural reading of "exceeds" means strictly greater than, so 1200 exactly doesn't trigger. The tilde adds fuzz. Not a practical problem (1200 vs 1201 doesn't matter) but technically ambiguous. |

### TC14: Ordering — word count after self-review

| | |
|---|---|
| **Scenario** | Verify instruction 5 (word count) fires after instruction 3 (self-review) and instruction 4 (intent gaps). |
| **Expected** | Strict sequential ordering. Word count check is last before checkpoint. |
| **Acceptance** | PASS if numbering + workflow sequencing rules make this unambiguous. FAIL if an agent could reorder. |
| **Result** | PASS |
| **Notes** | Numbered list + workflow.md critical rule "FOLLOW SEQUENCE: Execute sections in order" makes this airtight. |

### TC15: Post-trim spec still over threshold

| | |
|---|---|
| **Scenario** | 1400-word auth spec. User chooses [S]. Agent removes 2FA and email verification sections. Remaining spec (login + signup + password reset) is ~1050 words — or still ~1250 words. |
| **Expected** | Agent removes child story sections, does NOT re-check or re-trigger the word count menu. Proceeds to checkpoint even if residual exceeds 1200. |
| **Acceptance** | PASS if no re-check loop exists. AMBIGUOUS if instructions could be read as requiring re-evaluation. |
| **Result** | PASS |
| **Notes** | No recursive word count loop in the instructions. [S] branch says "Continue to checkpoint" unconditionally after removal. This is the correct design — avoid infinite negotiation. |

---

## Suite C: Cross-Step Integration

Tests the interaction between steps that share the deferred-findings file, variable resolution, bypass paths, and checkpoint menu consistency.

### IT1: Double-split — step-01 then step-02 both write deferred stories

| | |
|---|---|
| **Scenario** | User splits at step-01 (writes child stories). Narrowed scope still produces >1200 word spec. User splits again at step-02 (writes more child stories). |
| **Expected** | Both writes should coexist in the same file without data loss. |
| **Acceptance** | PASS if append semantics are specified. FAIL if no append/overwrite instruction exists and the second write could clobber the first. |
| **Result** | FAIL — Critical |
| **Notes** | Neither step specifies append vs. overwrite. Both use the same heading (`## Deferred Stories`). Second write may erase the first, or produce duplicate H2 headings. The "Append-Only Building" principle in workflow.md is about spec artifacts, not this file, and is not referenced in either step. |

### IT2: Step-01 deferred stories + step-04 deferred review findings

| | |
|---|---|
| **Scenario** | Step-01 writes child stories under `## Deferred Stories`. Later, step-04 writes deferred review findings to the same file. |
| **Expected** | Both should coexist with distinct sections. |
| **Acceptance** | PASS if step-04 uses a different section heading and specifies append. FAIL if step-04 has no heading and no append instruction. |
| **Result** | FAIL — Critical |
| **Notes** | Step-04 says "Write deferred findings to `{deferred_findings_file}`" with no section heading and no append/overwrite instruction. Semantically different content (review findings vs. child stories) gets mixed with no differentiation. |

### IT3: Clean run — deferred file doesn't exist when step-04 writes

| | |
|---|---|
| **Scenario** | No splits at step-01 or step-02. Step-04 is the first writer. |
| **Expected** | Step-04 creates the file from scratch. |
| **Acceptance** | PASS if agents typically handle file creation on write. AMBIGUOUS if the instruction doesn't address file creation. |
| **Result** | AMBIGUOUS — Minor |
| **Notes** | Most agents create files on write. The real issue is step-04 has no format specification — heading, template, or example — so the output structure varies between runs. |

### IT4: Variable resolution — `{output_dir}` undefined

| | |
|---|---|
| **Scenario** | All three steps reference `{deferred_findings_file}` = `{output_dir}/deferred-findings.md`. |
| **Expected** | `{output_dir}` resolves to a real path. |
| **Acceptance** | PASS if `{output_dir}` is defined in workflow.md initialization or config.yaml. FAIL if undefined. |
| **Result** | FAIL — Critical (pre-existing) |
| **Notes** | `{output_dir}` is NOT in workflow.md's INITIALIZATION SEQUENCE (sections 1 or 2). Not in the config.yaml variables list. Step-04 already used this variable before our change — this is pre-existing debt, not introduced by scope guardrails. If it resolves via an undocumented mechanism, that mechanism should be documented. If it doesn't resolve, every deferred-findings write is broken. |

### IT5: Ready-for-dev bypass skips both guardrails

| | |
|---|---|
| **Scenario** | A `ready-for-dev` spec exists in `{implementation_artifacts}`. Step-01 fast-paths to step-03, skipping both scope guardrails. |
| **Expected** | Intentional and correct — a ready-for-dev spec was already reviewed. |
| **Acceptance** | PASS if the bypass is documented and by design. FAIL if accidental. |
| **Result** | PASS |
| **Notes** | The fast-path is explicit in step-01's CONTEXT section. The scope guardrails are advisory by design ("Neither limit is a gate"), so skipping them for an already-approved spec is coherent. |

### IT6: Checkpoint menu consistency across steps

| | |
|---|---|
| **Scenario** | Compare all checkpoint menus for letter collisions, label consistency, and UX coherence. |
| **Expected** | No letter collisions within any single menu. Consistent S/K usage across scope checks. |
| **Acceptance** | PASS if no collisions and reasonable consistency. AMBIGUOUS if minor label drift. |
| **Result** | PASS (minor observations) |
| **Notes** | S/K used at both scope checkpoints (good consistency). A/E/F at approval checkpoint (no collision). Minor label drift: `[K] Keep as single spec` (step-01) vs `[K] Keep as-is` (step-02). Minor opacity: `[F] Full BMM` assumes BMM familiarity. Neither is a functional issue. |

---

## Summary

### Pass Rates

| Suite | Pass | Ambiguous | Fail | Total |
|-------|------|-----------|------|-------|
| A: Multi-Goal Detection | 5 | 2 | 0 | 7 |
| B: Word Count Check | 6 | 2 | 0 | 8 |
| C: Integration | 2 | 1 | 3 | 6 |
| **Total** | **13** | **5** | **3** | **21** |

### Issues by Severity

**Critical (3) — all pre-existing patterns, not introduced by this change:**

1. **`{output_dir}` undefined (IT4)** — variable used in 3 step frontmatters but never initialized in workflow.md. Every deferred-findings write targets an unresolved path.
2. **No append/overwrite semantics for deferred file (IT1)** — double-split scenario loses data from the first split.
3. **Step-04 writes with no section heading (IT2)** — review findings collide with child stories in the shared file.

**Ambiguous (5) — hardening opportunities:**

4. **Independent-verb test doesn't specify scope of application (TC3, TC7)** — coupled sub-goals and noun-phrase conjunctions may false-trigger in weaker agents. Fix: clarify the test applies to top-level actions only.
5. **Tilde threshold ambiguity at exactly 1200 (TC13)** — "exceeds ~1200" is technically fuzzy at the boundary. Fix: drop the tilde or add "use 1200 as the threshold."
6. **Word count echo instruction is parenthetical (TC11)** — correct but could be missed by a hasty agent. Fix: make it imperative.
7. **No re-check after trim (TC15)** — implicit that no loop exists, could be made explicit.
8. **Step-04 has no format specification (IT3)** — output structure varies between runs.

**Minor observations (non-blocking):**

9. `[K]` label drift between step-01 and step-02.
10. `[F] Full BMM` is opaque for new users.
11. No user warning when [K] at step-01 will likely hit Full BMM at routing.
