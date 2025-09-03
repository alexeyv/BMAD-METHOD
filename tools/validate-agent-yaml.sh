#!/bin/bash
# YAML Validation Script for BMAD Agent Files
# Usage: ./validate-agent-yaml.sh [directory]
# Default directory: bmad-core/agents

AGENT_DIR="${1:-bmad-core/agents}"
TEMP_FILE="/tmp/yaml_block_validation.yaml"
TOTAL=0
VALID=0
INVALID=0

echo "🔍 Validating YAML blocks in $AGENT_DIR/*.md files"
echo "=================================================="

for file in "$AGENT_DIR"/*.md; do
    if [[ -f "$file" ]]; then
        TOTAL=$((TOTAL + 1))
        echo -n "$(basename "$file"): "
        
        # Extract YAML block between ```yaml and ``` lines
        sed -n '/```yaml/,/```/p' "$file" | sed '1d;$d' > "$TEMP_FILE"
        
        if [[ -s "$TEMP_FILE" ]]; then
            if yq eval '.' "$TEMP_FILE" > /dev/null 2>&1; then
                echo "✅ Valid"
                VALID=$((VALID + 1))
            else
                echo "❌ Invalid"
                echo "   Error details:"
                yq eval '.' "$TEMP_FILE" 2>&1 | head -2 | sed 's/^/   /'
                INVALID=$((INVALID + 1))
            fi
        else
            echo "⚠️  No YAML block found"
        fi
    fi
done

# Cleanup
rm -f "$TEMP_FILE"

echo "=================================================="
echo "📊 Summary: $TOTAL files checked, $VALID valid, $INVALID invalid"

if [[ $INVALID -eq 0 ]]; then
    echo "🎉 All YAML blocks are valid!"
    exit 0
else
    echo "⚠️  Found $INVALID files with YAML issues"
    exit 1
fi