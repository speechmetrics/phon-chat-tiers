# Phon Tiers in CHAT

This repository holds the specification of the four dependent tiers Phon
writes to CHAT files — `%modsyl`, `%phosyl`, `%phoaln` and `%phoint` — and
the example files that implementations test against.

| | |
|---|---|
| Specification | [spec/phon-chat-tiers.md](spec/phon-chat-tiers.md) |
| Current version | 1.0 (draft; release candidate [v1.0-rc.1](https://github.com/speechmetrics/phon-chat-tiers/releases/tag/v1.0-rc.1)) |
| Changelog | [Appendix B of the specification](spec/phon-chat-tiers.md#appendix-b-changelog) |
| Examples | [examples/](examples/) — one zip per version on the [releases page](https://github.com/speechmetrics/phon-chat-tiers/releases) |
| Change process | [CONTRIBUTING.md](CONTRIBUTING.md) |

## Citing a version

Link to the tagged file, never to `main`:

    https://github.com/speechmetrics/phon-chat-tiers/blob/v1.0/spec/phon-chat-tiers.md

## Who implements what

- **Phon** writes these tiers, owns this specification, and will ship a
  command-line validator, `phon-chat-check`, that reports broken rules by
  number ([speechmetrics/phon#702](https://github.com/speechmetrics/phon/issues/702)).
- **Chatter** validates CHAT files, including these tiers, from this
  specification. Chatter and Phon test against the same example files; a
  disagreement between them is a question for this specification.

## Licence

This repository is public. The specification and the example files may be
read, copied, redistributed, implemented and used for conformance testing
without asking. Keep the version number with any copy you pass on so that
readers know which revision they hold. A formal licence file will be added
in a later version; until then, these terms apply.
