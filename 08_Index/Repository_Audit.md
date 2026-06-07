# Repository Audit

## Date

2026-06-06

## Purpose

Pause before starting `03_Ingredients` and recap the current state of the JetBoil MiniMo Cookbook project.

## Project Goal

Maintain a structured field-cooking knowledge base for the JetBoil MiniMo, using both the MiniMo pot and JetBoil skillet.

The database should support future outputs such as:

- Minimal field books
- Standard recipe books
- Comprehensive reference manuals
- Recipe cards
- Shopping lists
- Pantry modules
- Meal plans
- Searchable databases
- Printable PDFs

## Current Repository Structure

Expected major folders are present:

- `00_Project_Notes`
- `01_Recipes`
- `02_Techniques`
- `03_Ingredients`
- `04_Components`
- `05_Pantry_Modules`
- `06_Source_Research`
- `07_Output_Templates`
- `08_Index`

## Recipe Layer Status

Status: Complete v1

Completed work:

- Official JetBoil recipe collection pass completed.
- Alcoholic beverages excluded by project rule.
- Derived/non-official recipes identified separately.
- Canonical recipe schema created.
- Provenance migration completed.
- Completeness check passed for ingredient amounts and instructions.
- Batch 10 recipes converted to canonical schema.

Current conclusion:

The recipe layer is stable enough to build on.

## Technique Layer Status

Status: Mostly complete v1

Completed work:

- Technique schema created.
- Technique acquisition plan created.
- Technique Batch 01 created.
- Technique Batch 02 created and normalized.
- Technique Batch 03 created and normalized.
- Technique Batch 04 created and normalized.

Current conclusion:

The technique layer is structurally usable, though some files may later need deeper enrichment from source articles.

## Known Repository Hygiene Issue

Live GitHub review still showed:

```text
01_Recipes/.DS_Store
```

This should be removed before starting the ingredients phase.

Recommended local verification:

```bash
git ls-files | grep DS_Store
```

If it appears, remove with:

```bash
git rm 01_Recipes/.DS_Store
git commit -m "Remove tracked DS Store from recipes"
```

Then push using GitHub Desktop.

## Drift Check

The project did drift briefly when derived field-system recipes were introduced during the JetBoil recipe phase.

Correction already made:

- Official JetBoil recipes now use official provenance.
- Derived field-system recipes should be marked separately.
- Source provenance rules exist.
- Future non-JetBoil sources should not be mixed into official JetBoil source work.

Current rule:

```text
Do not add invented, adapted, or derived recipes unless they are intentionally marked as derived_field_system or assigned to a clear external source.
```

## Current Layer Completion

| Layer | Status |
|---|---|
| `01_Recipes` | Complete v1 |
| `02_Techniques` | Complete enough for v1 |
| `03_Ingredients` | Not started beyond early naming standards |
| `04_Components` | Not yet developed |
| `05_Pantry_Modules` | Not yet developed |
| `06_Source_Research` | Started |
| `07_Output_Templates` | Placeholder / future |
| `08_Index` | Active project control layer |

## Recommended Next Step Before Ingredients

1. Confirm `.DS_Store` is removed from Git tracking.
2. Commit this repository audit.
3. Begin `03_Ingredients` with a small, high-value Ingredient Batch 01.

## Recommended Ingredient Batch 01

Start with ingredients that appear repeatedly across recipes and techniques:

- Ramen Noodles
- Instant Rice
- Couscous
- Tortillas
- Powdered Milk
- Olive Oil
- Bouillon
- Chicken Packets
- Tuna Packets
- Beef Jerky
- Dehydrated Vegetables

## Why Ingredients Next

The recipe and technique layers are now stable enough that ingredients can become the connecting layer.

Ingredient files should eventually support:

- Recipe links
- Technique links
- Shelf-stability notes
- Field-use notes
- Fresh vs shelf-stable alternatives
- Availability notes
- Cleanup impact
- Storage notes
- Substitutions
- Pantry module generation

## Final Recommendation

Do not start pantry modules yet.

Build ingredients first, because pantry modules depend on ingredient metadata.
