---
name: simplified-technical-english
description: Write or rewrite software documentation (README, INSTALL, BUILD, CLI --help, man pages, API docs, code comments) in ASD-STE100 Simplified Technical English Issue 9. Covers all 53 writing rules paraphrased with software examples, the technical noun/verb categories that make software vocabulary legal, four conformance tiers for different documentation genres, markdown skip regions, the word-count algorithm, and a repo-by-repo rollout workflow. Use for Simplified Technical English, STE, ASD-STE100, controlled English, plain technical English, or docs aimed at non-native English readers.
---

# Simplified Technical English (ASD-STE100) for Software Documentation

ASD-STE100 is a controlled natural language: a fixed set of writing rules plus a
controlled dictionary.  It was built so that aircraft maintenance manuals could be
understood by technicians who do not read English natively.  It is now maintained
as a general standard for technical documentation.

**Current edition: Issue 9, published 2025-01-15.**  Issue 9 has 53 numbered
writing rules in 9 sections (Part 1), 8 general recommendations, and a controlled
dictionary of roughly 900 approved words (Part 2).

This skill applies it to software project documentation.

---

## Part 0: Read This First — Scope

STE was designed for *procedures*.  Applied to a whole README without judgment it
produces flat, hectoring prose and destroys legitimate voice.  Applied to the
procedural and safety-critical parts of documentation it is a large, real
improvement.

**Use the tier system in Part 2.  Do not apply all 53 rules to all text.**

### Where STE genuinely helps software docs

- Install / build / setup steps — ambiguity here costs the reader real time
- Troubleshooting and error-recovery instructions
- Warnings about data loss, irreversible operations, and corrupt output
- CLI `--help` text and man pages, where terseness already fights clarity
- Any project with international contributors or users
- Terminology consistency across a multi-repo family (rule 1.11 is the highest
  value rule in the whole standard for a project like this)
- Machine translation quality, which improves sharply on controlled input

### Where STE makes software docs worse

- The one-line project description and the opening pitch.  These are marketing.
  STE will flatten "Super optimizing C compiler targeting Z80" into something
  duller and no clearer.
- Reference tables (opcodes, registers, config variables, exit codes).  These are
  fragments by design; sentence rules do not apply.
- Explanations of *why* an algorithm works, historical notes, and design
  rationale.  These need subordinate clauses and comparison, which STE restricts.
- Humor, personality, and community tone in CONTRIBUTING.
- Inline `// why` code comments.  See Part 9.

### The honest verdict

Apply **strict STE to procedures and safety text**, a **reduced rule set to
conceptual prose**, **terminology rules only to reference material**, and
**nothing but terminology to voice-bearing prose**.  A full-strength rewrite of
every sentence in every repo is not the goal and will not survive contact with
the actual documentation.

Rough volume split for a typical developer-tool repo: ~30% procedural (full STE,
real win), ~35% descriptive (structural rules only), ~20% voice (terminology
only), ~15% frozen.

### What the evidence actually supports

The measured comprehension gains for controlled English are concentrated in
**difficult procedural text read by non-native speakers** (Chervak & Drury,
n=175; Shubert et al. 1995).  That is exactly "bootstrap a Z80 cross-compiler on
an unfamiliar host," and it is a real effect.

Two claims to **not** make:

- **Do not claim STE improves LLM or RAG comprehension.**  There is no evidence
  for it.
- **The translation-cost argument does not apply** to a personal open-source
  project.  Nobody is paying a vendor per word, and browser translation of
  English is now good.

The comprehension case for procedures is the only claim that survives contact
with the evidence — and it is enough on its own.

### The correctness trap

The most serious failure mode is not ugly prose.  It is this: STE bans the
perfect and progressive tenses, the conditional, and most modal nuance.  Applied
to hedged prose — *"runs green apart from a few known, unrelated failures"*,
*"boots but does not yet play to a win"* — a rewrite either deletes the hedge or
triples the word count.  **Deleting a hedge turns a calibrated claim into an
overclaim. That is a correctness bug, not a style change.**  Tier D exists
specifically to prevent it.

---

## Part 1: Copyright — What You May and May Not Ship

The specification is © ASD (Aerospace, Security and Defence Industries
Association of Europe), Brussels.  "ASD-STE100 Simplified Technical English" is
an EU registered trademark.

Issue 9 grants irrevocable free reproduction rights to a **closed list**: ASD
national associations and their member companies, AIA and AIAC members, ICCAIA
members, customers of those companies, ministries of defence of member countries,
Airlines for America, airworthiness authorities, and universities and research
institutes for educational purposes.

**A personal public repository is not on that list.**  Therefore:

| Action | Allowed |
|---|---|
| Paraphrase the rules in your own words and cite the standard | Yes |
| State rule numbers and what they require | Yes |
| Write your own examples | Yes |
| Reproduce rule text verbatim at length | No |
| Ship the Part 2 dictionary, or a transcription of it | No |
| Ship a derived "approved word list" copied from Part 2 | No |
| Call your output "ASD-STE100 certified" or use the mark as a badge | No |

Get the official spec free (registration required) from **https://asd-ste100.org/**.
Everything in this skill is paraphrase plus original software examples.

Say "written in the style of ASD-STE100 Simplified Technical English," not
"ASD-STE100 compliant."  Compliance is a claim you cannot verify without the
dictionary and a checker.

---

## Part 2: The Five Conformance Tiers

Assign every region of a document to exactly one tier before rewriting anything.

