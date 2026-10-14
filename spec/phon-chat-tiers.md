# Phon Tiers in CHAT

**Version:** 1.0 (draft)
**Date:** 2026-10-13
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
manual and checked by Chatter. A file that breaks a rule here is invalid
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
space or mark. Rule 1.3 ties it to the source tier. IPA length is written
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
- Definitions D1 to D7 added.
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
