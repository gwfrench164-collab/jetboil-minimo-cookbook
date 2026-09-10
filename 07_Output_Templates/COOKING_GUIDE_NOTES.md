# Cooking guide maintenance

The user-facing entry point is `START_HERE.md`, which links to the printable guide. Users need no software installation or command-line steps to read it.

The guide is built from `quick-start-breakfasts.json` using `tools/build_cooking_guide.py`. These are editorial cooking cards, deliberately separate from the exact official recipe records. The cards retain links and checksums for the source snapshots from which they were adapted. A changed source checksum stops a rebuild until the card has been reviewed.

For maintainers only:

```sh
python -m pip install -r tools/requirements-pdf.txt
python tools/build_cooking_guide.py
```

Output: `output/pdf/MiniMo_Cooking_Guide.pdf`. Keep the filename stable. Inspect all rendered pages after every revision. The first edition has six pages: introduction, four individual recipes, sources/review limits. If pagination changes, update the page references in the guide and START_HERE.

Do not present the simplified directions as exact Jetboil instructions. Preserve the official originals. Quinoa is explicitly a half-batch editorial adaptation; its performance has not been field-tested. The skillet lighting sequence follows the MiniMo manual. Egg doneness and cold-storage guidance cite USDA sources on the final page.
