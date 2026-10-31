# Governance: ein Repository als Quelle der Wahrheit ordnen

**Stand:** 2026-10-31 · **Verantwortlich:** Ramona. Übernommen aus dem Projekt *anderswie-product-intelligence*.
Die Beispiele stammen aus echter Praxis — sie sind der Wert dieses Dokuments.

---


## When to Use
Use for a repository audit or reorganization that must expose current status, backlog, change history, policies, test gates, and architecture without confusing plans with working code.

## Procedure

1. **Inventory before writing.** Read project instructions and existing README, policy/rules, architecture, test configuration, Git status, tracked files, untracked files, and diff. Distinguish pre-existing work from your own; do not stage, discard, or commit unrelated changes. Do not assume the current working directory is the requested repo if the user names a different project.
2. **Run a bounded local baseline.** Check the relevant test command and report exact passing/failing/collected counts. If a `test_*.py` is an imperative script with top-level prints rather than collected assertions, run it separately and check whether failures produce a nonzero exit code; never call it a pytest gate merely because its filename starts with `test_`. A health endpoint proves only the web process answered, not the downstream pipeline.
3. **Map authority before adding documents.** Keep one canonical owner per concern: product vision, binding product rules, observed status, future architecture, backlog, change log, operational policy, and test gates. Treat a short vision as direction, not a specification or proof of current performance: preserve the owner's voice, qualify unverified promises about purchaseability, comparison, or time saved, and link it from README and the SoT/index with a rule that binding policies outrank aspirations. Record unresolved MVP scope and measurable success criteria as owner decisions in the backlog instead of silently deciding them. Mark design drafts and historical logs as such; a Markdown JSON-schema sketch is not an executable validator.
4. **Make minimal changes.** Preview the scope for die Projektleitung, back up each existing file immediately before editing, change in small steps, verify each write and cross-link. Never delete tracked images, feeds, or history merely to make a repo look lean; `.gitignore` only affects untracked files. Flag license contradictions and rights questions for the owner instead of choosing a license.
5. **Guard external effects.** No push, deployment, paid API calls, or history rewrite as a side effect of documentation housekeeping. Before any eventual publication, inspect the staged diff *and Git history* for credentials, personal images, licensed data, and rights. Do not expose secret values during checks.
6. **Commit only the agreed scope.** Before staging, inspect `git status --short`, the untracked-file list, and configured Git author identity; exclude unrelated new files and keep credentials, backups, builds, images, and feeds out unless explicitly approved. Stage the intended paths, then inspect `git diff --cached --name-status` and `git diff --cached --check`; scan the exact staged blobs for secrets, since working-tree or historical scans alone do not prove what will be committed. For migrated Markdown drafts, fix whitespace flagged by the staged diff after a backup rather than waiving the gate. Run relevant tests and only then commit locally; a commit is not permission to push.
7. **Verify and report plainly.** Align README/STATUS/release-gate claims with the new committed state *before the final commit*, so they do not say the working tree is still uncommitted. Check links, test results, final commit ID and `git status --porcelain` immediately before answering; if a link checker reports implausibly few links, fix the extractor and rerun it before claiming coverage. Recheck if another file appears during verification and leave unapproved late arrivals untouched. Distinguish local commits from remote publication. List unfinished gates and who must approve them; never claim a clean tree when a new untracked file appeared.

## Reviewing the owner's rule set before changing it

When the owner asks to go through their binding rules, the deliverable of that turn is an
**inventory, not an edit**. Present, then wait for decisions.

- Name which file holds which authority first (binding product rules vs. agent workflow
  rules vs. process/security policy) and say how many rules each holds.
- List every rule with its ID, title and a one-line gist, in ID order, plus the next free
  number. A review is only possible against a complete list.
- Add a short section of **observations, explicitly marked as not yet changed**:
  rules duplicated across two IDs, rules that are a subset of another rule, adjacent
  topics that blur together, tables broken by doubled pipe characters, and numbering gaps
  (state per gap whether the number was never assigned or was renamed — verify, do not
  guess).
- Propose the working order (e.g. go rule by rule, or start with the duplicates because
  they clean up fastest) and let the owner pick the entry point.