```
Tier  Name          Applies to                                    Sentence limit
────  ───────────   ───────────────────────────────────────────   ──────────────
  A   PROCEDURE     Anything the reader executes or must obey:      20 words
                    install, build, quick start, usage walk-
                    throughs, troubleshooting recipes, numbered
                    steps, WARNING/CAUTION blocks, runtime error
                    strings, the synopsis line of --help/man
  B   DESCRIPTION   Architecture, how it works, data flow,         25 words
                    memory layout, feature prose, README lede,
                    the GitHub one-line description, man
                    DESCRIPTION, public docstring summaries,
                    module and file-header comments
  C   REFERENCE     Two-column option/env/opcode/exit-code         none
                    tables, the description column of --help,
                    man OPTIONS one-liners, param/returns lists,
                    feature and requirement bullet lists
  D   VOICE         Status / "what works today" / "the frontier"   none
                    / limitations narratives, "why this exists"
                    rationale, comparisons with prior art,
                    forensic bug analyses, test-rationale
                    docstrings, CONTRIBUTING tone, credits
  E   FROZEN        Code fences, inline code, terminal            untouched
                    transcripts, program output, ASCII art,
                    URLs, badges, LICENSE/SPDX/warranty,
                    third-party attribution, quoted upstream
                    spec text, RFC 2119 keywords, generated
                    blocks
```

**Tier D is the one most skill-writers omit, and it is the one that prevents the
worst damage.**  It is a named region where STE is deliberately switched off.
The only permitted edits in Tier D are: enforce the glossary term, fix a factual
error, remove slurs or vulgarity.  Nothing else.  This prose is doing real
epistemic work — its hedges and comparatives are the point.

**Tier E is enforced mechanically, not by care.**  Extract every fenced block,
code span, URL, link target, image src, and table row before and after; assert
byte-identical; block the commit on any difference.  This is the only reliable
guard against a confident model "improving" a command line.

### Rule assignment by tier

All 53 rules, explicitly placed.  "—" means the rule does not apply to that tier.

| Rules | Topic | A | B | C | D | E |
|---|---|:-:|:-:|:-:|:-:|:-:|
| 1.1–1.4 | Approved words, part of speech, meaning, forms | ✓ | glossary¹ | — | — | — |
| 1.5–1.6 | Technical nouns | ✓ | ✓ | ✓ | — | — |
| 1.7 | No technical noun as a verb | ✓ | ✓ | ✓ | — | — |
| 1.8–1.10 | Glossary source, short names, no slang | ✓ | ✓ | ✓ | — | — |
| **1.11** | **One item, one name** | ✓ | ✓ | ✓ | **✓** | — |
| 1.12–1.13 | Technical verbs | ✓ | ✓ | ✓ | — | — |
| 1.14 | American spelling | ✓ | ✓ | ✓ | — | — |
| 2.1–2.2 | Multi-word nouns ≤ 3 words | ✓ | ✓ | ✓ | — | — |
| 3.1–3.4 | Verb forms and tenses | ✓ | ✓ | — | — | — |
| 3.5 | `-ing` only in a technical noun (headings exempt) | ✓ | ✓ | — | — | — |
| 3.6 | Active voice | ✓ | ✓ ² | — | — | — |
| 3.7 | Verbs describe actions, not nouns | ✓ | ✓ | — | — | — |
| 4.1–4.2 | Short sentences, no contractions, no omitted words | ✓ | ✓ | — | — | — |
| 4.3 | Vertical lists for complex text | ✓ | ✓ | — | — | — |
| 4.4 | Connecting words | ✓ | ✓ | — | — | — |
| 4.5 | Articles before nouns | ✓ | ✓ | **off** ³ | — | — |
| 5.1 | 20-word maximum | ✓ | — | — | — | — |
| 5.2 | One instruction per sentence | ✓ | — | — | — | — |
| 5.3 | Imperative form | ✓ | — | **off** ³ | — | — |
| 5.4 | Condition first, then comma, then command | ✓ | — | — | — | — |
| 5.5 | Notes give information, not instructions | ✓ | ✓ | — | — | — |
| 6.1–6.2 | Gradual information, key words | — | ✓ | — | — | — |
| 6.3 | 25-word maximum | — | ✓ | — | — | — |
| 6.4–6.6 | Paragraphs, one topic, max 6 sentences | — | ✓ | — | — | — |
| 7.1–7.3 | Safety instructions | ✓ | ✓ | ✓ ⁴ | — | — |
| 8.1 | No semicolons | ✓ | ✓ | ✓ | — | — |
| 8.2–8.3 | Hyphens, parentheses | ✓ | ✓ | ✓ | — | — |
| 8.4–8.7 | Word counting | ✓ | ✓ | — | — | — |
| 9.1–9.3 | Sentence reconstruction, correct words, no phrasal verbs | ✓ | ✓ | ✓ | — | — |
| **9.4** | **Consistent style and terminology** | ✓ | ✓ | ✓ | **✓** | — |
| GR-1…GR-6, GR-8 | General recommendations | ✓ | ✓ | partial | — | — |
| GR-7 | Inclusive language | ✓ | ✓ | ✓ | ✓ | — |

¹ Rules 1.1–1.4 cannot be enforced at Tier B without the Part 2 dictionary, which
cannot ship (Part 1).  Substitute the project glossary plus the table in Part 4.

² Passive is permitted at Tier B only when the agent is genuinely unknown **or**
deliberately unspecified — and the surviving passive should be marked as which.
At Tier A there is no exception; use the imperative.

³ A `--help` description column is a label, not a sentence.  Inflating
`-v  Verbose output` into `This option makes the output verbose.` costs terminal
width and buys nothing.  argparse/clap conventions are what users expect, and STE
has no standing to overrule them.

⁴ Only the hazard clause: where a flag is destructive, say so
(`overwrites the source file`).

---

## Part 3: The 53 Rules, Paraphrased for Software Docs

Rule numbers are the standard's.  Wording and examples are original.

### Section 1 — Words (1.1–1.14)

**1.1** Use only three kinds of word: words approved in the dictionary, technical
nouns, and technical verbs.

**1.2** An approved word may be used only as its listed part of speech.  This is
the rule software English breaks constantly — see Part 4.

**1.3** Use an approved word only with its approved meaning.

**1.4** Use only approved verb and adjective forms.

