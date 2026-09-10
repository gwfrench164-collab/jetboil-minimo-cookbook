# Canonical Recipe Schema

The executable authority is [recipe.schema.json](../schemas/recipe.schema.json). Run [the documented local checks](../README.md#run-on-your-mac).

## Version 1: legacy records

Existing unversioned records keep the familiar `id`, `title`, `source`, `recipe_status`, and `recipe_card` structure. Ingredients use `item`, `amount`, `unit`, optional `preparation` and `notes`. Instructions use consecutive `step` numbers and `text`. Existing card notes and relationship labels are supported. All unknown fields and duplicate YAML keys are errors.

Allowed source types in this phase:

- `official_jetboil_recipe`, publisher Jetboil, content type `recipe`.
- `derived_field_system`, publisher `internal`, content type `recipe`.

Technique articles belong outside `01_Recipes`. REI and other publishers require a deliberate schema/provenance extension in their future phase. A blank official URL is a visible backlog warning, never a source verification.

## Version 2: audited official records

Set `schema_version: 2`. Preserve existing paths and stable IDs. Add these required sections:

| Field | Meaning |
|---|---|
| `official_recipe.source_title` | Published title |
| `official_recipe.ingredients_exact` | Exact ingredient lines, including quantities as written |
| `official_recipe.instructions_exact` | Exact instruction text, in source order |
| `official_recipe.instruction_groups` | Source headings and the instruction number each precedes |
| `official_recipe.tools_exact` | Explicit tools list, or empty if absent |
| `official_recipe.featured_products_exact` | Featured products, separately from recipe tools |
| `audit` | Verification status, date, retrieval method, snapshot path and SHA-256 |
| `minimo_adaptation` | Editorial review status, notes and supporting sources |
| `field_tested_variations` | Separate entries with tester/date/evidence; empty if undocumented |
| `proposed_variations` | Untested suggestions, kept outside official content |

The card is a generated projection with `content_basis: official_recipe`. Its ingredients use `source_text`, not guessed numeric amounts; instructions retain `step` and `text`. The renderer and validator enforce exact equality with the authoritative fields. Future exporters must branch on this representation and preserve instruction groups. Legacy schema/template documents describe historical formats and cannot override this standard.

Official sections are rendered between explicit generated markers in the Markdown body. Editor-authored MiniMo and variation prose remains outside the markers. The source audit checks the source snapshot, extract checksum and official rendered block. It never certifies cooking results, storage safety, nutrition or field performance.

`verified_cached` and `verified_live` are distinct. Only reviewed direct source evidence can support a live claim. Dates must be quoted ISO strings. Unspecified servings are `null`; unspecified yields/times are empty strings. Do not invent values to satisfy an exporter.

## Current checks

Required fields and types; unknown fields at every defined recipe mapping; duplicate YAML keys, IDs, normalized titles, normalized source URLs and identical recipe-card content; sequential instruction numbers; source type/domain/publisher consistency; supported verification claims; snapshot/recipe agreement; snapshot and extract checksums; generated official-body agreement; local Markdown links in recipe bodies; deterministic audit/index outputs. Field-tested entries require explicit evidence metadata.

See [maintenance instructions](../00_Project_Notes/MAINTENANCE.md) for source capture and review. The library still contains unaudited version 1 records; schema validity is not content authenticity.
