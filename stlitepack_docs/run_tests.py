import subprocess
from pathlib import Path
import datetime
import os

# --- Paths ---
repo_root = Path(__file__).resolve().parent
os.chdir(repo_root)

log_dir = repo_root / "test_logs"
log_dir.mkdir(exist_ok=True)

timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
logfile = log_dir / f"pytest_{timestamp}.log"
html_report = log_dir / f"pytest_report_{timestamp}.html"

# --- Run pytest ---
with open(logfile, "w") as f:
    process = subprocess.run(
        [
            "pytest",
            "-q",
            "--disable-warnings",
            "--maxfail=1",
            f"--html={html_report}",  # pytest-html plugin
            "--self-contained-html"   # standalone HTML with CSS
        ],
        stdout=f,
        stderr=subprocess.STDOUT,
        text=True
    )

print(f"Tests finished, log saved to {logfile}")
print(f"HTML report saved to {html_report}")
