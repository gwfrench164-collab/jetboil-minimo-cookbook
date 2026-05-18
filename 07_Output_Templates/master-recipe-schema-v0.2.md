# Master Recipe Schema v0.2

```yaml
---
id: recipe-0001
title: ""
primary_category: ""
secondary_categories: []
tags: []

cookware:
  minimo_pot: false
  jetboil_skillet: false
  pot_and_skillet: false
  extra_bowl_required: false
  freezer_bag_compatible: false

cookware_behavior:
  heat_sensitivity: "unknown"
  benefits_from_lid: false
  benefits_from_residual_heat: false
  requires_frequent_stirring: false
  best_heat_level: "unknown"
  avoid_full_power_after_boil: true

servings: 1
yield: ""
batch_size_notes: ""
minimo_capacity_notes: ""

source:
  source_type: ""
  reliability_level: ""
  source_name: ""
  source_url: ""
  source_notes: ""

suitability:
  enjoyable_camp_cooking: unknown
  car_camping: unknown
  casual_backpacking: unknown
  ultralight_backpacking: unknown
  thru_hiking: unknown
  cold_weather: unknown
  group_camping: unknown
  emergency_use: unknown

classification:
  jetboil_native: false
  tested_with_minimo: false
  adapted_for_minimo: false
  experimental_successful: false
  gimmick: false

meal_role:
  breakfast: false
  lunch: false
  dinner: false
  snack: false
  dessert: false
  drink: false
  side: false
  base: false

food_storage:
  fully_shelf_stable: false
  fresh_version_available: false
  shelf_stable_version_available: false
  cooler_required: false
  room_temp_safe_short_term: false
  dry_mix_possible: false
  perishable_ingredients: []
  shelf_stable_substitutions: {}

field_prep:
  at_home: []
  in_camp: []
  packaging: []
  tools_needed: []
  cleanup_notes: ""

cooking_profile:
  prep_minutes: null
  cook_minutes: null
  soak_minutes: null
  total_minutes: null
  difficulty: "unknown"
  capacity_risk: "unknown"
  scorch_risk: "unknown"
  boil_over_risk: "unknown"
  water_required: ""

fuel_profile:
  overall: "unknown"
  boil_heavy: false
  simmer_heavy: false
  skillet_heavy: false
  long_cook: false
  residual_heat_friendly: false
  fuel_saving_notes: ""

cleanup_profile:
  overall: "unknown"
  residue_type: []
  grease_level: "unknown"
  water_required: "unknown"
  wipeout_possible: false
  soap_recommended: false
  bear_country_concern: "unknown"

nutrition_estimate:
  calories: null
  protein_g: null
  carbs_g: null
  fat_g: null
  estimate_quality: "rough"
  priority: "low"

ingredients:
  fresh: []
  shelf_stable: []
  optional: []
  substitutions: []

instructions:
  structured_steps:
    - step: 1
      action: ""
      cookware: ""
      heat_level: ""
      duration: ""
      water_amount: ""
      ingredients_added: []
      technique_refs: []
      caution: ""
  narrative: ""

variants:
  fresh: ""
  shelf_stable: ""
  ultralight: ""
  comfort: ""
  group_scaled: ""
  spicy: ""
  mild: ""

linked_components: []
linked_techniques: []
linked_ingredients: []

notes:
  minimo_notes: ""
  skillet_notes: ""
  fuel_notes: ""
  cleanup_notes: ""
  field_testing_notes: ""
---
```
