# Simplified Technical English — before / after samples

Worked conversions for [`skills/simplified-technical-english.md`](../../skills/simplified-technical-english.md).

Each case is real documentation from a live repository, not a constructed example.  The point is
to show what applying ASD-STE100 to software documentation actually costs and actually buys —
including the places where the right answer is **do not change this**.

## Two kinds of case

| | What it is | Live upstream? |
|---|---|---|
| **`*-full-rewrite/`** | A whole README converted end to end, pinned to a commit. Two of them, chosen to show opposite lessons. | No — illustrative only |
| **everything else** | The Related Projects section of one repository, rewritten and committed. 32 of them. | **Yes — this is what is live today** |

Because the applied pass changed those 32 READMEs, the pinned `before.md` in the two
`*-full-rewrite` cases no longer matches current upstream.  That is expected; each records the
commit it was taken from.

Every case is `before.md` + `after.md`.  The two full rewrites add a `NOTES.md` with rule-by-rule
rationale, measured counts, and what was deliberately left alone.

## The two full rewrites

| Case | Source | Demonstrates |
|---|---|---|
| [`uplm80-full-rewrite`](uplm80-full-rewrite/) | [avwohl/uplm80](https://github.com/avwohl/uplm80) @ `d99b72f` | **What STE fixes.** A data-corrupting hazard buried in a 43-word sentence promoted to a CAUTION (7.1–7.3), 11 passives made active, 2 semicolons removed, 6 over-length sentences split. 40 → 6 issues. |
| [`iospharo-full-rewrite`](iospharo-full-rewrite/) | [avwohl/iospharo](https://github.com/avwohl/iospharo) @ `d2ba261` | **What STE must not touch.** All five tiers, with a Tier D `## Status` section left untouched to protect its hedges and a Tier E credits block whose semicolons are copyright notices. 10 of its 12 remaining findings are in regions correctly not edited. |

## The applied rollout — 32 repositories

**420 Related Projects entries** across **32 repositories**, reducing to
**56 distinct texts**: 19 were the same line copy-pasted into 6 or more READMEs, 28 were one-off
entries hand-written for a single README.  All of it is committed upstream.

The full text of all 56 rewrites, split into copy-paste and context-carrying, is in
[ENTRY-REWRITES.md](ENTRY-REWRITES.md).

In every repository, **only the Related Projects section changed** — verified mechanically by
asserting the file is byte-identical with that section excised.

| Repository | Entries | | Repository | Entries |
|---|---:|---|---|---:|
| [`uc80`](uc80/) | 21 | | [`ucow`](ucow/) | 18 |
| [`uc_core`](uc_core/) | 21 | | [`um80_and_friends`](um80_and_friends/) | 18 |
| [`uplm80`](uplm80/) | 19 | | [`upeepz80`](upeepz80/) | 18 |
| [`80un`](80un/) | 18 | | [`z80cpmw`](z80cpmw/) | 18 |
| [`cpmdroid`](cpmdroid/) | 18 | | [`uc386`](uc386/) | 9 |
| [`cpmemu`](cpmemu/) | 18 | | [`iospharo`](iospharo/) | 5 |
| [`ioscpm`](ioscpm/) | 18 | | [`pharo-headless-test`](pharo-headless-test/) | 5 |
| [`learn-ada-z80`](learn-ada-z80/) | 18 | | [`soogle`](soogle/) | 5 |
| [`mbasic`](mbasic/) | 18 | | [`validate_smalltalk_image`](validate_smalltalk_image/) | 5 |
| [`mbasic2025`](mbasic2025/) | 18 | | [`claude-skills`](claude-skills/) | 4 |
| [`mbasicc`](mbasicc/) | 18 | | [`freedos_micro_python`](freedos_micro_python/) | 4 |
| [`mbasicc_web`](mbasicc_web/) | 18 | | [`smalltalk80-2026`](smalltalk80-2026/) | 4 |
| [`mpm2`](mpm2/) | 18 | | [`uplox`](uplox/) | 4 |
| [`romwbw_emu`](romwbw_emu/) | 18 | | [`freedos_git`](freedos_git/) | 3 |
| [`scelbal`](scelbal/) | 18 | | [`hearzork`](hearzork/) | 3 |
| [`uada80`](uada80/) | 18 | | [`dosiz`](dosiz/) | 2 |

## Why the rollout was not a regeneration

These lists look machine-generated, and an earlier assumption in this work was that a generator
produced them from the GitHub repo description fields.  **That was wrong.**  Checking 151 entries
against the descriptions found only 46 percent matched.  The other 54 percent had been hand-edited
— correcting `mbasic` to `MBASIC`, dropping a stale parenthetical, or adding a relationship the
description does not carry, such as *sibling backend sharing the uc_core frontend*.

No generator exists in any repository and there are no `BEGIN/END GENERATED` markers.  So the
entries were re-authored deliberately, and every number, file name, test result and inline code
span in an original was checked to survive the rewrite.

## How to reproduce a measurement

```bash
python3 tools/ste_check.py --tier B samples/ste100/uplm80-full-rewrite/before.md
python3 tools/ste_check.py --tier B samples/ste100/uplm80-full-rewrite/after.md
```

Use `--tier A` (20-word limit) for install/build/usage procedures and `--tier B` (25-word limit)
for descriptive prose.  See Part 2 of the skill for the tier definitions.

## How to read these

1. **The Tier E diff is empty.**  Code fences, tables, badges, and URLs come through
   byte-identical.  A conversion that edits them is broken, not strict.
2. **The safety rewrite is the biggest single win.**  Rules 7.1–7.3 take a hazard buried in a
   subordinate clause and make it impossible to miss.
3. **Some rules were deliberately not applied.**  The project pitch, reference tables, and text
   owned by other repositories are left alone, with reasons recorded.
4. **The remaining issue count is not the score.**  In the iospharo case, 10 of the 12 surviving
   "violations" are inside Tier D and Tier E regions that must not be edited — including
   semicolons that are part of copyright notices.  Read the checker output against the tier map.

A caution the samples exist to make concrete: a conversion can pass every mechanical rule and
still be worse.  Three edits in the uplm80 case did exactly that and were reverted; the NOTES
records them rather than hiding them.

## A note on the standard

These samples are written in the *style of* ASD-STE100 Issue 9.  They are not certified, and
cannot be: certification would need the Part 2 controlled dictionary, which is copyright ASD,
Brussels, and is not redistributable here.  Get the free official copy from
<https://asd-ste100.org/>.

