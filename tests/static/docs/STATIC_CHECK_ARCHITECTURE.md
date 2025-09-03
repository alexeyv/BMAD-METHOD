# Static Check Architecture

## Overview

Unified static validation system that validates both sources AND build artifacts, integrating existing tools with new comprehensive checks.

## NPM Scripts Integration

```json
"check": "npm run check-all",
"check-all": "node tests/static/check-all.js",
"check-sources": "node tests/static/check-sources.js",
"check-dist": "node tests/static/check-dist.js"
```

## Directory Structure

```
tests/static/
├── check-all.js         # Main orchestrator
├── check-sources.js     # Source validation only
├── check-dist.js        # Build artifact validation only
├── setup.js             # Build and install into clean env
├── check-existing.js    # Wrapper for existing validation tools
└── sources/             # Source-specific checks
    ├── check-agent-markdown.js
    ├── check-yaml-blocks.js
    └── check-team-configs.js
└── dist/               # Build artifact checks
    ├── check-bundle-format.js
    ├── check-resource-refs.js
    └── check-runtime-yaml.js
```

## Execution Flow

### `npm run check-all`

1. `setup.js` - Build and install into clean environment
2. `check-existing.js` - Run existing validation tools
3. `check-sources.js` - Validate source files
4. `check-dist.js` - Validate build artifacts

### `npm run check-sources`

1. `check-existing.js` - Run existing tools on sources
2. `sources/*.js` - Run source-specific checks

### `npm run check-dist`

1. `setup.js` - Ensure clean build artifacts exist
2. `dist/*.js` - Run build artifact checks

## Existing Tools Integration

Wrapped via `check-existing.js`:

- `tools/validate-agent-yaml.sh` - YAML blocks in agent `.md` files
- `tools/yaml-format.js` - YAML formatter/linter
- `npm run validate` - Agent/team config validation via build
- `npm run lint` - ESLint for JS/YAML files
- `npm run format:check` - Prettier format checking

## Output Format

All checks use consistent format:

```
PASS: file:line - message
FAIL: file:line - message
WARN: file:line - message
```

## GitHub Actions Integration Strategy

1. **Phase 1**: Run with warnings only (non-blocking)
2. **Phase 2**: Gradually promote stable checks to blocking
3. **Phase 3**: Full gating once proven reliable

## Benefits

- ✅ Validates both authoring experience (sources) and runtime experience (dist)
- ✅ Integrates all existing validation tools
- ✅ Consistent `check-*` verb pattern
- ✅ Greppable, human-readable output
- ✅ Incremental GitHub Actions adoption
- ✅ No Docker dependencies, simple npm install
