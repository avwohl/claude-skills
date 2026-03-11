#!/usr/bin/env python3
"""Generate iOS + Mac Catalyst app icons at all required sizes.

Usage:
    python3 generate_ios_icon.py --bg '#E8683A' --shape paw output_dir/
    python3 generate_ios_icon.py --bg '#2A9D8F' --shape circle --fg '#FFFFFF' output_dir/
    python3 generate_ios_icon.py --bg '30,120,200' --text 'AB' output_dir/

Icons are always RGB (no alpha channel) to pass App Store validation.
"""

import argparse
import os
import sys

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("pip3 install Pillow", file=sys.stderr)
    sys.exit(1)

SIZE = 1024

ALL_SIZES = [16, 20, 29, 32, 40, 58, 60, 64, 76, 80, 87,
             120, 128, 152, 167, 180, 256, 512, 1024]


def parse_color(s):
    """Parse '#RRGGBB' or 'R,G,B' into (r, g, b) tuple."""
    s = s.strip().lstrip('#')
    if ',' in s:
        parts = [int(x.strip()) for x in s.split(',')]
        return tuple(parts[:3])
    if len(s) == 6:
        return (int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16))
    raise ValueError(f"Cannot parse color: {s}")


def draw_paw(draw, cx, cy, color):
    """Draw a paw print centered at (cx, cy)."""
    # Main pad — tri-lobed
    draw.ellipse([cx-140, cy-20, cx+140, cy+180], fill=color)
    draw.ellipse([cx-165, cy-50, cx-10, cy+130], fill=color)
    draw.ellipse([cx+10, cy-50, cx+165, cy+130], fill=color)
    # Four toe beans
    for x, y, rx, ry in [
        (cx-175, cy-175, 55, 65),
        (cx-65, cy-235, 52, 62),
        (cx+65, cy-235, 52, 62),
        (cx+175, cy-175, 55, 65),
    ]:
        draw.ellipse([x-rx, y-ry, x+rx, y+ry], fill=color)


def draw_circle_shape(draw, cx, cy, color):
    """Draw a filled circle centered in the icon."""
    r = 200
    draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=color)


def draw_text_shape(draw, cx, cy, color, text):
    """Draw centered text."""
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 400)
    except (OSError, IOError):
        font = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text((cx - tw/2, cy - th/2 - bbox[1]), text, fill=color, font=font)


def generate(bg_color, fg_color, shape, text, output_dir):
    img = Image.new('RGB', (SIZE, SIZE), bg_color)
    draw = ImageDraw.Draw(img)
    cx, cy = SIZE // 2, SIZE // 2 + 28  # slight vertical offset for visual center

    if shape == 'paw':
        draw_paw(draw, cx, cy, fg_color)
    elif shape == 'circle':
        draw_circle_shape(draw, cx, cy, fg_color)
    elif shape == 'text':
        draw_text_shape(draw, cx, cy, fg_color, text or '?')
    # shape == 'none': solid background only

    os.makedirs(output_dir, exist_ok=True)
    for s in ALL_SIZES:
        resized = img.resize((s, s), Image.LANCZOS) if s != SIZE else img
        resized.save(os.path.join(output_dir, f'icon_{s}.png'))

    print(f"Generated {len(ALL_SIZES)} icons in {output_dir}/")
    print(f"Mode: RGB (no alpha) — ready for App Store")


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('output_dir', help='Directory to write icon_*.png files')
    parser.add_argument('--bg', default='#E8683A', help='Background color (#hex or R,G,B)')
    parser.add_argument('--fg', default='#FFFFFF', help='Foreground color (#hex or R,G,B)')
    parser.add_argument('--shape', choices=['paw', 'circle', 'text', 'none'],
                        default='paw', help='Icon shape (default: paw)')
    parser.add_argument('--text', default=None, help='Text to render (with --shape text)')
    args = parser.parse_args()

    generate(
        bg_color=parse_color(args.bg),
        fg_color=parse_color(args.fg),
        shape=args.shape,
        text=args.text,
        output_dir=args.output_dir,
    )


if __name__ == '__main__':
    main()
