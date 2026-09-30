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

- **device-geometry** - iPhone and iPad screen geometry and squircle corner math
- **apple-hig** - Apple Human Interface Guidelines reference
- **simplified-technical-english** - ASD-STE100 Simplified Technical English for software documentation
- **ios-app-scaffold** - recipe for a new iOS/Mac Catalyst app with XcodeGen

The `skills/` directory holds every skill file.

## Tools and Samples

- `tools/generate_ios_icon.py` - iOS and Mac Catalyst app icons at all sizes
- `tools/apply_device_mask.py` - device screen mask over a simulator screenshot
- `tools/ste_check.py` - mechanical ASD-STE100 checks for Markdown
- `samples/ste100/` - before/after ASD-STE100 conversions of real READMEs

## Documentation

- [Available skills](docs/skills.md) - a detailed description of each skill
- [Tools and samples](docs/tools_and_samples.md) - tool usage, command examples and the ASD-STE100 samples

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