**1.5** Any word that fits a *technical noun category* is legal.  Issue 9's
category 19 is **"Computer science, information and communication technology."**
This is what makes software documentation possible under STE.

**1.6** A word not approved in the dictionary is still usable when it is a
technical noun or part of one.

**1.7** Never use a technical noun as a verb.

> BAD: `Backup the database before you upgrade.`
> GOOD: `Do a backup of the database before you upgrade.`
> BAD: `Interface the emulator with the host filesystem.`
> GOOD: `Connect the emulator to the host filesystem.`

**1.8** Use the technical nouns approved in your project glossary.

**1.9** When you must invent a technical noun, keep it short and clear
(three words maximum).

**1.10** No regional words, slang, or jargon.  The standard's own example is from
software: *"do not brick the router"* is not acceptable — write what actually
happens.

> BAD: `A bad HBIOS image will brick the board.`
> GOOD: `An incorrect HBIOS image makes the board unserviceable.`
> BAD: `The linker chokes on malformed OMF records.`
> GOOD: `The linker stops with an error when an OMF record is malformed.`

**1.11** Never use two different names for the same thing.  For a project family
this is the single most valuable rule: pick `object file` or `.rel file`, pick
`work step` or `stage`, and never alternate.

**1.12** Any verb that fits a *technical verb category* is legal.  Category 2 is
**"Computer processes and applications."**  But: if a plain approved verb says the
same thing, use the plain verb instead.

**1.13** Never use a technical verb as a noun.

> BAD: `Run the compile.`  GOOD: `Compile the source file.`
> BAD: `Do an install of the package.`  GOOD: `Install the package.`

**1.14** American spelling.  `initialize`, `behavior`, `analog`, `license` (noun
and verb), `catalog`.

### Section 2 — Multi-word nouns (2.1–2.2)

**2.1** Three words maximum in a noun cluster.

> BAD: `post-assembly tail merging optimization pass` (5)
> GOOD: `an optimization pass that merges tails after assembly`
> BAD: `cross-module local variable storage allocation` (5)
> GOOD: `the allocation of local variable storage across modules`

**2.2** When a technical noun genuinely needs more than three words, write it out
in full once, then either define a short form or hyphenate the unit.

> `The 16-bit unsigned multiply routine (??MUL) ...` then `??MUL` thereafter.

### Section 3 — Verbs (3.1–3.7)

**3.1** Use only the dictionary's verb forms.

**3.2** Only these forms: infinitive, imperative, simple present, simple past,
simple future, and the past participle used as an adjective.  No perfect tenses,
no continuous tenses.

> BAD: `The compiler has been generating relocatable output since v2.`
> GOOD: `The compiler generates relocatable output. Version 2 added this function.`

**3.3** The past participle is permitted as an adjective (`the compiled output`,
`a damaged file`).

**3.4** No auxiliary-verb stacks.

> BAD: `The image may have been being written when power was lost.`
> GOOD: `A power failure can occur while the system writes the image.`

**3.5** The `-ing` form is permitted **only** inside a technical noun.  This
collides head-on with README convention — see Part 6 for headings.

> BAD: `Installing from source is done by cloning the repository.`
> GOOD: `To install from source, clone the repository.`
> LEGAL: `the operating system`, `a floating-point value` (technical nouns)

**3.6** Active voice.  Passive is permitted in descriptive text **only** when the
agent is genuinely unknown.

> BAD: `A unified call graph is built across all modules.`
> GOOD: `The compiler builds one call graph across all modules.`

**3.7** Express an action with a verb, not a nominalization.

> BAD: `Perform an examination of the object file.`
> GOOD: `Examine the object file.`
> BAD: `The utility provides support for compression.`
> GOOD: `The utility decompresses files.`

### Section 4 — Sentences (4.1–4.5)

**4.1** Write short, clear sentences.

**4.2** Do not shorten by dropping words or using contractions.  Keep `that`.

> BAD: `Note the linker defaults to 100H.`
> GOOD: `Note that the linker defaults to 100H.`
> BAD: `They're inherited by every part.`
> GOOD: `Every part inherits them.`

**4.3** Use a vertical list when text becomes complex.

**4.4** Connect related sentences with explicit connecting words (`Then,`,
`Before you do this,`, `As a result,`).

**4.5** Use an article or demonstrative before a noun wherever English allows it.

> BAD: `Compiler emits entry preamble at start of image.`
> GOOD: `The compiler emits the entry preamble at the start of the image.`

### Section 5 — Procedural writing (5.1–5.5) — Tier A only

**5.1** 20 words maximum per sentence, including warnings and cautions.

**5.2** One instruction per sentence, unless two actions truly occur together.

> BAD: `Clone the repository and run pip install -e . then add the bin directory to PATH.`
> GOOD:
> ```
> 1. Clone the repository.
> 2. Run `pip install -e .`
> 3. Add the bin directory to PATH.
> ```

**5.3** Instructions are imperative.  Not "the user should", not "you can now".

**5.4** When a condition must be known first, state the condition, then a comma,
then the command.

> `If the marker file contains the current period key, skip the script.`

**5.5** A note gives information only.  Never hide an instruction inside a note.

> BAD: `Note: you must delete the marker file first.`
> GOOD: `Delete the marker file. Note: the marker file records the last period key.`

### Section 6 — Descriptive writing (6.1–6.6) — Tier B only

**6.1** Release information gradually; one subject per sentence.

**6.2** Use key words and headings to give the text a logical shape.

**6.3** 25 words maximum per sentence.

**6.4** One paragraph per group of related information.

**6.5** One topic per paragraph.

**6.6** Six sentences maximum per paragraph.

### Section 7 — Safety instructions (7.1–7.3)

**7.1** Label the level of risk.  The standard's aerospace pair is
**WARNING** (risk of injury or death) and **CAUTION** (risk of damage).  For
software documentation the useful mapping is:

