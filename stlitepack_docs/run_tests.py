import subprocess
from pathlib import Path
import datetime
import os

# --- Paths ---
repo_root = Path(__file__).resolve().parent.parent
os.chdir(repo_root)

log_dir = repo_root / "test_logs"
log_dir.mkdir(exist_ok=True)

timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
html_report = log_dir / f"pytest_report_{timestamp}.html"

# --- Run pytest ---
process = subprocess.run(
    [
        "pytest",
        "-q",
        "--disable-warnings",
        "--maxfail=1",
        f"--html={html_report}",  # pytest-html plugin
        "--self-contained-html",  # standalone HTML with CSS
    ]
)

print(f"HTML report saved to {html_report}")
