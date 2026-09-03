#!/usr/bin/env python3
"""Remove the language pie chart from a github-profile-3d-contrib SVG.

The action has no "calendar without the pie" type, and the pie duplicates the
languages card that sits right under it. This finds the smallest <g> that wraps
both the pie's arcs and its legend and drops it.
"""

import re
import sys
from pathlib import Path

LEGEND_LAST = ">other<"


def enclosing_groups(svg, pos):
    """Yield (start, end) of every <g>…</g> that contains `pos`, innermost first."""
    opens = [m for m in re.finditer(r"<g\b[^>]*>", svg) if m.start() < pos]
    for m in reversed(opens):
        depth, i = 0, m.start()
        for t in re.finditer(r"<g\b[^>]*>|</g>", svg[m.start():]):
            depth += 1 if t.group(0) != "</g>" else -1
            if depth == 0:
                end = m.start() + t.end()
                if end > pos:
                    yield m.start(), end
                break


def strip(svg):
    legend = svg.find(LEGEND_LAST)
    if legend < 0:
        return svg, False
    for start, end in enclosing_groups(svg, legend):
        block = svg[start:end]
        # The pie's group holds arc paths and the legend; the calendar group does not
        # contain the legend at all, and the outer wrapper contains everything.
        if "<path" in block and block.count("<rect") < 40:
            return svg[:start] + svg[end:], True
    return svg, False


def main(argv):
    for name in argv:
        path = Path(name)
        out, done = strip(path.read_text())
        if done:
            path.write_text(out)
        print(f"{'stripped' if done else 'no pie  '} {path}")
    return 0 if argv else 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
