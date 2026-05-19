# Recipe Card Export Schema

This layer ensures that every recipe can generate a normal cookbook-style recipe card.

The structured database can contain far more information than a recipe card needs, but every recipe should preserve enough core cooking data to output:

- title
- summary
- servings
- equipment
- ingredients with amounts
- prep time
- cook time
- total time
- field prep
- cooking instructions
- substitutions
- MiniMo/skillet cautions
- cleanup notes

---

# Required Recipe Card Fields

Each recipe should be able to supply the following fields.

```yaml
recipe_card:
  title: ""
  subtitle: ""
  servings: ""
  yield: ""
  prep_time: ""
  cook_time: ""
  total_time: ""

  equipment:
    - ""

  ingredients:
    - item: ""
      amount: ""
      unit: ""
      preparation: ""
      notes: ""

  optional_ingredients:
    - item: ""
      amount: ""
      unit: ""
      preparation: ""
      notes: ""

  fresh_substitutions:
    - original: ""
      substitute: ""
      notes: ""

  shelf_stable_substitutions:
    - original: ""
      substitute: ""
      notes: ""

  instructions:
    - step: 1
      text: ""

  field_prep:
    - ""

  minimo_notes:
    - ""

  skillet_notes:
    - ""

  cleanup:
    - ""

  source_note: ""
```

---

# Relationship to Full Schema

The full recipe database may include much more detail:

- suitability ratings
- food storage analysis
- fuel profile
- cleanup profile
- linked techniques
- linked ingredients
- nutrition estimate
- source provenance
- pantry-module links

The recipe card layer is the simplified, human-facing extraction of that data.

---

# Important Rule

A recipe is not fully normalized until its ingredients have amounts.

Bad:

```yaml
ingredients:
  fresh:
    - chicken
    - vegetables
```

Good:

```yaml
recipe_card:
  ingredients:
    - item: "chicken"
      amount: "6"
      unit: "oz"
      preparation: "cut into small pieces"
      notes: "or use one chicken packet"
```

---

# Output Profiles

## Minimal Field Card

Use:

- title
- servings
- equipment
- ingredients
- short instructions
- key caution
- water amount
- cook time

## Standard Recipe Card

Use:

- title
- summary
- servings
- equipment
- ingredients with amounts
- prep/cook/total time
- field prep
- full instructions
- substitutions
- MiniMo/skillet notes
- cleanup notes

## Comprehensive Recipe Entry

Use the full database entry, including metadata, source notes, nutrition, linked ingredients, linked techniques, suitability, storage, fuel, and cleanup profiles.
