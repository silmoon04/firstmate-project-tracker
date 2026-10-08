"""Verify the only files eligible for Pages publication."""
import json
from pathlib import Path
import re
import subprocess

shell = {"index.html", "app.css", "app.js", "favicon.svg", "connection.json", ".nojekyll"}
allowed = shell | {"README.md", "tools/check_public.py", ".github/workflows/pages.yml"}
tracked = set(subprocess.check_output(["git", "ls-files"], text=True).splitlines())
if tracked != allowed:
    raise SystemExit("Public repository allowlist mismatch")
for name in shell:
    path = Path(name)
    if path.is_symlink() or not path.is_file() or path.stat().st_size > 250_000:
        raise SystemExit("Invalid shell file")
    text = path.read_text(encoding="utf-8")
    patterns = [r"(?i)[a-z]:[/\\]Users[/\\]", r"\b01[a-f0-9]{6}-[a-f0-9-]{28}\b",
                r"\bgh[pousr]_[A-Za-z0-9]{20,}\b", r"\bsk-[A-Za-z0-9_-]{20,}\b",
                r"Bearer [A-Za-z0-9_-]{43}\b", r"(?i)<script[^>]+src=[\"']https?://"]
    if any(re.search(pattern, text) for pattern in patterns):
        raise SystemExit("Private content or external script found")
connection = json.loads(Path("connection.json").read_text())
if set(connection) != {"schema_version", "endpoint", "proof"} or connection["schema_version"] != 1:
    raise SystemExit("Connection file has unexpected fields")
if connection["endpoint"] and not re.fullmatch(r"https://[a-z0-9]+(?:-[a-z0-9]+)*\.trycloudflare\.com", connection["endpoint"]):
    raise SystemExit("Invalid public connection address")
if (connection["endpoint"] and not re.fullmatch(r"[a-f0-9]{64}", connection["proof"])) or (not connection["endpoint"] and connection["proof"]):
    raise SystemExit("Invalid public connection proof")
print("Public shell allowlist and content checks passed")
