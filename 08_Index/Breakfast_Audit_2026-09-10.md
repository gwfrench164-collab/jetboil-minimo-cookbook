# Official breakfast audit — September 10, 2026

Seven breakfast recipes match the seven entries shown in the [official breakfast category](https://jetboil.johnsonoutdoors.com/us/recipes/breakfast). Savory Oatmeal remains a separate derived recipe. This audit compares indexed official-page text, not a new live-site capture: direct HTTP access returned a challenge page and the browser showed a security check. The indexed copies were described by the retrieval service as several weeks to seven months old. Current live text could differ.

## Changes by recipe

| Recipe | Discrepancies and corrections | Classification |
|---|---|---|
| [Baggie Omelets](../01_Recipes/Breakfast/baggie-omelets-camp-eggs.md) | Its prior `official_recipe` wording matched the source extract, but the visible body changed capitalization, omitted the parenthetical water quantity, split one instruction and rephrased steps. Generate body/card from that verified wording. Remove the unsupported SUMO rationale. Treat half-full as the manual ceiling, accounting for bag displacement. Restore original ID `recipe-0009` from Git history. | Transcription drift; separate manual-based notes; prior additions reclassified as untested. |
| [Bobsadilla](../01_Recipes/Breakfast/bobsadilla-breakfast-quesadilla.md) | Restore the full official title, bell pepper, tomato and onion quantities, separate oil/butter quantities, one tortilla and the published cheese range. Prior card instead had two tortillas, 1/2 cup cheese and optional meat. Replace the scrambled-egg sandwich method with the source's four steps, including sautéed vegetables, pressing the tortilla onto eggs, flipping/folding and optional steaming. | Incorrect official attribution of an undocumented variation; old idea retained separately. |
| [Caffeinated Oatmeal](../01_Recipes/Breakfast/caffeinated-oatmeal-blast.md) | Restore exact ingredient wording/fractions, original tools and all seven instructions in two phases. Prior summary omitted advance topping preparation, the oxygen absorber and the separate coffee-brewing and oatmeal-hydration waits. Toppings belong at the final stage. Keep MiniMo/Grande press compatibility outside the source tools list. | Transcription omissions and equipment adaptation. |
| [French Toast](../01_Recipes/Breakfast/french-toast.md) | Restore the official title, seven ingredient lines and five instructions. Prior card added egg size and unspecified topping quantities and rewrote/split steps. Source already names MiniMo, Pot Support and Summit Skillet. Featured products are recorded separately. | Transcription and unsupported metadata corrections. |
| [Hot Granola](../01_Recipes/Breakfast/hot-granola-breakfast.md) | Restore exact five ingredient lines and four instructions. Prior card omitted advance bag packing and changed the combined cooking order, boil duration and immediate serving. Flag full-batch volume against manual guidance separately. | Transcription corrections; untested batching adaptation. |
| [Jack Pine Jim's Power Brunch](../01_Recipes/Breakfast/jack-pine-jims-power-brunch.md) | Restore six official ingredient lines and night-before/morning groups. Water is specified in the overnight instruction, not listed as an ingredient. Prior card replaced that with “as needed,” omitted the soak, lost the three-plus-two-minute sequence and covered cooling, and changed the lunch Tabasco instruction. | Material transcription omissions and unsupported quantity. |
| [Quinoa Breakfast Bowl](../01_Recipes/Breakfast/quinoa-breakfast-bowl.md) | Restore half-cup quinoa, one-cup water, coconut milk, dried fruit, pumpkin seeds, coconut chips and honey; five source instructions include the 15-minute covered simmer. Prior card doubled grain/water and substituted milk powder, sugar, cinnamon and nuts, with a shorter simmer and invented finishing time. | Different undocumented recipe attributed as official; retained only as a proposed variation. |

All seven gained official URLs, recorded title/source evidence and clear annotation sections. Unspecified servings/yield/preparation/total times were cleared rather than presented as source facts. Instruction durations remain in the official instructions. The Caffeinated article's six-minute introductory claim conflicts with its two sequential five-minute waits; the note identifies this without rewriting either instruction.

## Evidence and preservation

The [dated evidence folder](../06_Source_Research/JetBoil/audits/2026-09-10/) contains per-recipe text extracts and JSON snapshots, with SHA-256 checksums. Published text was imported mechanically from retrieved source output; HTML/retrieval markup and surrounding whitespace were removed. Numbering is represented structurally, including the unnumbered overnight step. Internal wording, case, punctuation and spacing are preserved. This is text fidelity, not byte-for-byte HTML fidelity.

[Prior recipe cards and prior official blocks](../06_Source_Research/JetBoil/audits/2026-09-10/prior-records.json) retain every earlier card field for comparison. Git commit `a6641c7` retains the complete prior files. The table above classifies the changes; the prior records plus snapshots provide a field-by-field comparison.

MiniMo notes cite the [manufacturer's operating manual](https://jetboil.johnsonoutdoors.com/sites/default/files/2023-02/JB_product_manual_MicroMo_MiniMo_SUMO_0.pdf), including fill limits, stirring and ignition before cookware placement. Coffee-press compatibility is separately supported by the [MiniMo product page](https://jetboil.johnsonoutdoors.com/us/shop/stoves-systems/minimo-cooking-system/mnmad). These are editorial reviews, not field tests. No tested variations are documented. No safety/storage validation of the overnight food method is asserted.

## Actual remaining work

- Fresh live-page checks for these seven recipes once source access is available.
- Source identification and ingredient/instruction audits for the other 26 official records. The library has 33 official records, not 41; eight records are derived.
- Ingredient/technique/pantry relationship review and practical cooking tests remain separate work.
- Trail Life next, then REI as its own future provenance phase. No REI content added.

Use the [generated tracker](Recipe_Accuracy_Audit_Tracker.md) for ongoing status. Older collection counts and completion claims are historical, not proof of verification.
