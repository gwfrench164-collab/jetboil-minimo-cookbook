# Ready to cook?

Open the [MiniMo Cooking Guide](output/pdf/MiniMo_Cooking_Guide.pdf), or read [START HERE](START_HERE.md). No installation or technical steps are needed.

The guide has four breakfasts, with ingredients, equipment and numbered steps. Start with French Toast on page 2 if you have the skillet, or Quinoa Breakfast Bowl on page 4 if you use only the pot.

---

# JetBoil MiniMo Field Cookbook

A structured field-cooking reference for the MiniMo pot and compatible skillet. Recipes, techniques, ingredients and pantry modules are maintained separately, with future recipe cards, books and shopping lists built from those records.

## Current status

The repository has 41 recipe files: 33 labeled official Jetboil and eight derived field systems. Seven official breakfast recipes were compared with indexed text of their official source pages on September 10, 2026. Direct site access encountered a security challenge, so **fresh live-page verification is still pending**. Source excerpts, dates, checksums and prior records are retained. None of these audits establishes a field test.

- [Complete recipe index](08_Index/recipe-index.md)
- [Generated audit tracker and outstanding checks](08_Index/Recipe_Accuracy_Audit_Tracker.md)
- [Breakfast corrections and limitations](08_Index/Breakfast_Audit_2026-09-10.md)
- [Machine-readable schema](schemas/recipe.schema.json) and [schema notes](08_Index/Schema_Standard.md)

The other 26 official records remain unreviewed with blank source URLs. Collection is not verification. The checks display this backlog instead of inventing URLs or declaring the collection complete.

## Run on your Mac

Use Python 3.10 or newer (`python3 --version`). If Python is missing, install it from [python.org](https://www.python.org/downloads/macos/) and reopen Terminal. Open Terminal in this repository, or run:

```sh
cd "$HOME/Library/Mobile Documents/com~apple~CloudDocs/Cooking/jetboil-minimo-cookbook"
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r tools/requirements.txt
```

The installation needs internet access. All normal checks run offline; no AI account or API key is required. Each new Terminal session needs `source .venv/bin/activate` after entering the repository.

```sh
python tools/validate_recipes.py --baseline tools/audit_backlog.json
python tools/check_provenance.py --baseline tools/audit_backlog.json
python tools/render_recipes.py
python tools/build_project_audit.py --check
python -m unittest discover -s tests -v
```

Exit 0 means the check passed. Exit 1 means errors, stale output or a changed warning backlog. The baseline currently permits 52 visible warnings (two for each unaudited official record). It rejects both new warnings and obsolete entries, so remove resolved entries as audits advance. Do not add entries merely to make a failure disappear.

For an uncompromising source-completeness check:

```sh
python tools/check_provenance.py --strict
```

That command intentionally exits 1 until the remaining source backlog is resolved. Without `--strict` or `--baseline`, warnings are reported but do not fail the command. Schema errors, duplicate keys/IDs/titles/source URLs/recipe content, unknown fields, broken recipe Markdown links and evidence mismatches always fail.

After intentional edits, regenerate the derived card/body projections and reports:

```sh
python tools/render_recipes.py --write
python tools/validate_recipes.py --baseline tools/audit_backlog.json
python tools/build_project_audit.py
python tools/build_project_audit.py --check
```

`render_recipes.py` changes only the audited card projection and marked official Markdown block. It never edits the official transcription or its evidence. The report generator refuses to overwrite reports if validation has errors. Run the checks again before committing.

## Maintain source fidelity

[The maintenance guide](00_Project_Notes/MAINTENANCE.md) explains source capture, comparison, evidence, audit review and schema migration. The ingredients and instructions inside `official_recipe` are the authoritative transcription. MiniMo adaptations and proposed/field-tested variations remain separate. Never silently fix a source typo, contradiction, quantity or cooking method.

Legacy recipes keep their original structured ingredient fields. Audited version 2 cards use `source_text` for each exact ingredient line; quantities are not guessed by a parser. Future exporters must support this representation and the source's instruction groups. No prior executable exporter or automation existed in this checkout.

## Source phases

1. Finish official Jetboil recipe audits, continuing to exclude alcoholic beverages under the existing project rule.
2. Audit the collected Trail Life material separately.
3. Review REI as a future source with its own provenance category and schema update. No REI recipes have been added to the official collection.
4. Consider other sources only after explicit provenance and scope decisions.

The GitHub Actions workflow runs the offline checks on pushes and pull requests once this change is committed and pushed. It does not publish, rewrite recipes, accept source changes or contact Jetboil automatically.
