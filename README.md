# Phon Tiers in CHAT

This repository holds the specification of the four dependent tiers Phon
writes to CHAT files — `%modsyl`, `%phosyl`, `%phoaln` and `%phoint` — and
the example files that implementations test against.

| | |
|---|---|
| Specification | [spec/phon-chat-tiers.md](spec/phon-chat-tiers.md) |
| Current version | 1.0 (draft; release candidate [v1.0-rc.2](https://github.com/speechmetrics/phon-chat-tiers/releases/tag/v1.0-rc.2)) |
| Changelog | [Appendix B of the specification](spec/phon-chat-tiers.md#appendix-b-changelog) |
| IPA characters | [Appendix D of the specification](spec/phon-chat-tiers.md#appendix-d-ipa-characters) — every character accepted on `%mod` and `%pho` |
| Examples | [examples/](examples/) — one zip per version on the [releases page](https://github.com/speechmetrics/phon-chat-tiers/releases) |
| Checking a file or a folder | [VALIDATING.md](VALIDATING.md) — the `phon-chat-check` command and the `check_chat_tiers` MCP tool shipped with Phon |
| Change process | [CONTRIBUTING.md](CONTRIBUTING.md) |

## Citing a version

Link to the tagged file, never to `main`:

    https://github.com/speechmetrics/phon-chat-tiers/blob/v1.0/spec/phon-chat-tiers.md

## Who implements what

- **Phon** writes these tiers, owns this specification, and ships a
  validator that reports broken rules by number, as the command
  `phon-chat-check` and the MCP tool `check_chat_tiers` (Phon 4.2.0 and
  later; see [VALIDATING.md](VALIDATING.md)).
- **Chatter** validates CHAT files, including these tiers, from this
  specification. Chatter and Phon test against the same example files; a
  disagreement between them is a question for this specification.

## Licence

This repository is public. The specification and the example files may be
read, copied, redistributed, implemented and used for conformance testing
without asking. Keep the version number with any copy you pass on so that
readers know which revision they hold. A formal licence file will be added
in a later version; until then, these terms apply.
