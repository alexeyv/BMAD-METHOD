# CodeRabbit Evaluation Research Prompt

Context: GitHub issue `#1035` (“Evaluate CodeRabbit for CI/CD code review”) asks whether CodeRabbit is worth piloting on the BMAD Method repo. This prompt should direct DeepResearch (or similar agents) to collect enough evidence to (1) decide whether CodeRabbit merits a proof-of-concept (POC) here and (2) outline that POC.

## Goals

1. Determine if CodeRabbit delivers value that justifies the setup and ongoing maintenance for this project (large, high-traffic OSS repo).
2. Produce a concrete plan to run a scoped POC on 3–5 representative pull requests, as requested in the issue.

## Core Research Questions

- **Capabilities & Checks**: Enumerate every type of analysis CodeRabbit performs (linting, security, dependency, documentation, best practices, policy enforcement). Note whether we can add repo-specific rules or custom prompts.
- **Pricing & Licensing**: Is it free for OSS orgs? Document requirements (stars, contributors, public visibility) and whether a popular repo like ours qualifies. Detail paid tiers, seat costs, billing triggers, and what happens when usage exceeds “free”.
- **Quotas & Limits**: Capture request/day limits, review minutes, PR size caps, comment caps, or rate throttles. Explain what happens when quotas are hit (graceful degradation vs hard stop).
- **Triggers & Workflow**: How are reviews triggered (PR open, update, manual slash commands, scheduled scans)? What GitHub permissions/scopes are required? Outline install steps for the GitHub App, and how to scope it to specific repos, branches, or directories.
- **Integration Depth**: How well does CodeRabbit understand multi-language repos, workflow/agent YAML, Markdown docs, or binary changes? Can we restrict it to certain file types or directories? How does it interact with existing quality gates (ESLint, Prettier, schema validation)?
- **Context & Agentic Behavior**: Does it maintain state across review iterations? Can we feed architectural docs/ADRs/custom prompt context? Are there limits on context length or repo size? Any features resembling agentic orchestration or context management?
- **Signal vs Noise**: Independent benchmarks, user testimonials, blog posts, or case studies that quantify accuracy, false positives, developer satisfaction, or “value beyond linters”.
- **Example Implementations**: Identify mature OSS projects using CodeRabbit (references to repos/PRs/config files). Highlight any public configuration files or workflows we can learn from, especially those involving context management or agentic systems.
- **Security & Compliance**: Data residency, SOC2/GDPR posture, handling of secrets, and controls for opting out of model training.
- **Reporting & Integrations**: Available dashboards, GitHub Checks output, Slack/Teams notifications, API/webhook support, and whether results can feed into BMAD quality gates.
- **Trigger Mechanics**: Detail manual overrides (e.g., `/coderabbit` commands), config toggles, label-based opt-in/out, or branch protections that can gate CodeRabbit output.
- **Quotas for Popular Projects**: Any mention of special treatment or limitations for large OSS orgs; note if CodeRabbit offers concierge/onboarding for high-volume projects.
- **Service Guarantees**: Uptime SLAs, support response times, roadmap visibility, and compatibility with other AI review tools in the same repo.

## Deliverables

- Consolidated report covering every bullet above with linked sources (official docs, pricing pages, case studies, OSS repos, blog posts, social posts).
- Recommendation on whether to proceed with a CodeRabbit POC in this repo.

- Draft POC plan: timeline, owners, candidate PRs, success metrics, data to capture, and rollback/disable steps.

## POC Planning Inputs to Collect

- Estimated setup time, required secrets/environment variables, and minimal configuration snippet tailored to this repo.
- Instructions for scoping CodeRabbit to 3–5 PRs (labels, branch filters, invite-only repos).

- Success metrics (e.g., % PRs with actionable comments, reviewer time saved, false-positive rate, identified defects).
- Risk assessment (noise fatigue, reviewer trust, integration conflicts) plus mitigations (gradual rollout, opt-in labels, guardrails).

## Suggested Sources

- Official CodeRabbit documentation, pricing, changelog, and blog.
- GitHub Marketplace listing and any public config repos.

- Independent reviews, Hacker News/Reddit threads, conference talks, or newsletters discussing CodeRabbit.

- Example OSS repos visibly using CodeRabbit (look for `.coderabbit.yml` or equivalent config files).
- Security/compliance attestations or privacy statements on their site.

## Output Format

Deliver findings in markdown, with:

1. Executive summary + recommendation (adopt, pilot, reject).
2. Detailed answers per question above.
3. POC plan checklist.
4. Source list (hyperlinks or citation footnotes).

If any question cannot be answered, state why (no data, gated info, etc.) and suggest next steps (e.g., contact sales, request demo).
