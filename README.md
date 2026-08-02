# Claude Skills

Open source skills for [Claude Code](https://claude.ai/code) -- reusable
knowledge, algorithms, and reference data packaged as markdown files.

## What are skills?

Claude Code skills are markdown files that live in `.claude/skills/` in your
project.  They load on-demand when the topic is relevant, or manually via
`/skill-name`.  Unlike CLAUDE.md (loaded every session), skills only consume
context when needed.

Each skill has a YAML front matter header:

```yaml
---
name: device-geometry
description: iPhone/iPad screen geometry and squircle math for layout
---
```

Followed by the reference content, algorithms, worked examples, and
implementation guidance.

## Available Skills

### device-geometry

iPhone and iPad screen dimensions, corner radii, safe area insets, notch
and Dynamic Island measurements for every Face ID iPhone model.  Includes
the exact superellipse (n=5) formula for computing squircle corner intrusion
at any screen coordinate, with verified worked examples and a pixel bitmask
generation algorithm.

Eliminates guesswork when positioning UI elements near camera cutouts and
rounded screen edges.

### apple-hig

Apple Human Interface Guidelines reference covering typography (Dynamic Type
sizes, SF Pro text styles, the complete size table from xSmall to AX5), color
system (semantic and system colors for light/dark mode), layout (8pt grid,
spacing tokens, margins, component heights, safe areas), UI components (bars,
buttons, sheets, alerts with SwiftUI mappings), navigation patterns
(hierarchical, flat, modal), accessibility checklist (Dynamic Type, VoiceOver,
contrast ratios, Reduce Motion), app icon requirements, platform differences
(iPhone vs iPad vs Mac), and the Liquid Glass design system introduced in
iOS 26.

Includes a "what NOT to do" section with the 12 most common HIG violations.

### simplified-technical-english

Applies [ASD-STE100 Simplified Technical English](https://asd-ste100.org/)
Issue 9 to software documentation -- READMEs, INSTALL/BUILD docs, CLI `--help`
text, man pages, API docs, and source comments.

All 53 writing rules paraphrased with software examples, plus the two things
that make the standard usable outside aerospace: the **technical noun/verb
categories** (Issue 9 added category 19 "computer science, ICT" and verb
category 2 "computer processes", which legalize `compiler`, `opcode`, `linker`,
`boot`, `debug`, `install`) and a **five-tier conformance system** so the rules
are applied at the right strength per document region.

The fifth tier is the important one: a named VOICE region where STE is
deliberately switched off, because rewriting hedged prose ("runs green apart
from a few known failures") deletes the hedge and turns a calibrated claim into
an overclaim -- a correctness bug, not a style change.

Also covers the vocabulary collision (the dictionary rejects `compile`, `link`,
`build`, `run`, `execute`, `support`, and even `however` and `therefore`) and
the rule 1.12 registration step that resolves it legally.

Ships no dictionary: ASD-STE100 Part 2 is copyright ASD Brussels and its free
reproduction grant does not cover a public repo.  The skill is rules-only and
says so.

### ios-app-scaffold

Complete recipe for creating a new iOS/Mac Catalyst app from scratch using
XcodeGen.  Covers project.yml configuration, Config.xcconfig with optional
Local.xcconfig for code signing, asset catalog setup, app icon generation
(RGB, no alpha), Info.plist keys needed for App Store validation, and the
full setup sequence from `mkdir` to `gh repo create`.

Handles the private-vs-public repo decision (team ID in project.yml vs
gitignored Local.xcconfig) and includes a "what NOT to do" section covering
the alpha channel, missing icon keys, and export compliance pitfalls.

## Tools

Companion scripts that implement skill algorithms.

### tools/generate_ios_icon.py

Generates iOS + Mac Catalyst app icons at all required sizes (16px through
1024px).  Always outputs RGB with no alpha channel.  Supports built-in shapes
(paw print, circle, text) or use as a starting point for custom icons.

```bash
pip3 install Pillow
python3 tools/generate_ios_icon.py --bg '#E8683A' --shape paw output_dir/
python3 tools/generate_ios_icon.py --bg '#2A9D8F' --shape text --text 'AB' output_dir/
python3 tools/generate_ios_icon.py --bg '30,120,200' --shape none output_dir/
```

### tools/apply_device_mask.py

Overlays a device screen mask on a simulator screenshot.  Renders squircle
corners, Dynamic Island / notch cutout, and optional safe area boundary lines.
Auto-detects device from pixel dimensions.

```bash
pip3 install Pillow numpy
python3 tools/apply_device_mask.py screenshot.png              # basic mask
python3 tools/apply_device_mask.py --safe-areas screenshot.png # + safe area lines
python3 tools/apply_device_mask.py --device iphone16pro screenshot.png
```

### tools/ste_check.py

Mechanical ASD-STE100 checks for Markdown.  Implements only the automatable
subset (sentence length using the standard's own word-counting rules, semicolons,
contractions, `-ing` forms, passive voice, Latin abbreviations, banned words,
phrasal verbs, paragraph length).  Skips code fences, inline code, tables, URLs,
badges and ASCII art.  Ships no dictionary.

```bash
python3 tools/ste_check.py --tier A docs/INSTALL.md   # procedural, 20-word limit
python3 tools/ste_check.py --tier B README.md         # descriptive, 25-word limit
python3 tools/ste_check.py --json before.md after.md
python3 tools/ste_check.py --quiet --max-issues 0 README.md   # CI gate
```

Its `2.1` and `3.5` checks are heuristics without a POS tagger and will produce
false positives.  Read them; do not obey them blindly.

## Samples

Before/after conversions demonstrating a skill on real files from live repos.

### samples/ste100/

ASD-STE100 conversions, each with `before.md`, `after.md`, and a `NOTES.md`
giving rule-by-rule rationale, measured issue counts, and -- just as important --
what was deliberately left alone and why.

Two cases, chosen to show opposite things:

- **[uplm80](samples/ste100/uplm80-readme/)** (engagement leader) -- what STE
  fixes.  40 mechanical issues to 6, all 10 code fences byte-identical, and a
  data-corrupting hazard buried in a 43-word sentence promoted to a labeled
  CAUTION block.
- **[iospharo](samples/ste100/iospharo-readme/)** (highest-starred) -- what STE
  must not touch.  All five tiers, with a `## Status` section left untouched to
  protect its calibrated hedges, and a credits block whose semicolons are
  copyright notices.  10 of its 12 remaining "violations" are in regions that
  were correctly not edited.

## Installation

Copy a skill file into your project:

```bash
mkdir -p .claude/skills
cp skills/device-geometry.md .claude/skills/
```

Or symlink to keep it updated:

```bash
mkdir -p .claude/skills
ln -s /path/to/claude-skills/skills/device-geometry.md .claude/skills/
```

## Contributing

PRs welcome.  A good skill:

- Solves a problem that causes repeated trial-and-error across sessions
- Contains precise, unambiguous algorithms (not vague guidance)
- Includes worked examples that serve as correctness checks
- Lists common mistakes in a "what NOT to do" section
- References authoritative sources

## Related

Other repos in this collection:

- [iospharo](https://github.com/avwohl/iospharo) — Virtual machine for Pharo Smalltalk on iOS and macOS. The C++ interpreter runs Pharo 13 and Pharo 14 images without a just-in-time compiler, and it uses low-bit oop encoding to work with ASLR.
- [pharo-headless-test](https://github.com/avwohl/pharo-headless-test) — Headless test runner for Pharo Smalltalk with a fake GUI. It clicks menus, takes screenshots, and runs the SUnit suite without a display.
- [soogle](https://github.com/avwohl/soogle) — Search engine for Smalltalk source code. It indexes packages and labels each one with its dialect, such as Pharo, Squeak, or GemStone.
- [validate_smalltalk_image](https://github.com/avwohl/validate_smalltalk_image) — Standalone validator and export tool for Spur-format Smalltalk images. It checks the heap, and it writes SHA-256 manifests and reference graphs.

## License

GPLv3 -- see LICENSE file.
