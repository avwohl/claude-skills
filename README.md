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

Eliminates guesswork when positioning UI elements near rounded screen edges.

## Tools

Companion scripts that implement skill algorithms.

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
