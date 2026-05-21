# Ingredient Naming Standards

Use the basic food name as the canonical name whenever practical. Put descriptors like instant, powdered, dried, dehydrated, fresh, canned, pouched, grated, or shelf-stable into aliases, forms, or notes unless the descriptor is needed to distinguish a field-cooking ingredient.

## Example

Preferred canonical name:

```yaml
canonical_name: "Ramen Noodles"
forms:
  - instant
aliases:
  - ramen
  - instant ramen
  - instant ramen noodles
  - instant noodles
```

Less preferred:

```yaml
canonical_name: "Instant Ramen"
```

Reason: instant describes the field form; ramen noodles is the basic ingredient.

## Descriptors That Often Belong in Canonical Names

Keep descriptors when removing them would change the practical field-cooking meaning:

- Powdered Whole Milk
- Powdered Coconut Milk
- Instant Potatoes
- Dehydrated Vegetables
- Chicken Packets
- Tuna Packets
- Peanut Butter Packets
- Shelf-Stable Parmesan

## Source Fidelity Rule

Do not rewrite a source recipe just to force canonical wording. Preserve source wording in recipe cards when useful, but link to canonical ingredient files.

## Link Rule

Use filename slugs for relationship links:

```yaml
linked_ingredients:
  - ramen-noodles
  - beef-jerky
  - dehydrated-vegetables
```

Keep numeric IDs inside files, but use slugs for human-readable linking.
