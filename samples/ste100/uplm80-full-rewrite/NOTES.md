# Conversion notes — uplm80 README

Source: [avwohl/uplm80](https://github.com/avwohl/uplm80) README.md at commit
`d99b72f216b4`.  Converted with `skills/simplified-technical-english.md`.
Measured with `tools/ste_check.py`.

This repo was chosen because it leads the account on combined engagement
(11 stars, 3 forks, 7 watchers) and because its README exercises four of the
five conformance tiers in one file: A (Installation, Usage), B (Runtime Modes,
Multi-File Compilation), C (Options, Directives, Runtime Library tables) and
E (code fences, badges, the Related Projects block).  It happens to have no
Tier D voice section, which is why a second case is worth adding.

## Measured result

```
python3 tools/ste_check.py --tier B before.md after.md
```

| Rule | What it detects | before | after |
|---|---|---:|---:|
| 6.3 | Sentence over 25 words | 6 | **0** |
| 3.6 | Passive voice | 11 | **0** |
| 8.1 | Semicolon | 2 | **0** |
| 4.2 | Contraction | 2 | **0** |
| GR-6 | Latin abbreviation / `via` | 4 | **0** |
| word | Banned word or marketing filler | 2 | **0** |
| GR-4 | Bare sentence-initial `This` | 1 | **0** |
| 3.5 | `-ing` form outside a technical noun | 13 | 5 † |
| 2.1 | Long multi-word noun | 1 | 2 ‡ |
| **Total** | | **42** | **7** |

† All 5 survive on purpose: `tail merging` is a technical noun (legal under
rule 3.5), and three `targeting` hits are inside the **Related Projects** list,
which quotes the descriptions of *other* repositories verbatim.  Those are Tier E
— they are not this document's prose to rewrite.

‡ Both are checker false positives.  The 2.1 heuristic looks for runs of 4+
non-function words and cannot tell a noun cluster from an ordinary clause without
part-of-speech tagging.  See "Checker limits" below.

## Tier E invariants — verified

| Invariant | Result |
|---|---|
| Code fences | 10 before, 10 after, **byte-identical** |
| Table rows | 21 before, 21 after, **unchanged** |
| URLs | 31 before, 31 after, **none dropped** |
| Badge block | unchanged |
| Project-structure tree | unchanged |

## Rule-by-rule changes

### 8.1 — Semicolons removed (2)

> **before:** `**PL/M source files should not declare `100H:` themselves**; doing so causes the assembler to emit a `cseg org 100H`, which the linker then honors by padding the binary with 256 zero bytes from 0–FFH.`

This one sentence broke five rules at once: a semicolon (8.1), 43 words (6.3),
an `-ing` form (3.5), passive construction, and it buried a real hazard inside
descriptive prose (7.1–7.3).  It became a labeled caution:

> **after:**
> ```
> > **CAUTION: DO NOT WRITE `100H:` IN A PL/M SOURCE FILE.**
> > The assembler emits a `cseg org 100H`. The linker then obeys it and pads the
> > binary with 256 zero bytes from 0 to FFH.
> ```

Rule 7.2 puts the command first, rule 7.3 puts the consequence second, and the
block sits **before** the material it applies to.

> **before:** `Peephole optimization is provided by the external upeepz80 package; the front-end is generated from plox grammars (`plm_pre` + `plm_full`) and loaded at import time from the JSON bundle in `data/`.`
>
> **after:** `The external upeepz80 package does the peephole optimization. The front-end comes from plox grammars (`plm_pre` and `plm_full`). The compiler loads the front-end at import time from the JSON bundle in `data/`.`

Semicolon removed, two passives removed, one 33-word sentence became three.

### 3.6 — Passive voice made active (11)

Concentrated in the Multi-File Compilation list, where every bullet hid the agent:

| before | after |
|---|---|
| All files are parsed together before code generation | The compiler parses all the files before it generates code. |
| A unified call graph is built across all modules | The compiler builds one call graph across all the modules. |
| A single combined output file is generated | The compiler generates one combined output file. |
| Symbols can also be defined from the command line | You can also define symbols on the command line. |
| A comment-wrapped form … is also accepted | The compiler also accepts a comment-wrapped form … |
| The first 100H bytes … are reserved by the operating system | The operating system reserves the first 100H bytes … |

The last one is the clearest win: the agent was already in the sentence, just
demoted to a `by`-phrase.

### 6.3 — Sentences split (6)

> **before (47 words):** `Local variable storage (`??AUTO`) is optimally allocated based on which procedures can be active simultaneously across module boundaries`  … and the following 28-word sentence.
>
> **after:** `The compiler allocates the local variable storage (`??AUTO`). The allocation depends on which procedures can be active at the same time, across module boundaries.`

> **before (50 words):** `The directives are **control lines** — a leading `$` at the left margin (column 1), exactly like `$INCLUDE` and `$TITLE` — so the same source can target different configurations (e.g., CP/M 2.2 vs CP/M 3, single-user vs MP/M). No enabling directive is required.`
>
> **after:** four sentences, longest 17 words, `e.g.` and `vs` removed.

### 4.2 — Contractions removed (2)

| before | after |
|---|---|
| they're inherited by every part | Every part inherits them |
| a CP/M binary's *contents* | the contents of a CP/M binary (also GR-8) |

### GR-6 — Latin abbreviations removed (4)

`e.g.` → `For example`; `etc.` → `and others`; `vs` → `or`.

### 3.7 / word — Nominalizations and filler

| before | after |
|---|---|
| Full PL/M-80 language support | Compiles the full PL/M-80 language |
| Multiple optimization passes | Does more than one optimization pass |
| Generates relocatable object files **compatible with** standard CP/M linkers | Generates relocatable object files **for** standard CP/M linkers |
| Produces code **competitive with** the original | Produces code that **is comparable to** the original |
| Contributions are welcome! Please feel free to submit… | Contributions are welcome. You can submit… |

### 1.10 — Jargon removed

| before | after |
|---|---|
| to **forge** a different jump | to **make** a different jump |
| PIP.PLM, which **fakes** a JMP table | PIP.PLM … and **makes** a JMP table |
| **byte-compatibly** (kept — it is precise and standard in this field) | unchanged |

### 3.5 — Headings deliberately NOT changed

An earlier pass renamed `## Contributing` to `## How to Contribute`.  **That was
wrong and has been reverted.**

Rule 3.5 restricts `-ing` forms in running prose, but explicitly permits an
`-ing` word used as a technical noun, and the standard names *procedural titles
and headings* as its example case — listing `Cleaning`, `Handling`, `Packaging`,
`Shipping`, and `Troubleshooting` as legal.  `Contributing` was already
conformant.  Renaming it broke the `#contributing` anchor and bought nothing.

This is the single most common false alarm when applying STE to a README, which
is why it is recorded here rather than quietly fixed.  Every heading in this file
is now unchanged from the original.

### Corrected while passing through

`Targets Z80 instruction` was an incomplete sentence in the original.  It is now
`Targets the Z80 instruction set`.  A missing blank line before
`## Related Projects` was also restored.

Fixing genuine errors found during a rewrite is in scope.  Changing *meaning* is
not — nothing here alters what the compiler does.

## What was deliberately NOT changed

| Left alone | Why |
|---|---|
| `A modern PL/M-80 compiler targeting Zilog Z80 assembly language.` | The project pitch. Part 0 of the skill: STE will not improve it. Also contains `targeting`. |
| The Options list, Directives table, Runtime Library table | Tier C — fragments by design |
| The Related Projects list | Descriptions owned by other repos |
| All code fences, the directory tree, badges | Tier E |
| `PL/M-80 was the primary systems programming language…` | Already 17 and 12 words, active, clear |

## Checker limits

`tools/ste_check.py` implements only the mechanical subset (Part 10 of the
skill).  It cannot check approved meaning (1.3), technical-noun categorization
(1.5), whether meaning survived the rewrite, one-topic-per-paragraph (6.5), or a
note that hides an instruction (5.5).  Its 2.1 and 3.5 checks are heuristics
without a POS tagger and will produce false positives — read them, do not obey
them blindly.

It ships **no dictionary**.  ASD-STE100 Part 2 is copyright ASD, Brussels.
