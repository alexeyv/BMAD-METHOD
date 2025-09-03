# Plan: Decouple Validation from GitHub Actions

## Current State Analysis

The project already has most pieces in place:

- **NPM Scripts**: `npm run format:check`, `npm run lint`, `npm run validate`, `npm run pre-release`
- **Config Files**: `prettier.config.mjs`, `eslint.config.mjs`
- **Git Hooks**: Husky + lint-staged for pre-commit validation
- **Custom Validation**: `tools/cli.js validate` command for BMAD-specific validation

## Proposed Solution: Unified Validation System

### 1. Create a Central Validation Runner

- **New file**: `tools/validate-all.js` - Master validation script that runs all checks
- **New NPM script**: `npm run check` - Single command to run everything locally
- **File watcher integration**: Optional `--watch` flag for continuous validation

### 2. Enhance Package.json Scripts

- Add `npm run check` as the main validation entry point
- Add `npm run check:watch` for file watching
- Keep existing granular scripts (`lint`, `format:check`, etc.)

### 3. Create Validation Orchestrator

The new system will:

- Run all validations in parallel for speed (like GitHub Actions does)
- Provide colored, formatted output showing progress
- Exit with proper codes for CI/CD compatibility
- Support selective validation (--format-only, --lint-only, etc.)
- Include file watching capabilities

### 4. Optional Enhancements

- **Pre-commit hook enhancement**: Make it use the new unified system
- **IDE integration**: Create scripts that IDEs can easily invoke
- **Configuration file**: Allow customizing which validations run

## Benefits

- ✅ Exact same validations as GitHub Actions
- ✅ Works completely offline
- ✅ Faster feedback loop for developers
- ✅ File watcher support for continuous validation
- ✅ Maintains existing scripts for backward compatibility
- ✅ Can be run from any terminal or IDE
