# Example files

One complete, minimal CHAT file per case.

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
