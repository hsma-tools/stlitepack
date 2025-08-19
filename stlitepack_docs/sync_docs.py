import shutil
from pathlib import Path

root = Path(__file__).parent.parent
docs = root / "stlitepack_docs"

files = {
    "README.md": "index.qmd",
    "LICENCE.md": "licence.qmd",
}

for src, dest in files.items():
    shutil.copy(root / src, docs / dest)
