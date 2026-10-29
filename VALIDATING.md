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

    phon-chat-check [--format text|json] [--] <file.cha|folder>...
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

The fields of a line:

| Field | Meaning |
|---|---|
| `<file>` | The file name exactly as given on the command line, not resolved to an absolute path. |
| `<line>` | The 1-based line of the file on which the offending tier starts. A tier continued over several lines (a continuation line starts with a tab) is reported at its first line. |
| `<rule>` | The rule number, `<section>.<rule>`, for example `3.4`. |
| `<title>` | The rule's title in the rule index. |
| `<message>` | What broke the rule, quoting the tier content involved. |

The prefix is always `error`, whether or not the rule is repairable; the
JSON report carries that distinction. One file can give several lines.
They come in the order of the file's utterances and, within one
utterance, in the order `%modsyl`, `%phosyl`, `%phoaln`, `%phoint`.

The report goes to standard output, encoded as UTF-8 whatever the console
encoding, since messages quote IPA.

### JSON report

`--format json` prints one JSON object per file checked, in the order
the files were named. Each object is printed compactly on one line, so
the output of several files is JSON Lines (one object per line), not a
JSON array. A file that breaks no rule still gets an object, with
`status` `valid` and an empty `violations` array. Shown here indented
for reading:

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

The fields of the object:

| Field | Type | Meaning |
|---|---|---|
| `file` | string | The file name as given on the command line. |
| `status` | string | `valid` if no rule is broken, otherwise `invalid`. |
| `spec_version` | string | The specification version the checker implements, as `--spec-version` prints it. |
| `spec` | string | A link to the rule index of that version of the specification. |
| `violations` | array | One object per broken rule, in the order of the text report; empty for a valid file. |

The fields of a violation:

| Field | Type | Meaning |
|---|---|---|
| `rule` | string | The rule number, as in the text report. |
| `title` | string | The rule's title in the rule index. |
| `status` | string | The rule's status in the specification: `error` or `error, repairable`. |
| `line` | number | The 1-based line on which the offending tier starts. |
| `message` | string | What broke the rule. |

### Checking a folder

A folder named on the command line stands for every `.cha` file below
it, subfolders included, checked in path order. Hidden files and folders
(names starting with `.`) are skipped, which also skips the `._*` files
macOS leaves on shared drives. Files and folders can be mixed in one
run. File names in the report are the folder as given followed by the
path below it.

Folder checking needs Phon 4.2.0-beta.3 or later; earlier builds treat
a folder as an unreadable file.

When at least one folder is named, the run reports only the files that
break a rule (or cannot be read) and ends with one summary line on
standard output. From the root of this repository:

    $ phon-chat-check examples
    examples/invalid/invalid-1-1-no-codes.cha:9: error[1.1] ...
    ...
    examples/invalid/invalid-3-8-pause-inside-group.cha:10: error[3.8] ...
    42 files checked, 25 invalid, 25 violations

The summary counts every file found (`files checked`), the files that
break at least one rule (`invalid`) and the broken rules
(`violations`). When a file cannot be read, `, 1 unreadable` (or the
count) is appended. Each count is printed even when it is zero, so a
clean folder prints only the summary:

    $ phon-chat-check examples/valid
    17 files checked, 0 invalid, 0 violations

With `--format json`, a run that names a folder prints a single object
for the whole run instead of one object per file:

    {
      "summary": {"files": 40, "invalid": 23, "violations": 23, "unreadable": 0},
      "spec_version": "1.0",
      "spec": "https://github.com/speechmetrics/phon-chat-tiers/blob/v1.0/spec/phon-chat-tiers.md#appendix-c-rule-index",
      "files": [
        {"file": "examples/invalid/invalid-1-1-no-codes.cha", "status": "invalid", ...},
        ...
      ]
    }

| Field | Type | Meaning |
|---|---|---|
| `summary` | object | The counts of the summary line: `files`, `invalid`, `violations`, `unreadable`. |
| `spec_version` | string | As in a per-file object. |
| `spec` | string | As in a per-file object. |
| `files` | array | The per-file object of every file that breaks a rule or cannot be read, in path order. Files that break no rule are counted but not listed. |

