# Regelwerk umbauen (Nummern-Kürzung, Verfahren)

**Stand:** 2026-10-31 · **Verantwortlich:** Ramona. Übernommen aus dem Projekt *anderswie-product-intelligence*.

Dies ist ein **einmaliger Schnitt am Ende einer Regelwerk-Prüfung** — danach eingefroren. Die
Prüfung selbst steht in [`GOVERNANCE.md`](GOVERNANCE.md).

---

# Restructuring and renumbering a rules file

Depth for the review in `SKILL.md` ("Reviewing the owner's rule set before changing it").
Use when a rules file is being slimmed, its IDs are being changed, or rules are being removed.

## 1. Decide what the numbering *means* before touching it

A number can be a **stable identifier** or merely an **ordering aid**. Pick one explicitly and
say it out loud, because the two imply opposite edits:

- Stable identifier → never renumber; accept gaps; record dissolved IDs as "absorbed into
  <ID>". References stay valid everywhere, including in historical logs.
- Ordering aid → renumber **once**, at the end of a full review, then freeze again. Freezing
  matters: if you renumber at every review, every reference in every document rots on a
  schedule the owner cannot track.

## 2. Renumbering is a cross-repository edit, not a text edit

1. **Count the blast radius first.** `git grep -nE '<ID-PREFIX>-[0-9]' -- .` and group by file.
   Report the count to the owner; a number that looks like one line in one file is usually a
   dozen references in code, tests, specs, README and indexes.
2. **Split current from historical.** Current documents (rules file, policy, index, README,
   agent instructions, implementation map, module specs, active code and tests) get updated.
   Historical logs (changelog, status reports, session records, archived concepts) **keep the
   numbers that were valid when written** — rewriting them falsifies the record of what was
   decided then. Say this to the owner; it is the one counter-intuitive part of renumbering.
3. **Publish an old → new history table** in the rules file or the decisions log. Without it,
   every older document and every memory of "we discussed PI-18" becomes unreadable.
4. **Update the implementation map and the index in the same commit.** A pointer to a
   dissolved ID is a defect, not a leftover.
5. **Run the test suite.** If only documentation changed, a fully green suite is the evidence
   that the restructure changed nothing else. Note honestly when it is green *despite* code
   that mentions the old IDs in comments and docstrings — decide whether those move too.
6. **Re-check the exit condition.** `grep` again for dissolved IDs and for old→new mismatches
   over the *current* document set only.

## 3. Keep rule IDs out of machine-readable output

A rule ID embedded in code, an API response field or a stored artifact turns documentation
work into a release: a rename then means a code change, a test change and a rebuild. Report
the **rulebook's version** (or a semantic name for the rule) in such places instead, and note
this in the renumbering commit as the actual repair — otherwise the same trap is rebuilt next
time.

## 4. Removing rules instead of parking them

When a rule's module is far off or unplanned, remove it from the rulebook and keep only a
one-line decision record (what was removed, why, where the text can be recovered from). Git
history and the timestamped backup are the archive; a parking document that duplicates them
is clutter, not safety. Before removing, walk each rule for an obligation that already applies
today and move that obligation into a surviving rule — the owner will notice lost intent, not
lost files.

## 5. Doc-surgery pitfalls that cost a rebuild of the edit

- **Re-read the file immediately before a full overwrite.** A long session holds a stale copy,
  and the write guard refuses a full overwrite that is not based on a fresh read. Patch
  targeted spans, or re-read and then write.
- **Inserting above a heading duplicates it.** When a find/replace inserts a new section
  directly above an existing heading, replace that heading line in the same edit. Verify after
  a multi-section edit: `grep -c '^## ' <file>` and compare against the intended section count.
- **Markdown hard line breaks fail the whitespace gate.** Two trailing spaces at line ends
  make `git diff --check` fail. Convert header metadata blocks to list items instead of
  waiving the gate.
- **Doubled pipe characters break tables silently.** `||---|` renders as text, not a table.
  Fix them while the file is open, and mention it — a formatting fix in a rules file is worth
  a clause in the commit message.
- **Multi-line commit messages belong in a file:** write the message to a scratch file and use
  `git commit -F <file>`; a multi-line message inside a shell wrapper string breaks parsing.
- **`pkill -f <pattern>` matches the running wrapper's own command line** when the pattern
  appears in it, so the shell kills itself (the caller sees a signal 15). Find the PID first
  and kill that, or match a pattern that cannot occur in your own command.

## 6. Migrating a document into a per-module specification

When an older spec document is absorbed into a uniformly shaped per-module specification:

- **Do not delete the old file.** Replace its body with a short pointer: what replaced it,
  the date, and the new ID range ("requirements are now `KAT-01`…`KAT-49"). The old text stays
  reachable in Git history, and any existing link keeps working instead of 404-ing.
- **One spec per module, one shape for all.** Same header fields (module, date, status,
  requirement-ID prefix, code, machine-readable artifact) and same sections, so a reader can
  jump between specs without relearning the layout. Give each module its own ID prefix
  (`VIS`, `KAT`, `SUZ`, `LAB`) — a requirement then stays addressable when the text moves again.
- **Migrate the facts, then the deltas since.** Fold in everything learned after the old spec
  was written (new discovery mechanisms, changed rules), not just its original text.
- **Mark superseded decisions explicitly.** If the new spec contradicts a decision the owner
  accepted earlier, give it its own short section: what was decided then, that it is
  superseded, the date, and what replaces it. Two documents stating opposite truths is worse
  than either — this is the single most likely defect of a migration, because the old
  decision is usually embedded in a bullet list nobody re-reads.
- **Accept temporary duplication during the migration and say so.** Creating the specs first
  and reducing the old rule file in one later pass beats interleaving dozens of small edits;
  but tell the owner that content briefly lives in two places, and prove at the end with a
  grep that every moved sentence exists exactly once.

## 7. Verification checklist for a restructure commit

- Section numbering continuous (no gaps where a block was deleted).
- No current document references a dissolved ID; the history table covers every change.
- Backup of each rewritten file taken immediately before the edit, with timestamp.
- Moved text exists in exactly one place — grep the sentences, not just the filenames.
- Index, README and agent instructions point at the new homes.
- Tests run; open items and who must approve them named in the reply.
