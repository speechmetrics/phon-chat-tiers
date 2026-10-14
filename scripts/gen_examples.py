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
