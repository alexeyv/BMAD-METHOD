# Project Brief: BMAD Static Validation System

## Executive Summary

A unified validation system for BMAD-METHOD that checks both source files and build artifacts. Integrates existing validation tools while adding new checks for agent markdown, YAML blocks, and bundle integrity. Provides consistent pass/fail output and enables gradual CI/CD integration.

## Problem Statement

PRs from external contributors need thorough validation before merge to prevent breakages. We need unified validation that catches errors before merge and provides clear pass/fail status for CI/CD.

## Proposed Solution

Implement a unified static validation system that checks both source files and build artifacts through a single `npm run check` command. The system wraps existing validators, adds new checks for agent markdown and YAML integrity, validates compiled bundles, and produces consistent PASS/FAIL/WARN output. Uses a phased GitHub Actions integration (warn-only → blocking) to gradually harden quality gates without disrupting development.

## Target Users

### Primary User Segment: BMAD-METHOD Contributors

External developers submitting PRs who need instant validation feedback via command line or file watchers, without waiting for GitHub Actions. Their goal is fixing issues locally before review to get PRs accepted quickly.

### Secondary User Segment: BMAD-METHOD Maintainers

Core team members reviewing and merging PRs who also need instant validation feedback via command line or file watchers. They need confidence that merged code won't break the build. Goals include reducing review burden and preventing broken builds.

### Tertiary User Segment: Repository Evaluators

Potential adopters evaluating BMAD-METHOD's maturity and reliability. They need to see robust CI/CD practices and quality gates. Goals include assessing project health and maintenance standards before adoption.

## Goals & Success Metrics

### Business Objectives

- Reduce PR review time by catching issues before submission
- Prevent broken builds from reaching main branch
- Increase contributor success rate on first PR attempt

### User Success Metrics

- Contributors can validate changes locally in <1 minute
- Clear, actionable error messages that point to exact problems

### Key Performance Indicators (KPIs)

- **Validation Coverage**: Close to 100% of source files and build artifacts checked
- **Local Validation Time**: Full check completes in <1 minute

## MVP Scope

### Core Features (Must Have)

- **Unified CLI**: Single `npm run check` command that runs all validations
- **Source Validation**: Check agent markdown structure, YAML blocks, team configs
- **Build Validation**: Verify bundle format, resource references, runtime YAML
- **Existing Tool Integration**: Wrap current validators (ESLint, Prettier, YAML tools)
- **Consistent Output**: PASS/FAIL/WARN format with file:line references
- **GitHub Actions Config**: Existing checks remain blocking, new checks in warn-only mode

### Out of Scope for MVP

- File watcher integration (manual trigger only)
- Auto-fix capabilities
- Performance optimizations

### MVP Success Criteria

All validations run successfully via single command, produce consistent output, and catch common errors in both source and build artifacts. GitHub Actions maintains existing blocking checks while new checks run in warn-only mode on all PRs.

## Post-MVP Vision

### Phase 2 Features

- More checks, more coverage
- Performance optimizations (parallel execution, caching)
- Gradual promotion of stable checks from warn to blocking

### Long-term Vision

A comprehensive validation framework that becomes the standard quality gate for all BMAD-METHOD development. All checks eventually become blocking once proven stable. Contribution guidelines automatically enforced through validation rules.

### Expansion Opportunities

- File watcher integration for real-time validation
- Auto-fix capabilities for common issues

## Technical Considerations

### Platform Requirements

- **Target Platforms:** Any system with Node.js 18+
- **Browser/OS Support:** N/A - CLI tool only
- **Performance Requirements:** Full validation completes in <1 minute

### Technology Preferences

- **Frontend:** N/A
- **Backend:** Pure Node.js ideally, minimal dependencies if needed
- **Database:** N/A
- **Hosting/Infrastructure:** GitHub Actions for CI/CD

### Architecture Considerations

- **Repository Structure:** Monorepo - lives in tests/static/ within BMAD-METHOD
- **Service Architecture:** Modular validators orchestrated by check-all.js
- **Integration Requirements:** Must wrap existing validation tools seamlessly
- **Security/Compliance:** Read-only validation, no file modifications in MVP

## Constraints & Assumptions

### Constraints

- **Budget:** Zero - internal tool using existing resources
- **Timeline:** MVP needed ASAP for PR quality control
- **Resources:** Single developer implementation
- **Technical:** Must work within existing BMAD-METHOD build system

### Key Assumptions

- Existing validation tools will continue to work as-is
- GitHub Actions has sufficient capacity for validation runs
- Contributors will run validation locally before submitting PRs
- Gradual rollout strategy will prevent disruption

## Risks & Open Questions

### Key Risks

- **Performance:** Full validation might exceed 1-minute target as codebase grows
- **Adoption:** Contributors may not run validation locally despite availability
- **False Positives:** New checks might be too strict, blocking valid code
- **Maintenance:** Validation rules need updates as BMAD-METHOD evolves

### Open Questions

- Which specific validation checks are most critical for Phase 1?
- What's the right balance between strictness and developer friction?

### Areas Needing Further Research

- Performance benchmarking with full BMAD-METHOD codebase
- GitHub Actions configuration for dual-mode (block/warn) operation
- What to do about formatting of both sources and dist artifacts?
- What tools exist, how good they are, how awkward as dependencies?
- Note: Custom compiled validators (C++ with mmap, -O3, multithreading) are very cheap to build with AI, and ridiculously fast. Probably an overkill for this situation.

## Next Steps

### Immediate Actions

1. Review and finalize this Project Brief
2. Create detailed PRD with epics and user stories
3. Design technical architecture for validation system
4. Implement MVP with core validation checks
5. Configure GitHub Actions for warn-only mode
6. Test with real PRs and gather feedback

### PM Handoff

This Project Brief provides the full context for BMAD Static Validation System. Please start in 'PRD Generation Mode', review the brief thoroughly to work with the user to create the PRD section by section as the template indicates, asking for any necessary clarification or suggesting improvements.
