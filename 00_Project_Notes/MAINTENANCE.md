# Recipe maintenance without AI

## Authoritative files

- `01_Recipes/**/*.md`: existing Markdown with YAML frontmatter; stable paths and IDs.
- `schemas/recipe.schema.json`: executable recipe schema. Unknown fields are rejected at every defined recipe mapping level.
- `official_recipe`: authoritative exact source transcription for audited version 2 records.
- `recipe_card`: validated export projection. In version 2, ingredients use `{source_text: "published line"}` and instruction text matches `official_recipe`. Do not split ingredient quantities unless a future reviewed schema supports that separately.
- `06_Source_Research/JetBoil/audits/<date>/`: reviewed source extracts and snapshots, with a checksum chain from recipe to snapshot to extract. Checksums detect drift; they do not prove a publisher authored content or replace review.
- `08_Index/Recipe_Accuracy_Audit_Tracker.md`, `recipe-index.md`, `recipe-audit.json`: generated from recipe metadata and actual validation results.

Normal validation is offline and read-only. Scripts use their own location to find the repository; `--root` supports isolated test copies.

## Review an official source

1. Open the recipe's actual official Jetboil page. Record the exact URL and access date; confirm the title and full ingredient/instruction sections, including preparation the night before, optional steps and subheadings. Do not infer recipe quantities from photos, summaries or featured products.
2. Capture a candidate into a **new temporary directory**. This does not change a recipe or mark it verified:

   ```sh
   python tools/capture_jetboil_source.py \
     'https://jetboil.johnsonoutdoors.com/us/recipes/quinoa-breakfast-bowl' \
     --output /tmp/minimo-quinoa-candidate
   ```

   Direct retrieval can fail on Jetboil's security challenge. The script rejects pages with missing recipe sections even if the server returns HTTP 200. It does not solve security challenges. If you saved the official page as HTML in your browser, use `--html /path/to/saved-page.html` with the same URL. The program cannot verify the origin of a supplied HTML file; that is part of your review.

3. Compare the candidate with the recipe:

   ```sh
   python tools/compare_source.py \
     01_Recipes/Breakfast/quinoa-breakfast-bowl.md \
     /tmp/minimo-quinoa-candidate/candidate.json
   ```

   Exit 0 means matching official fields; 1 means differences. Compare output does not change either file. Capture is deliberately a candidate: changes to page structure, inline whitespace or labels can require manual review. Check the displayed source page, especially list boundaries, ingredient quantities, instruction phases and featured products.

4. Accept only after review. Copy evidence and candidate to a new dated folder in `06_Source_Research/JetBoil/audits/`; do not overwrite older evidence. Change the snapshot's `evidence_file` to the repository-relative path of the retained HTML. Its `evidence_sha256` already describes that file. Set recipe `official_recipe` to the reviewed object, update titles/URL, and update `audit.evidence_file`, `audit.checked_on`, `audit.method`, `audit.live_check` and `audit.status`. Set `source.source_verified` and `recipe_status.official_recipe_verified` consistently. Use `shasum -a 256 path/to/snapshot.json` for `audit.snapshot_sha256` **after** all snapshot edits.
5. `verified_live` requires a direct official-page capture, `method: direct_official_page`, and `live_check: verified`. `verified_cached` means comparison with an indexed official-page extract and `method: indexed_official_page`; it must not imply a fresh live check. A missing or incomplete source remains pending/blocked, never verified from memory. Quote date values in YAML (`'2026-09-10'`).
6. Regenerate the recipe projection, run validation, remove resolved warning-baseline entries, generate reports, run tests and review the Git diff. A successful schema check is not a source audit or a field test.

## Keep annotations separate

- Official wording remains as recorded. The September 2026 extraction removed HTML/retrieval markup, represented list numbering structurally and trimmed outer whitespace. It preserved wording, case, punctuation and internal whitespace, including awkward source spacing.
- `minimo_adaptation` contains editorial notes, source URLs and review status. A reviewed note can still describe an untested adaptation. Follow equipment manuals where recipe directions are abbreviated or conflict; explain that separately instead of changing the official transcription.
- `field_tested_variations.entries` requires description, named tester, test date and evidence for each entry. Do not turn proposed additions into claimed tests.
- `proposed_variations` retains useful untested ideas. The prior Baggie Omelets additions have no recorded test evidence.
- Unspecified source metadata remains null/empty. Times within steps remain in those steps. Equipment mentioned in instructions is not necessarily a separate tools list; featured-product links are not compatibility certification.
- Maintain the prose annotation sections alongside their YAML notes; the official block and card projection are generated, but editorial prose outside the marked block is maintained by the editor.

## Warning backlog and scope

`tools/audit_backlog.json` lists the 26 remaining official recipe files that lack both a source URL and a completed audit. CI permits exactly that known backlog. New warnings and stale baseline entries fail. Full `--strict` mode fails for any warning. Do not create placeholder URLs to clear the backlog.

The validator covers recipe files, not a complete ingredient/technique/pantry schema migration. It checks Markdown links appearing in recipes, but does not assert that old relationship labels identify real canonical records. Those relationship reviews remain future work.

No task scheduler is needed for local checks. GitHub Actions performs the checks on repository pushes and pull requests after the workflow is pushed. Source capture is opt-in; changes are never accepted automatically.

## Stable ID repair

On September 10, 2026, history showed Baggie Omelets had been changed from `recipe-0009` to `recipe-0001` in commit `a6641c7`, colliding with Sesame Chicken. Restore Baggie Omelets to `recipe-0009`; keep Sesame Chicken and its existing references at `recipe-0001`.

Four files previously had no ID: Russian Tea (`recipe-0038`), Ultralight Backpackers' Spiced Tea (`recipe-0039`), Keto Chili (`recipe-0040`), and Mocha Hot Chocolate (`recipe-0041`). No culinary content in those files was audited or changed.

`audit.live_check: not_checked` explicitly records an indexed-source audit when no direct retrieval was attempted. It must not be described as blocked or live-verified.
