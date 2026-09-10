# Source Provenance Rules

## Active Source Scope

Current active source:

```text
Official Jetboil website
```

## Recipe Source Types

Use one of these:

```yaml
source:
  type: official_jetboil_recipe
  publisher: Jetboil
  source_url: ""
```

```yaml
source:
  type: derived_field_system
  publisher: internal
  source_url: ""
```

## Rules

1. Do not label a derived recipe as official Jetboil.
2. Do not collect alcoholic beverage recipes.
3. Preserve source title and source URL.
4. A recipe is not `recreatable` unless it has ingredients with amounts and usable instructions.
5. If a page is a technique/article rather than a true recipe, store it outside `01_Recipes`.

## Audits and future sources

Collection and source verification are distinct. Use the [current schema](../../08_Index/Schema_Standard.md) and [maintenance guide](../../00_Project_Notes/MAINTENANCE.md). Store exact source text separately from MiniMo notes and untested proposals. Mark indexed-page checks distinctly from fresh live checks. Field-tested variations need a tester, date and evidence. Finish official recipes, then Trail Life, then REI as a separate future provenance phase; do not classify REI as official Jetboil.
