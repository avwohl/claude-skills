# Conversion notes — iospharo README

Source: [avwohl/iospharo](https://github.com/avwohl/iospharo) README.md at commit
`d2ba26187721`.  Converted with `skills/simplified-technical-english.md`.

This is the account's highest-starred repo (13★).  It was chosen as the second
case because it exercises **all five conformance tiers**, including the two that
the uplm80 case cannot demonstrate: **Tier D (VOICE)** and a Tier E region that
is a *legal instrument* rather than code.

## Measured result

| Rule | What it detects | before | after |
|---|---|---:|---:|
| 3.6 | Passive voice | 8 | 2 † |
| GR-6 | Latin abbreviation / `via` | 6 | 1 † |
| 8.1 | Semicolon | 6 | 5 † |
| 3.5 | `-ing` outside a technical noun | 6 | 3 † |
| 6.3 | Sentence over 25 words | 1 | **0** |
| GR-4 | Bare sentence-initial `This` | 1 | **0** |
| 4.2 | Contraction | 1 | **0** |
| 2.1 | Long multi-word noun | 0 | 1 ‡ |
| **Total** | | **29** | **12** |

† **10 of the 12 remaining are inside Tier D and Tier E regions that were
deliberately not touched.**  Only 2 are in editable prose, and both are checker
false positives.  A tier-blind tool reports 12 problems here; 10 of them are the
tool being wrong about what it is allowed to edit.

‡ 2.1 heuristic false positive — `because local repository support needs it` is
an ordinary clause, not a noun cluster.

## The two tiers this case exists to show

### Tier D — VOICE: the `## Status` section, untouched

```
**VM core (solid):**
- **99.90% test pass rate** on Mac Catalyst (13,040 / 13,053)
```

Not one character changed.  `(solid)`, `(working)`, and the exact fraction
`13,040 / 13,053` are calibrated claims.  A tier-blind STE pass would "improve"
`99.90% test pass rate` into something declarative and would be tempted to drop
the parenthetical hedges.  **Deleting a hedge converts an honest claim into an
overclaim — a correctness bug, not a style change.**

The same protection covers the `**Note:** Pharo 12 and earlier…` limitation.  Its
sentence *was* split for readability (rule 6.3 territory), but its content — that
the VM does not yet handle that layout — is preserved exactly, including
"not yet".

### Tier E — a license condition that only looks like prose

The final line of the file is:

> This software is based in part on the work of the Independent JPEG Group.

This is **required wording under the IJG license**, not a sentence about the
project.  Paraphrasing it is a legal change, not an editorial one.  The entire
`## Credits and Acknowledgements` block is Tier E for the same reason: every
`(MIT; Copyright 2008-2019 …)` string is an attribution obligation.

Those attributions are also the source of 5 of the 6 remaining "semicolon
violations".  **A semicolon inside a copyright notice is not a style defect.**
This is the clearest illustration in either sample of why the checker's output
must be read against the tier map rather than obeyed.

## What changed in Tier A and Tier B

### 8.1 — the one semicolon that was a real violation

> **before:** `The first Xcode build will take several minutes while it compiles the VM; subsequent builds are fast unless you change VM sources.`
>
> **after:** `The first Xcode build takes some minutes, because it compiles the VM. Subsequent builds are fast, unless you change the VM sources.`

Semicolon removed, progressive `will take … while it compiles` reduced to simple
present, and the causal relation made explicit with `because`.

### 3.6 / GR-4 — agentless "This …" openers

The build steps repeatedly opened with a bare `This`, which GR-4 forbids and
which also hides the agent:

| before | after |
|---|---|
| This downloads, cross-compiles, and packages libffi… | These scripts download, cross-compile, and package libffi… |
| This downloads source tarballs and builds for… | The script downloads source tarballs. Then it builds them for… |
| Cairo, freetype … **are cross-compiled** as static xcframeworks | This script **cross-compiles** cairo, freetype … |
| The xcframeworks **are gitignored** due to size | The xcframeworks are large, thus `.gitignore` contains them |
| Pharo images **are downloaded** in-app | The app downloads the Pharo images |
| Touch gestures **are mapped** to Pharo mouse events | The app maps touch gestures to Pharo mouse events |

### 5.2 — one instruction per sentence

> **before:** `copy Local.xcconfig.example to Local.xcconfig and fill in your Apple Developer Team ID.`
>
> **after:**
> ```
> 1. Copy `Local.xcconfig.example` to `Local.xcconfig`.
> 2. Put your Apple Developer Team ID in `Local.xcconfig`.
> ```

Two actions became two numbered steps, so a reader who fails at step 2 knows
exactly where they are.

### GR-6 — Latin removed

`via Catalyst` → `through Catalyst`; `via FFI` → `through FFI`;
`e.g. after a git pull` → `for example, after a git pull`;
`(stubbed SDL2, missing font glyphs, etc.)` → `for example the stubbed SDL2 and
the missing font glyphs`.

`etc.` inside the Status bullet list was **left alone** — Tier D.

### GR-8 / first person

`The image's OSSDL2Driver` → `The OSSDL2Driver of the image`.
`Our SDL2 stubs` → `The SDL2 stubs of this project`.

### 6.6 — paragraph split

The Startup patches paragraph ran to 7 sentences (max 6).  Split at the natural
boundary between *what the app does automatically* and *what you can add
yourself*.

## Tier E invariants — verified

| Invariant | Result |
|---|---|
| Code fences | 8 before, 8 after, **byte-identical** |
| URLs | 21 before, 21 after, **none dropped** |
| `## Status` block (Tier D) | **unchanged** |
| `## Credits and Acknowledgements` (Tier E) | **unchanged** |
| `## Related` (Tier E) | **unchanged** |
| Architecture box diagram | **unchanged** |
| Project-structure tree | **unchanged** |

## The lesson from this case

uplm80 shows what STE *fixes*.  iospharo shows what STE must be *stopped from
touching*.  The second is the harder engineering problem, and it is why the tier
map is the first artifact you produce and the checker output is the last thing
you trust.
