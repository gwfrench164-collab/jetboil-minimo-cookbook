# Provenance Migration Plan

## Purpose

Add canonical source metadata to all recipes.

## Official JetBoil Recipes

Will receive:

```yaml
source:
  type: official_jetboil_recipe
  publisher: JetBoil
  source_url: ""
  source_content_type: recipe
```

## Derived Recipes

Will receive:

```yaml
source:
  type: derived_field_system
  publisher: internal
  source_url: ""
  source_content_type: recipe
```

Derived recipes:

- loaded-potato-soup.md
- chicken-ranch-wrap.md
- camp-sausage-potatoes.md
- chili-couscous-bowl.md
- coconut-curry-rice-bowl.md
- savory-oatmeal-bowl.md
- creamy-ramen-chowder.md
- tuna-melt-quesadilla.md

## How To Run

From repo root:

```bash
python3 scripts/migrate_recipe_provenance.py
```

Then review:

```text
08_Index/Provenance_Migration_Report.md
```
