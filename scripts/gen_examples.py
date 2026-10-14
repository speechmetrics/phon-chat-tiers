#!/usr/bin/env python3
"""Generate the conformance example files. Run from the repository root:
    python3 scripts/gen_examples.py
Every file is data below; never edit a generated .cha by hand.

Tier lines marked "survey" are copied from Phon's writer survey
(speechmetrics/phon, docs/specs/survey/writer-survey.cha), so the valid
files hold the tiers exactly as Phon writes them."""
from __future__ import annotations
import pathlib
from dataclasses import dataclass

NAK = "\x15"


def b(start: int, end: int) -> str:
    """A CLAN time bullet."""
    return f"{NAK}{start}_{end}{NAK}"


@dataclass
class Case:
    name: str            # file stem, e.g. "valid-syl-cat"
    label: str           # "valid" or "invalid 3.4"
    lines: list[str]     # main line and tiers, each "name:\tcontent", in order
    media: bool = False  # add @Media and expect bullets
    note: str | None = None  # a second @Comment line, after the label

    def text(self) -> str:
        head = ["@UTF8", "@Begin", f"@Comment:\tphon-conformance: {self.label}"]
        if self.note:
            head.append(f"@Comment:\t{self.note}")
        head += ["@Languages:\teng", "@Participants:\tCHI Target_Child",
                 "@ID:\teng|corpus|CHI|||||Target_Child|||"]
        if self.media:
            head.append(f"@Media:\t{self.name}, audio")
        body = head + self.lines + ["@End"]
        for line in body:
            assert "\n" not in line and not line.startswith("\t"), line
            assert ":\t" in line or line.startswith(("@UTF8", "@Begin", "@End")), line
        return "\n".join(body) + "\n"


def main(media: bool, label: str, name: str, *lines: str, note: str | None = None) -> Case:
    return Case(name=name, label=label, lines=list(lines), media=media, note=note)


