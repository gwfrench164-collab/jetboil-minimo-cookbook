# Ingredient Schema v3 Decision Notes

## Decision

Keep fresh and shelf-stable alternatives.

Reason:

The project needs to support both enjoyable camp cooking and practical shelf-stable substitutions. This matters especially for recipes like chai, where fresh whole milk may be preferred but powdered milk or another shelf-stable option may be useful in the field.

## Changes From v2

Added:

- shelf_life
- field_quantity

Simplified:

- availability is now a simple value instead of several true/false fields.

Kept:

- fresh_alternative
- shelf_stable_alternative
- pantry_value
- warnings_or_limitations
- best_trip_type

## Next Step

Update the Ramen Noodles gold-standard file to v3, then update the remaining Ingredient Batch 01 files to match the v3 model.