- Apply nothing until every decision is in. Then change the rule file in ONE commit with a
  backup, so the owner can follow the whole revision in a single piece rather than as a
  trail of small unexplained edits.
- Keep a decisions table (rule / kept / rewritten / merged / parked, each with one clause of
  reason) in an ignored working file for the duration of the review; a review that spans
  several turns must not live in chat memory only.

### A single status column is usually lying

When a rules file marks every rule "aktiv" while the implementation map says most are not
built, one word is doing two jobs: *fachlich gewollt* and *im Tool gebaut*. Replace it with
**two** columns — **Geltung** (in Kraft / vorgemerkt) and **Umsetzung** (umgesetzt /
teilweise / offen, backed by the implementation map). When the owner asks "is this rule even
for us?", the answer is almost always this ambiguity, not a content problem.

Then split the rulebook by **one** criterion: *can the tool keep this rule today?*

- Yes → stays in the rules file, complete, with its MUSS/DARF NICHT.
- No, because a module is missing → into a separate parking document, and in the rules file
  reduced to a one-line pointer plus the list of parked IDs.

A parked rule is only worth keeping when the missing module is **near-term**. When the
capability is far off or unplanned, owner-preference is to **remove the rule outright** rather
than park it: Git history plus a timestamped backup already archive the text, and a parking
document merely re-archives what Git holds while leaving the rulebook feeling cluttered. Keep
exactly one line of decision record — what was removed and why — in the changelog or the
review's decisions table, so a later session need not re-derive it. Either way, carry every
obligation that **already applies today** out of the removed rule into a rule that stays
(e.g. "missing data must never be displayed as confirmed"): an in-force duty must not leave
the rulebook just because its feature module is deferred.

Keep IDs stable during the review; record a dissolved rule in the register as "aufgegangen in
<ID>". Renumbering is a separate, **one-time cut at the end of the review** and then frozen —
procedure, history table and the doc-surgery pitfalls are in
[`references/rulebook-restructure.md`](REGELWERK-UMBAU.md).

### Give every rule exactly one home

Consolidating must make the existing documents **thinner**, not add a parallel one. Do not
invent a file name for a rule class that already has a conventional home:

| Kind of rule | Conventional home |
|---|---|
| How to work here: steps, commits, code quality, tests, version, release | `CONTRIBUTING.md` |
| Boundaries needing the owner's approval, data protection, truth and quality claims | the policy file (e.g. `docs/POLICIES.md`) |
| How the AI agent behaves | `AGENTS.md` — short role note plus a "one topic, one source" pointer table |
| Binding product rules | the rules file, cross-cutting principles only |
| Feature requirements per component | **one specification document per module** |

An invented `ENGINEERING.md` is not a convention and the owner will rightly reject it. After
moving text, grep the source documents to prove no copy survived, and leave a pointer instead
of a second version. Product specifications, requirements and process descriptions belong in
the per-module specification; the cross-cutting rules file keeps only principles that apply to
every module plus one pointer per topic.

Never let a rule ID become a **machine-readable value** in code or serialized output (an API
field reporting `"regelversion": "PI-18"` makes every future renumbering a code change plus a
rebuild). Report the rulebook's *version* there, and free the ID to change.

**The agent's own notes are a document too — and likewise get exactly one home.** An
agent-maintained note (a skill, a memory entry, a start prompt) that restates the repo's rules is a
*second copy* that drifts the moment the repo changes; the repo always wins. Keep the note as a
**pointer table** naming which topic lives in which repo file, and keep in the note only what has
**no** repo home — the language of communication, where plans must be written, a standing approval
boundary. Before deleting a duplicated item, prove it has a home: process rules → the contributing
guide, boundaries and approvals → the policy file, agent behaviour → the agent instruction file,
feature behaviour → the owning specification, build and operations → the release document. Move the
homeless items there **first**, as their own reviewable change, and only then slim the note;
deleting before the new home exists silently loses the knowledge. A note that has grown past the
platform's size limit for its main file is the *symptom* of this drift, not a storage problem — the
fix is subtracting duplication, not moving depth around.

### Sharpening a rule that is too vague to check

