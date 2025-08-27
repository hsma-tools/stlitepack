import shutil
from pathlib import Path

root = Path(__file__).parent.parent
docs = root / "stlitepack_docs"

files = {
    "README.md": "index.qmd",
    "LICENCE.md": "licence.qmd",
    "CODE_OF_CONDUCT.md": "code_of_conduct.qmd",
    "HISTORY.md": "changelog.qmd",
}

for src, dest in files.items():
    shutil.copy(root / src, docs / dest)
