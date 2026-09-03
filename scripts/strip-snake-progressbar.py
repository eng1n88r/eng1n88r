#!/usr/bin/env python3
"""Remove the stacked progress bar from a Platane/snk contribution-snake SVG.

snk draws a segmented bar under the grid that fills as the snake eats cells. It
reads as a UI chrome element bolted onto the animation, so this strips the bar
(its rects, CSS rules and keyframes) and crops the canvas back to the grid plus
the margin the snake actually moves through.
"""

import re
import sys
from pathlib import Path

CELL = 12       # .c { width/height: 12px }
MARGIN = 34     # snk's own gap between grid and bar; the snake travels in it


def strip(svg):
    # The bar's rects all carry class="u uN".
    svg = re.sub(r'<rect\b[^>]*class="u u\d+"[^>]*/?>(?:</rect>)?', "", svg)

    # ...along with their styling and animations.
    # Segments are compound selectors (`.u.u0{...}`); eat the whole selector, or a
    # dangling `.u` fuses onto the next rule and takes the snake's fill with it.
    svg = re.sub(r'(?:\.u\d*)+\s*\{[^}]*\}', "", svg)
    svg = re.sub(r'@keyframes\s+u\d+\s*\{(?:[^{}]|\{[^{}]*\})*\}', "", svg)

    # Crop the canvas: the bar sat below the grid, so the box can end a margin
    # under the last row instead of a bar's height further down.
    m = re.search(r'viewBox="(-?[\d.]+) (-?[\d.]+) ([\d.]+) ([\d.]+)"', svg)
    if not m:
        return svg
    x, y, w, _ = (float(v) for v in m.groups())

    rows = [float(r) for r in re.findall(r'<rect\b[^>]*class="c[^"]*"[^>]*\by="([\d.]+)"', svg)]
    if not rows:
        return svg

    height = (max(rows) + CELL + MARGIN) - y
    svg = svg.replace(m.group(0), f'viewBox="{x:g} {y:g} {w:g} {height:g}"')
    return re.sub(r'(<svg\b[^>]*?)\bheight="[\d.]+"', rf'\1height="{height:g}"', svg, count=1)


def main(argv):
    if not argv:
        print("usage: strip-snake-progressbar.py <svg> [svg ...]", file=sys.stderr)
        return 2
    for name in argv:
        path = Path(name)
        before = path.read_text()
        after = strip(before)
        path.write_text(after)
        bars = before.count('class="u u')
        print(f"{path}: removed {bars} bar segment(s), "
              f"{re.search(r'viewBox=\"[^\"]*\"', after).group(0)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
