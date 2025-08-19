#!/usr/bin/env python3
import pathlib

# Where your tests live
TESTS_DIR = pathlib.Path("tests")
DOCS_DIR = pathlib.Path("stlitepack_docs")
# Where to write the Quarto page
OUTPUT_FILE = DOCS_DIR / "test_outputs.qmd"

def main():
    # Find all index.html files inside tests/
    html_files = sorted(TESTS_DIR.rglob("index.html"))

    # Build Markdown content
    lines = ["---", "title: Test Results", "format: html", "---", "", "# Test Results", ""]

    for html_file in html_files:
        rel_path = html_file.relative_to(TESTS_DIR)   # e.g. "test_name/deeper_test_name/index.html"
        parent = rel_path.parent                      # e.g. "test_name/deeper_test_name"
        label = "/".join(parent.parts)                # human-friendly label
        link = rel_path.as_posix()                    # URL path
        lines.append(f"- [{label}]({link})")

    # Write index.qmd
    OUTPUT_FILE.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUTPUT_FILE} with {len(html_files)} entries.")

if __name__ == "__main__":
    main()
