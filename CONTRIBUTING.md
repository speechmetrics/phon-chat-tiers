# Changing the specification

A tier change goes through this specification first. Phon and Chatter
change their implementations only after the change is released here.

## Process

1. Open an issue describing the change and which rules it touches.
2. Open a pull request that changes `spec/phon-chat-tiers.md` **and** adds
   or updates the example files under `examples/` for every rule touched.
   A new rule takes the next free number in its section; a withdrawn rule
   keeps its number, marked *retired*. Numbers are never reused.
3. Add an entry to Appendix B (changelog) under the next version. MINOR
   for a change that keeps existing conforming writers conforming; MAJOR
   when a conforming writer must change its output.
4. Phon and Chatter maintainers both review. The pull request merges when
   both approve.
5. The maintainer tags `vMAJOR.MINOR` on `main`. The release workflow
   attaches the example zip and the specification to the release.

## Example files

See `examples/README.md` for the file format and naming.