| Label | Means | Software example |
|---|---|---|
| WARNING | Data loss, or damage outside the tool | Overwrites the target disk image |
| CAUTION | Wrong output, or wasted work | Produces a binary padded with 256 zero bytes |
| NOTE | Information only, no risk | Explains why the default is 100H |

**7.2** Start with the command or the condition, not the explanation.

**7.3** Then give the risk or the result.

> BAD: `Because the linker honors a cseg org, writing 100H: in your source will
>       cause the binary to be padded with 256 zero bytes from 0 to FFH.`
> GOOD:
> ```
> CAUTION: DO NOT WRITE `100H:` IN A PL/M SOURCE FILE.
> The assembler emits `cseg org 100H`. The linker then pads the binary
> with 256 zero bytes from 0 to FFH.
> ```

Put the safety instruction **before** the step it applies to, never after.

### Section 8 — Punctuation and word count (8.1–8.7)

**8.1** No semicolons.  Write two sentences.

**8.2** Hyphenate words that act as one unit before a noun: `16-bit value`,
`command-line option`, `read-only file`, `zero-page memory`.

**8.3** Parentheses are permitted for references, identifiers, step numbers,
abbreviations, singular/plural, short explanations, and alternatives.

**8.4** In a vertical list, a colon ends a sentence for counting purposes.

**8.5** Text in parentheses counts as one word.

**8.6** Each of these counts as **one word**: a number; a number with its unit; an
abbreviation; an alphanumeric identifier; quoted text; a title, heading or label;
a proper noun of a person, group, organization, or geopolitical entity.

**8.7** A hyphenated word counts as one word.

### Section 9 — Writing practices (9.1–9.4) and GR-1…GR-8

**9.1** When a word-for-word substitution does not work, rebuild the sentence.

**9.2** Use each approved word correctly and only as approved.

**9.3** Do not build phrasal verbs.

> BAD: `set up the environment` → GOOD: `prepare the environment`
> BAD: `carry out the test` → GOOD: `do the test`
> BAD: `back up the file` → GOOD: `make a backup of the file`

**9.4** Keep terminology and wording consistent.

**General recommendations:** GR-1 keep the conjunction `that`; GR-2 be careful
with `with`; GR-3 make pronoun references unambiguous; GR-4 never start a sentence
with a bare `This` — write `This file`, `This option`; GR-5 avoid false friends;
GR-6 avoid Latin abbreviations (`e.g.` → `for example`, `i.e.` → `that is`,
`etc.` → name the items or write `and other …`); GR-7 use inclusive language;
GR-8 avoid the possessive form where a prepositional phrase is clearer.

> BAD: `the compiler's output`  GOOD: `the output of the compiler`
> BAD: `Optimization levels (0-3, etc.)`  GOOD: `Optimization levels 0 through 3`

---

## Part 4: The Vocabulary Problem

This is the hardest part of applying STE to software, and where most of the work
goes.

### The escape hatch: technical noun category 19

Issue 9 category 19 is *Computer science, information and communication
technology*, and its examples include: authentication, backup, backup file,
cursor, cybersecurity, database, field, file, firewall, HTML, icon, interface,
internet, laptop, machine learning, memory, menu, metadata, network, operating
system, plug-in, screen, search engine, status bar, token, toolbar, update, XML.

**The category lists are explicitly examples, not an exhaustive list.**  So these
are all legal technical nouns for a retro-computing toolchain:

`compiler, assembler, linker, librarian, disassembler, emulator, opcode,
register, bytecode, object file, symbol table, call graph, peephole optimizer,
stack, heap, buffer, parser, lexer, grammar, image, sector, track, directory
entry, FCB, BDOS, BIOS, zero page, warm boot, story file`

Category 7 (mathematical, scientific, engineering terms) covers the rest:
`checksum, offset, mask, radix, two's complement, relocation record`.

### The escape hatch: technical verb category 2

Issue 9 category 2 is *Computer processes and applications*:

- **2a Input and output:** click, digitize, enter, press, print, swipe, tap, type
- **2b User interface:** clear, close, copy, cut, delete, deselect, disable, drag,
  enable, encrypt, erase, filter, highlight, maximize, minimize, navigate, open,
  paste, save, scroll, sort, store, validate, zoom
- **2c System operations:** abort, boot, communicate, debug, download, format,
  install, load, manage, process, reboot, update, upgrade, upload

Extending by the same logic: `compile, assemble, link, disassemble, parse,
emulate, decompress, relocate, patch, mount, allocate` are legal technical verbs.

**But rule 1.12 caps this:** if a plain approved verb says the same thing, use the
plain verb.  Do not write `instantiate` when `make` works.

### The collision you must plan for

Checked against the Issue 9 dictionary, **every verb a compiler or emulator
README is built from is not approved**:

```
NOT APPROVED:  compile  link  build  run  execute  generate  support
               require  enable  handle  allow  provide  load  emit
               depend  repeat  submit
NOT APPROVED:  via   however   therefore          (connectives!)
APPROVED:      use  do  make  install  start  stop  operate  assemble
               obey  supply  give  get  put  keep  find  show  let  follow
APPROVED:      thus  then  also  because  but  and  or  if  when  after  before
NOUN ONLY:     test  check      (so: "Do a test of X", never "Test X")
```

Following the dictionary literally produces `assemble the compiler`, `operate
make`, and `the emulator holds 48 KB of RAM`.  That is unusable.

**The sanctioned fix is rule 1.12, and you must perform it explicitly.**  Register
your domain verbs as technical verbs under category 2c (system operations) in the
project glossary.  The standard itself puts `boot, install, load, debug,
download, format, process, update` in that category; `compile, link, build,
disassemble, parse, relocate, emulate` are the same kind of operation.

**Write the registration down.  It is a documented deviation, not an oversight.**

Two traps:

- `assemble` and `disassemble` are *already* approved dictionary verbs meaning
  "put together" and "take apart".  Use them in the translation sense only, and
  consistently.
