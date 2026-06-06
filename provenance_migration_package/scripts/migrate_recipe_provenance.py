#!/usr/bin/env python3
from pathlib import Path

DERIVED = {
    "loaded-potato-soup.md",
    "chicken-ranch-wrap.md",
    "camp-sausage-potatoes.md",
    "chili-couscous-bowl.md",
    "coconut-curry-rice-bowl.md",
    "savory-oatmeal-bowl.md",
    "creamy-ramen-chowder.md",
    "tuna-melt-quesadilla.md",
}

recipe_root = Path("01_Recipes")
updated = []
skipped = []

for file in recipe_root.rglob("*.md"):
    text = file.read_text(encoding="utf-8")

    if "source:" in text:
        skipped.append(str(file))
        continue

    if not text.startswith("---"):
        skipped.append(str(file))
        continue

    lines = text.splitlines()
    insert_at = None

    for i in range(1, len(lines)):
        if lines[i].startswith("title:"):
            insert_at = i + 1
            break

    if insert_at is None:
        skipped.append(str(file))
        continue

    if file.name in DERIVED:
        block = [
            "source:",
            "  type: derived_field_system",
            "  publisher: internal",
            '  source_url: ""',
            "  source_content_type: recipe",
        ]
    else:
        block = [
            "source:",
            "  type: official_jetboil_recipe",
            "  publisher: JetBoil",
            '  source_url: ""',
            "  source_content_type: recipe",
        ]

    lines[insert_at:insert_at] = block + [""]
    file.write_text("\n".join(lines) + "\n", encoding="utf-8")
    updated.append(str(file))

report = Path("08_Index/Provenance_Migration_Report.md")
report.parent.mkdir(parents=True, exist_ok=True)

with report.open("w", encoding="utf-8") as f:
    f.write("# Provenance Migration Report\n\n")
    f.write(f"Updated files: {len(updated)}\n\n")
    for item in updated:
        f.write(f"- {item}\n")
    f.write("\nSkipped files:\n\n")
    for item in skipped:
        f.write(f"- {item}\n")

print(f"Updated {len(updated)} files")
print("Report written to 08_Index/Provenance_Migration_Report.md")
