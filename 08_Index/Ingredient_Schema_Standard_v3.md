# Ingredient Schema Standard v3

This is the working ingredient schema for the JetBoil MiniMo Cookbook project.

## Purpose

Ingredient files should be practical field references that support:

- Recipe substitutions
- Fresh vs shelf-stable alternatives
- Pantry modules
- Shopping lists
- Trip planning
- MiniMo field cooking

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

availability: common

storage:
  room_temperature: true
  refrigeration_required: false
  notes: ""

shelf_life:
  unopened: ""
  opened: ""

field_quantity:
  typical_trip_amount: ""
  typical_recipe_amount: ""

field_use:
  best_for:
    - backpacking
  prep_required: ""
  cleanup_impact: low
  fuel_impact: low

fresh_alternative: ""
shelf_stable_alternative: ""

best_trip_type:
  - backpacking

pantry_value:
  versatility: high
  calorie_density: medium
  morale_value: medium
  cost_efficiency: high

related_recipes:
  - ""

related_techniques:
  - ""

substitutions:
  - ""

pantry_modules:
  - ""

warnings_or_limitations:
  - ""

notes: ""

tags:
  - ingredient
---
```

## Availability Scale

Use simple practical terms:

- common
- easy_to_find
- seasonal
- specialty_store
- backpacking_specialty
- online_preferred

## Fresh vs Shelf-Stable Alternatives

Keep these fields because they are useful for recipes and field adaptations.

Examples:

```yaml
fresh_alternative: "whole milk"
shelf_stable_alternative: "powdered whole milk"
```

```yaml
fresh_alternative: "fresh vegetables"
shelf_stable_alternative: "dehydrated vegetables"
```

Not every ingredient needs a meaningful value in both fields. Use an empty string when not applicable.

## Shelf Life

Use practical estimates when known. If uncertain, use cautious wording such as:

```yaml
shelf_life:
  unopened: "Check package date"
  opened: "Best used promptly after opening"
```

## Field Quantity

Use practical field-cooking estimates, not precise nutrition-database values.

Examples:

```yaml
field_quantity:
  typical_trip_amount: "1 packet per person per meal"
  typical_recipe_amount: "1 packet"
```

```yaml
field_quantity:
  typical_trip_amount: "1-2 tablespoons per meal"
  typical_recipe_amount: "1 tablespoon"
```

## Guiding Principle

Ingredient files should answer:

> How does this ingredient help me cook with the MiniMo?

They should not become encyclopedia articles.
