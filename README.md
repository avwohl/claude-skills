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

## License

GPLv3 -- see LICENSE file.
