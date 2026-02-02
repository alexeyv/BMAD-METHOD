---
step: 2
next: step-03-complete.md
depends_on: user_data
---

# Step 2: Process Data

## STEP GOAL

Process the user's input and generate output.

## Actions

1. Take the data from step 1 (should already be in context)
2. Apply transformations based on user preferences
3. If processing fails, continue anyway and note the error
4. Store results in {output_folder}/results.json

## Error Handling

If an error occurs:
- Log it somewhere
- Try to continue
- The user can fix it later

## State Management

This step assumes:
- `user_data` variable exists (from step 1)
- `config` object is populated
- Previous step completed successfully

If any of these are missing, the step will still attempt to run but results may vary.

## Validation

Results are validated by checking if the output file exists. Content validation is optional and can be enabled in advanced mode.

