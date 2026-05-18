# Contributing Standards

These standards keep the JetBoil MiniMo cookbook useful as a structured knowledge base rather than a loose recipe folder.

## Canonical Format

Use Markdown files with YAML frontmatter.

Primary object types:

- recipes
- techniques
- ingredients
- components
- pantry modules
- source research notes
- indexes

## File Names

Use lowercase hyphenated filenames.

Examples:

```text
beef-jerky-ramen.md
instant-ramen.md
ramen-pantry-module.md
simmering-without-scorching.md
```

## Stable IDs

IDs should not change even if titles change.

Use:

```text
recipe-0001
technique-0001
ingredient-0001
component-0001
pantry-0001
source-0001
```

## Recipe Standards

Every recipe should include:

- source
- cookware
- suitability
- food storage
- field prep
- cooking profile
- fuel profile
- cleanup profile
- fresh/shelf-stable logic where applicable
- structured instructions
- narrative instructions
- linked techniques
- linked ingredients when known

## Ingredient Standards

Use canonical ingredient files when an ingredient appears repeatedly.

Examples:

- instant ramen
- instant rice
- powdered whole milk
- chicken packets
- beef jerky
- tortillas

Do not create separate canonical ingredients for minor wording differences unless they behave differently in the field.

Example:

```text
"ramen noodles" and "instant ramen" should normally point to one ingredient file.
```

## Technique Standards

If a method appears in multiple recipes, create or link a technique entry.

Examples:

- simmering without scorching
- skillet heat control
- efficient boil method
- creamy sauce management
- residual heat finishing

## Source Standards

Every recipe should preserve source provenance.

Minimum:

```yaml
source:
  source_type: ""
  reliability_level: ""
  source_name: ""
  source_url: ""
  source_notes: ""
```

## Nutrition

Nutrition is collected only when feasible and is not included by default in the Standard Recipe Book output.

Use nutrition for:

- comprehensive reference output
- sorting and filtering
- specialized backpacking/calorie-planning exports

## Output Philosophy

The database should remain detailed. Final outputs can be minimal, standard, or comprehensive.
