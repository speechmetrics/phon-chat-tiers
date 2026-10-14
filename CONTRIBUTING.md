# Changing the specification

A tier change goes through this specification first. Phon and Chatter
change their implementations only after the change is released here.

## Process

1. Open an issue describing the change and which rules it touches.
2. Open a pull request that changes `spec/phon-chat-tiers.md` **and** adds
   or updates the example files under `examples/` for every rule touched.
   The example files are generated: add or change a case in
   `scripts/gen_examples.py` and run it; never edit a `.cha` by hand (see
   `examples/README.md`). A new rule takes the next free number in its
   section; a withdrawn rule keeps its number, marked *retired*. Numbers
   are never reused.
3. Add an entry to Appendix B (changelog) under the next version, and set
   `**Version:**` and `**Date:**` in the specification's header and the
   *Current version* row of `README.md` to that version. The release
   workflow refuses a tag whose version the header does not state. MINOR
   for a change that keeps existing conforming writers conforming; MAJOR
   when a conforming writer must change its output.
4. Phon and Chatter maintainers both review. The pull request merges when
   both approve.
5. The maintainer tags `vMAJOR.MINOR` on `main` (`vMAJOR.MINOR-rc.N` for
   a pre-release) and pushes the tag. The release workflow creates the
   release and attaches the example zip and the specification; do not
   create the release by hand, since the workflow fails when one already
   exists. A final tag needs a header without `(draft)`.

## Example files

See `examples/README.md` for the file format and naming.