CASES: list[Case] = [
    # ---- valid: the two Chatter samples, renamed (the invalid one is in section 3 below) ----
    main(True, "valid", "valid-phoint-cat",
         f"*CHI:\tcat . {b(0,300)}",
         "%pho:\tkæt",
         f"%phoint:\tk {b(0,100)} æ {b(100,200)} t {b(200,300)}"),
    # ---- valid: syllabification and alignment (survey records) ----
    main(False, "valid", "valid-syl-cat",
         "*CHI:\tcat .",
         "%mod:\tkæt", "%modsyl:\tk:Oæ:Nt:C",
         "%pho:\tkæt", "%phosyl:\tk:Oæ:Nt:C",
         "%phoaln:\tk↔k,æ↔æ,t↔t"),
    main(False, "valid", "valid-aln-substitution-and-deletion",
         "*CHI:\tthe cat stood .",
         "%mod:\tðə kæt stʊd", "%modsyl:\tð:Oə:N k:Oæ:Nt:C s:Ot:Oʊ:Nd:C",
         "%pho:\tdə kæt tʊd", "%phosyl:\td:Oə:N k:Oæ:Nt:C t:Oʊ:Nd:C",
         "%phoaln:\tð↔d,ə↔ə k↔k,æ↔æ,t↔t s↔∅,t↔t,ʊ↔ʊ,d↔d"),
    main(False, "valid", "valid-syl-pause-between-words",
         "*CHI:\tcat (.) dog .",
         "%mod:\tkæt (.) dɔɡ", "%modsyl:\tk:Oæ:Nt:C (.) d:Oɔ:Nɡ:C",
         "%pho:\tkæt (.) dɔɡ", "%phosyl:\tk:Oæ:Nt:C (.) d:Oɔ:Nɡ:C",
         "%phoaln:\tk↔k,æ↔æ,t↔t (.)↔(.) d↔d,ɔ↔ɔ,ɡ↔ɡ"),
    main(False, "valid", "valid-syl-pause-inside-word",
         "*CHI:\tbaba .",
         "%mod:\tbʌ^bʌ", "%modsyl:\tb:Oʌ:N^b:Oʌ:N",
         "%pho:\tbʌ^bʌ", "%phosyl:\tb:Oʌ:N^b:Oʌ:N",
         "%phoaln:\tb↔b,ʌ↔ʌ,^↔^,b↔b,ʌ↔ʌ"),
    # Phon mirrors a main-line pause into both IPA tiers, so a one-sided
    # pause arises only when the main line has no pause (survey point 6).
    main(False, "valid", "valid-aln-one-sided-pause",
         "*CHI:\tcat dog .",
         "%mod:\tkæt (.) dɔɡ", "%modsyl:\tk:Oæ:Nt:C (.) d:Oɔ:Nɡ:C",
         "%pho:\tkæt dɔɡ", "%phosyl:\tk:Oæ:Nt:C d:Oɔ:Nɡ:C",
         "%phoaln:\tk↔k,æ↔æ,t↔t (.)↔∅ d↔d,ɔ↔ɔ,ɡ↔ɡ"),
    main(False, "valid", "valid-syl-tone-number",
         "*CHI:\tma .",
         "%mod:\tma⁶", "%modsyl:\tm:Oa:N⁶:U",
         "%pho:\tma⁶", "%phosyl:\tm:Oa:N⁶:U",
         "%phoaln:\tm↔m,a↔a,⁶↔⁶"),
    main(False, "valid", "valid-syl-sandhi",
         "*CHI:\tdoes_it .",
         "%mod:\tdʌz‿ɪt", "%modsyl:\td:Oʌ:Nz:C‿:Uɪ:Nt:C",
         "%pho:\tdʌz‿ɪt", "%phosyl:\td:Oʌ:Nz:C‿:Uɪ:Nt:C",
         "%phoaln:\td↔d,ʌ↔ʌ,z↔z,ɪ↔ɪ,t↔t"),
    main(False, "valid", "valid-syl-untranscribed",
         "*CHI:\tthe xxx .",
         "%mod:\tðə *", "%modsyl:\tð:Oə:N *:U",
         "%pho:\tdə *", "%phosyl:\td:Oə:N *:U",
         "%phoaln:\tð↔d,ə↔ə ∅↔*,*↔∅",
         note="D4: the untranscribed-word marker * is a timed element, so a %phoint for this utterance would end with a group holding * and one bullet; this file has no %phoint."),
    main(False, "valid", "valid-syl-phonetic-group",
         "*CHI:\tau_revoir .",
         "%mod:\t‹o ʁəvwaʁ›", "%modsyl:\to:Nʁ:Oə:Nv:Ow:Oa:Nʁ:C",
         "%pho:\tovwa", "%phosyl:\to:Nv:Ow:Oa:N",
         "%phoaln:\to↔o,ʁ↔∅,ə↔∅,v↔v,w↔w,a↔a,ʁ↔∅"),
    main(False, "valid", "valid-aln-stress-and-boundary",
         "*CHI:\trecord .",
         "%mod:\tˈɹɛkɔɹd", "%modsyl:\tˈɹ:Oɛ:Nk:Oɔ:Dɹ:Dd:C",
         "%pho:\tˈɹɛ.kɔɹd", "%phosyl:\tˈɹ:Oɛ:N.k:Oɔ:Dɹ:Dd:C",
         "%phoaln:\tˈ↔ˈ,ɹ↔ɹ,ɛ↔ɛ,∅↔.,k↔k,ɔ↔ɔ,ɹ↔ɹ,d↔d"),
    # ---- valid: intervals ----
    main(True, "valid", "valid-phoint-gap",
         f"*CHI:\tcat . {b(0,400)}",
         "%pho:\tkæt",
         f"%phoint:\tk {b(0,100)} æ {b(150,250)} t {b(300,400)}"),
    main(True, "valid", "valid-phoint-geminate",
         f"*CHI:\tbutter . {b(0,400)}",
         "%pho:\tbʌtt",
         f"%phoint:\tb {b(0,100)} ʌ {b(100,200)} tt {b(200,400)}"),
    main(True, "valid", "valid-phoint-two-words-and-pauses",
         f"*CHI:\tbaba (.) cat . {b(0,1000)}",
         "%pho:\tbʌ^bʌ (.) kæt",
         f"%phoint:\tb {b(0,100)} ʌ {b(100,200)} ^ {b(200,300)} b {b(300,400)} ʌ {b(400,500)} / (.) {b(500,700)} / k {b(700,800)} æ {b(800,900)} t {b(900,1000)}"),
    main(True, "valid", "valid-phoint-one-ms-outside-record",
         f"*CHI:\tcat . {b(100,300)}",
         "%pho:\tkæt",
         f"%phoint:\tk {b(99,150)} æ {b(150,250)} t {b(250,301)}"),
    main(True, "valid", "valid-phoint-one-ms-overlap",
         f"*CHI:\tcat . {b(0,300)}",
         "%pho:\tkæt",
         f"%phoint:\tk {b(0,100)} æ {b(99,200)} t {b(199,300)}"),
    # ---- invalid: syllabification (section 1), one rule each ----
    main(False, "invalid 1.1", "invalid-1-1-no-codes",
         "*CHI:\tcat .", "%pho:\tkæt", "%phosyl:\tkæt"),
    main(False, "invalid 1.2", "invalid-1-2-unknown-code",
         "*CHI:\tcat .", "%pho:\tkæt", "%phosyl:\tk:Oæ:Nt:T"),
    main(False, "invalid 1.3", "invalid-1-3-wrong-phone",
         "*CHI:\tcat .", "%pho:\tkæt", "%phosyl:\tk:Oɛ:Nt:C"),
    main(False, "invalid 1.4", "invalid-1-4-word-count",
         "*CHI:\tcat .", "%pho:\tkæt", "%phosyl:\tk:Oæ:Nt:C k:Oæ:Nt:C"),
    main(False, "invalid 1.5", "invalid-1-5-source-tier-missing",
         "*CHI:\tcat .", "%phosyl:\tk:Oæ:Nt:C"),
    main(False, "invalid 1.6", "invalid-1-6-pause-inside-group",
         "*CHI:\tcat .", "%pho:\t‹kæ (.) t›", "%phosyl:\tk:Oæ:Nt:C"),
    # ---- invalid: alignment (section 2) ----
    main(False, "invalid 2.1", "invalid-2-1-empty-side",
         "*CHI:\tcat .", "%mod:\tkæt", "%pho:\tkæt", "%phoaln:\tk↔k,æ↔,t↔t"),
    main(False, "invalid 2.2", "invalid-2-2-null-pair",
         "*CHI:\tcat .", "%mod:\tkæt", "%pho:\tkæt", "%phoaln:\tk↔k,∅↔∅,æ↔æ,t↔t"),
    main(False, "invalid 2.3", "invalid-2-3-model-side",
         "*CHI:\tcat .", "%mod:\tkæt", "%pho:\tkæt", "%phoaln:\tk↔k,ɛ↔æ,t↔t"),
    main(False, "invalid 2.4", "invalid-2-4-actual-side",
         "*CHI:\tcat .", "%mod:\tkæt", "%pho:\tkæt", "%phoaln:\tk↔k,æ↔ɛ,t↔t"),
    main(False, "invalid 2.5", "invalid-2-5-word-count",
         "*CHI:\tcat dog .", "%mod:\tkæt dɔɡ", "%pho:\tkæt dɔɡ",
         "%phoaln:\tk↔k,æ↔æ,t↔t"),
    main(False, "invalid 2.6", "invalid-2-6-source-tier-missing",
         "*CHI:\tcat .", "%pho:\tkæt", "%phoaln:\tk↔k,æ↔æ,t↔t"),
    main(False, "invalid 2.7", "invalid-2-7-pause-inside-group",
         "*CHI:\tcat .", "%mod:\tkæt", "%pho:\t‹kæ (.) t›", "%phoaln:\tk↔k,æ↔æ,t↔t"),
    # ---- invalid: intervals (section 3) ----
    main(True, "invalid 3.1", "invalid-3-1-missing-bullet",
         f"*CHI:\tcat . {b(0,300)}", "%pho:\tkæt",
         f"%phoint:\tk {b(0,100)} æ {b(100,200)} t"),
    main(True, "invalid 3.2", "invalid-3-2-wrong-element",
         f"*CHI:\tcat . {b(0,300)}", "%pho:\tkæt",
         f"%phoint:\tk {b(0,100)} æ {b(100,200)} d {b(200,300)}"),
    main(True, "invalid 3.3", "invalid-3-3-empty-interval",
         f"*CHI:\tcat . {b(0,300)}", "%pho:\tkæt",
         f"%phoint:\tk {b(0,100)} æ {b(100,100)} t {b(100,300)}"),
    # Chatter's own invalid sample, with its @Media renamed.
    main(True, "invalid 3.4", "invalid-3-4-start-before-previous-end",
         f"*CHI:\tcat . {b(0,300)}", "%pho:\tkæt",
         f"%phoint:\tk {b(0,100)} æ {b(200,300)} t {b(50,150)}"),
    main(True, "invalid 3.4", "invalid-3-4-two-ms-overlap",
         f"*CHI:\tcat . {b(0,300)}", "%pho:\tkæt",
         f"%phoint:\tk {b(0,100)} æ {b(98,200)} t {b(200,300)}"),
    main(True, "invalid 3.5", "invalid-3-5-ends-after-record",
         f"*CHI:\tcat . {b(0,300)}", "%pho:\tkæt",
         f"%phoint:\tk {b(0,100)} æ {b(100,200)} t {b(200,302)}"),
    main(True, "invalid 3.5", "invalid-3-5-starts-before-record",
         f"*CHI:\tcat . {b(100,300)}", "%pho:\tkæt",
         f"%phoint:\tk {b(98,150)} æ {b(150,250)} t {b(250,300)}"),
    main(True, "invalid 3.6", "invalid-3-6-group-count",
         f"*CHI:\tcat dog . {b(0,600)}", "%pho:\tkæt dɔɡ",
         f"%phoint:\tk {b(0,100)} æ {b(100,200)} t {b(200,300)}"),
    main(True, "invalid 3.7", "invalid-3-7-source-tier-missing",
         f"*CHI:\tcat . {b(0,300)}",
         f"%phoint:\tk {b(0,100)} æ {b(100,200)} t {b(200,300)}"),
    main(True, "invalid 3.8", "invalid-3-8-pause-inside-group",
         f"*CHI:\tcat . {b(0,300)}", "%pho:\t‹kæ (.) t›",
         f"%phoint:\tk {b(0,100)} æ {b(100,200)} t {b(200,300)}"),
]


def write_all(root: pathlib.Path) -> int:
    n = 0
    for case in CASES:
        for line in case.lines:
            assert "COPY " not in line, f"{case.name}: unresolved COPY marker"
        folder = "valid" if case.label == "valid" else "invalid"
        path = root / "examples" / folder / f"{case.name}.cha"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(case.text().encode("utf-8"))
        n += 1
    return n


if __name__ == "__main__":
    root = pathlib.Path(__file__).resolve().parent.parent
    print(f"wrote {write_all(root)} files under {root / 'examples'}")
