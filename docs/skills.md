# Available Skills

## device-geometry

iPhone and iPad screen dimensions, corner radii, safe area insets, notch
and Dynamic Island measurements for every Face ID iPhone model.  Includes
the exact superellipse (n=5) formula for computing squircle corner intrusion
at any screen coordinate, with verified worked examples and a pixel bitmask
generation algorithm.

Eliminates guesswork when positioning UI elements near camera cutouts and
rounded screen edges.

## apple-hig

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

## simplified-technical-english

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

## ios-app-scaffold

Complete recipe for creating a new iOS/Mac Catalyst app from scratch using
XcodeGen.  Covers project.yml configuration, Config.xcconfig with optional
Local.xcconfig for code signing, asset catalog setup, app icon generation
(RGB, no alpha), Info.plist keys needed for App Store validation, and the
full setup sequence from `mkdir` to `gh repo create`.

Handles the private-vs-public repo decision (team ID in project.yml vs
gitignored Local.xcconfig) and includes a "what NOT to do" section covering
the alpha channel, missing icon keys, and export compliance pitfalls.
