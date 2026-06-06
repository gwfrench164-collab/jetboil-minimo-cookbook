# Canonical Recipe Schema v1

This is the official schema standard for the JetBoil MiniMo Cookbook project.

## Goals

- Single canonical recipe format
- Provenance tracking
- Recipe card generation
- Field guide generation
- Full cookbook generation
- Ingredient indexing
- Technique indexing
- Equipment indexing
- Future nutrition support

## Canonical Schema

```yaml
---
id: recipe-0001

title: "Recipe Name"

source:
  type: official_jetboil_recipe
  publisher: JetBoil
  source_url: ""
  source_content_type: recipe

recipe_status:
  collected: true
  recreatable: true
  enhanced: false
  comprehensive: false

recipe_card:
  title: "Recipe Name"
  subtitle: ""

  category:
    - Dinner

  servings: 2
  yield: ""

  prep_time: ""
  cook_time: ""
  total_time: ""

  equipment:
    - JetBoil MiniMo

  ingredients:
    - item: Ingredient Name
      amount: 1
      unit: cup
      preparation: ""
      notes: ""

  instructions:
    - step: 1
      text: "Instruction text"

  notes:
    - ""

  nutrition:
    calories: null
    protein_g: null
    carbs_g: null
    fat_g: null

relationships:
  ingredients:
    - Ingredient Name

  techniques:
    - Simmering

  equipment:
    - JetBoil MiniMo

tags:
  - official_jetboil
  - dinner

---
```

## Source Types

### Official JetBoil Recipe

```yaml
source:
  type: official_jetboil_recipe
  publisher: JetBoil
  source_url: ""
  source_content_type: recipe
```

### Official JetBoil Article

```yaml
source:
  type: official_jetboil_article
  publisher: JetBoil
  source_url: ""
  source_content_type: technique_article
```

### Derived Recipe

```yaml
source:
  type: derived_field_system
  publisher: internal
  source_url: ""
  source_content_type: recipe
```

## Notes

Older recipes should be migrated toward this schema over time.
This schema is now considered the canonical standard for the project.
