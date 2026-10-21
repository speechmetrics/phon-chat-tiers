# Checking a file against this specification

Phon (4.2.0 and later) ships two ways to check a CHAT file against the
rules of this specification: the command `phon-chat-check` and the MCP
tool `check_chat_tiers`. They run the same checks and give the same
report, and both meet the specification's definition of a validator:
every broken rule is reported by its number, and nothing is reported for
a file that breaks no rule.

Both check the Phon tiers only — `%modsyl`, `%phosyl`, `%phoaln`,
`%phoint`, and the superseded `%x…` names under the same rules. General
CHAT validity (the main line, the headers, `%mod`, `%pho`) is checked by
Chatter; see [Chatter](#chatter) below.

## The command: phon-chat-check

Phon installs the command in the `bin` folder of its install directory.
On macOS that is `Phon.app/Contents/Resources/app/bin/phon-chat-check`;
on Windows and Linux it is `<install dir>/bin/phon-chat-check` (with
`.exe` on Windows). It needs no running Phon and no project.

    phon-chat-check [--format text|json] [--] <file.cha>...
    phon-chat-check --spec-version
    phon-chat-check --help

### Text report

The default format prints one line per broken rule and nothing for a
file that breaks none:

    <file>:<line>: error[<rule>] <title>: <message>

For example, over two files of this repository's example set:

    $ phon-chat-check examples/invalid/invalid-3-4-start-before-previous-end.cha \
                      examples/invalid/invalid-1-2-unknown-code.cha
    examples/invalid/invalid-3-4-start-before-previous-end.cha:10: error[3.4] Start before the previous end: %phoint start 50 is before the previous end 300
    examples/invalid/invalid-1-2-unknown-code.cha:9: error[1.2] Legal constituent code: %phosyl word 'k:Oæ:Nt:T' has code 'T'; legal codes are O N C L R E A D U

The rule number and title are those of the rule index (Appendix C of the
specification), so a line can be read beside it.

### JSON report

`--format json` prints one object per file:

    {
      "file": "examples/invalid/invalid-3-4-start-before-previous-end.cha",
      "status": "invalid",
      "spec_version": "1.0",
      "spec": "https://github.com/speechmetrics/phon-chat-tiers/blob/v1.0/spec/phon-chat-tiers.md#appendix-c-rule-index",
      "violations": [
        {
          "rule": "3.4",
          "title": "Start before the previous end",
          "status": "error",
          "line": 10,
          "message": "%phoint start 50 is before the previous end 300"
        }
      ]
    }

`status` is `valid` or `invalid`. A violation's `status` is the rule's
status in the specification, `error` or `error, repairable`.

### Exit status

- `0` — no file breaks a rule.
- `1` — at least one file breaks at least one rule.
- `2` — a usage error, or a file that could not be read; the other files
  named on the command line are still checked.

### Matching the specification version

`phon-chat-check --spec-version` prints the version of this specification
the command implements (`1.0` for Phon 4.2.0). Compare it with the
**Version** line in the header of `spec/phon-chat-tiers.md`: a command
older than the specification does not know the rules added since.

### Checking the example set

From the root of this repository:

    phon-chat-check examples/valid/*.cha      # prints nothing, exits 0
    phon-chat-check examples/invalid/*.cha    # one line per file, exits 1

Each invalid file's line names the rule in the file's name.

## The MCP route: check_chat_tiers

Phon's MCP server offers the same check as the tool `check_chat_tiers`,
for AI agents and other Model Context Protocol clients. The server is the
command `phon-mcp-stdio`, next to `phon-chat-check` in Phon's `bin`
folder; it needs no running Phon either. Register it with a client, for
example with Claude Code:

    claude mcp add phon -- /Applications/Phon.app/Contents/Resources/app/bin/phon-mcp-stdio

Then call the tool:

| Parameter | Meaning |
|---|---|
| `file` | The CHAT file to check: an absolute path, or one relative to the directory the client started the server in. Required. |
| `format` | `text` (the default) or `json`. |

The text result is a verdict line, the command's lines, and a link to the
rule index:

    examples/invalid/invalid-3-4-start-before-previous-end.cha: invalid (spec 1.0, 1 violation)
    examples/invalid/invalid-3-4-start-before-previous-end.cha:10: error[3.4] Start before the previous end: %phoint start 50 is before the previous end 300
    Rule index: https://github.com/speechmetrics/phon-chat-tiers/blob/v1.0/spec/phon-chat-tiers.md#appendix-c-rule-index

A file that breaks no rule answers `<file>: valid (spec 1.0, no rule
broken)`. With `format` set to `json` the result is the command's JSON
object. A file that cannot be read, or is not UTF-8, comes back as an
error result.

When the Phon application is running with its MCP server enabled, the
same tool is available through that server and to Schwa, Phon's built-in
assistant. The "MCP Server" topic of the Phon manual covers connecting a
client and the other tools the server offers.

## Chatter

Chatter, the TalkBank validator, checks general CHAT validity and these
tiers as well, under its own error codes:

    chatter validate --format json <file.cha>

`examples/CHATTER-VERDICTS.md` records Chatter's verdict on every file of
the example set and the known differences from this specification. A
disagreement between Chatter and `phon-chat-check` is a question for this
specification, not for either tool. Phon bundles Chatter and runs it when
publishing a project.
