# Connected cooking database

## Source and generated files

The Markdown/YAML records in folders 01 through 05 remain the editable source of truth. `tools/build_database.py` validates the recipes and compiles all five collections into:

- `output/database/cookbook.sqlite`: portable SQLite database, requiring no server.
- `output/database/library.json`: complete structured export.
- `Open Cookbook.html`: self-contained offline search, meal selection, and document generation interface.
- `08_Index/Database_Status.md`: actual record counts, missing or duplicate identifiers and unresolved references.

Edit source records rather than generated outputs. The browser template is `app/library.html`. Rebuild after changes using the README Mac environment and `python tools/build_database.py`. `python tools/build_database.py --check` fails when a generated output is missing or stale. SQLite comparison uses logical schema/data, allowing different SQLite versions on Mac and CI. Existing recipe validation, provenance checks and audit reports remain required. GitHub Actions checks both the database and recipe audit outputs.

## Identity and connections

Each record's relative path is its primary key. Original identifiers are retained but cannot be primary keys: existing ingredient and technique records have duplicate identifiers referring to different concepts. No source record is deleted or merged by the compiler. Renaming a source file changes its key and can invalidate saved meal plans; plan migrations must accompany intentional renames.

Relationships retain their original label and field. Matching uses a normalized exact identifier, title, filename stem or explicit alias within the target record type. Normalization ignores punctuation and case. Exactly one candidate resolves a link; multiple candidates remain ambiguous with no selected target; zero candidates remain unresolved. A resolved relationship means a unique record match, not an independently verified culinary assertion. No fuzzy matching or parsing quantities out of official text is performed.

## SQLite tables

- `entities`: full original metadata JSON, Markdown body, type, title, source, source-file checksum and audit status.
- `ingredient_lines`, `instructions`: ordered recipe lines. Official ingredient text stays exact; legacy quantities are not guessed or recalculated.
- `relationships`: original references, match status and candidate keys.
- `equipment_mentions`: equipment and featured-product wording with its source context, not an inferred compatibility table.
- `review_issues`: identifier problems for repair.
- `build_info`: data schema version and content digest.
- Convenience views: `recipes`, `ingredients`, `techniques`, `pantry_modules`, `components`.

Example query using the Mac's `sqlite3` command:

```sh
sqlite3 output/database/cookbook.sqlite 'SELECT title, audit_status FROM recipes ORDER BY title;'
```

The JSON and browser are projections of the same compiled records as SQLite. Generating a selected cookbook or shopping list is deterministic and needs no AI service. Original source instructions, MiniMo notes and field-test status remain separate in generated cookbooks.

## Current boundaries

The interface reads the library; it does not edit the source records. Meal selections can be saved as JSON, with browser storage as a convenience. No data is uploaded. Source links open only when clicked. Printing and downloads use normal browser functions.

One selection represents one recipe batch; portion scaling, repeated batches, automatic ingredient consolidation, nutrition calculation and fuel estimates are not implemented. Ingredient units and portions need more structured, reviewed data before those calculations can be reliable. Shopping lists preserve each recipe's lines separately and remind readers that instructions may mention additional ingredients.

Next data work: resolve duplicate legacy identities against record content, review missing relationships, and continue source audits. Seven official breakfasts have cached-source checks; 26 official recipes still need source review. REI remains a separate future source phase.

## Reviewed connection corrections

`08_Index/connection_reviews.json` records explicit, per-link editorial decisions separately from original recipe and reference files. Each includes the original label/field, destination path, explanation, review date and SHA-256 checksums of both records. The compiler validates it against `schemas/connection-reviews.schema.json` and rejects duplicate fields, duplicate decisions, missing connections, unknown fields, bad dates and changed source/destination records. Renew a correction only after reading the changed records; do not simply refresh hashes to clear a failure.

Reviewed links show their reason and retained alternative records in the library. The original automatic match is preserved in the JSON export; the SQLite `connection_reviews` table preserves review evidence. No original records or legacy identifiers were merged, deleted or rewritten. Duplicate identifiers remain flagged until an explicit identity migration is designed. A name-based preferred destination is a navigation choice, not proof that every statement in either record is accurate.

The September 15 cleanup routes matching ingredient names to their categorized record and corrects exact-name references filed under the wrong record type. Numeric-ID collisions, missing ingredient profiles, generic labels such as coffee/tea, and broader interpretive matches remain pending. Official source audit status is unchanged.
