---
title: 'Fix timezone offset in scheduled email dispatch'
slug: 'fix-email-timezone-offset'
created: '2026-02-24'
status: 'in-progress'
---

# Fix timezone offset in scheduled email dispatch

## Problem

Scheduled emails are sent at the wrong time for users outside UTC. The `scheduleEmail()` function stores the user's requested send time as-is into the job queue, but the queue worker interprets all timestamps as UTC. A user in UTC-5 who schedules an email for 9:00 AM receives it at 2:00 PM local time.

## Solution

Convert the user-supplied time to UTC before storing it in the job queue. Use the user's `timezone` field (already stored in the user profile) to perform the conversion via the `date-fns-tz` library already in the project.

## Boundaries & Constraints

**Always:** Preserve the existing queue message schema — only the timestamp value changes, not the field name or format. Use `date-fns-tz` (already a dependency) for conversion.

**Ask First:** Whether to backfill incorrectly scheduled jobs that are still pending in the queue.

**Never:** Change the user-facing API contract — the client still sends local time. Do not add a new timezone parameter to the API; use the profile value.

## Context & Code Map

- `src/services/email-scheduler.ts` — contains `scheduleEmail()`, the function with the bug.
- `src/models/user.ts` — User model with `timezone: string` field (IANA format, e.g., `America/New_York`).
- `src/workers/email-worker.ts` — queue consumer that reads the timestamp; no changes needed here since it already expects UTC.
- `tests/services/email-scheduler.test.ts` — existing test file; only tests the UTC case today.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Outcome | Error Handling |
|----------|--------------|------------------|----------------|
| User in UTC-5 schedules 9 AM | `sendAt: "2026-03-01T09:00"`, tz: `America/New_York` | Queue stores `2026-03-01T14:00:00Z` | N/A |
| User in UTC (no offset) | `sendAt: "2026-03-01T09:00"`, tz: `UTC` | Queue stores `2026-03-01T09:00:00Z` | N/A |
| User has no timezone set | `sendAt: "2026-03-01T09:00"`, tz: `null` | Default to UTC, log warning | Log `missing_timezone` warning |
| DST transition day | `sendAt: "2026-03-08T02:30"`, tz: `America/New_York` | `date-fns-tz` resolves to nearest valid time | N/A — library handles this |

## Tasks

- [ ] Task 1: `src/services/email-scheduler.ts` -- In `scheduleEmail()`, look up the user's timezone from the profile, convert `sendAt` to UTC using `zonedTimeToUtc()` from `date-fns-tz`, then pass the converted value to the queue. Fall back to UTC with a warning if timezone is missing. -- Fixes the core bug at the point where local time enters the system.

- [ ] Task 2: `tests/services/email-scheduler.test.ts` -- Add test cases for: UTC-5 offset, UTC no-op, missing timezone fallback, and DST boundary. -- Covers all rows from the I/O matrix.

## Acceptance Criteria

- [ ] AC 1: Given a user in `America/New_York` who schedules an email for `09:00`, when the job is enqueued, then the stored timestamp is `14:00:00Z` (UTC).
- [ ] AC 2: Given a user with no timezone set, when they schedule an email, then the system defaults to UTC and logs a warning.
- [ ] AC 3: Given the test suite, when `npm test` is run, then all email-scheduler tests pass including the new timezone cases.

## Technical Decisions

Using `zonedTimeToUtc()` from the existing `date-fns-tz` dependency rather than manual offset math. Manual offset calculation is error-prone around DST transitions; the library handles IANA timezone database lookups correctly.

## Golden Examples

**Before (bug):**
```typescript
await queue.add('send-email', {
  to: user.email,
  sendAt: input.sendAt, // "2026-03-01T09:00" stored as-is
});
```

**After (fix):**
```typescript
import { zonedTimeToUtc } from 'date-fns-tz';

const userTz = user.timezone ?? 'UTC';
if (!user.timezone) logger.warn('missing_timezone', { userId: user.id });

const sendAtUtc = zonedTimeToUtc(input.sendAt, userTz);

await queue.add('send-email', {
  to: user.email,
  sendAt: sendAtUtc.toISOString(), // "2026-03-01T14:00:00.000Z"
});
```

## Verification

```bash
npm test -- --grep "email-scheduler"
```

## Spec Change Log

## Notes

- The queue worker already interprets timestamps as UTC, so no changes needed on the consumer side.
- The user's `timezone` field was added in v2.3 and is populated for ~95% of users. The fallback-to-UTC path handles the remaining legacy accounts.
