# Chatter verdicts

Chatter 0.29.0, run on 2026-10-14 with `chatter validate --format json` on
every file of the example set. The `Label` column is the file's
`phon-conformance` label; `Chatter` is Chatter's status for the file.

The table is a snapshot. To rerun it with another Chatter release, run
from the repository root and replace the rows below with the output:

    python3 scripts/chatter_verdicts.py <path to chatter> examples/valid/*.cha examples/invalid/*.cha

Then revisit the Disagreements section, which is written by hand.

| File | Label | Chatter | Codes |
|------|-------|---------|-------|
| valid-aln-one-sided-pause.cha | valid | invalid | E734 |
| valid-aln-stress-and-boundary.cha | valid | valid |  |
| valid-aln-substitution-and-deletion.cha | valid | valid |  |
| valid-phoint-cat.cha | valid | valid |  |
| valid-phoint-gap.cha | valid | valid |  |
| valid-phoint-geminate.cha | valid | valid |  |
| valid-phoint-one-ms-outside-record.cha | valid | valid |  |
| valid-phoint-one-ms-overlap.cha | valid | valid |  |
| valid-phoint-two-words-and-pauses.cha | valid | valid |  |
| valid-syl-cat.cha | valid | valid |  |
| valid-syl-intonation-group.cha | valid | invalid | E316 E316 E600 |
| valid-syl-pause-between-words.cha | valid | valid |  |
| valid-syl-pause-inside-word.cha | valid | valid |  |
| valid-syl-phonetic-group.cha | valid | valid |  |
| valid-syl-sandhi.cha | valid | valid |  |
| valid-syl-tone-number.cha | valid | valid |  |
| valid-syl-untranscribed.cha | valid | valid |  |
| invalid-1-1-no-codes.cha | invalid 1.1 | invalid | E735 |
| invalid-1-2-unknown-code.cha | invalid 1.2 | invalid | E736 |
| invalid-1-3-wrong-phone.cha | invalid 1.3 | invalid | E738 |
| invalid-1-4-word-count.cha | invalid 1.4 | invalid | E726 |
| invalid-1-5-source-tier-missing.cha | invalid 1.5 | valid |  |
| invalid-1-6-pause-inside-group.cha | invalid 1.6 | valid |  |
| invalid-2-1-empty-side.cha | invalid 2.1 | invalid | E741 |
| invalid-2-2-null-pair.cha | invalid 2.2 | invalid | E739 |
| invalid-2-3-model-side.cha | invalid 2.3 | invalid | E740 |
| invalid-2-4-actual-side.cha | invalid 2.4 | invalid | E741 |
| invalid-2-5-word-count.cha | invalid 2.5 | invalid | E727 E728 |
| invalid-2-6-source-tier-missing.cha | invalid 2.6 | valid |  |
| invalid-2-7-pause-inside-group.cha | invalid 2.7 | valid |  |
| invalid-3-1-missing-bullet.cha | invalid 3.1 | invalid | E601 E600 |
| invalid-3-2-wrong-element.cha | invalid 3.2 | invalid | E745 |
| invalid-3-3-empty-interval.cha | invalid 3.3 | invalid | E742 |
| invalid-3-4-start-before-previous-end.cha | invalid 3.4 | invalid | E743 |
| invalid-3-4-two-ms-overlap.cha | invalid 3.4 | valid |  |
| invalid-3-5-ends-after-record.cha | invalid 3.5 | invalid | E744 |
| invalid-3-5-starts-before-record.cha | invalid 3.5 | invalid | E744 |
| invalid-3-6-group-count.cha | invalid 3.6 | invalid | E746 |
| invalid-3-7-source-tier-missing.cha | invalid 3.7 | valid |  |
| invalid-3-8-pause-inside-group.cha | invalid 3.8 | valid |  |

## Disagreements

A disagreement is a `valid` file that Chatter rejects, an `invalid` file
that Chatter accepts, or an `invalid` file for which Chatter reports more
than one code. Each is one of:

- **(a)** Chatter has no check for this rule yet.
- **(b)** Chatter checks something the specification does not; a question for the specification.
- **(c)** The example is wrong.

| File | Chatter says | Kind | Note |
|------|--------------|------|------|
| valid-aln-one-sided-pause.cha | invalid, E734: main tier has 2 alignable items, `%mod` has 3 | (b) | Chatter counts the pause on `%mod` against the main line, which has no pause. Phon writes this when the main line has no pause (writer survey, point 6). Open question: https://github.com/speechmetrics/phon-chat-tiers/issues/1 |
| valid-syl-intonation-group.cha | invalid, E316 on `%mod` and `%pho`, then E600 | (b) | Chatter's `%mod`/`%pho` grammar does not accept the intonation-group mark `\|`; it rejects `%pho: ka\|ta` on its own. Phon's parser accepts it and Appendix D lists it. Reported: https://github.com/TalkBank/chatter/issues/8. Verdict from Chatter 0.30.0, added 2026-10-22 |
| invalid-1-5-source-tier-missing.cha | valid | (a) | No check that `%phosyl` has a `%pho` (rule 1.5) |
| invalid-1-6-pause-inside-group.cha | valid | (a) | No check for a pause inside a phonetic group on the source tier (rule 1.6) |
| invalid-2-5-word-count.cha | invalid, E727 and E728 | — | Two codes for one defect: the alignment word count is checked once against `%mod` and once against `%pho`. Rule 2.5 counts slots, so one check |
| invalid-2-6-source-tier-missing.cha | valid | (a) | No check that `%phoaln` has a `%mod` (rule 2.6) |
| invalid-2-7-pause-inside-group.cha | valid | (a) | No check for a pause inside a phonetic group on `%mod` or `%pho` (rule 2.7) |
| invalid-3-1-missing-bullet.cha | invalid, E601 and E600 | — | E600 is a warning that the main-line alignment was skipped after the parse error of E601; both come from the one defect |
| invalid-3-4-two-ms-overlap.cha | valid | (a) | E743 checks that each start is not before the previous *start*; an interval that starts 2 ms before the previous *end* is not reported. Rule 3.4 measures against the previous end |
| invalid-3-7-source-tier-missing.cha | valid | (a) | No check that `%phoint` has a `%pho` (rule 3.7) |
| invalid-3-8-pause-inside-group.cha | valid | (a) | No check for a pause inside a phonetic group on `%pho` (rule 3.8) |

## Notes

- Rules 3.5 (fit inside the record interval, E744) and 3.6 (group count, E746) are checked by Chatter 0.29.0, with the same 1 ms allowance as the specification: both `one-ms` valid files pass and both 2 ms files fail.
- The 1 ms allowance of rule 3.4 agrees too: `valid-phoint-one-ms-overlap.cha` passes.
- Chatter's messages name the tiers `%xphosyl`, `%xphoaln` and `%xphoint` (E735, E736, E738, E727, E728, E601, E743–E746) even when the file uses `%phosyl`, `%phoaln` and `%phoint`; E726 says `%phosyl`.
- Every disagreement of kind (a) is a known difference for Phon's validator (speechmetrics/phon#702).
