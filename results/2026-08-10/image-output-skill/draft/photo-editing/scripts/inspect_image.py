#!/usr/bin/env python3
"""Measure an image before editing it. Prints JSON facts to stdout.

Usage: python3 inspect_image.py <image_path>

Requires Pillow (pip install pillow). Every edit decision — crop box, resize
target, format conversion — should start from these measured numbers, never
from visual estimation: rendered previews hide padding, EXIF rotation, and
alpha, and a crop planned by eye inherits all three errors.

content_bounds follows PIL's crop-box convention (right/bottom exclusive),
so it can be passed to Image.crop() as-is.
"""
import json
import sys

from PIL import Image, ImageChops, ExifTags

# 10/255 ≈ 4% channel difference: below this, a border pixel is "the same
# color" as the corner for content-bounds purposes. Tolerates JPEG noise
# without eating real content.
BORDER_TOLERANCE = 10


def content_bounds(im):
    """Bounding box of content that differs from the border color, or None
    if the image is one flat color. Border color is sampled at (0, 0)."""
    rgb = im.convert("RGB")
    border = Image.new("RGB", rgb.size, rgb.getpixel((0, 0)))
    diff = ImageChops.difference(rgb, border)
    diff = diff.point(lambda p: 255 if p > BORDER_TOLERANCE else 0)
    return diff.getbbox()


def exif_orientation(im):
    """EXIF Orientation tag value (1-8) or None. Values other than 1 mean
    the stored pixels are rotated/flipped relative to how viewers show them —
    apply ImageOps.exif_transpose() before any geometry math."""
    try:
        exif = im.getexif()
    except Exception:
        return None
    return exif.get(next(k for k, v in ExifTags.TAGS.items()
                         if v == "Orientation"), None) if exif else None


def main():
    if len(sys.argv) != 2:
        print(__doc__, file=sys.stderr)
        sys.exit(2)
    path = sys.argv[1]
    im = Image.open(path)
    bounds = content_bounds(im)
    w, h = im.size
    facts = {
        "path": path,
        "format": im.format,
        "mode": im.mode,
        "size": {"width": w, "height": h},
        "has_alpha": im.mode in ("RGBA", "LA", "PA")
                     or "transparency" in im.info,
        "exif_orientation": exif_orientation(im),
        "content_bounds": {"left": bounds[0], "top": bounds[1],
                           "right": bounds[2], "bottom": bounds[3]}
                          if bounds else None,
        "uniform_border_px": {"left": bounds[0], "top": bounds[1],
                              "right": w - bounds[2],
                              "bottom": h - bounds[3]}
                             if bounds else None,
    }
    print(json.dumps(facts, indent=2))


if __name__ == "__main__":
    main()
