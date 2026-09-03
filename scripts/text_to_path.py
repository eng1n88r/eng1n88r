#!/usr/bin/env python3
"""Convert text to SVG path data using a TTF.

GitHub serves README images as <img>, and raw.githubusercontent.com sends
`default-src 'none'` — so an SVG cannot pull a webfont, whether by @import or by
a data: @font-face. Naming a family in font-family only works if the viewer
happens to have it installed, which for Chakra Petch is nobody.

Outlines sidestep all of it: the glyphs travel with the file and render the same
everywhere. The trade is that the text stops being selectable, which is fine for
banner lettering and not fine for body copy.
"""

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

_cache = {}


def _load(ttf):
    if ttf not in _cache:
        font = TTFont(ttf)
        _cache[ttf] = (font, font.getGlyphSet(), font.getBestCmap(),
                       font["head"].unitsPerEm, font["hmtx"])
    return _cache[ttf]


def measure(text, ttf, size, tracking=0.0):
    """Advance width of `text` in user units, including tracking between glyphs."""
    font, glyphs, cmap, upem, hmtx = _load(ttf)
    scale = size / upem
    total = 0.0
    for ch in text:
        name = cmap.get(ord(ch))
        if name is None:
            continue
        total += hmtx[name][0] * scale + tracking
    return total - tracking if text else 0.0


def to_path(text, ttf, size, x=0.0, y=0.0, tracking=0.0):
    """Return (path_d, width) with the baseline at `y` and the left edge at `x`."""
    font, glyphs, cmap, upem, hmtx = _load(ttf)
    scale = size / upem
    sink = SVGPathPen(glyphs)
    pen_x = x
    for ch in text:
        name = cmap.get(ord(ch))
        if name is None:
            continue
        # Font space is Y-up; SVG is Y-down, hence the negative vertical scale.
        glyphs[name].draw(TransformPen(sink, (scale, 0, 0, -scale, pen_x, y)))
        pen_x += hmtx[name][0] * scale + tracking
    return sink.getCommands(), (pen_x - tracking - x if text else 0.0)


def metrics(ttf, size):
    """Ascent and descent in user units, for vertical centring."""
    font, _, _, upem, _ = _load(ttf)
    hhea = font["hhea"]
    scale = size / upem
    return hhea.ascent * scale, -hhea.descent * scale
