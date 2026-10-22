"""Report every warning / bad box in build/main.log together with the source file it came from.
usage: check_log.py [LOG] [--strict]   (--strict: exit 1 unless clean; in GitHub Actions each finding
is also emitted as a warning annotation)"""
import os, re, sys, pathlib
args = [a for a in sys.argv[1:] if a != "--strict"]
log = pathlib.Path(args[0] if args else "build/main.log").read_text(errors="ignore")
stack, out = [], []
for line in log.splitlines():
    for m in re.finditer(r"\((\./[^\s()]+\.tex)|(\))", line):
        if m.group(1): stack.append(m.group(1))
        elif stack and m.group(2): pass
    if re.search(r"Overfull|Underfull|Warning|Missing character|undefined", line) and "infwarerr" not in line:
        cur = next((s for s in reversed(stack) if "sections/" in s), stack[-1] if stack else "?")
        out.append(f"{cur}: {line.strip()}")
seen = []
for o in out:
    if o not in seen: seen.append(o)
print("\n".join(seen) if seen else "CLEAN: no warnings or bad boxes")
if seen and os.environ.get("GITHUB_ACTIONS") == "true":
    for o in seen:
        print(f"::warning title=LaTeX log::{o}")
sys.exit(1 if seen and "--strict" in sys.argv else 0)
