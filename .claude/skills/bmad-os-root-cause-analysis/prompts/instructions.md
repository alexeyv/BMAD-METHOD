# Bug-Fix Root Cause Analysis

Analyze a bug-fix commit or PR and produce a structured Root Cause Analysis report.

## Important

- **Direct attribution.** This report names the individual who introduced the defect. Industry convention (Google SRE, PagerDuty, Atlassian) advocates blameless postmortems. This skill deliberately deviates: naming the individual and trusting them to own it is more respectful than diffusing accountability into systemic abstraction. Direct, factual, not accusatory.
- **Pyramid principle.** The executive summary must convey the full picture. A reader who stops after the first paragraph gets the gist. Everything else is supporting evidence.

## Step 1: Identify the Bug Fix

Accept the user's input — commit SHA, PR number/URL, issue link, or description.

Resolve to the specific fix:
- PR number → `gh pr view {number} --json title,body,commits,files,url,author,mergedAt`
- Commit SHA → `git show {sha} --stat` and `git log {sha} -1 --format="%H %s %an %ad"`
- Issue → `gh issue view {number} --json title,body,comments` → find the linked PR/commit
- Vague description → search with `gh pr list --search "{query}" --state merged --json number,title` or `git log --grep="{query}" --oneline`

If ambiguous or no clear match: **ask the user**. Do not guess.

## Step 2: Gather Evidence

Once the fix is identified, collect:

1. **The fix diff** — `git show {fix-sha}` or `gh pr diff {number}`
2. **PR/issue context** — description, comments, review discussion (`gh pr view`, `gh issue view`)
3. **The introducing commit** — use `git log`, `git blame` on the fixed lines (pre-fix state), and reasoning to identify when the bug was introduced. If unclear, state your best hypothesis and confidence level.
4. **The introducing PR/context** — `gh pr list --search {introducing-sha} --state merged` or check the commit message for PR references
5. **Test changes** — did the fix add/modify tests? What was the test coverage gap?
6. **Timeline data** — when introduced, when reported/detected, when fixed

## Step 3: Analyze Root Cause

Apply **5 Whys** — ask "why?" iteratively until you reach a systemic cause. Stop when the next "why" would leave the team's sphere of influence.

Classify the root cause into one of these categories:
- **Requirements** — ambiguous, incomplete, or changing requirements
- **Design** — architectural decision that made the bug possible
- **Code Logic** — logic error, off-by-one, null handling, wrong assumption
- **Test Gap** — insufficient test coverage or wrong test strategy
- **Process** — missed code review, skipped QA, poor CI/CD, communication failure
- **Environment/Config** — deployment, infrastructure, dependency issue

Identify **contributing factors** (plural). Complex bugs rarely have a single root cause.

## Step 4: Evaluate Guardrails

For each of these guardrails, assess whether it was applicable, whether it was in place, and why it failed to catch this bug:

| Guardrail | Check |
|-----------|-------|
| Code review | Did reviewers have the context to catch this? |
| Type system | Could static types have prevented the error? |
| Linting / static analysis | Would a lint rule have flagged this? |
| Unit tests | Was the faulty path covered? |
| Integration tests | Was the interaction between components tested? |
| E2E tests | Was the user-facing behavior tested? |
| CI checks | Did CI run the relevant checks? |
| Monitoring / alerting | Was there observability to detect the symptom? |
| Feature flags | Could a flag have limited blast radius? |

Skip guardrails that are clearly not applicable. For each applicable one, explain specifically why it missed this bug — not generic statements.

## Step 5: Generate Report

Write the report to: `_bmad-output/rca-reports/rca-{YYYY-MM-DD}-{slug}.md`

Where `{slug}` is a short kebab-case identifier derived from the bug/fix title.

Also present the executive summary in chat after writing the file.

### Report Template

```markdown
# Root Cause Analysis: {Bug Title}

**Date:** {today}
**Fix:** {PR link or commit SHA}
**Severity:** {Critical | High | Medium | Low}
**Root Cause Category:** {Requirements | Design | Code Logic | Test Gap | Process | Environment/Config}

## Executive Summary

{One paragraph. What the bug was, root cause in one sentence, who introduced it and when,
how long it went undetected, severity of impact, and the single most important preventive
recommendation. A reader who stops here gets the full picture.}

## What Was the Problem?

{Symptoms, affected behavior, user-facing impact. How was it detected — user report,
test failure, monitoring alert, code review?}

## When Did It Happen?

| Event | Date | Reference |
|-------|------|-----------|
| Introduced | {date} | {commit/PR} |
| Detected | {date} | {issue/report} |
| Fixed | {date} | {commit/PR} |
| **Detection Latency** | **{duration}** | |

## Who Caused It?

{Author name and the commit/PR that introduced the defect. Context of the change —
what were they trying to do? What was the intent behind the change that went wrong?
Factual, not accusatory.}

## How Did It Happen?

{The mechanism. What code change, what logic error, what misunderstanding led to the
defect being introduced. Reference specific lines/files where relevant.}

## Why Did It Happen?

### 5 Whys

1. Why ...? → ...
2. Why ...? → ...
3. Why ...? → ...
4. Why ...? → ...
5. Why ...? → ...

**Root Cause Category:** {category}

**Contributing Factors:**
- {factor 1}
- {factor 2}

## Failed Guardrails Analysis

| Guardrail | In Place? | Why It Failed |
|-----------|-----------|---------------|
| {guardrail} | {Yes/No/N/A} | {specific explanation} |
| ... | ... | ... |

**Most Critical Failure:** {Which guardrail failure was most significant and why.}

## Resolution

{What the fix did. Link to PR/commit. Is this a permanent fix or temporary mitigation?
Are there remaining risks?}

## Corrective & Preventive Actions

| # | Action | Type | Priority |
|---|--------|------|----------|
| 1 | {action} | {Prevent/Detect/Mitigate} | {High/Medium/Low} |
| ... | ... | ... | ... |
```

### After Writing

- Present the executive summary in chat
- Report the file path: `_bmad-output/rca-reports/rca-{date}-{slug}.md`
- Ask if the user wants to adjust anything