Turn description into something testable: give it a **decision order** ("check in this order;
the first matching condition wins"), an **explicit default** for the case where nothing can be
proven, and an **evidence duty** (source + timestamp + check path) for every state other than
the default. A rule with a named default cannot be silently satisfied by a guess, and a rule
with an order stops two signals from fighting over the same outcome.

### Merging a duplicate

Dissolve the narrower rule into the fuller one — but first re-read the narrow rule for a
detail the fuller one lacks and carry that detail across in the same edit; that detail is
exactly what a merge loses. Then note the absorbed ID in the register. Before restructuring a
rules file at all, grep code and tests for the file name and for the rule IDs as strings:
nothing should reference them, and a passing test suite afterwards proves the restructure
changed documentation only.

## Reconciling a backlog against the code

"Survey the backlog and reconcile it" means: a **reconciled overview plus surgical edits** —
not a rewrite, and not a promise to look at it later.

1. **Read the backlog whole, then measure every number in it.** Numbers typed into a backlog
   drift silently: a field-coverage figure can stay at "51 %" for many versions while the real
   value moved to 100 % for one provider and stayed 0 % for the rest. Recompute per
   module/provider from the artifacts on disk and write the measured values in.
2. **Check each "done" claim for the way it is half-done.** A rule can be built and covered by
   tests while being *switched on for exactly one instance* — the per-provider profile flag, the
   config value, the optional field. "Data part done" is not "in operation": name the instances
   where it is still dark and what switching it on would cost.
3. **Strike completed items with their evidence** (version, test, measurement) instead of
   deleting them; that line is what stops a finished topic from being re-decided. As a *first*
   pass, delete nothing — the reconciled state is a proposal. **When the owner then says
   "eliminate the historical", remove the block from the active file** (Git and the dated status
   log keep it) and carry its **still-open** content over **under descriptive names, not the old
   ticket IDs**: split every row into archival and open *before* deleting, or the deletion takes
   live work with it. An ambiguous "historical" heading whose rows read like open tasks is exactly
   what the owner will order removed; prepare that split in the same turn you report it.
4. **One home per topic — cross-reference, do not copy.** Work items live in the backlog; open
   decisions live in the spec or handoff section that owns them. Replace a duplicated decision
   list with one pointer plus the note that it is deliberately not mirrored.
5. **Flag contradictions for the owner instead of silently repairing them:** a section headed
   "historical" whose rows read like open tasks, two documents naming the same phase differently,
   a status column that disagrees with the code. Propose the ways out and let the owner choose —
   a silent cleanup destroys the only record of the ambiguity.
6. **Verify any status column against the code before repeating it**, and read a document's header
   together with its own progress table. A delivered handoff is a snapshot, not a live tracker: its
   phase table can still read "open" for work that is built and covered by tests. A plan can also
   contradict **itself** — a header saying "proposal, not implemented" above a table whose rows all
   read "done", with the version/commit column for the finished stages left empty; the header is the
   part nobody edits while the work proceeds. Report the corrected status in the backlog; edit the
   delivered artifact only if the owner asks.
7. **Turn "this part looks thin" into a checkable list.** When a release is deliberately split,
   name which acceptance criteria cannot pass before the deferred release, and why — that is what
   keeps a known limitation from being reported later as a defect.
8. This is a **documentation** job: no code change, no push. Land the relations you introduced
   (index rows for plans that were never listed, provenance notes) as the same small commits.

## Enforcing document order (a cleanup that is not checked regresses)

Cleaning up stale documents once changes nothing durable: the next session adds a draft, a plan
header quietly contradicts its own progress table, and the tree is inconsistent again. Write the
order down **and** make the gates fail on it.

**Rules the repo states, each with one home (the SoT/index document):**

- The active docs folder holds only what the index lists as authoritative. Drafts, replaced
  versions and historical texts live under `archive/<topic>/` with a **banner on top** naming the
  date and the valid successor. An "older drafts, not approved" section in the index means those
  files are still in the active folder — move them and drop that section.
- Every active document names a status date in `YYYY-MM-DD`. Only ISO is machine-checkable, so
  convert prose dates rather than trusting a reader. **One document, one status line:** rename the
  second one (e.g. `Angelegt:`), never leave two different dates in the same file.
- **One name, one meaning.** Keep a table of the identifiers the repo uses — version number,
  delivery slices, plan steps, handoff steps, rule IDs, gate IDs, acceptance-test IDs — in the same
  SoT document, and forbid **free letters for steps**. Two documents with "steps A–D" and
  "phases A–D" of different content make one label unresolvable, and a reader (or an agent)
  answers the wrong question with full confidence; give each family its own scheme (plan steps
  `M1…`, handoff steps `Ü1…`) and let the check reject the free-letter pattern. **Dated logs keep
  their old words:** a status log is history — do not rewrite its entries, add a **dated naming
  note** at its top ("X is now called Y") and exempt that file in the check.
- The backlog holds only open work, every heading dated, every line unambiguously open, partly
  done or done. The changelog holds only dated version blocks plus an `[Unreleased]` note;
  statements that later became false go in as a **dated note** there, never by rewriting a
  released block.

**The checks worth automating** — cheap, and every one of them found a true violation on the first
run: active docs carry a date; no active doc declares itself a draft/unapproved in its header;
every active doc is linked from the index's authoritative table; every backlog heading is dated;
every changelog block is dated; every archived document carries its banner; **no relative markdown
link in an active document is dead**. Wire them into the gate script the repo already runs, so a
violating session fails instead of shipping. Starter to adapt:
[`templates/document-order-test.py`](../tests/test_dokumentenordnung.py).

**Two traps found while building the checks:**

- **Non-ASCII text checks must not run through a shell filter** (locale can make a pattern report
  zero matches), which reads as "the reference is gone" while the text is right there. Use the
  native content-search tool for repo text checks and Python for the check logic; keep any shell
  pattern ASCII-only, and re-verify a surprising zero by a second method before concluding from it.
- The "active doc must be listed" check is what makes the index complete — expect it to fail on
  the index itself and on legitimate documents nobody ever entered there (the SoT map, the
  versioning rules). Add the index row; do not weaken the check.

## Documenting as you go (the duty is per topic, not per project)

The owner's standing rule: the essential outcome of every larger topic goes into the repo **in that
same turn** — not at the end of the project, and not only into the chat. A chat is not a source of
truth; when the session ends, whatever lived only there is gone.

- **Where each piece goes:** dated state into the status log, the change into the changelog, open
  work into the backlog — plus the owning specification when a rule or a boundary moved. If a rule
  ID appears, update **both** the range and the prose row of the module map.
- **Numbers need their source.** A measured value in a document is a claim: commit the script that
  produced it (e.g. `scripts/messungen/`) and keep a table mapping value → script, so the number
  stays reproducible. A value whose script is untracked is not evidence — it is a sentence.
- **Automate the part that is checkable.** The enforceable part is mechanical: a test that reads
  `git status --porcelain` and fails when files under `src/` changed while the changelog did not.
  Consequence for the working order: write the changelog entry **in the same turn** as the code, or
  the gate run at the end of that turn is red. A check can prove **that** something was documented,
  never that it is **correct** — so the duty itself also stays written in the agent instruction file.
- **The start prompt is a pointer, not a rulebook.** A short entry prompt naming the repo, the
  reading order (agent rules → index → source-of-truth map → status → backlog) and the few working
  rules is enough. Restating the rules inside the prompt creates a second copy that drifts.
- **One session per topic.** When a topic is finished, or the session's working memory is filling
  up, say so explicitly and propose the next session **with a name** (`<project> – <version or
  item> – <topic>`, e.g. `PI 0.34.0 – LAN-Fix Scan`); the owner starts it with the short prompt.
  Before closing, make sure the open work list sits in the backlog **with order, cause and
  approach** — then the next session works from the repo instead of from chat memory.

### Parallel work: one repo, one release channel, one writer

Splitting a repo into sub-agents per area (catalogs, scan, UI) is tempting and is the wrong shape
while those areas stay coupled:

- Sub-agents get separate conversations: they do not see the current chat, do not know the repo's
  rules, cannot ask the owner anything and cannot obtain an approval — yet they write into the same
  files (status log, changelog, central modules). The result is write conflicts plus
  plausible-sounding but unverified work.
- With **one** artifact and one activation step per release, the pipeline is strictly serial: two
  writers or two builders can break the running system. The same holds for deleting, building,
  activating and every step that needs a decision.
- Areas are better bounded as **versioned documents** (one specification per module plus a
  rule/module map); a coordinator — the main agent — reads those.
- Delegate only **independent, read-only** work: reading several sources in parallel and reporting,
  digesting one very large document so it does not fill the main context, or work in a genuinely
  separate project. Never parallel writing into one repo.

## Pitfalls

- When a protected agent-instruction file requires approval and the prompt times out, do not retry through another tool or path; record the missing control file as an open item. Silence is not consent.
- Do not treat a command's exit code or a filename as sufficient evidence of a test: inspect collection and failure signaling, because hand-written scripts can print failures yet return success.
- Keep the operational status dated and evidence-based; otherwise old aspirational README claims can masquerade as current functionality.
- Before archiving conceptual directories, search for runtime/test references to their old paths; update only those references, run the affected script, and verify that every archived file matches its private pre-move backup by hash. Treat archived logs as history, not operational instructions.
- Removing a tracked generated cache requires `git rm --cached` (ignoring it alone does nothing); keep its local files and disclose the staged index change. Keep private QA outputs and backups ignored, but do not silently delete them.
- For release workflows, reconcile package/CLI/API versions before labeling artifacts; inspect wheel contents for templates and private data, record commit/channel/hash/dirty state, and distinguish a local test wheel from a production release. A clean annotated tag plus security, rights, license, and real E2E evidence are separate gates; do not infer container readiness from a wheel build. If Docker copies an archived path or tracked feeds into the image, keep OCI release explicitly blocked until repaired and actually built.
- A commit-bound build (one that copies `git show HEAD:<path>` into its build context) may refuse on *any* unclean tree — including **untracked** files it could never include. When such a gate fires, read `git status --porcelain --untracked-files=normal` before reading code: the gate is usually right about the fact and silent about the cause. If the offending entry is content you did not create, whether it gets committed, parked outside the build path, or ignored is the **owner's** decision; never move or delete foreign untracked content to unblock a build.
- A gate that reports only the exception type ("RuntimeError") costs the reader the entire diagnosis, because the reason has to be dug out of the tool's source. Print the reason in plain words on every failure path, and verify a new message by re-triggering the gate with a throwaway file you own, then removing it.
- A release can end up **tagged with no artifact** — a blocked build, a failed gate. Record that plainly in the changelog and the status ("this version received no image; its content ships under the next version") rather than letting the tag imply a build that never ran; afterwards a version without an artifact must not look like one with an artifact.
- When a numbered spec (rules, gates, requirements) has gaps in its numbering and you must explain them without guessing, verify provenance per missing number before writing: `git log --all -S '<ID>' -- <file>` shows whether it ever existed in that file's history, and grepping the archive/backup dirs surfaces surviving references. Distinguish "never assigned" from "renamed at consolidation" and state which — an unexplained gap reads as lost content even when nothing was actually lost.
- **Never chain `commit`/`tag` onto a `git add` that can be refused.** A `git add` naming a path inside an ignored directory exits non-zero; with `&&` the commit is then skipped **silently**, while a command on the next line still runs and tags the **old** HEAD. Stage in its own step (`;` or a separate call), read its output, and never batch staging with tagging. After tagging, prove the pointer **two ways**: `git rev-parse v<version>^{commit}` must equal `git rev-parse HEAD`, **and** the tagged commit's subject must be the release commit (`git log -1 --format=%s v<version>` starts with `release: <version>`). The equality alone is not sufficient — when a commit is skipped for having nothing to stage, the tag lands on the **previous** commit and the equality still holds; tagging the newest docs/script commit is the same mistake from the other side, because later follow-up commits move HEAD. The tag belongs on the release commit, not on the latest commit. `git rev-parse v<version>` alone prints the **annotated tag object's own** SHA and so looks like a wrong pointer even when the tag is correct. A path under an ignored runtime directory cannot be staged without `-f`; when that content is runtime state, say in the commit message that it is deliberately unversioned rather than forcing it in.
- **A document is not authoritative because it exists.** Before citing one as "the plan", check three cheap things: the index/map's classification (current vs. an "older drafts, not approved" section), the document's own date/status line, and its origin (`git log --follow --format='%h %ad %s' -- <file>`). A draft can sit in the tree for many versions while its model names, prices and promised phases go stale — quoting it as the next step hands the owner a plan that was superseded. **Locate a label before acting on it:** the same `Phase B` can mean the test phase of one evaluation in one document and the second release slice in another; grep the docs for the exact phrase, name the file you mean, or ask which one is intended.
- **Moving or editing a file can break a checksum manifest nobody looked at.** A delivered package may carry `MANIFEST.sha256` plus a sentence elsewhere claiming "all N files verified". Before editing anything inside such a package, grep for the manifest and for the claim; afterwards regenerate the manifest, prove it (`sha256sum -c` from the **documented** directory) and record the change in the package's own changelog. Watch for a manifest that is **not verifiable at all**: mixed path prefixes (one bare file name beside `docs/...` entries) fail from every directory while looking authoritative — normalise the paths first, then check. The same pre-move grep applies to renames and archives: index, README, specifications and generated package manifests all carry old paths — **and the build/packaging files**: a build script's explicit file list and a wheel `force-include` map name the file by path, so a moved schema ships missing or fails the next build even though every document was updated. Grep the build script and the packaging metadata too, and let the repo's own link check prove the documents.
- **A release document's header must name two versions.** One field cannot report both the source version (with its commit) and the artifact that is actually running: the header then reads "the new version is live" while the deployed image is several versions behind, and it goes stale silently because nobody edits a header while patching code. Name the source version + commit and, separately, the active artifact version, and say that a lagging build is expected until it is built and activated.
- **Never cite a rule ID you have not located in its owning document.** Typing an ID (e.g. `LAB-46`)
  into the status log, the backlog and the changelog while the specification never defined it produces
  several false statements that *look* like citations, and no gate catches it: the checks verify that
  the IDs a specification **defines** are consistent (listed in the index, present in the module map),
  not that every ID **quoted** anywhere exists. Before writing an ID, grep its definition; is it
  missing, either write the requirement into its owning document in the same change or drop the ID
  from the sentence. Promising a rule ID as the anchor of a fix is itself a claim about the repo.
- **A test-mode switch makes the suite green while the shipped path is dead.** When the code under
  test branches on a flag (`TESTING`, a mock adapter, a dry-run) and the entire suite sets that flag,
  the production branch is **untested**: a feature can be unreachable, or a required progress signal
  never sent, while every check passes. Before calling a change verified, read the branch the
  *shipped* path takes and prove it is reachable — an indentation slip that nests the real code inside
  a test-only `if` leaves the endpoint answering `null`, and `compileall` does not see it because the
  indentation is valid. Two cheap proofs: inspect the shipped source structurally (does the endpoint
  function still *end* in its real `return`? `print(type(fn.body[-1]).__name__)` via `ast`), and keep
  at least one test that exercises the production path with the switch **off**. A gate that bypasses
  the path it certifies is not a weaker gate — it is a gate for something else.

---

## Aufräum-Bericht (Müllabfuhr)

Ein Bericht findet, was im Alltag untergeht: überlange Dateien, Namen wie `final-final` oder
`Kopie`, Häufungen von `TODO`/`FIXME`, Dokumente ohne Index-Eintrag. Aufruf aus dem Projektordner:

    python3 scripts/muellabfuhr.py

**Der Bericht meldet nur.** Er löscht nichts, ändert nichts und endet immer mit Erfolg — Aufräumen
ist ein menschlicher Entscheid, und Löschen braucht Zustimmung (`docs/POLICIES.md` §1). Er gehört
deshalb bewusst **nicht** in `gates.sh`: eine Prüfung, die bei jedem Lauf rot wird, wird abgeschaltet
statt gelesen.

Empfohlener Zeitpunkt: monatlich und vor einem Release. Der Bericht nennt Kandidaten; entschieden
wird einzeln, nie in einem Zug.
