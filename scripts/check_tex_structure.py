"""Structural sanity checks for the split arXiv source (no LaTeX needed)."""

import re
from pathlib import Path

files = sorted(Path("manuscript/arxiv").rglob("*.tex"))
print("files:", [str(f.relative_to("manuscript/arxiv")) for f in files])

alltext = "".join(f.read_text(encoding="utf-8") for f in files)

# Environment balance, counted globally (sections are concatenated by \input).
depth = {}
for kind, name in re.findall(r"\\(begin|end)\{([a-zA-Z*]+)\}", alltext):
    depth[name] = depth.get(name, 0) + (1 if kind == "begin" else -1)
unbalanced = {k: v for k, v in depth.items() if v != 0}
print("unbalanced environments:", unbalanced or "none")

# Cross-references.
labels = set(re.findall(r"\\label\{([^}]+)\}", alltext))
refs = set(re.findall(r"\\(?:eq)?ref\{([^}]+)\}", alltext))
cites = set()
for group in re.findall(r"\\cite\{([^}]+)\}", alltext):
    cites.update(key.strip() for key in group.split(","))
bibitems = set(re.findall(r"\\bibitem\{([^}]+)\}", alltext))
print("dangling refs:", sorted(refs - labels) or "none")
print("unused labels:", sorted(labels - refs) or "none")
print("dangling cites:", sorted(cites - bibitems) or "none")
print("uncited bibitems:", sorted(bibitems - cites) or "none")

# Every \input target must exist.
root = Path("manuscript/arxiv")
missing = [
    t for t in re.findall(r"\\input\{([^}]+)\}", (root / "main.tex").read_text(encoding="utf-8"))
    if not (root / (t + ".tex")).exists()
]
print("missing \\input targets:", missing or "none")

# Brace balance per file (catches a truncated split).
for f in files:
    t = f.read_text(encoding="utf-8")
    stripped = re.sub(r"\\[{}]", "", t)
    if stripped.count("{") != stripped.count("}"):
        print(f"  BRACE IMBALANCE in {f.name}: "
              f"{stripped.count('{')} open vs {stripped.count('}')} close")
print("brace check complete")
