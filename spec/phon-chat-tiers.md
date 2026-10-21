# Phon Tiers in CHAT

**Version:** 1.0 (draft)
**Date:** 2026-10-21
**Maintainer:** Phon (https://www.phon.ca)
**Status:** Draft. Becomes 1.0 when tagged `v1.0`.

## Scope

This document defines four dependent tiers that Phon writes to CHAT files
and that carry phonological detail with no home in the standard CHAT tier
set:

| Tier | Source tier(s) | Carries | Word separator |
|------|----------------|---------|----------------|
| `%modsyl` | `%mod` | Syllabification of the model transcription | single space |
| `%phosyl` | `%pho` | Syllabification of the actual transcription | single space |
| `%phoaln` | `%mod`, `%pho` | Phone-by-phone alignment of model and actual | single space |
| `%phoint` | `%pho` | Time interval of each phone and pause of the actual transcription | ` / ` |

It defines each tier's syntax (a grammar), its relation to its source
tiers, and a numbered list of rules. It does not define CHAT itself: the
main line, `%mod`, `%pho`, headers and bullets are defined by the CHAT
manual and checked by Chatter. The one exception is the content of a
`%mod` or `%pho` word: definition D8 and Appendix D state which
characters it may hold and how they form phones, since every tier here
is built from those phones. A file that breaks a rule here is invalid
even when Chatter's general checks pass.

### Conformance

- A **writer** conforms when every file it produces satisfies every rule.
- A **validator** conforms when it reports every broken rule by its number
  and reports nothing for a file that breaks no rule.
- A **reader** conforms when it reports every broken rule, or, for a rule
  marked *repairable*, recomputes the tier from its source tiers instead
  of using the tier as written. A reader must not treat a file that breaks
  a rule as valid.

### Rule numbers and statuses

Rules are numbered `section.rule`. A number is permanent: a withdrawn
rule's number is retired, and a new rule takes the next free number in its
section. Each rule has one status:

| Status | Meaning |
|--------|---------|
| error | The file is invalid. No recovery is defined |
| error, repairable | The file is invalid. A reader may recover by recomputing the tier from its source tier(s) |

Rules are evaluated per utterance and per tier in this order: first the
presence rule (1.5, 2.6, 3.7), then the group-pause rule (1.6, 2.7, 3.8),
then the grammar rule (1.1, 2.1, 3.1), then the others. When one of
those three fails, the section's other rules are not evaluated for that
tier, so a tier that lacks its source tier, whose source tier holds a
pause inside a phonetic group, or that fails to parse breaks exactly one
rule of its section.

### Versions

Versions are `MAJOR.MINOR`. MINOR increases for a change that keeps
existing conforming writers conforming (a clarification, a new example, a
loosened rule). MAJOR increases when a conforming writer must change its
output. Each release is tagged `vMAJOR.MINOR`; the changelog in Appendix B
lists, per version, every rule added, changed or retired.

## Definitions

The rules below refer to these definitions by their identifiers.

**D1 — Word on `%mod` and `%pho`.** The line splits on single spaces
(U+0020). A pause token (the `pause` production of section 1: `(.)`,
`(..)`, `(...)` or a timed pause such as `(2.)` or `(1:3.5)`) is a word.
A phonetic group, from `‹` (U+2039) to the matching `›` (U+203A), is
one word regardless of the spaces inside it. Every other run of characters
between spaces is a word.

**D2 — Comparison text of a word.** The word's characters with `‹`, `›`
and the spaces inside a group removed. Example: `‹o ʁəvwaʁ›` → `oʁəvwaʁ`.

**D3 — Alignment text of a word.** The comparison text (D2) of the word
with the linking ties `‿` (U+203F) and `⁀` (U+2040) removed. Every other
character, including `^`, stress marks, syllable boundaries and tone
numbers, is kept. Example: `dʌz‿ɪt` → `dʌzɪt`; `‹o ʁəvwaʁ›` → `oʁəvwaʁ`.

**D4 — Timed elements of a word.** In order, each phone and each
intra-word pause `^` (U+005E), except that two identical adjacent
consonants (a geminate) form one element whose text is both characters.
A pause word has one timed element, the pause token itself. The
untranscribed-word marker `*` is a timed element. Tone numbers, stress
marks, syllable boundaries, compound-word markers and linking ties are
not timed elements. Example: `bʌtt` → `b`, `ʌ`, `tt`; `bʌ^bʌ` → `b`,
`ʌ`, `^`, `b`, `ʌ`.

**D5 — Slots of `%mod` and `%pho`.** Walk the word lists (D1) of both
tiers in order. When the next word on each tier is a pause, or the next
word on each tier is not a pause, the two words form one slot and both
tiers advance. When one is a pause and the other is not, the pause forms a
slot on its own and only its tier advances. When one tier has no next
word, the next word on the other tier forms a slot on its own.

**D6 — Record interval.** The bullet (D7) at the end of the main line.

**D7 — Bullet.** The byte `0x15`, a start in milliseconds, `_` (U+005F),
an end in milliseconds, and `0x15`, as CLAN writes on `%wor` and on main
lines. Examples in this document show a bullet as `•start_end•`.

**D8 — Phones of a word on `%mod` and `%pho`.** Appendix D lists every
accepted character and gives each one a role. A word other than a pause
token is accepted when every character in it is listed in Appendix D and
every character finds its place by the steps below; otherwise the word is
not accepted. Inside a phonetic group, apply the steps to each part
between spaces on its own; the group markers `‹` and `›` take no part.
Read the characters from left to right:

1. A **base glyph** (D.1) begins a new phone, unless a ligature stands
   directly before it.
2. A **combining diacritic** belongs to the phone that ends directly
   before it: after a base glyph, a diacritic or a length mark of that
   phone. U+0335 directly after a base glyph or a combining diacritic is
   a combining diacritic.
3. A **length mark** belongs to the phone that ends directly before it.
4. A **suffix diacritic** belongs to the phone that ends directly before
   it. With no phone directly before it (at the start of the part, or
   after a mark or a tone number), it is a prefix of the next base glyph,
   which must exist. A suffix diacritic followed by U+0335 is a prefix of
   the next base glyph in the part when there is one, and otherwise
   belongs to the phone before it.
5. A **prefix diacritic** is a prefix of the next base glyph in the part.
   With no base glyph after it, it belongs to the phone that ends directly
   before it. A prefix diacritic followed by U+0335 directly after a
   phone belongs to that phone.
6. A **ligature** joins the phone that ends directly before it and the
   phone that the base glyph directly after it begins into one phone.
   Both must exist, and nothing may stand between the ligature and that
   base glyph. Ligatures chain: `a͡b͡c` is one phone.
7. A run of **tone numbers** is one unit of its own. It ends the phone
   before it, so a diacritic directly after a tone number has no phone
   directly before it.
8. A **mark** (D.4: stress, syllable boundary, intra-word pause,
   compound-word marker, sandhi, intonation group) is one unit of its
   own and ends the phone before it. No two of `.`, `ˈ` and `ˌ` stand
   next to each other.

Examples: `ⁿdʰa̤ː²¹⁴` → phones `ⁿdʰ`, `a̤ː` and the tone unit `²¹⁴`;
`t͡sʰa` → `t͡sʰ`, `a`; `ʰta` → `ʰt`, `a`; `aⁿ` → `aⁿ`; `aᵐba` → `a`,
`ᵐb`, `a`; `kʰ̵a` → `k`, `ʰ̵a`. Not accepted: `a⁶̃` (a combining
diacritic after a tone number), `a͡ⁿb` (a prefix between a ligature and
its base glyph), `ta..ta` (two syllable boundaries), `kæt~` (`~` is not
listed).

### Pauses

Inter-word pauses `(.)`, `(..)`, `(...)` and `(` *number* `)` are words
(D1) on `%mod` and `%pho` and so occupy a word slot on every dependent
tier. An intra-word pause `^` is a character inside a word: it passes
through bare on `%modsyl` and `%phosyl`, it is part of the alignment text
(D3) on `%phoaln`, and it is a timed element (D4) on `%phoint`. A pause
token inside a phonetic group, as in `‹əda da (.)›`, is an error (rules
1.6, 2.7 and 3.8): the dependent tiers have no defined form for such a
word, so a validator reports the source tier and checks nothing else on
the dependent tier for that utterance.

---

## 1. Syllabification tiers — `%modsyl` and `%phosyl`

Both tiers use the same format. `%modsyl` syllabifies the model tier
`%mod`; `%phosyl` syllabifies the actual tier `%pho`.

### Grammar

    syltier ::= word (space word)*
    word    ::= pause | unit+
    unit    ::= mark | phone colon code
    mark    ::= "^" | "ˈ" | "ˌ" | "." | "+"      /* U+005E U+02C8 U+02CC U+002E U+002B */
    phone   ::= [^#x20#x3A#x5E#x2C8#x2CC#x2E#x2B]+ /* maximal run */
    code    ::= [^#x20#x3A]                      /* exactly one character */
    pause   ::= "(.)" | "(..)" | "(...)" | "(" number ")"
    number  ::= digit+ ("." digit*)? | digit+ ":" digit+ ("." digit*)?
    space   ::= #x20
    colon   ::= #x3A
    digit   ::= [#x30-#x39]

A `phone` is lexical: the longest run of characters up to the next colon,
space or mark. Rule 1.3 ties it to the source tier, where D8 defines the
phones. IPA length is written
with the modifier letter `ː` (U+02D0), never an ASCII colon, so the colon
before a code is unambiguous. A tone number such as `⁶` and a sandhi
marker `‿` or `⁀` are units, not marks: each carries a code, always `U`. A
`mark` — an intra-word pause, a stress mark, a syllable boundary or a
compound-word marker — stands bare between units and carries no code. A
pause word is the pause token alone, with no code; its `number` is
seconds, or minutes and seconds, as CHAT writes a timed pause (`(2.)`,
`(2.5)`, `(1:3.5)`).

### Legal constituent codes

The code is one character drawn from Phon's `SyllableConstituentType`
mnemonics:

| Code | Constituent | Notes |
|------|-------------|-------|
| `O` | Onset | |
| `N` | Nucleus | monophthong nucleus |
| `C` | Coda | |
| `L` | Left appendix | e.g. /s/ in an /s/-stop cluster: `s:Lt:O…` |
| `R` | Right appendix | e.g. final /z/ in a complex coda: `…v:Cz:R` |
| `E` | OEHS (onset of empty-headed syllable) | e.g. the stop element of an affricate: `d:Eʒ:O…` |
| `A` | Ambisyllabic | |
| `D` | Diphthong | a nucleus member belonging to a diphthong/triphthong; treated as a Nucleus. e.g. `o:Dʊ:D` |
| `U` | Unknown | a phone with no concrete constituent assignment; in particular the untranscribed-word marker is always written `*:U`. Also the code given to a tone number or a sandhi marker, which have no syllable role |

Phon's remaining `SyllableConstituentType` mnemonics — `B` (syllable
boundary), `S` (syllable stress), `W` (word boundary) and `T` (tone
number) — are not codes on these tiers: a boundary or stress mark stands
bare (it is a `mark`), a word boundary is the space between words, and a
tone number takes `U`.

### Rules

| Rule | Status | Check |
|------|--------|-------|
| 1.1 | error, repairable | The tier content matches `syltier` |
| 1.2 | error, repairable | Every `code` is one of `O`, `N`, `C`, `L`, `R`, `E`, `A`, `D`, `U` |
| 1.3 | error, repairable | For each position that has a word on both tiers, the word with every `colon code` removed equals the comparison text (D2) of the word at that position on the source tier (`%mod` for `%modsyl`, `%pho` for `%phosyl`) |
| 1.4 | error, repairable | The number of words equals the number of words (D1) on the source tier |
| 1.5 | error, repairable | The source tier is present in the same utterance |
| 1.6 | error | No phonetic group on the source tier contains a pause token |

### Examples

As written by Phon (`survey/writer-survey.cha`):

```
%pho:	kæt
%phosyl:	k:Oæ:Nt:C
```

A phonetic group is one word, with the markers and the inner space dropped:

```
%mod:	‹o ʁəvwaʁ›
%modsyl:	o:Nʁ:Oə:Nv:Ow:Oa:Nʁ:C
```

A tone number and a sandhi marker are units with the code `U`:

```
%pho:	ma⁶
%phosyl:	m:Oa:N⁶:U
%pho:	dʌz‿ɪt
%phosyl:	d:Oʌ:Nz:C‿:Uɪ:Nt:C
```

An intra-word pause, a stress mark, a syllable boundary and a
compound-word marker stand bare:

```
%pho:	bʌ^bʌ
%phosyl:	b:Oʌ:N^b:Oʌ:N
%pho:	ˈɹɛ.kɔɹd
%phosyl:	ˈɹ:Oɛ:N.k:Oɔ:Dɹ:Dd:C
%pho:	kæt+dɔɡ
%phosyl:	k:Oæ:Nt:C+d:Oɔ:Nɡ:C
```

An inter-word pause is a word of its own, and the untranscribed-word marker
takes `U`:

```
%mod:	kæt (.) dɔɡ
%modsyl:	k:Oæ:Nt:C (.) d:Oɔ:Nɡ:C
%pho:	də *
%phosyl:	d:Oə:N *:U
```

---

## 2. Alignment tier — `%phoaln`

`%phoaln` records Phon's phone-level alignment between the model (`%mod`)
and actual (`%pho`) transcriptions, one word at a time.

### Grammar

    alntier ::= word (space word)*
    word    ::= pair ("," pair)*
    pair    ::= side arrow side
    side    ::= [^#x20#x2C#x2194]+
    arrow   ::= #x2194
    space   ::= #x20

A `side` is one phone from the source word, one mark (`^`, stress mark,
syllable boundary, compound-word marker or tone number) from the source
word, a pause token, the untranscribed-word marker `*`, or the null
symbol `∅` (U+2205). `∅` on the
left is epenthesis (produced, not in the model); `∅` on the right is
deletion (in the model, not produced). Neither a linking tie nor a
phonetic-group marker appears on either side. Pairs inside a word are
separated by `,` (U+002C) with no surrounding space; words are separated
by single spaces.

### Rules

| Rule | Status | Check |
|------|--------|-------|
| 2.1 | error, repairable | The tier content matches `alntier` |
| 2.2 | error, repairable | No pair has `∅` on both sides |
| 2.3 | error, repairable | For each alignment word that has a slot (D5), the left sides of its pairs other than `∅`, concatenated in order, equal the alignment text (D3) of the slot's `%mod` word; for a slot with no `%mod` word, every left side is `∅` |
| 2.4 | error, repairable | For each alignment word that has a slot (D5), the right sides of its pairs other than `∅`, concatenated in order, equal the alignment text (D3) of the slot's `%pho` word; for a slot with no `%pho` word, every right side is `∅` |
| 2.5 | error, repairable | The number of alignment words equals the number of slots (D5) |
| 2.6 | error, repairable | `%mod` and `%pho` are both present in the same utterance |
| 2.7 | error | No phonetic group on `%mod` or `%pho` contains a pause token |

### Examples

As written by Phon (`survey/writer-survey.cha`). A substitution and a
deletion:

```
%mod:	ðə kæt
%pho:	də kæt
%phoaln:	ð↔d,ə↔ə k↔k,æ↔æ,t↔t
%mod:	stʊd
%pho:	tʊd
%phoaln:	s↔∅,t↔t,ʊ↔ʊ,d↔d
```

A pause on both tiers is one slot; a pause on one tier is a slot of its
own, so the alignment has one word more than `%pho`:

```
%mod:	kæt (.) dɔɡ
%pho:	kæt (.) dɔɡ
%phoaln:	k↔k,æ↔æ,t↔t (.)↔(.) d↔d,ɔ↔ɔ,ɡ↔ɡ
%mod:	kæt (.) dɔɡ
%pho:	kæt dɔɡ
%phoaln:	k↔k,æ↔æ,t↔t (.)↔∅ d↔d,ɔ↔ɔ,ɡ↔ɡ
```

The untranscribed-word marker is aligned as two pairs; each side still
rebuilds its word:

```
%mod:	ðə *
%pho:	də *
%phoaln:	ð↔d,ə↔ə ∅↔*,*↔∅
```

Stress marks, syllable boundaries, the intra-word pause and the
compound-word marker have columns of their own; a linking tie has none:

```
%mod:	kæt+dɔɡ
%pho:	kæt+dɔɡ
%phoaln:	k↔k,æ↔æ,t↔t,+↔+,d↔d,ɔ↔ɔ,ɡ↔ɡ
%mod:	ˈɹɛkɔɹd
%pho:	ˈɹɛ.kɔɹd
%phoaln:	ˈ↔ˈ,ɹ↔ɹ,ɛ↔ɛ,∅↔.,k↔k,ɔ↔ɔ,ɹ↔ɹ,d↔d
%mod:	bʌ^bʌ
%pho:	bʌ^bʌ
%phoaln:	b↔b,ʌ↔ʌ,^↔^,b↔b,ʌ↔ʌ
%mod:	dʌz‿ɪt
%pho:	dʌz‿ɪt
%phoaln:	d↔d,ʌ↔ʌ,z↔z,ɪ↔ɪ,t↔t
```

---

## 3. Interval tier — `%phoint`

`%phoint` gives the time interval of each timed element (D4) of the `%pho`
tier: phone-level bullets, analogous to the word-level timing on `%wor`.

### Grammar

    inttier ::= group (space "/" space group)*
    group   ::= token (space token)*
    token   ::= text space bullet
    text    ::= [^#x20#x15]+
    bullet  ::= #x15 digit+ "_" digit+ #x15
    space   ::= #x20
    digit   ::= [#x30-#x39]

Groups are the words of `%pho`, in order. Each token is one timed element
(D4) of the word followed by its interval. The word separator is ` / `
(space, U+002F, space) because spaces already separate tokens inside a
group. Start and end are non-negative integer millisecond offsets.

### Rules

| Rule | Status | Check |
|------|--------|-------|
| 3.1 | error | The tier content matches `inttier` |
| 3.2 | error | For each position that has both a group and a `%pho` word, the `text` of the group's tokens, in order, equal the timed elements (D4) of the word |
| 3.3 | error | In every bullet, start is less than end |
| 3.4 | error | Every interval after the first starts no earlier than 1 ms before the end of the interval before it, across group boundaries |
| 3.5 | error | When the main line ends with a bullet (D6), the first interval starts no earlier than 1 ms before the record start, and the last interval ends no later than 1 ms after the record end |
| 3.6 | error | The number of groups equals the number of words (D1) on `%pho` |
| 3.7 | error | `%pho` is present in the same utterance |
| 3.8 | error | No phonetic group on `%pho` contains a pause token |

#### Why 1 ms

Phon stores every boundary as a floating-point number of seconds and
rounds each one to milliseconds on export, and the record interval is
converted by a separate path. Two boundaries that are equal in principle
can therefore differ by 1 ms in the file. Rules 3.4 and 3.5 allow that
difference. Rule 3.4 has no other tolerance: an interval that starts 2 ms
or more before the previous end is an error, and so is an interval that
starts before the previous start. Gaps between intervals are not an error;
contiguity is not a rule.

### Examples

Bullets are shown as `•start_end•`; in a file each `•` is the byte `0x15`.
`%phoint` is generated by the Phon application rather than by its CHAT
writer, so these examples are illustrative; the shared example set holds
files as Phon writes them. Two words (`%pho:	twʌ̾z bɹɪlɪɡ …`):

```
%phoint:	t •0_110• w •110_220• ʌ̾ •220_330• z •330_440• / b •440_513• …
```

An intra-word pause is a token; an inter-word pause is a group of its own:

```
%pho:	bʌ^bʌ (.) …
%phoint:	b •440_530• ʌ •530_620• ^ •620_710• b •710_800• ʌ •800_890• / (.) •890_1140• / …
```

A geminate is one token:

```
%pho:	bʌtt
%phoint:	b •0_100• ʌ •100_200• tt •200_400•
```

---

## Appendix A: Legacy `%x` tier names

Phon releases before 4.0 wrote these tiers as `%xmodsyl`, `%xphosyl`,
`%xphoaln` and `%xphoint`. Those names are not part of this
specification. A reader may accept each `x` form as an alias of the
corresponding name above and apply the same rules to its content. A
conforming writer never produces an `x` form.

## Appendix B: Changelog

### 1.0

First versioned release. Relative to the July 2026 draft:

- Final names `%modsyl`, `%phosyl`, `%phoaln`, `%phoint`; `x` forms moved to Appendix A.
- Formal grammars for each tier; `phone` defined lexically.
- Rules split so that each states one check; numbers are permanent.
- New rules 1.5, 2.6, 3.7 (presence of source tiers); rule 3.6 (group count) split out of the draft's section 3 rule 2.
- Rule 2.2 now states only the `∅↔∅` check; the shape of a pair is covered by the grammar (rule 2.1).
- Marks on the syllabification tiers enumerated: `^`, `ˈ`, `ˌ`, `.`, `+`.
- Rule 3.4 now measures each start against the previous end, with a 1 ms allowance; rule 3.5 (fit inside the record interval, 1 ms allowance) split out of it. Contiguity is not a rule.
- Status (error / error, repairable) assigned to every rule.
- Definitions D1 to D8 added.
- Appendix D lists every character accepted on `%mod` and `%pho`; D8 defines how they form phones.
- A pause token inside a phonetic group is an error: rules 1.6, 2.7 and 3.8.

## Appendix C: Rule index

One row per rule, with the smallest input that breaks that rule and no
other when the rest of the utterance is the `cat` example of section 1
(`%mod:	kæt`, `%pho:	kæt`, `%phoaln:	k↔k,æ↔æ,t↔t`,
`%phoint:	k •0_100• æ •100_200• t •200_300•`, main line bullet
`•0_300•`). Bullets are shown as `•…•`; in a file they are `0x15 … 0x15`.
The shared example set has at least one file per row.

| Rule | Name | Status | Minimal breaking input (everything else valid) |
|------|------|--------|-----------------------------------------------|
| 1.1 | Syllabification grammar | error, repairable | `%phosyl:	kæt` (no codes) |
| 1.2 | Legal constituent code | error, repairable | `%phosyl:	k:Oæ:Nt:T` |
| 1.3 | Unit text matches the source word | error, repairable | `%pho:	kæt` with `%phosyl:	k:Oɛ:Nt:C` |
| 1.4 | Word count matches the source tier | error, repairable | `%pho:	kæt` with `%phosyl:	k:Oæ:Nt:C k:Oæ:Nt:C` |
| 1.5 | Source tier present | error, repairable | `%phosyl` present, no `%pho` (and no `%phoaln` or `%phoint`) |
| 1.6 | No pause inside a phonetic group on the source tier | error | `%pho:	‹kæ (.) t›` with `%phosyl:	k:Oæ:Nt:C` (and no `%phoaln` or `%phoint`) |
| 2.1 | Alignment grammar | error, repairable | `%phoaln:	k↔k,æ↔` |
| 2.2 | No null pair | error, repairable | `%phoaln:	k↔k,∅↔∅,æ↔æ,t↔t` |
| 2.3 | Left sides rebuild the `%mod` word | error, repairable | `%mod:	kæt` with `%phoaln:	k↔k,ɛ↔æ,t↔t` |
| 2.4 | Right sides rebuild the `%pho` word | error, repairable | `%pho:	kæt` with `%phoaln:	k↔k,æ↔ɛ,t↔t` |
| 2.5 | Alignment word count matches the slots | error, repairable | `%mod:	kæt dɔɡ`, `%pho:	kæt dɔɡ` (two words on every tier) with one alignment word `k↔k,æ↔æ,t↔t` |
| 2.6 | Source tiers present | error, repairable | `%phoaln` with `%pho` and no `%mod` (and no `%modsyl`) |
| 2.7 | No pause inside a phonetic group on `%mod` or `%pho` | error | `%pho:	‹kæ (.) t›` with `%phoaln:	k↔k,æ↔æ,t↔t` (and no `%phosyl` or `%phoint`) |
| 3.1 | Interval grammar | error | `%phoint:	k •0_100• æ •100_200• t` |
| 3.2 | Token text matches the timed element | error | `%pho:	kæt` with `%phoint:	k •0_100• æ •100_200• d •200_300•` |
| 3.3 | Start before end | error | `%phoint:	k •100_100• æ •100_200• t •200_300•` |
| 3.4 | Start before the previous end | error | `%phoint:	k •0_100• æ •200_300• t •50_150•` (Chatter's sample) |
| 3.5 | Fit inside the record interval | error | main line `•0_300•` with `%phoint:	k •0_100• æ •100_200• t •200_302•` |
| 3.6 | Group count matches `%pho` | error | `%pho:	kæt dɔɡ` (two words on every tier) with one group |
| 3.7 | `%pho` present | error | `%phoint` present, no `%pho` (and no `%phosyl` or `%phoaln`) |
| 3.8 | No pause inside a phonetic group on `%pho` | error | `%pho:	‹kæ (.) t›` with `%phoint:	k •0_100• æ •100_200• t •200_300•` (and no `%phosyl` or `%phoaln`) |

## Appendix D: IPA characters

This appendix is normative. It lists every character that a word on
`%mod` or `%pho` may hold, with its role in D8. A character not listed
here is not accepted. The list is taken from Phon's IPA parser (Phon 4.2):
every Unicode code point was passed through it, and each one it accepts
on its own is listed, except the characters excluded below. The colon of
a timed pause token is added, since the `pause` production allows it.

The tables are generated from `data/ipa-characters.tsv` by
`scripts/gen_ipa_table.py`; change the data file and run the script,
never the tables. Combining characters are shown on a dotted circle
`◌` (U+25CC), which is not part of them.

Where a character may stand:

- **Base glyphs** (D.1) begin a phone. Of the cover symbols, `*` is the
  untranscribed-word marker, `∅` (U+2205) the empty set, and the capital
  letters `A`–`Z` stand for a class of phones.
- **Diacritics** (D.2) attach to a phone by D8.
- **Tone numbers** (D.3) form a tone unit (D8 step 7).
- **Marks and separators** (D.4) stand between phones (D8 step 8). The
  space separates words (D1); `‹` and `›` delimit a phonetic group.
- **Pause tokens** (D.5): `(`, `)`, `:` and the digits stand only inside
  a pause token (D1, the `pause` production of section 1), and `.` stands
  there or as a syllable boundary. A pause token is a word of its own.

Excluded. These characters appear in Phon's character tables or are
read by its parser, but they are not accepted on `%mod` or `%pho`:

| Code point | Character | Reason |
|------------|-----------|--------|
| U+005C | `\` | Phon query syntax (a reference to a matched group) |
| U+007B | `{` | Phon query syntax (a named group) |
| U+007D | `}` | Phon query syntax (a named group) |
| U+2194 | `↔` | The alignment marker of `%phoaln`, not part of a transcription |
| U+0009, U+000A, U+000D | (tab, line feed, carriage return) | CHAT line structure; only the space separates words |
| U+FF0E | `．` | The parser reports it as an invalid token |
| U+007E | `~` | Listed in Phon's older character table but not accepted by its parser |

<!-- BEGIN ipa-characters: generated by scripts/gen_ipa_table.py -->

400 characters in all.

### D.1 Base glyphs (188)

**Consonants** (116)

| Code point | Character | Unicode name |
|------------|-----------|--------------|
| U+0062 | `b` | LATIN SMALL LETTER B |
| U+0063 | `c` | LATIN SMALL LETTER C |
| U+0064 | `d` | LATIN SMALL LETTER D |
| U+0066 | `f` | LATIN SMALL LETTER F |
| U+0067 | `g` | LATIN SMALL LETTER G |
| U+0068 | `h` | LATIN SMALL LETTER H |
| U+006B | `k` | LATIN SMALL LETTER K |
| U+006C | `l` | LATIN SMALL LETTER L |
| U+006D | `m` | LATIN SMALL LETTER M |
| U+006E | `n` | LATIN SMALL LETTER N |
| U+0070 | `p` | LATIN SMALL LETTER P |
| U+0071 | `q` | LATIN SMALL LETTER Q |
| U+0072 | `r` | LATIN SMALL LETTER R |
| U+0073 | `s` | LATIN SMALL LETTER S |
| U+0074 | `t` | LATIN SMALL LETTER T |
| U+0076 | `v` | LATIN SMALL LETTER V |
| U+0078 | `x` | LATIN SMALL LETTER X |
| U+007A | `z` | LATIN SMALL LETTER Z |
| U+00A1 | `¡` | INVERTED EXCLAMATION MARK |
| U+00E7 | `ç` | LATIN SMALL LETTER C WITH CEDILLA |
| U+00F0 | `ð` | LATIN SMALL LETTER ETH |
| U+0127 | `ħ` | LATIN SMALL LETTER H WITH STROKE |
| U+014B | `ŋ` | LATIN SMALL LETTER ENG |
| U+0180 | `ƀ` | LATIN SMALL LETTER B WITH STROKE |
| U+0188 | `ƈ` | LATIN SMALL LETTER C WITH HOOK |
| U+0192 | `ƒ` | LATIN SMALL LETTER F WITH HOOK |
| U+0199 | `ƙ` | LATIN SMALL LETTER K WITH HOOK |
| U+019B | `ƛ` | LATIN SMALL LETTER LAMBDA WITH STROKE |
| U+019E | `ƞ` | LATIN SMALL LETTER N WITH LONG RIGHT LEG |
| U+01A5 | `ƥ` | LATIN SMALL LETTER P WITH HOOK |
| U+01AA | `ƪ` | LATIN LETTER REVERSED ESH LOOP |
| U+01AB | `ƫ` | LATIN SMALL LETTER T WITH PALATAL HOOK |
| U+01AD | `ƭ` | LATIN SMALL LETTER T WITH HOOK |
| U+01B9 | `ƹ` | LATIN SMALL LETTER EZH REVERSED |
| U+01BA | `ƺ` | LATIN SMALL LETTER EZH WITH TAIL |
| U+01C0 | `ǀ` | LATIN LETTER DENTAL CLICK |
| U+01C1 | `ǁ` | LATIN LETTER LATERAL CLICK |
| U+01C2 | `ǂ` | LATIN LETTER ALVEOLAR CLICK |
| U+01C3 | `ǃ` | LATIN LETTER RETROFLEX CLICK |
| U+0234 | `ȴ` | LATIN SMALL LETTER L WITH CURL |
| U+0235 | `ȵ` | LATIN SMALL LETTER N WITH CURL |
| U+0236 | `ȶ` | LATIN SMALL LETTER T WITH CURL |
| U+0253 | `ɓ` | LATIN SMALL LETTER B WITH HOOK |
| U+0255 | `ɕ` | LATIN SMALL LETTER C WITH CURL |
| U+0256 | `ɖ` | LATIN SMALL LETTER D WITH TAIL |
| U+0257 | `ɗ` | LATIN SMALL LETTER D WITH HOOK |
| U+025F | `ɟ` | LATIN SMALL LETTER DOTLESS J WITH STROKE |
| U+0260 | `ɠ` | LATIN SMALL LETTER G WITH HOOK |
| U+0261 | `ɡ` | LATIN SMALL LETTER SCRIPT G |
| U+0262 | `ɢ` | LATIN LETTER SMALL CAPITAL G |
| U+0263 | `ɣ` | LATIN SMALL LETTER GAMMA |
| U+0266 | `ɦ` | LATIN SMALL LETTER H WITH HOOK |
| U+0267 | `ɧ` | LATIN SMALL LETTER HENG WITH HOOK |
| U+026B | `ɫ` | LATIN SMALL LETTER L WITH MIDDLE TILDE |
| U+026C | `ɬ` | LATIN SMALL LETTER L WITH BELT |
| U+026D | `ɭ` | LATIN SMALL LETTER L WITH RETROFLEX HOOK |
| U+026E | `ɮ` | LATIN SMALL LETTER LEZH |
| U+0271 | `ɱ` | LATIN SMALL LETTER M WITH HOOK |
| U+0272 | `ɲ` | LATIN SMALL LETTER N WITH LEFT HOOK |
| U+0273 | `ɳ` | LATIN SMALL LETTER N WITH RETROFLEX HOOK |
| U+0274 | `ɴ` | LATIN LETTER SMALL CAPITAL N |
| U+0278 | `ɸ` | LATIN SMALL LETTER PHI |
| U+0279 | `ɹ` | LATIN SMALL LETTER TURNED R |
| U+027A | `ɺ` | LATIN SMALL LETTER TURNED R WITH LONG LEG |
| U+027B | `ɻ` | LATIN SMALL LETTER TURNED R WITH HOOK |
| U+027C | `ɼ` | LATIN SMALL LETTER R WITH LONG LEG |
| U+027D | `ɽ` | LATIN SMALL LETTER R WITH TAIL |
| U+027E | `ɾ` | LATIN SMALL LETTER R WITH FISHHOOK |
| U+027F | `ɿ` | LATIN SMALL LETTER REVERSED R WITH FISHHOOK |
| U+0280 | `ʀ` | LATIN LETTER SMALL CAPITAL R |
| U+0281 | `ʁ` | LATIN LETTER SMALL CAPITAL INVERTED R |
| U+0282 | `ʂ` | LATIN SMALL LETTER S WITH HOOK |
| U+0283 | `ʃ` | LATIN SMALL LETTER ESH |
| U+0286 | `ʆ` | LATIN SMALL LETTER ESH WITH CURL |
| U+0287 | `ʇ` | LATIN SMALL LETTER TURNED T |
| U+0288 | `ʈ` | LATIN SMALL LETTER T WITH RETROFLEX HOOK |
| U+028B | `ʋ` | LATIN SMALL LETTER V WITH HOOK |
| U+028D | `ʍ` | LATIN SMALL LETTER TURNED W |
| U+028E | `ʎ` | LATIN SMALL LETTER TURNED Y |
| U+0290 | `ʐ` | LATIN SMALL LETTER Z WITH RETROFLEX HOOK |
| U+0291 | `ʑ` | LATIN SMALL LETTER Z WITH CURL |
| U+0292 | `ʒ` | LATIN SMALL LETTER EZH |
| U+0293 | `ʓ` | LATIN SMALL LETTER EZH WITH CURL |
| U+0294 | `ʔ` | LATIN LETTER GLOTTAL STOP |
| U+0295 | `ʕ` | LATIN LETTER PHARYNGEAL VOICED FRICATIVE |
| U+0296 | `ʖ` | LATIN LETTER INVERTED GLOTTAL STOP |
| U+0297 | `ʗ` | LATIN LETTER STRETCHED C |
| U+0298 | `ʘ` | LATIN LETTER BILABIAL CLICK |
| U+0299 | `ʙ` | LATIN LETTER SMALL CAPITAL B |
| U+029B | `ʛ` | LATIN LETTER SMALL CAPITAL G WITH HOOK |
| U+029C | `ʜ` | LATIN LETTER SMALL CAPITAL H |
| U+029D | `ʝ` | LATIN SMALL LETTER J WITH CROSSED-TAIL |
| U+029E | `ʞ` | LATIN SMALL LETTER TURNED K |
| U+029F | `ʟ` | LATIN LETTER SMALL CAPITAL L |
| U+02A0 | `ʠ` | LATIN SMALL LETTER Q WITH HOOK |
| U+02A1 | `ʡ` | LATIN LETTER GLOTTAL STOP WITH STROKE |
| U+02A2 | `ʢ` | LATIN LETTER REVERSED GLOTTAL STOP WITH STROKE |
| U+02A3 | `ʣ` | LATIN SMALL LETTER DZ DIGRAPH |
| U+02A4 | `ʤ` | LATIN SMALL LETTER DEZH DIGRAPH |
| U+02A5 | `ʥ` | LATIN SMALL LETTER DZ DIGRAPH WITH CURL |
| U+02A6 | `ʦ` | LATIN SMALL LETTER TS DIGRAPH |
| U+02A7 | `ʧ` | LATIN SMALL LETTER TESH DIGRAPH |
| U+02A8 | `ʨ` | LATIN SMALL LETTER TC DIGRAPH WITH CURL |
| U+02A9 | `ʩ` | LATIN SMALL LETTER FENG DIGRAPH |
| U+02AA | `ʪ` | LATIN SMALL LETTER LS DIGRAPH |
| U+02AB | `ʫ` | LATIN SMALL LETTER LZ DIGRAPH |
| U+02AC | `ʬ` | LATIN LETTER BILABIAL PERCUSSIVE |
| U+02AD | `ʭ` | LATIN LETTER BIDENTAL PERCUSSIVE |
| U+03B2 | `β` | GREEK SMALL LETTER BETA |
| U+03B4 | `δ` | GREEK SMALL LETTER DELTA |
| U+03B8 | `θ` | GREEK SMALL LETTER THETA |
| U+03BB | `λ` | GREEK SMALL LETTER LAMDA |
| U+03C0 | `π` | GREEK SMALL LETTER PI |
| U+03C7 | `χ` | GREEK SMALL LETTER CHI |
| U+1D91 | `ᶑ` | LATIN SMALL LETTER D WITH HOOK AND TAIL |
| U+2C71 | `ⱱ` | LATIN SMALL LETTER V WITH RIGHT HOOK |

**Vowels** (38)

| Code point | Character | Unicode name |
|------------|-----------|--------------|
| U+0061 | `a` | LATIN SMALL LETTER A |
| U+0065 | `e` | LATIN SMALL LETTER E |
| U+0069 | `i` | LATIN SMALL LETTER I |
| U+006F | `o` | LATIN SMALL LETTER O |
| U+0075 | `u` | LATIN SMALL LETTER U |
| U+0079 | `y` | LATIN SMALL LETTER Y |
| U+00E6 | `æ` | LATIN SMALL LETTER AE |
| U+00F8 | `ø` | LATIN SMALL LETTER O WITH STROKE |
| U+0131 | `ı` | LATIN SMALL LETTER DOTLESS I |
| U+0153 | `œ` | LATIN SMALL LIGATURE OE |
| U+0250 | `ɐ` | LATIN SMALL LETTER TURNED A |
| U+0251 | `ɑ` | LATIN SMALL LETTER ALPHA |
| U+0252 | `ɒ` | LATIN SMALL LETTER TURNED ALPHA |
| U+0254 | `ɔ` | LATIN SMALL LETTER OPEN O |
| U+0258 | `ɘ` | LATIN SMALL LETTER REVERSED E |
| U+0259 | `ə` | LATIN SMALL LETTER SCHWA |
| U+025A | `ɚ` | LATIN SMALL LETTER SCHWA WITH HOOK |
| U+025B | `ɛ` | LATIN SMALL LETTER OPEN E |
| U+025C | `ɜ` | LATIN SMALL LETTER REVERSED OPEN E |
| U+025D | `ɝ` | LATIN SMALL LETTER REVERSED OPEN E WITH HOOK |
| U+025E | `ɞ` | LATIN SMALL LETTER CLOSED REVERSED OPEN E |
| U+0264 | `ɤ` | LATIN SMALL LETTER RAMS HORN |
| U+0268 | `ɨ` | LATIN SMALL LETTER I WITH STROKE |
| U+0269 | `ɩ` | LATIN SMALL LETTER IOTA |
| U+026A | `ɪ` | LATIN LETTER SMALL CAPITAL I |
| U+026F | `ɯ` | LATIN SMALL LETTER TURNED M |
| U+0275 | `ɵ` | LATIN SMALL LETTER BARRED O |
| U+0276 | `ɶ` | LATIN LETTER SMALL CAPITAL OE |
| U+0277 | `ɷ` | LATIN SMALL LETTER CLOSED OMEGA |
| U+0284 | `ʄ` | LATIN SMALL LETTER DOTLESS J WITH STROKE AND HOOK |
| U+0285 | `ʅ` | LATIN SMALL LETTER SQUAT REVERSED ESH |
| U+0289 | `ʉ` | LATIN SMALL LETTER U BAR |
| U+028A | `ʊ` | LATIN SMALL LETTER UPSILON |
| U+028C | `ʌ` | LATIN SMALL LETTER TURNED V |
| U+028F | `ʏ` | LATIN LETTER SMALL CAPITAL Y |
| U+029A | `ʚ` | LATIN SMALL LETTER CLOSED OPEN E |
| U+02AE | `ʮ` | LATIN SMALL LETTER TURNED H WITH FISHHOOK |
| U+03B1 | `α` | GREEK SMALL LETTER ALPHA |

**Glides** (5)

| Code point | Character | Unicode name |
|------------|-----------|--------------|
| U+003E | `>` | GREATER-THAN SIGN |
| U+006A | `j` | LATIN SMALL LETTER J |
| U+0077 | `w` | LATIN SMALL LETTER W |
| U+0265 | `ɥ` | LATIN SMALL LETTER TURNED H |
| U+0270 | `ɰ` | LATIN SMALL LETTER TURNED M WITH LONG LEG |

**Cover symbols** (29)

| Code point | Character | Unicode name |
|------------|-----------|--------------|
| U+002A | `*` | ASTERISK |
| U+0041 | `A` | LATIN CAPITAL LETTER A |
| U+0042 | `B` | LATIN CAPITAL LETTER B |
| U+0043 | `C` | LATIN CAPITAL LETTER C |
| U+0044 | `D` | LATIN CAPITAL LETTER D |
| U+0045 | `E` | LATIN CAPITAL LETTER E |
| U+0046 | `F` | LATIN CAPITAL LETTER F |
| U+0047 | `G` | LATIN CAPITAL LETTER G |
| U+0048 | `H` | LATIN CAPITAL LETTER H |
| U+0049 | `I` | LATIN CAPITAL LETTER I |
| U+004A | `J` | LATIN CAPITAL LETTER J |
| U+004B | `K` | LATIN CAPITAL LETTER K |
| U+004C | `L` | LATIN CAPITAL LETTER L |
| U+004D | `M` | LATIN CAPITAL LETTER M |
| U+004E | `N` | LATIN CAPITAL LETTER N |
| U+004F | `O` | LATIN CAPITAL LETTER O |
| U+0050 | `P` | LATIN CAPITAL LETTER P |
| U+0051 | `Q` | LATIN CAPITAL LETTER Q |
| U+0052 | `R` | LATIN CAPITAL LETTER R |
| U+0053 | `S` | LATIN CAPITAL LETTER S |
| U+0054 | `T` | LATIN CAPITAL LETTER T |
| U+0055 | `U` | LATIN CAPITAL LETTER U |
| U+0056 | `V` | LATIN CAPITAL LETTER V |
| U+0057 | `W` | LATIN CAPITAL LETTER W |
| U+0058 | `X` | LATIN CAPITAL LETTER X |
| U+0059 | `Y` | LATIN CAPITAL LETTER Y |
| U+005A | `Z` | LATIN CAPITAL LETTER Z |
| U+2205 | `∅` | EMPTY SET |
| U+25CC | `◌` | DOTTED CIRCLE |

### D.2 Diacritics (177)

**Prefix diacritics** (7)

| Code point | Character | Unicode name |
|------------|-----------|--------------|
| U+1D50 | `ᵐ` | MODIFIER LETTER SMALL M |
| U+1D51 | `ᵑ` | MODIFIER LETTER SMALL ENG |
| U+1DAC | `ᶬ` | MODIFIER LETTER SMALL M WITH HOOK |
| U+1DAE | `ᶮ` | MODIFIER LETTER SMALL N WITH LEFT HOOK |
| U+1DAF | `ᶯ` | MODIFIER LETTER SMALL N WITH RETROFLEX HOOK |
| U+1DB0 | `ᶰ` | MODIFIER LETTER SMALL CAPITAL N |
| U+207F | `ⁿ` | SUPERSCRIPT LATIN SMALL LETTER N |

**Suffix diacritics** (56)

| Code point | Character | Unicode name |
|------------|-----------|--------------|
| U+02B0 | `ʰ` | MODIFIER LETTER SMALL H |
| U+02B1 | `ʱ` | MODIFIER LETTER SMALL H WITH HOOK |
| U+02B2 | `ʲ` | MODIFIER LETTER SMALL J |
| U+02B3 | `ʳ` | MODIFIER LETTER SMALL R |
| U+02B4 | `ʴ` | MODIFIER LETTER SMALL TURNED R |
| U+02B5 | `ʵ` | MODIFIER LETTER SMALL TURNED R WITH HOOK |
| U+02B6 | `ʶ` | MODIFIER LETTER SMALL CAPITAL INVERTED R |
| U+02B7 | `ʷ` | MODIFIER LETTER SMALL W |
| U+02B8 | `ʸ` | MODIFIER LETTER SMALL Y |
| U+02BB | `ʻ` | MODIFIER LETTER TURNED COMMA |
| U+02BC | `ʼ` | MODIFIER LETTER APOSTROPHE |
| U+02BD | `ʽ` | MODIFIER LETTER REVERSED COMMA |
| U+02BE | `ʾ` | MODIFIER LETTER RIGHT HALF RING |
| U+02BF | `ʿ` | MODIFIER LETTER LEFT HALF RING |
| U+02C0 | `ˀ` | MODIFIER LETTER GLOTTAL STOP |
| U+02C1 | `ˁ` | MODIFIER LETTER REVERSED GLOTTAL STOP |
| U+02C2 | `˂` | MODIFIER LETTER LEFT ARROWHEAD |
| U+02C3 | `˃` | MODIFIER LETTER RIGHT ARROWHEAD |
| U+02C4 | `˄` | MODIFIER LETTER UP ARROWHEAD |
| U+02C5 | `˅` | MODIFIER LETTER DOWN ARROWHEAD |
| U+02D6 | `˖` | MODIFIER LETTER PLUS SIGN |
| U+02D7 | `˗` | MODIFIER LETTER MINUS SIGN |
| U+02DC | `˜` | SMALL TILDE |
| U+02DE | `˞` | MODIFIER LETTER RHOTIC HOOK |
| U+02E0 | `ˠ` | MODIFIER LETTER SMALL GAMMA |
| U+02E1 | `ˡ` | MODIFIER LETTER SMALL L |
| U+02E2 | `ˢ` | MODIFIER LETTER SMALL S |
| U+02E3 | `ˣ` | MODIFIER LETTER SMALL X |
| U+02E4 | `ˤ` | MODIFIER LETTER SMALL REVERSED GLOTTAL STOP |
| U+02E5 | `˥` | MODIFIER LETTER EXTRA-HIGH TONE BAR |
| U+02E6 | `˦` | MODIFIER LETTER HIGH TONE BAR |
| U+02E7 | `˧` | MODIFIER LETTER MID TONE BAR |
| U+02E8 | `˨` | MODIFIER LETTER LOW TONE BAR |
| U+02E9 | `˩` | MODIFIER LETTER EXTRA-LOW TONE BAR |
| U+02EC | `ˬ` | MODIFIER LETTER VOICING |
| U+02ED | `˭` | MODIFIER LETTER UNASPIRATED |
| U+02EF | `˯` | MODIFIER LETTER LOW DOWN ARROWHEAD |
| U+02F0 | `˰` | MODIFIER LETTER LOW UP ARROWHEAD |
| U+02F1 | `˱` | MODIFIER LETTER LOW LEFT ARROWHEAD |
| U+02F2 | `˲` | MODIFIER LETTER LOW RIGHT ARROWHEAD |
| U+1D47 | `ᵇ` | MODIFIER LETTER SMALL B |
| U+1D48 | `ᵈ` | MODIFIER LETTER SMALL D |
| U+1D4A | `ᵊ` | MODIFIER LETTER SMALL SCHWA |
| U+1D4D | `ᵍ` | MODIFIER LETTER SMALL G |
| U+1D4F | `ᵏ` | MODIFIER LETTER SMALL K |
| U+1D56 | `ᵖ` | MODIFIER LETTER SMALL P |
| U+1D57 | `ᵗ` | MODIFIER LETTER SMALL T |
| U+1DA6 | `ᶦ` | MODIFIER LETTER SMALL CAPITAL I |
| U+1DB4 | `ᶴ` | MODIFIER LETTER SMALL ESH |
| U+1DB7 | `ᶷ` | MODIFIER LETTER SMALL UPSILON |
| U+1DBB | `ᶻ` | MODIFIER LETTER SMALL Z |
| U+1DBE | `ᶾ` | MODIFIER LETTER SMALL EZH |
| U+1DBF | `ᶿ` | MODIFIER LETTER SMALL THETA |
| U+207C | `⁼` | SUPERSCRIPT EQUALS SIGN |
| U+A71D | `ꜝ` | MODIFIER LETTER RAISED EXCLAMATION MARK |
| U+A71E | `ꜞ` | MODIFIER LETTER RAISED INVERTED EXCLAMATION MARK |

**Combining diacritics** (108)

| Code point | Character | Unicode name |
|------------|-----------|--------------|
| U+02C6 | `ˆ` | MODIFIER LETTER CIRCUMFLEX ACCENT |
| U+02C7 | `ˇ` | CARON |
| U+02C9 | `ˉ` | MODIFIER LETTER MACRON |
| U+02CA | `ˊ` | MODIFIER LETTER ACUTE ACCENT |
| U+02CB | `ˋ` | MODIFIER LETTER GRAVE ACCENT |
| U+02D4 | `˔` | MODIFIER LETTER UP TACK |
| U+02D5 | `˕` | MODIFIER LETTER DOWN TACK |
| U+02F5 | `˵` | MODIFIER LETTER MIDDLE DOUBLE GRAVE ACCENT |
| U+02F6 | `˶` | MODIFIER LETTER MIDDLE DOUBLE ACUTE ACCENT |
| U+02F8 | `˸` | MODIFIER LETTER RAISED COLON |
| U+02F9 | `˹` | MODIFIER LETTER BEGIN HIGH TONE |
| U+02FA | `˺` | MODIFIER LETTER END HIGH TONE |
| U+02FB | `˻` | MODIFIER LETTER BEGIN LOW TONE |
| U+02FC | `˼` | MODIFIER LETTER END LOW TONE |
| U+02FD | `˽` | MODIFIER LETTER SHELF |
| U+02FE | `˾` | MODIFIER LETTER OPEN SHELF |
| U+02FF | `˿` | MODIFIER LETTER LOW LEFT ARROW |
| U+0300 | `◌̀` | COMBINING GRAVE ACCENT |
| U+0301 | `◌́` | COMBINING ACUTE ACCENT |
| U+0302 | `◌̂` | COMBINING CIRCUMFLEX ACCENT |
| U+0303 | `◌̃` | COMBINING TILDE |
| U+0304 | `◌̄` | COMBINING MACRON |
| U+0306 | `◌̆` | COMBINING BREVE |
| U+0307 | `◌̇` | COMBINING DOT ABOVE |
| U+0308 | `◌̈` | COMBINING DIAERESIS |
| U+0309 | `◌̉` | COMBINING HOOK ABOVE |
| U+030A | `◌̊` | COMBINING RING ABOVE |
| U+030B | `◌̋` | COMBINING DOUBLE ACUTE ACCENT |
| U+030C | `◌̌` | COMBINING CARON |
| U+030F | `◌̏` | COMBINING DOUBLE GRAVE ACCENT |
| U+0310 | `◌̐` | COMBINING CANDRABINDU |
| U+0311 | `◌̑` | COMBINING INVERTED BREVE |
| U+0312 | `◌̒` | COMBINING TURNED COMMA ABOVE |
| U+0314 | `◌̔` | COMBINING REVERSED COMMA ABOVE |
| U+0316 | `◌̖` | COMBINING GRAVE ACCENT BELOW |
| U+0318 | `◌̘` | COMBINING LEFT TACK BELOW |
| U+0319 | `◌̙` | COMBINING RIGHT TACK BELOW |
| U+031A | `◌̚` | COMBINING LEFT ANGLE ABOVE |
| U+031C | `◌̜` | COMBINING LEFT HALF RING BELOW |
| U+031D | `◌̝` | COMBINING UP TACK BELOW |
| U+031E | `◌̞` | COMBINING DOWN TACK BELOW |
| U+031F | `◌̟` | COMBINING PLUS SIGN BELOW |
| U+0320 | `◌̠` | COMBINING MINUS SIGN BELOW |
| U+0321 | `◌̡` | COMBINING PALATALIZED HOOK BELOW |
| U+0322 | `◌̢` | COMBINING RETROFLEX HOOK BELOW |
| U+0323 | `◌̣` | COMBINING DOT BELOW |
| U+0324 | `◌̤` | COMBINING DIAERESIS BELOW |
| U+0325 | `◌̥` | COMBINING RING BELOW |
| U+0329 | `◌̩` | COMBINING VERTICAL LINE BELOW |
| U+032A | `◌̪` | COMBINING BRIDGE BELOW |
| U+032B | `◌̫` | COMBINING INVERTED DOUBLE ARCH BELOW |
| U+032C | `◌̬` | COMBINING CARON BELOW |
| U+032E | `◌̮` | COMBINING BREVE BELOW |
| U+032F | `◌̯` | COMBINING INVERTED BREVE BELOW |
| U+0330 | `◌̰` | COMBINING TILDE BELOW |
| U+0331 | `◌̱` | COMBINING MACRON BELOW |
| U+0332 | `◌̲` | COMBINING LOW LINE |
| U+0333 | `◌̳` | COMBINING DOUBLE LOW LINE |
| U+0334 | `◌̴` | COMBINING TILDE OVERLAY |
| U+0339 | `◌̹` | COMBINING RIGHT HALF RING BELOW |
| U+033A | `◌̺` | COMBINING INVERTED BRIDGE BELOW |
| U+033B | `◌̻` | COMBINING SQUARE BELOW |
| U+033C | `◌̼` | COMBINING SEAGULL BELOW |
| U+033D | `◌̽` | COMBINING X ABOVE |
| U+033E | `◌̾` | COMBINING VERTICAL TILDE |
| U+033F | `◌̿` | COMBINING DOUBLE OVERLINE |
| U+0346 | `◌͆` | COMBINING BRIDGE ABOVE |
| U+0347 | `◌͇` | COMBINING EQUALS SIGN BELOW |
| U+0348 | `◌͈` | COMBINING DOUBLE VERTICAL LINE BELOW |
| U+0349 | `◌͉` | COMBINING LEFT ANGLE BELOW |
| U+034A | `◌͊` | COMBINING NOT TILDE ABOVE |
| U+034B | `◌͋` | COMBINING HOMOTHETIC ABOVE |
| U+034C | `◌͌` | COMBINING ALMOST EQUAL TO ABOVE |
| U+034D | `◌͍` | COMBINING LEFT RIGHT ARROW BELOW |
| U+034E | `◌͎` | COMBINING UPWARDS ARROW BELOW |
| U+0350 | `◌͐` | COMBINING RIGHT ARROWHEAD ABOVE |
| U+0351 | `◌͑` | COMBINING LEFT HALF RING ABOVE |
| U+0352 | `◌͒` | COMBINING FERMATA |
| U+0353 | `◌͓` | COMBINING X BELOW |
| U+0354 | `◌͔` | COMBINING LEFT ARROWHEAD BELOW |
| U+0355 | `◌͕` | COMBINING RIGHT ARROWHEAD BELOW |
| U+0356 | `◌͖` | COMBINING RIGHT ARROWHEAD AND UP ARROWHEAD BELOW |
| U+0357 | `◌͗` | COMBINING RIGHT HALF RING ABOVE |
| U+035D | `◌͝` | COMBINING DOUBLE BREVE |
| U+035E | `◌͞` | COMBINING DOUBLE MACRON |
| U+035F | `◌͟` | COMBINING DOUBLE MACRON BELOW |
| U+0360 | `◌͠` | COMBINING DOUBLE TILDE |
| U+0363 | `◌ͣ` | COMBINING LATIN SMALL LETTER A |
| U+0364 | `◌ͤ` | COMBINING LATIN SMALL LETTER E |
| U+0365 | `◌ͥ` | COMBINING LATIN SMALL LETTER I |
| U+0366 | `◌ͦ` | COMBINING LATIN SMALL LETTER O |
| U+0367 | `◌ͧ` | COMBINING LATIN SMALL LETTER U |
| U+0368 | `◌ͨ` | COMBINING LATIN SMALL LETTER C |
| U+0369 | `◌ͩ` | COMBINING LATIN SMALL LETTER D |
| U+036A | `◌ͪ` | COMBINING LATIN SMALL LETTER H |
| U+036B | `◌ͫ` | COMBINING LATIN SMALL LETTER M |
| U+036C | `◌ͬ` | COMBINING LATIN SMALL LETTER R |
| U+036D | `◌ͭ` | COMBINING LATIN SMALL LETTER T |
| U+036E | `◌ͮ` | COMBINING LATIN SMALL LETTER V |
| U+036F | `◌ͯ` | COMBINING LATIN SMALL LETTER X |
| U+1DC4 | `◌᷄` | COMBINING MACRON-ACUTE |
| U+1DC5 | `◌᷅` | COMBINING GRAVE-MACRON |
| U+1DC6 | `◌᷆` | COMBINING MACRON-GRAVE |
| U+1DC7 | `◌᷇` | COMBINING ACUTE-MACRON |
| U+1DC8 | `◌᷈` | COMBINING GRAVE-ACUTE-GRAVE |
| U+1DC9 | `◌᷉` | COMBINING ACUTE-GRAVE-ACUTE |
| U+A71B | `ꜛ` | MODIFIER LETTER RAISED UP ARROW |
| U+A71C | `ꜜ` | MODIFIER LETTER RAISED DOWN ARROW |

**Role reversal** (1)

| Code point | Character | Unicode name |
|------------|-----------|--------------|
| U+0335 | `◌̵` | COMBINING SHORT STROKE OVERLAY |

**Length** (2)

| Code point | Character | Unicode name |
|------------|-----------|--------------|
| U+02D0 | `ː` | MODIFIER LETTER TRIANGULAR COLON |
| U+02D1 | `ˑ` | MODIFIER LETTER HALF TRIANGULAR COLON |

**Ligatures** (3)

| Code point | Character | Unicode name |
|------------|-----------|--------------|
| U+035C | `◌͜` | COMBINING DOUBLE BREVE BELOW |
| U+0361 | `◌͡` | COMBINING DOUBLE INVERTED BREVE |
| U+0362 | `◌͢` | COMBINING DOUBLE RIGHTWARDS ARROW BELOW |

### D.3 Tone numbers (10)

| Code point | Character | Unicode name |
|------------|-----------|--------------|
| U+00B2 | `²` | SUPERSCRIPT TWO |
| U+00B3 | `³` | SUPERSCRIPT THREE |
| U+00B9 | `¹` | SUPERSCRIPT ONE |
| U+2070 | `⁰` | SUPERSCRIPT ZERO |
| U+2074 | `⁴` | SUPERSCRIPT FOUR |
| U+2075 | `⁵` | SUPERSCRIPT FIVE |
| U+2076 | `⁶` | SUPERSCRIPT SIX |
| U+2077 | `⁷` | SUPERSCRIPT SEVEN |
| U+2078 | `⁸` | SUPERSCRIPT EIGHT |
| U+2079 | `⁹` | SUPERSCRIPT NINE |

### D.4 Marks and separators (12)

**Stress** (2)

| Code point | Character | Unicode name |
|------------|-----------|--------------|
| U+02C8 | `ˈ` | MODIFIER LETTER VERTICAL LINE |
| U+02CC | `ˌ` | MODIFIER LETTER LOW VERTICAL LINE |

**Syllable boundary** (1)

| Code point | Character | Unicode name |
|------------|-----------|--------------|
| U+002E | `.` | FULL STOP |

**Intra-word pause** (1)

| Code point | Character | Unicode name |
|------------|-----------|--------------|
| U+005E | `^` | CIRCUMFLEX ACCENT |

**Compound-word marker** (1)

| Code point | Character | Unicode name |
|------------|-----------|--------------|
| U+002B | `+` | PLUS SIGN |

**Sandhi** (2)

| Code point | Character | Unicode name |
|------------|-----------|--------------|
| U+203F | `‿` | UNDERTIE |
| U+2040 | `⁀` | CHARACTER TIE |

**Intonation group** (2)

| Code point | Character | Unicode name |
|------------|-----------|--------------|
| U+007C | `\|` | VERTICAL LINE |
| U+2016 | `‖` | DOUBLE VERTICAL LINE |

**Phonetic group** (2)

| Code point | Character | Unicode name |
|------------|-----------|--------------|
| U+2039 | `‹` | SINGLE LEFT-POINTING ANGLE QUOTATION MARK |
| U+203A | `›` | SINGLE RIGHT-POINTING ANGLE QUOTATION MARK |

**Word separator** (1)

| Code point | Character | Unicode name |
|------------|-----------|--------------|
| U+0020 | (space) | SPACE |

### D.5 Pause tokens (13)

| Code point | Character | Unicode name |
|------------|-----------|--------------|
| U+0028 | `(` | LEFT PARENTHESIS |
| U+0029 | `)` | RIGHT PARENTHESIS |
| U+0030 | `0` | DIGIT ZERO |
| U+0031 | `1` | DIGIT ONE |
| U+0032 | `2` | DIGIT TWO |
| U+0033 | `3` | DIGIT THREE |
| U+0034 | `4` | DIGIT FOUR |
| U+0035 | `5` | DIGIT FIVE |
| U+0036 | `6` | DIGIT SIX |
| U+0037 | `7` | DIGIT SEVEN |
| U+0038 | `8` | DIGIT EIGHT |
| U+0039 | `9` | DIGIT NINE |
| U+003A | `:` | COLON |

<!-- END ipa-characters -->
