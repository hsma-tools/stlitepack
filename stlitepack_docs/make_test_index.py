#!/usr/bin/env python3
import pathlib

# Where your tests live
TESTS_DIR = pathlib.Path("tests")
DOCS_DIR = pathlib.Path("stlitepack_docs")
# Where to write the Quarto page
OUTPUT_FILE = DOCS_DIR / "test_outputs.qmd"

def main():
    # Find all index.html files
    html_files = sorted(TESTS_DIR.rglob("index.html"))

    # Start the Quarto page
    lines = [
        "---",
        "title: Test Results",
        "format: html",
        "---",
        "",
        "# Test Results",
        ""
    ]

    current_top = None
    for html_file in html_files:
        rel_path = html_file.relative_to(TESTS_DIR)   # e.g. "test_a/deeper/index.html"
        parts = rel_path.parts[:-1]                  # drop "index.html"

        top = parts[0]
        if top != current_top:
            # New top-level section
            lines.append("")
            lines.append(f"## {top}")
            lines.append("")
            current_top = top

        if len(parts) == 1:
            # Direct index.html under top
            lines.append(f"- ..\{TESTS_DIR}/[index]({rel_path.as_posix()})")

        else:
            # Nested bullets for deeper folders
            indent = "  " * (len(parts) - 2)
            label = parts[-2]
            link = rel_path.as_posix()
            lines.append(f"{indent}- [{label}](..\{TESTS_DIR/link})")

    # Write index.qmd
    OUTPUT_FILE.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUTPUT_FILE} with {len(html_files)} entries.")

if __name__ == "__main__":
    main()