- Where an approved verb states it accurately, use the approved verb.
  `The compiler writes an object file` beats `emits`.
  `The emulator can use 48 KB` beats `supports`.

For connectives, `however` and `therefore` are not approved but `but`, `thus`,
`then`, and `because` are — so the fix costs nothing.

### The part-of-speech collision

STE rule 1.2 fixes each word to one part of speech.  Software English routinely
uses the same token as both noun and verb.  Rules 1.7 and 1.13 forbid this.
Resolve it by choosing which one the word is in your project, then rebuilding the
other usage.

| Word | Problem | Resolution |
|---|---|---|
| build | noun and verb | verb: `Build the project.` / noun: `the compiled output` |
| test | noun in STE | `Do a test of the parser.` not `Test the parser.` |
| backup | noun (cat. 19) | `Do a backup of X.` not `Backup X.` |
| install | verb (cat. 2c) | `Install the package.` not `Do an install.` |
| run | verb | noun sense → `the run of the compiler` → prefer `each time you start it` |
| cache | noun | `Write the data to the cache.` not `Cache the data.` |
| link | verb (cat. 2c) | noun sense → `hyperlink` or `object file reference` |
| debug | verb (cat. 2c) | noun sense → `the debug output` is an adjective use — legal |
| log | noun | `Write a record to the log file.` not `Log the error.` |
| commit | verb | noun sense is git jargon — keep, and gloss it once |
| mask | noun | `Apply the mask to the value.` not `Mask the value.` |
| dump | noun | `Do a dump of memory.` or `Write the memory contents to a file.` |
| patch | noun | `Apply the patch.` not `Patch the file.` |
| boot | verb (cat. 2c) | noun sense → `the boot sector` is adjective use — legal |
| format | verb (cat. 2c) | noun sense → `the file format` — legal as a modifier |
| load | verb (cat. 2c) | noun sense → `the load address` — legal as a modifier |

### Substitution table for software prose

Words that appear constantly in READMEs and should be replaced.  Written in plain
language; this is not a transcription of the STE dictionary.

