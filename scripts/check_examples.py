#!/usr/bin/env python3
"""Check the example set against the specification. Exit 1 on any problem."""
from __future__ import annotations
import pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SPEC = ROOT / "spec" / "phon-chat-tiers.md"
LABEL = re.compile(r"^@Comment:\tphon-conformance: (valid|invalid (\d+\.\d+))$")
VALID_NAME = re.compile(r"^valid-[a-z0-9]+(-[a-z0-9]+)*$")
INVALID_NAME = re.compile(r"^invalid-(\d+)-(\d+)-[a-z0-9]+(-[a-z0-9]+)*$")
RULE_ROW = re.compile(r"^\| (\d+\.\d+) \| (error(?:, repairable)?) \|", re.M)


def spec_rules() -> set[str]:
    rules = set(RULE_ROW.findall(SPEC.read_text(encoding="utf-8")))
    return {r for r, _ in rules}


def check_file(path: pathlib.Path, rules: set[str], problems: list[str]) -> str | None:
    rel = path.relative_to(ROOT)
    data = path.read_bytes()
    if data.startswith(b"\xef\xbb\xbf"):
        problems.append(f"{rel}: has a BOM"); return None
    if b"\r" in data:
        problems.append(f"{rel}: has CR line endings"); return None
    lines = data.decode("utf-8").split("\n")
    if lines[:2] != ["@UTF8", "@Begin"]:
        problems.append(f"{rel}: must start with @UTF8 and @Begin"); return None
    m = LABEL.match(lines[2]) if len(lines) > 2 else None
    if not m:
        problems.append(f"{rel}: line 3 is not a phon-conformance label"); return None
    labels = [l for l in lines if l.startswith("@Comment:\tphon-conformance:")]
    if len(labels) != 1:
        problems.append(f"{rel}: {len(labels)} label lines, expected 1")
    kind, rule = m.group(1), m.group(2)
    stem, folder = path.stem, path.parent.name
    if kind == "valid":
        if folder != "valid" or not VALID_NAME.match(stem):
            problems.append(f"{rel}: valid file name or folder is wrong")
    else:
        nm = INVALID_NAME.match(stem)
        if folder != "invalid" or not nm:
            problems.append(f"{rel}: invalid file name or folder is wrong")
        elif f"{nm.group(1)}.{nm.group(2)}" != rule:
            problems.append(f"{rel}: name says {nm.group(1)}.{nm.group(2)}, label says {rule}")
        if rule not in rules:
            problems.append(f"{rel}: rule {rule} is not in the specification")
    if lines[-1] != "" or (lines[-2] if len(lines) > 1 else "") != "@End":
        problems.append(f"{rel}: must end with @End and one newline")
    has_bullet = any("\x15" in l for l in lines)
    if any("\u2022" in l for l in lines):
        problems.append(f"{rel}: has a U+2022 bullet character; a bullet is the byte 0x15")
    media = [l for l in lines if l.startswith("@Media:\t")]
    if has_bullet and not media:
        problems.append(f"{rel}: has bullets but no @Media")
    for l in media:
        name = l[len("@Media:\t"):].split(",")[0].strip()
        if name != stem:
            problems.append(f"{rel}: @Media name {name!r} != file stem {stem!r}")
    for i, l in enumerate(lines, 1):
        if l.startswith("\t"):
            problems.append(f"{rel}:{i}: continuation line; tiers must be one line")
        if (l.startswith("@") or l.startswith("%") or l.startswith("*")) and l not in ("@UTF8", "@Begin", "@End") and ":\t" not in l:
            problems.append(f"{rel}:{i}: no tab after the colon")
    return rule


def main() -> int:
    problems: list[str] = []
    rules = spec_rules()
    if len(rules) < 15:
        problems.append(f"only {len(rules)} rules found in {SPEC}; the table regex may be stale")
    covered: set[str] = set()
    files = sorted((ROOT / "examples").rglob("*.cha"))
    if not files:
        problems.append("no example files found")
    for path in files:
        rule = check_file(path, rules, problems)
        if rule:
            covered.add(rule)
    for rule in sorted(rules - covered, key=lambda r: tuple(map(int, r.split(".")))):
        problems.append(f"rule {rule} has no invalid example")
    for p in problems:
        print(p)
    print(f"{len(files)} files, {len(rules)} rules, {len(problems)} problems")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
