"""Every narration line of the scenes, read statically: the first argument of each `self.say(...)` in
video/scenes/ch*.py with its [span] markers removed, exactly the text ManimGX hands to the voice (checked against
the lines collected by running the scenes in VIDEO_VOICE=collect mode: identical sets).

usage (from the repo root): python3 video/tools/collect_lines.py [--write]
Lints every line (voice.lint), prints counts and words, and with --write replaces video/build/tts/requests.jsonl
with the current lines in scene order, so the batch synthesiser never spends time on lines no scene uses. Store
entries no longer referenced are listed (not deleted).
"""
from __future__ import annotations

import ast
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCENES = ROOT / "video" / "scenes"
sys.path.insert(0, str(SCENES))

from voice import REQUESTS, STORE, Breeze, line_key, lint  # noqa: E402


def spoken(raw: str) -> str:
    return re.sub(r"\s+", " ", raw.replace("[", "").replace("]", "")).strip()


def steps_lines(steps: list) -> list[str]:
    """The narration of a Walk scene (ch18_tests.Walk): what Walk.construct passes to say() for each step."""
    out = []
    for step in steps:
        if step[0] == "code":
            out += [text for _, text in step[4]]
        elif step[0] == "out":
            out.append(step[4].replace("FAIL", ""))
        else:
            out.append(step[2])
    return out


def lines() -> list[tuple[str, str, str]]:
    """(file, scene class, text) for every say() line, in file and source order. Walk scenes (a STEPS list instead
    of say() calls) contribute their steps' narration; Walk's own generic say() calls are skipped."""
    out = []
    for path in sorted(SCENES.glob("ch*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        consts = {t.id: n.value.value for n in tree.body if isinstance(n, ast.Assign)
                  and isinstance(n.value, ast.Constant) and isinstance(n.value.value, str)
                  for t in n.targets if isinstance(t, ast.Name)}

        class Inline(ast.NodeTransformer):  # module-level string constants (a file path) inside STEPS
            def visit_Name(self, node):
                return ast.Constant(consts[node.id]) if node.id in consts else node

        for cls in [n for n in tree.body if isinstance(n, ast.ClassDef)]:
            if cls.name == "Walk":
                continue
            for node in cls.body:
                if isinstance(node, ast.Assign) and any(getattr(t, "id", "") == "STEPS" for t in node.targets):
                    value = ast.fix_missing_locations(Inline().visit(node.value))
                    out += [(path.name, cls.name, spoken(t)) for t in steps_lines(ast.literal_eval(value))]
            for node in ast.walk(cls):
                if isinstance(node, ast.Call) and getattr(node.func, "attr", "") == "say" and node.args:
                    try:
                        raw = ast.literal_eval(node.args[0])
                    except ValueError:
                        raise SystemExit(f"{path.name}:{node.lineno}: say() text is not a literal")
                    out.append((path.name, cls.name, spoken(raw)))
    return out


def main() -> None:
    speaker = Breeze().speaker
    found = lines()
    bad = [(f, c, t, p) for f, c, t in found for p in [lint(t)] if p]
    for f, c, t, p in bad:
        print(f"LINT {f}:{c}: {'; '.join(p)}\n     {t[:120]}")
    seen, ordered = set(), []
    for f, c, t in found:
        if t not in seen:
            seen.add(t)
            ordered.append(t)
    words = sum(len(t.split()) for t in ordered)
    print(f"{len(found)} say() calls, {len(ordered)} distinct lines, {words} words (~{words / 2.3 / 60:.0f} min at "
          f"2.3 words/s), {len(bad)} lint problems")
    keys = {line_key(t, speaker) for t in ordered}
    orphans = [p.stem for p in STORE.glob("*.wav") if p.stem not in keys] if STORE.exists() else []
    if orphans:
        print(f"{len(orphans)} store entries no scene uses: {' '.join(orphans[:8])}{' …' if len(orphans) > 8 else ''}")
    if "--write" in sys.argv:
        if bad:
            raise SystemExit("not writing requests: fix the lint problems first")
        REQUESTS.parent.mkdir(parents=True, exist_ok=True)
        with REQUESTS.open("w", encoding="utf-8") as fh:
            for t in ordered:
                fh.write(json.dumps({"key": line_key(t, speaker), "speaker": speaker, "text": t}, ensure_ascii=False)
                         + "\n")
        print(f"wrote {len(ordered)} requests -> {REQUESTS.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
