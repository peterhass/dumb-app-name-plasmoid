#!/usr/bin/env python3
"""Create a Plasma installation file. Use only the Python standard library."""
from pathlib import Path
import json
import zipfile

root = Path(__file__).resolve().parents[1]
metadata = json.loads((root / "metadata.json").read_text())
assert metadata["KPackageStructure"] == "Plasma/Applet"
output = root / "dist" / "dumb-app-name-plasmoid.plasmoid"
output.parent.mkdir(exist_ok=True)
files = [root / "metadata.json", root / "LICENSE", root / "README.md"]
files += sorted(path for path in (root / "contents").rglob("*") if path.is_file())
with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as archive:
    for path in files:
        archive.write(path, path.relative_to(root))
print(output)