| Avoid | Use | Why |
|---|---|---|
| leverage, utilize | use | Longer word, no added meaning |
| facilitate, enable (as filler) | lets you, makes X possible | Vague |
| provide support for, support | reads, writes, accepts | Say the actual action |
| handle, deal with | processes, reads, corrects | Vague |
| perform, carry out, execute | do, or the real verb | Rule 3.7 |
| implement | writes, adds, builds | Vague |
| ensure | make sure that | Rule 9.3 |
| allow, permit (of software) | lets you | Clearer agent |
| robust, powerful, seamless | delete, or state the property | Marketing |
| simply, just, easily, merely | delete | Insults a stuck reader |
| blazing fast, lightning | give the measured number | Unverifiable |
| comprehensive, full-featured | list what it does | Unverifiable |
| via | with, by, through | Latin |
| in order to | to | Wordy |
| prior to | before | Wordy |
| subsequent to, following | after | Wordy |
| in the event that | if | Wordy |
| a number of, several | the actual number | Vague |
| e.g. / i.e. / etc. | for example / that is / name them | GR-6 |
| should (for requirements) | must | Ambiguous obligation |
| shall | must | Ambiguous obligation |
| desired, appropriate | the one you want, the correct | Vague |
| leverages the fact that | uses | Wordy |
| note that (as a hedge) | delete, or make it a NOTE block | Rule 5.5 |
| please | delete | Not an instruction |
| feel free to | you can | Idiom |
| out of the box | with no configuration | Idiom |
| under the hood | internally | Idiom |
| kick off, fire off | start | Idiom |
| tweak | adjust, change | Informal |
| nuke, blow away, clobber | delete, overwrite | Slang, rule 1.10 |
| brick | make unserviceable | Slang, rule 1.10 (STE's own example) |
| choke on, barf, die | stops with an error | Slang |
| gotcha | a known problem | Slang |
| sane, sanity check | correct, a check for correctness | Non-inclusive, GR-7 |
| dummy value | placeholder value | GR-7 |
| master/slave | primary/replica, controller/device | GR-7 |
| whitelist/blacklist | allowlist/denylist | GR-7 |
| he, she (generic user) | they, or "the user" | GR-7 |
| and/or | and, or, or name both cases | Ambiguous |
| N/A | not applicable | Abbreviation |

### Is there a software equivalent of the STE dictionary?

**No.** This is a firm negative, not a failed search.

Nothing exists that is simultaneously (a) software-oriented, (b) a genuine
*closed* controlled vocabulary with one part of speech and one approved meaning
per word, and (c) openly licensed.  Kuhn's 2014 survey catalogues 100 English
controlled languages; exactly one names computing — Avaya Controlled English,
~250 terms, an internal 2004 style guide, unobtainable.  Boeing Technical English
was an explicit attempt to de-aerospace Simplified English and was never
deployed.  Caterpillar CTE/CFE, Kodak KISL, Nortel, Ericsson, Alcatel COGRAM,
Perkins PACE, Diebold, IBM EasyEnglish and Sun Proof are all dead and none was
ever published.  Every high-quality controlled vocabulary that does exist —
ASD-STE100, Oxford 3000/5000, the Longman Defining Vocabulary, Globish — is owned
by someone who monetizes it.

### ⚠ Do not use the "open" STE word lists on GitHub

Several repositories ship **verbatim ASD dictionary data under open-source badges
the uploaders had no right to grant**.  They rank well in search and look safe
until you open the data file.  A downstream license badge cannot cure upstream
copyright.

| Repository | Badge | What it actually contains |
|---|---|---|
| `sourdough-bread/asd-ste100-checker` | Apache-2.0 | 2,152 entries with ASD's approved meanings and verbatim examples, plus the Issue 9 PDF |
| `NikolaRHristov/STE-Code` | MIT | Both the Issue 9 and Issue 7 PDFs, ~840 pages of extraction |
| `dfch/biz.dfch.AsdSte100Vocab` | AGPL-3.0 | 2,200 JSONL records each stamped `"source":"STE100:9"` |
| `stilist/text_linter` | none | all rights reserved |
| `openste/openste` | MIT | 909 approved + 1,042 unapproved words; the alternatives mapping is ASD's editorial selection verbatim |

OpenSTE is also useless on the merits: 41 of 56 core software terms are missing
(`directory, server, database, command, repository, commit, parameter, package,
dependency, api, token, cache, path, json, string, module, library, shell,
plugin, debug, boot`) and it maps `file` → *remove*, `execute` → *do*, `compile`
→ *make a list*.  Applied to a README it produces nonsense.

### The stack that is actually legal and useful

Substitute for the dictionary with four layers.  Carry each as a **discrete file
with its own license notice** — do not dissolve them into GPLv3 sources.

| Layer | Source | Size | License | Ship? |
|---|---|---|---|---|
| Core approved vocabulary | **NGSL 1.2** | 2,809 words | CC BY-SA 4.0 | yes, discrete file |
| Substitution pairs (general) | **plainlanguage.gov** "Use simple words and phrases" | 237 pairs | **CC0** | yes, verbatim |
| Avoid-list (software) | **Google developer documentation word list** | 598 entries (~300 useful) | CC BY 4.0 | yes, with NOTICE |
| Substitution pairs (software) | **Microsoft Writing Style Guide A–Z**, GitHub snapshot | 866 entry files | CC BY 4.0 † | yes, with NOTICE |
| Enforcement swaps | **vale-at-red-hat** | ~236 useful pairs | **MIT** | yes, vendor freely |
| Checker engine | **Vale** (`errata-ai/vale`) | — | MIT | yes |
| STE rule skeleton | **`Syntaf/vale-llm-slop`** `styles/STE` | 12 rule files | MIT | yes, fork it |
| Entry-format model | **VOA Special English Word Book** | ~1,500 glosses | public domain | yes |
| Slang detector (**inverted**) | **The Jargon File 4.4.7** | 2,308 headwords | public domain | yes |
| Technical-noun authority | **SEVOCAB** / ISO-IEC-IEEE 24765, **POSIX Base Definitions ch. 3** | 5,404 / 428 terms | proprietary | **cite, never ship** |
| Your technical nouns and verbs | **`docs/glossary.yml`** | you write it | yours | — |

† The GitHub repo's LICENSE is full CC BY 4.0 and controls; the rendered
learn.microsoft.com pages carry a more restrictive notice.  Pin a commit.

**The Jargon File trick is the clever one:** rule 1.10 forbids slang and jargon,
and the Jargon File is 2,308 headwords of precisely the vocabulary STE forbids.
Invert it into a detector.  Curate out the terms that have since become ordinary
technical nouns (`daemon, kludge, patch, regexp, wildcard, spam`).

### What none of them give you

All of these are **open** lists.  STE's mechanism is a **closed** one: ~900 words,
each pinned to one part of speech and one meaning, everything else forbidden
unless it is a technical noun or verb.  You can write a sentence that violates
zero Google word-list entries and is still nowhere near STE.  An avoid-list can
*gate* output; it cannot *generate* it.

The gap is closed by the one artifact nobody can hand you: **`docs/glossary.yml`**,
your project's own closed list of technical nouns and verbs, each with one part of
speech and one meaning plus deprecated aliases.  Rules 1.5, 1.8, 1.11 and 1.12
explicitly instruct every project to maintain exactly this — so authoring it is
*conformance*, not a workaround.  Borrow the record schema from the Red Hat
supplementary style guide (headword, part of speech, description, `use: yes|no`,
incorrect forms, see-also), which is structurally isomorphic to an STE Part 2
record.  Take the schema, not the nouns.

```yaml
# docs/glossary.yml
- term: object file
  pos: noun
  meaning: The relocatable output of the assembler.
  category: technical-noun-19        # computer science / ICT
  do_not_use: [.rel file, REL, obj, output file]
- term: compile
  pos: verb
  meaning: Translate source code into assembly or object code.
  category: technical-verb-2c        # system operations; registered per rule 1.12
  note: Not approved in the STE dictionary. Registered as a technical verb.
```

---

## Part 5: Markdown Skip Regions (Tier E)

Never rewrite text inside these.  A rewrite pass that touches them is a bug.

1. Fenced code blocks — ` ``` ` … ` ``` ` and `~~~` … `~~~`
2. Indented code blocks (4 spaces or a tab, in a code context)
3. Inline code spans — `` `like this` ``
4. URLs, link targets, and reference definitions
5. Image and badge lines — `[![...](...)](...)`
6. YAML/TOML front matter
7. HTML comments and raw HTML blocks
8. License text and SPDX identifiers
9. ASCII art, box drawings, directory trees
10. Tables whose cells are identifiers, opcodes, or values (Tier C: fix prose in
    the description column only, leave the identifier columns alone)
11. Generated content and anything between generator markers
12. Shell prompts and terminal transcripts
13. File paths, flags, and environment variable names anywhere they appear

Practical segmentation: parse the markdown, walk block nodes, and rewrite only
`paragraph`, `list_item` text, `heading`, and `blockquote` content, skipping any
inline `code` node inside them.

---

## Part 6: Headings — Mostly a Non-Problem

**Do not rename your `-ing` headings.**  This is the most common false alarm when
applying STE to a README, and getting it wrong breaks anchors for no reason.

Rule 3.5 restricts `-ing` forms in running prose, but it explicitly permits an
`-ing` word used as a technical noun, and the standard names *procedural titles
and headings* as the example case.  Its own legal examples include `Cleaning`,
`Handling`, `Packaging`, `Shipping`, and `Troubleshooting`.

Therefore these are **already conformant** and need no change:

`Installing` · `Building` · `Testing` · `Troubleshooting` · `Contributing` ·
`Configuring` · `Debugging` · `Packaging` · `Logging`

A typical README's heading ladder is ~95% conformant as it stands.

### The two worth considering

| Heading | Change to | Why |
|---|---|---|
| `Getting Started` | `Quick Start` | `Getting` takes a complement, so it is a gerund phrase rather than a process noun |
| `Building from Source` | `Building` | Same reason; the bare process noun is cleaner |

Make either change **only** after `grep -rn '#the-old-anchor'` across the repo
family returns empty.  Renaming a heading breaks in-repo links, sibling-repo
links, and external bookmarks.  If you must rename, leave `<a id="old-anchor"></a>`
behind.

### Where `-ing` genuinely must go

In running prose, as a progressive tense or a gerund phrase:

> BAD: `When you are building the compiler, make sure that Python 3.12 is installed.`
> GOOD: `Before you build the compiler, make sure that Python 3.12 is installed.`

Compound technical nouns keep their `-ing` everywhere: `operating system`,
`floating-point value`, `calling convention`, `bank switching`, `tail merging`.

---

## Part 7: Word Counting (Rules 8.4–8.7)

To check the 20-word and 25-word limits you must count the way the standard
counts, not the way `wc -w` counts.

Each of the following is **one word**:

- A number: `256`, `0x100`, `3.14`
- A number with its unit: `256 bytes`, `100 MHz`, `16 bit`
- An abbreviation: `BDOS`, `CPU`, `PDF`
- An alphanumeric identifier: `??MUL`, `PIP.COM`, `0100H`
- Quoted text: `"Hello, World!$"`
- A title, heading, placard, or label
- A proper noun of a person, group, organization, or geopolitical entity:
  `Digital Research`, `Martin Homuth-Rosemann`
- A hyphenated word: `command-line`, `read-only`, `16-bit`
- Any parenthetical: `(see BDOS_REFERENCE.md)` counts as 1

A colon in a vertical list ends the sentence for counting.

**Software extension** (the standard does not cover these; this is a defensible
convention — apply it consistently):

| Element | Count as | Reason |
|---|---|---|
| Inline code span `` `--opt-level=2` `` | 1 | It is an alphanumeric identifier |
| A file path `/usr/local/bin/uplm80` | 1 | Single identifier |
| A URL | 1 | Single identifier |
| A flag `-m cpm` | 1 | One option with its argument |
| A function name `parse_header()` | 1 | Single identifier |
| A code fence | 0 | Not prose |

Worked example:

> `Run the compiler with the -m bare option to rebuild PIP.COM byte-compatibly.`
>
> Run(1) the(2) compiler(3) with(4) the(5) `-m bare`(6) option(7) to(8)
> rebuild(9) PIP.COM(10) byte-compatibly(11) = **11 words**.  Within the Tier A
> limit of 20.

---

## Part 8: The Rewrite Workflow for One Repo

1. **Read everything first.**  Do not rewrite file by file in isolation.  Rules
   1.11 and 9.4 need a whole-project view of terminology.
2. **Build the glossary.**  List every technical noun the project uses and pick
   one canonical name for each concept.  Write it to `docs/GLOSSARY.md`.  This
   satisfies rule 1.8 and is the deliverable with the longest useful life.
   ```markdown
   | Term | Meaning | Do not use |
   |---|---|---|
   | object file | Relocatable output of the assembler | .rel file, REL, obj |
   | work step | One numbered instruction in a procedure | stage, phase |
   ```
3. **Segment.**  Mark every region with its tier (Part 2).  Verify the Tier E
   regions are complete before touching anything.
4. **Rewrite by tier**, safety text first (highest value), then procedures, then
   descriptive prose.  Leave Tier C mostly alone.
5. **Verify mechanically** — see Part 10.
6. **Read the result end to end.**  A rule-compliant document can still be worse
   than what it replaced.  If it is, revert that section.
7. **Commit with the before/after visible.**  Documentation-only commit, no code
   changes mixed in, so the diff is reviewable.

### Rollout across many repos

- **Pilot on one repo first** and read the whole result before doing any others.
- Order: highest-traffic repos first, or the ones with the most install friction.
- **One pull request per repo**, never a bulk direct push.  You want the diff
  reviewable and revertible.
- Keep a `STE-STATUS.md` or a checklist issue so the pass is resumable.
- Do not rewrite a repo's README and its docs/ in the same PR.
- Re-run the glossary step per repo family (all the CP/M tools share terminology
  and should share a glossary).

---

## Part 9: Source Code Comments — Be Conservative

**Recommendation: rewrite selectively, and default to leaving comments alone.**

Rewriting comments churns `git blame` for no functional gain and risks destroying
information that is dense on purpose.

| Comment kind | Rewrite? | Why |
|---|---|---|
| Public API docstrings / doc comments | Yes | Generated into user-facing docs |
| File header blocks | Yes | Orientation for new readers |
| Procedure/function summary lines | Yes | Same audience as docs |
| Module overview comments | Yes | Descriptive text, Tier B |
| Inline `// why this is here` notes | **No** | Dense, contextual, high loss risk |
| Algorithm derivations, math notes | **No** | Needs subordinate clauses |
| Citations, paper references, URLs | **No** | Tier E |
| TODO / FIXME / HACK | **No** | Conventional markers |
| Commented-out code | **No** | Not prose |
| Generated headers, license blocks | **No** | Tier E |

When you do rewrite a doc comment, preserve the syntax exactly — the `@param`,
`:param:`, `\brief` structure is machine-read.  Rewrite only the prose after the
tag.

---

## Part 10: What Can Be Checked Mechanically

| Check | Rule | Method | False positives |
|---|---|---|---|
| Sentence too long | 5.1, 6.3 | Split on `.!?`, count per Part 7 | Abbreviations with periods |
| Semicolon | 8.1 | Literal `;` outside code | Code in prose, HTML entities |
| Contraction | 4.2 | `\b\w+'(s|t|re|ve|ll|d|m)\b` | Possessives, quoted output |
| `-ing` form | 3.5 | Word-initial capital + `ing\b` in headings; participles in prose | Technical nouns |
| Passive voice | 3.6 | `be`-verb + past participle | Adjectival participles |
| Multi-word noun run | 2.1 | 4+ consecutive nouns/adjectives (needs POS tagging) | Product names |
| Paragraph too long | 6.6 | Count sentences per paragraph | Lists |
| Banned word | various | Word list from Part 4 | Quoted text |
| Latin abbreviation | GR-6 | `\b(e\.g\.|i\.e\.|etc\.|vs\.)` | Bibliographies |
| Missing article | 4.5 | Needs POS tagging | Headings, list items |
| Terminology drift | 1.11, 9.4 | Glossary "do not use" column | — |

**Needs a language model, not a script:** approved-meaning checks (1.3),
technical-noun categorization (1.5), whether a rewrite preserved the meaning,
whether a paragraph has one topic (6.5), whether a note contains a hidden
instruction (5.5), and whether the result reads well.

There is no free official checker.  Commercial tools exist (HyperSTE, Congree,
Acrolinx) and are priced for enterprises.  A practical approach is a small script
for the table above plus a model pass for the rest.

---

## Part 11: What NOT To Do

**DO NOT rewrite the whole README at one strictness level.**  Tier the document
first.  This is the mistake that produces unusable output.

**DO NOT touch anything in a code fence, table of opcodes, or inline code span.**
Byte-identical or it is a bug.

**DO NOT rewrite the project's one-line description.**  It is the repo's
identity, it appears on GitHub, and STE will not improve it.

**DO NOT apply the 20-word procedural limit to descriptive prose.**  That limit
is Tier A only.  Applying it to an architecture section produces staccato text.

**DO NOT claim "ASD-STE100 compliant."**  You cannot verify it without the
dictionary.  Say "written in the style of."

**DO NOT ship the dictionary or a transcription of it.**  See Part 1.

**DO NOT invent a technical verb when a plain verb works.**  Rule 1.12 forbids it.
`Use the file`, not `Utilize the file`; `Make the object`, not `Instantiate`.

**DO NOT change headings that other documents link to** without checking the
anchors.

**DO NOT mix a documentation rewrite with code changes** in one commit.

**DO NOT rewrite inline `// why` comments.**  Highest churn, lowest gain.

**DO NOT delete the nuance.**  If a sentence is long because the idea is
genuinely conditional, split it into a condition and a command (rule 5.4) — do
not drop the condition.

---

## Part 12: Checklist

Per document:

- [ ] Every region assigned a tier. Tier E regions verified byte-identical
- [ ] Glossary written; one name per concept (1.11)
- [ ] No sentence over 20 words in Tier A, 25 in Tier B (counted per Part 7)
- [ ] No semicolons (8.1)
- [ ] No contractions; `that` retained (4.2)
- [ ] No `-ing` outside technical nouns (3.5)
- [ ] Active voice, except unknown-agent descriptive passives (3.6)
- [ ] Instructions imperative, one per sentence (5.2, 5.3)
- [ ] Conditions before commands, comma-separated (5.4)
- [ ] Warnings and cautions labeled, placed before their step (7.1–7.3)
- [ ] No noun cluster over three words (2.1)
- [ ] No Latin abbreviations (GR-6)
- [ ] No bare sentence-initial `This` (GR-4)
- [ ] No slang, jargon, or idiom (1.10)
- [ ] Inclusive language (GR-7)
- [ ] American spelling (1.14)
- [ ] Code blocks byte-identical to the original
- [ ] Read end to end — it is genuinely clearer than what it replaced

---

## Sources

**The standard**

- ASD-STE100 Simplified Technical English, Issue 9, 2025-01-15.
  © ASD, Brussels.  Free official copy: **https://asd-ste100.org/**
  Rule numbering and section structure follow Issue 9 Part 1.
  All rule statements here are paraphrase; all examples are original.

**Evidence**

- Chervak, S. & Drury, C. (n=175) and Shubert, S. et al. (1995) — the measured
  comprehension gains for Simplified English are concentrated in difficult
  procedural text read by non-native speakers.
- Kuhn, T. (2014), *A Survey and Classification of Controlled Natural
  Languages*, Computational Linguistics 40(1) — 100 English CNLs catalogued;
  one names computing as its domain.

**Word lists (see Part 4)**

- NGSL 1.2 — https://newgeneralservicelist.com/ — CC BY-SA 4.0
- plainlanguage.gov simple words and phrases — CC0 / US public domain
- Google developer documentation style guide word list —
  https://developers.google.com/style/word-list — CC BY 4.0
- Microsoft Writing Style Guide A–Z —
  https://github.com/MicrosoftDocs/microsoft-style-guide — CC BY 4.0 (pin a commit)
- vale-at-red-hat — https://github.com/redhat-documentation/vale-at-red-hat — MIT
- Vale — https://github.com/errata-ai/vale — MIT
- `Syntaf/vale-llm-slop` `styles/STE` — MIT
- VOA Special English Word Book — US public domain
- The Jargon File 4.4.7 — http://catb.org/jargon/ — public domain
- SEVOCAB (ISO/IEC/IEEE 24765) and POSIX Base Definitions — cite, do not ship

**Related style guides**

Google's guide, the Microsoft Writing Style Guide, and Diátaxis agree with STE on
active voice, short sentences, condition-before-command, and deleting
`simply`/`easily`.  They disagree on contractions and second person, which both
Google and Microsoft encourage and STE forbids.  Diátaxis's *explanation* quadrant
is the same territory as Tier D and is defined as requiring alternatives, opinion,
and outside connections — the opposite of a controlled language's design goal.
