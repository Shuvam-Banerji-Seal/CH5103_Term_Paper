"""T11c check: parse the T11c logs and print PASS/FAIL without re-running any DFT.

The DFT runs (t11c_distonic_functionals.py) take hours and were resumed several times, so their
results are spread over logs/t11c*.log.  This script collects the last result line for every
(system, functional) pair, checks the claims the slides and FINDINGS make about them, and
cross-checks the numbers copied into presentation/data/distonic.csv.

Result line format (one per run):
    <system> <formula> <functional> IE_T= x IE_CS= y eV  Delta(T-CS)=+z  alpha-SOMO is k below alpha-HOMO  <S2>_T=s
"""
import csv
import glob
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
LINE = re.compile(r"^(?P<label>.+?)\s+(?P<func>b3lyp|camb3lyp)\s+IE_T=\s*(?P<ie_t>[-+\d.]+)\s+IE_CS=\s*(?P<ie_cs>[-+\d.]+)\s+eV"
                  r"\s+Delta\(T-CS\)=(?P<delta>[-+\d.]+)\s+alpha-SOMO is (?P<rank>\d+) below alpha-HOMO\s+<S2>_T=(?P<s2>[\d.]+)")
# log label (first column) -> key used in presentation/data/distonic.csv
SYSTEMS = {"short acid": "shortacid", "short anion": "shortanion", "TEMPO-4-COOH": "tempoacid", "TEMPO-4-COO-": "tempoanion"}

results = {}
for path in sorted(glob.glob(os.path.join(HERE, "logs", "t11c*.log"))):
    for raw in open(path, encoding="utf-8", errors="replace"):
        m = LINE.match(raw.strip())
        if not m:
            continue
        label = next((k for k in SYSTEMS if m["label"].startswith(k)), None)
        if label is None:
            continue
        results[(SYSTEMS[label], m["func"])] = dict(ie_t=float(m["ie_t"]), ie_cs=float(m["ie_cs"]), delta=float(m["delta"]),
                                                    rank=int(m["rank"]), s2=float(m["s2"]), src=os.path.basename(path))

checks = []


def check(name, ok):
    checks.append(ok)
    print(f"  [{'ok' if ok else 'FAIL'}] {name}")


print("T11c results parsed from logs/t11c*.log")
print(f"  {'system':11s} {'functional':9s} {'IE_T':>7s} {'IE_CS':>7s} {'D(T-CS)':>8s} {'SOMO rank':>9s} {'<S2>_T':>7s}  source")
for (sysk, func), r in sorted(results.items()):
    print(f"  {sysk:11s} {func:9s} {r['ie_t']:7.3f} {r['ie_cs']:7.3f} {r['delta']:+8.3f} {r['rank']:9d} {r['s2']:7.3f}  {r['src']}")

print("checks")
need = [(s, f) for s in SYSTEMS.values() for f in ("b3lyp", "camb3lyp")]
check("all 8 (system, functional) runs present", all(k in results for k in need))
if all(k in results for k in need):
    check("Delta = IE_T - IE_CS for every run (to 0.002 eV)",
          all(abs(r["delta"] - (r["ie_t"] - r["ie_cs"])) < 2e-3 for r in results.values()))
    check("triplet products are clean triplets (|<S2> - 2| < 0.05)", all(abs(r["s2"] - 2) < 0.05 for r in results.values()))
    check("acids: SOMO is the alpha-HOMO (aufbau) for both functionals",
          all(results[(s, f)]["rank"] == 0 for s in ("shortacid", "tempoacid") for f in ("b3lyp", "camb3lyp")))
    check("anions: SOMO lies below the alpha-HOMO (non-aufbau) for both functionals",
          all(results[(s, f)]["rank"] >= 1 for s in ("shortanion", "tempoanion") for f in ("b3lyp", "camb3lyp")))
    check("acids oxidise to the closed shell (Delta > 0) for both functionals",
          all(results[(s, f)]["delta"] > 0 for s in ("shortacid", "tempoacid") for f in ("b3lyp", "camb3lyp")))
    check("CAM-B3LYP: anions oxidise to the triplet diradical (Delta < 0), i.e. the pH switch is reproduced",
          all(results[(s, "camb3lyp")]["delta"] < 0 for s in ("shortanion", "tempoanion")))
    b3 = [results[(s, "b3lyp")]["delta"] for s in ("shortanion", "tempoanion")]
    print(f"  [info] B3LYP anions: Delta = {b3[0]:+.3f}, {b3[1]:+.3f} eV (> 0: B3LYP misses the switch; "
          "reported as a finding, not a failure of this check)")
    csv_path = os.path.join(HERE, "..", "presentation", "data", "distonic.csv")
    if os.path.exists(csv_path):
        rows = {row["system"]: row for row in csv.DictReader(open(csv_path))}
        check("presentation/data/distonic.csv matches the logs (to 0.001 eV)",
              all(abs(float(rows[s][f]) - results[(s, f)]["delta"]) < 1e-3 for s, f in need))

print("T11c PASS" if checks and all(checks) else "T11c FAIL")
