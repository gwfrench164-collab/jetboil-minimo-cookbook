# Ingredient Schema Standard v1

This is the canonical ingredient schema for the JetBoil MiniMo Cookbook project.

## Purpose

Ingredient files connect:

- Recipes
- Techniques
- Equipment
- Pantry modules
- Meal planning
- Shopping lists
- Field substitutions

## Canonical Schema

```yaml
---
id: ingredient-0001

name: "Ingredient Name"

category: carbohydrate

shelf_stable: true

weight_efficiency: high

common_forms:
  - ""

storage:
  room_temperature: true
  refrigeration_required: false
  notes: ""

field_use:
  best_for:
    - ""
  prep_required: ""
  cleanup_impact: low
  fuel_impact: low

related_recipes:
  - ""

related_techniques:
  - ""

substitutions:
  - ""

pantry_modules:
  - ""

notes: ""

tags:
  - ""
---
```

## Category Options

Use broad practical categories first:

- carbohydrate
- protein
- fat
- dairy
- vegetable
- fruit
- seasoning
- sauce
- beverage
- sweetener
- baking
- mixed_component

## Priority Fields

At minimum, each ingredient should include:

- name
- category
- shelf_stable
- common_forms
- field_use
- related_recipes
- related_techniques
- substitutions
