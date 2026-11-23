"""Compare two runs on the same questions: accuracy, and an exact McNemar test on the paired answers.

Usage (from the repo root):
    .venv/bin/python experiments/temporal/compare.py results/sampled100/describe_speaker_focused.jsonl \
        experiments/temporal/results/sampled100/describe_speaker_focused_m3.jsonl [more runs ...]

The first file is the reference (normally the baseline). Questions are paired by qid. "Split clips" are the
questions whose clip a temporal run actually split (m_eff > 1, i.e. clips >= 2 s); clips that weren't split
get the baseline's exact request, so they can only differ through stages 2-3 (which are deterministic too).
"""
import json
import sys
from math import comb


def load(path):
    return {r["qid"]: r for r in map(json.loads, open(path))}


def mcnemar_exact(b, c):
    """Two-sided exact McNemar p-value: b = only reference right, c = only other run right."""
    n = b + c
    if n == 0:
        return 1.0
    tail = sum(comb(n, i) for i in range(min(b, c) + 1)) / 2 ** n
    return min(1.0, 2 * tail)


def report(name, ref, run, qids):
    if not qids:
        return
    a = sum(ref[q]["correct"] for q in qids)
    o = sum(run[q]["correct"] for q in qids)
    b = sum(ref[q]["correct"] and not run[q]["correct"] for q in qids)
    c = sum(run[q]["correct"] and not ref[q]["correct"] for q in qids)
    print(f"  {name:<28} n={len(qids):<4} reference {a / len(qids):.3f}  this run {o / len(qids):.3f}  "
          f"diff {(o - a) / len(qids):+.3f}   only-ref-right {b}, only-run-right {c}, McNemar p={mcnemar_exact(b, c):.3f}")


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    ref = load(sys.argv[1])
    print(f"Reference: {sys.argv[1]}")
    for path in sys.argv[2:]:
        run = load(path)
        qids = sorted(ref.keys() & run.keys())
        missing = len(ref.keys() ^ run.keys())
        print(f"\n{path}" + (f"   ({missing} questions not in both files, ignored)" if missing else ""))
        report("All questions", ref, run, qids)
        split = [q for q in qids if run[q].get("m_eff", 1) > 1]
        report("Split clips (>= 2 s)", ref, run, split)


if __name__ == "__main__":
    main()
