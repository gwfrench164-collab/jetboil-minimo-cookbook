# Beverage source audit — September 15, 2026

Two records were compared with full indexed official-page recipe sections. This is cached-source review, not fresh live verification or field testing. Dated source extracts, checksummed snapshots and complete prior recipe files are retained under `06_Source_Research/JetBoil/audits/2026-09-15/`.

## 30 Second Hot Chocolate

Source: https://jetboil.johnsonoutdoors.com/us/recipes/30-second-hot-chocolate

- Restored the six published ingredient lines, fractions, spelling and optional coffee wording. The old decimal quantities were editorial conversions, not exact transcriptions.
- Water and the per-drink dry-mix measure belong in the instructions. Removed them as additional ingredient-list entries; dry mix is prepared from the listed ingredients, not an additional purchase.
- Restored three published instructions and the separate home/trail headings. The old six steps paraphrased and rearranged the source.
- Removed unsupported six-serving claim, yield, preparation/cooking/total times and the inferred equipment list from the official card. A recipe title is not a measured full preparation time.
- Preserved Flash and MiniMo as featured products, separately from a tools list. The official instruction names Flash; the separate MiniMo cup-mixing workflow is editorial and untested.

## Russian Tea with Tang

Source: https://jetboil.johnsonoutdoors.com/us/recipes/russian-tea-tang

- Restored the six published ingredient lines, including the lemonade package size, fraction notation and abbreviated units.
- Removed water and prepared dry mix as extra ingredient-list entries. Their per-drink amounts remain in the official directions.
- Restored the two original instructions in place of five paraphrased steps.
- Removed unsupported 16-serving claim, dry-mix yield label, time estimates and inferred equipment list from the official card.
- Preserved the four featured product names as shown by the opened indexed page. The shorter search summary omitted this section; the retained extract follows the full indexed page.

## Database and remaining work

Nine of 33 official recipes now have indexed-source checks; 24 remain pending. The known-warning baseline drops from 52 to 48. No REI material was added. MiniMo notes remain separate and neither recipe has documented field tests.

The compiler does not parse ingredient names from exact source-text lines. These migrations therefore remove 16 old automatic ingredient-name references rather than pretending they remain reviewed structured links. This is a representation change, not the loss of official ingredients. Structured ingredient annotations are still needed before reliable portion scaling or combined shopping lists.

Three other beverage pages were located but not marked checked: Apple Cider Chai publishes a serving count, while Mocha Hot Chocolate and Ultralight Backpackers' Spiced Tea contain additional-note sections. The current audited schema cannot faithfully represent all those fields yet. The next schema extension must preserve those sections before these recipes can be accepted; do not discard them to pass validation. Mocha also has an optional alcohol note requiring explicit handling under the project's non-alcoholic collection rule.
