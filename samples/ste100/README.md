# Simplified Technical English — before / after samples

Worked conversions for [`skills/simplified-technical-english.md`](../../skills/simplified-technical-english.md).

Each case is real documentation from a live repository, not a constructed
example.  The point is to show what applying ASD-STE100 to software
documentation actually costs and actually buys — including the places where the
right answer is **do not change this**.

## Layout

```
<case>/
├── before.md    verbatim upstream file, pinned to a commit
├── after.md     converted
└── NOTES.md     rule-by-rule rationale, measured counts, and what was left alone
```

## Cases

| Case | Source | Demonstrates |
|---|---|---|
| [`uplm80-readme`](uplm80-readme/) | [avwohl/uplm80](https://github.com/avwohl/uplm80) @ `d99b72f` | **What STE fixes.** A data-corrupting hazard buried in a 43-word sentence promoted to a CAUTION (7.1–7.3), 11 passives made active, 2 semicolons removed, 6 over-length sentences split. Tiers A, B, C, E. 40 → 6 issues. |
| [`iospharo-readme`](iospharo-readme/) | [avwohl/iospharo](https://github.com/avwohl/iospharo) @ `d2ba261` | **What STE must not touch.** All five tiers, including a Tier D `## Status` section left untouched to protect its hedges, and a Tier E credits block whose semicolons are copyright notices. 29 → 12 issues, of which 10 are inside regions that were correctly not edited. |

## How to reproduce a measurement

```bash
python3 tools/ste_check.py --tier B samples/ste100/uplm80-readme/before.md
python3 tools/ste_check.py --tier B samples/ste100/uplm80-readme/after.md
```

Use `--tier A` (20-word limit) for install/build/usage procedures and `--tier B`
(25-word limit) for descriptive prose.  See Part 2 of the skill for the tier
definitions.

## How to read these

Four things are worth attention in every case:

1. **The Tier E diff is empty.**  Code fences, tables, badges, and URLs come
   through byte-identical.  A conversion that edits them is broken, not strict.
2. **The safety rewrite is the biggest single win.**  Rules 7.1–7.3 take a
   hazard buried in a subordinate clause and make it impossible to miss.  This
   is the part of STE that most repays the effort.
3. **Some rules were deliberately not applied.**  The project pitch, reference
   tables, and text owned by other repositories are left alone.  The NOTES file
   in each case lists these explicitly, with reasons.
4. **The remaining issue count is not the score.**  In the iospharo case, 10 of
   the 12 surviving "violations" are inside Tier D and Tier E regions that must
   not be edited — including semicolons that are part of copyright notices.
   Read the checker output against the tier map; never obey it blindly.

A caution the samples exist to make concrete: a conversion can pass every
mechanical rule and still be worse.  Three edits in the uplm80 case did exactly
that and were reverted; the NOTES records them rather than hiding them.

## A note on the standard

These samples are written in the *style of* ASD-STE100 Issue 9.  They are not
certified, and cannot be: certification would need the Part 2 controlled
dictionary, which is copyright ASD, Brussels, and is not redistributable here.
Get the free official copy from <https://asd-ste100.org/>.
