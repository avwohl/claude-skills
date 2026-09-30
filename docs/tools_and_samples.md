# Tools and Samples

Companion scripts that implement skill algorithms.

## tools/generate_ios_icon.py

Generates iOS + Mac Catalyst app icons at all required sizes (16px through
1024px).  Always outputs RGB with no alpha channel.  Supports built-in shapes
(paw print, circle, text) or use as a starting point for custom icons.

```bash
pip3 install Pillow
python3 tools/generate_ios_icon.py --bg '#E8683A' --shape paw output_dir/
python3 tools/generate_ios_icon.py --bg '#2A9D8F' --shape text --text 'AB' output_dir/
python3 tools/generate_ios_icon.py --bg '30,120,200' --shape none output_dir/
```

## tools/apply_device_mask.py

Overlays a device screen mask on a simulator screenshot.  Renders squircle
corners, Dynamic Island / notch cutout, and optional safe area boundary lines.
Auto-detects device from pixel dimensions.

```bash
pip3 install Pillow numpy
python3 tools/apply_device_mask.py screenshot.png              # basic mask
python3 tools/apply_device_mask.py --safe-areas screenshot.png # + safe area lines
python3 tools/apply_device_mask.py --device iphone16pro screenshot.png
```

## tools/ste_check.py

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

- **[uplm80](../samples/ste100/uplm80-full-rewrite/)** (engagement leader) -- what STE
  fixes.  40 mechanical issues to 6, all 10 code fences byte-identical, and a
  data-corrupting hazard buried in a 43-word sentence promoted to a labeled
  CAUTION block.
- **[iospharo](../samples/ste100/iospharo-full-rewrite/)** (highest-starred) -- what STE
  must not touch.  All five tiers, with a `## Status` section left untouched to
  protect its calibrated hedges, and a credits block whose semicolons are
  copyright notices.  10 of its 12 remaining "violations" are in regions that
  were correctly not edited.
