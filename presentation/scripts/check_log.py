"""Report every warning / bad box in build/main.log together with the source file it came from."""
import re, sys, pathlib
log = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "build/main.log").read_text(errors="ignore")
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