A file that cannot be read appears in `files` as
`{"file": ..., "status": "unreadable", "error": ...}`, with the same
reason the error line on standard error gives. A run that names only
files keeps the JSON Lines output above.

### Errors

A file that cannot be checked gives no lines in the text report and no
per-file JSON object (a folder run's JSON lists it as `unreadable`).
Instead one line goes to standard error and the other files are still
checked:

    <file>: not valid UTF-8
    <file>: not a readable file
    <file>: <reason>
    <folder>: no .cha files in this folder

A folder holding no `.cha` file is an error, so a mistyped path cannot
pass as a clean result. A usage error (an unknown option, a missing or
wrong `--format` value, no file named) prints the reason and the usage
text to standard error.

### Exit status

- `0` — no file breaks a rule.
- `1` — at least one file breaks at least one rule.
- `2` — a usage error, a file that could not be read, or a folder
  holding no `.cha` file; the other files and folders named on the
  command line are still checked.

### Matching the specification version

`phon-chat-check --spec-version` prints the version of this specification
the command implements (`1.0` for Phon 4.2.0). Compare it with the
**Version** line in the header of `spec/phon-chat-tiers.md`: a command
older than the specification does not know the rules added since.

### Checking the example set

From the root of this repository:

    phon-chat-check examples/valid/*.cha      # prints nothing, exits 0
    phon-chat-check examples/invalid/*.cha    # one line per file, exits 1
    phon-chat-check examples                  # the invalid files' lines and a summary, exits 1

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
| `file` | The CHAT file, or a folder of CHAT files, to check: an absolute path, or one relative to the directory the client started the server in. Required. |
| `format` | `text` (the default) or `json`. |

The text result is a verdict line, the command's lines, and a link to the
rule index:

    examples/invalid/invalid-3-4-start-before-previous-end.cha: invalid (spec 1.0, 1 violation)
    examples/invalid/invalid-3-4-start-before-previous-end.cha:10: error[3.4] Start before the previous end: %phoint start 50 is before the previous end 300
    Rule index: https://github.com/speechmetrics/phon-chat-tiers/blob/v1.0/spec/phon-chat-tiers.md#appendix-c-rule-index

The verdict line counts the violations (`1 violation`, `2 violations`),
and the rule index link closes a report with violations. A file that
breaks no rule answers with the verdict line alone:

    <file>: valid (spec 1.0, no rule broken)

Here `<file>` is the `file` argument as passed, before it is resolved.
A leading `~` in `file` stands for the user's home folder.

With `format` set to `json` the result is the command's JSON object for
the one file, indented by two spaces rather than on one line.

For a folder, the result lists only the files that break a rule or
cannot be read, between a verdict line and the command's summary line:

    <folder>: invalid (spec 1.0)
    /path/to/phon-chat-tiers/examples/invalid/invalid-1-1-no-codes.cha:9: error[1.1] ...
    ...
    42 files checked, 25 invalid, 25 violations
    Rule index: https://github.com/speechmetrics/phon-chat-tiers/blob/v1.0/spec/phon-chat-tiers.md#appendix-c-rule-index

The file names are absolute, since the folder is resolved before it is
searched. A file that cannot be read gives a `<file>: <reason>` line in
the list, and the verdict reads `not fully checked` when no file breaks
a rule but some could not be read. A clean folder answers with the
verdict line and the summary:

    <folder>: valid (spec 1.0, no rule broken)
    17 files checked, 0 invalid, 0 violations

With `format` set to `json`, a folder's result is the command's single
folder object, indented by two spaces.

A missing `file`, a wrong `format`, a folder holding no `.cha` file, or a file that cannot be read or is
not UTF-8 comes back as an MCP error result (`isError` set) whose text
is a single line starting `Error:`, for example:

    Error: examples/missing.cha: not a readable file

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
