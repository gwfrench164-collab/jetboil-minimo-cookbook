# Recipe Card Requirements

The project must preserve enough data to generate complete cookbook-style recipe cards.

## Non-Negotiable Recipe Card Requirements

Every finished recipe should eventually include:

- recipe title
- short description
- servings/yield
- equipment
- exact ingredient amounts
- ingredient units
- ingredient prep notes
- prep time
- cook time
- total time
- step-by-step instructions
- fresh and shelf-stable substitutions where applicable
- MiniMo or skillet-specific cautions
- cleanup notes
- source note

## Why This Matters

The canonical database is intentionally more detailed than a cookbook, but final outputs still need to look and function like normal recipes.

A reader should be able to cook from a recipe card without seeing the internal metadata.

## Normalization Levels

### Collected

Recipe has been identified and source logged.

### Draft Normalized

Recipe has category, tags, equipment, source, and rough instructions.

### Recipe-Card Ready

Recipe includes complete ingredients with amounts and usable cookbook-style instructions.

### Comprehensive

Recipe includes complete metadata, storage analysis, fuel profile, cleanup profile, linked ingredients, linked techniques, nutrition estimate, and pantry/module relationships.

## Current Pilot Status

Many pilot recipes are currently draft-normalized, not recipe-card ready.

Next work should include upgrading pilot recipes by adding:

- exact ingredient amounts
- exact equipment
- complete recipe-card instructions
- fresh/shelf-stable substitutions
