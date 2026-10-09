"""Verify the only files eligible for Pages publication."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

shell = {"index.html", "app.css", "app.js", "favicon.svg", "connection.json", ".nojekyll"}
font_hashes = {'fonts/Sora.ttf': '84ff7096ae3ec6c8be47d906d1a0ba4de7f2ce78c615275c77301964a316e16c', 'fonts/Manrope.ttf': '3ae11c49db0455a3cc33e37d380f20fdb8c7f8b41dc07625c177e3d87a9d6ae6', 'fonts/Sora-OFL.txt': 'ba0b9729c9428ba79a0459ab8ec575791b51509dbec213e383d0316d37fec299', 'fonts/Manrope-OFL.txt': '58172e0c0fac2cda8a37b348164bb55e44b0e69051e557e92b1d3f6910141f7b'}
allowed = shell | set(font_hashes) | {"README.md", "tools/check_public.py", ".github/workflows/pages.yml"}
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
for name, expected in font_hashes.items():
    path = Path(name)
    if path.is_symlink() or not path.is_file() or path.stat().st_size > 250_000:
        raise SystemExit("Invalid font asset")
    data = path.read_bytes()
    if name.endswith(".txt"):
        data = data.replace(b"\r\n", b"\n")
    if hashlib.sha256(data).hexdigest() != expected:
        raise SystemExit("Unreviewed font asset")
connection = json.loads(Path("connection.json").read_text())
if set(connection) != {"schema_version", "endpoint", "proof"} or connection["schema_version"] != 1:
    raise SystemExit("Connection file has unexpected fields")
if connection["endpoint"] and not re.fullmatch(r"https://[a-z0-9]+(?:-[a-z0-9]+)*\.trycloudflare\.com", connection["endpoint"]):
    raise SystemExit("Invalid public connection address")
if (connection["endpoint"] and not re.fullmatch(r"[a-f0-9]{64}", connection["proof"])) or (not connection["endpoint"] and connection["proof"]):
    raise SystemExit("Invalid public connection proof")
print("Public shell allowlist and content checks passed")
