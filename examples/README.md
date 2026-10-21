# Example files

One complete, minimal CHAT file per case.

Every file is written by `scripts/gen_examples.py`; never edit a `.cha` by
hand. To add or change a case, edit the `CASES` list in that script and run
it from the repository root:

    python3 scripts/gen_examples.py
    python3 scripts/check_examples.py

The first command writes the files (and removes any `.cha` the script does
not describe); the second checks the set against the specification. The
"Check examples" workflow runs both on every push and fails when a
committed file differs from what the script writes. Phon's validator can
be run over the set too; see [VALIDATING.md](../VALIDATING.md).

- `valid/valid-<slug>.cha` breaks no rule.
- `invalid/invalid-<section>-<rule>-<slug>.cha` breaks exactly the rule
  named and no other, and is otherwise valid CHAT.

The first line after `@Begin` is the label, with a tab after the colon:

    @Comment:	phon-conformance: valid
    @Comment:	phon-conformance: invalid 3.4

Only this `@Comment` line is read by tests; others may appear anywhere.

A file with time bullets has an `@Media` header whose name equals the
file name without `.cha`. File names use hyphens, not dots, because the
name is repeated in `@Media`.

Each release carries `phon-chat-tiers-examples-<version>.zip`, which
unpacks to a folder `phon-chat-tiers-examples-<version>/` holding
`valid/` and `invalid/`.
