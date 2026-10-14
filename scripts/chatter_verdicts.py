#!/usr/bin/env python3
"""Print Chatter's verdict on CHAT files as rows of the table in
examples/CHATTER-VERDICTS.md. Run from the repository root:

    python3 scripts/chatter_verdicts.py <path to chatter> examples/valid/*.cha examples/invalid/*.cha

One row per file: file name, phon-conformance label, Chatter's status,
error codes. The Disagreements section of that file is written by hand."""
from __future__ import annotations
import json, pathlib, subprocess, sys


def verdict(chatter: str, path: pathlib.Path) -> tuple[str, list[str]]:
    proc = subprocess.run([chatter, "validate", "--tui-mode", "disable", "--format", "json", "--", str(path)],
                          capture_output=True, text=True)
    status, codes = "?", []
    for line in proc.stdout.splitlines():
        try:
            d = json.loads(line)
        except json.JSONDecodeError:
            continue
        if d.get("type") == "file":
            status = d.get("status", "?")
            codes = [e.get("code", "?") for e in d.get("errors", [])]
    return status, codes


def main() -> int:
    if len(sys.argv) < 3:
        print(__doc__, file=sys.stderr)
        return 2
    chatter = sys.argv[1]
    for arg in sys.argv[2:]:
        path = pathlib.Path(arg)
        lines = path.read_text(encoding="utf-8").split("\n")
        label = next((l.split(": ", 1)[1] for l in lines if l.startswith("@Comment:\tphon-conformance: ")), "?")
        status, codes = verdict(chatter, path)
        print(f"| {path.name} | {label} | {status} | {' '.join(codes)} |")
    return 0


if __name__ == "__main__":
    sys.exit(main())
