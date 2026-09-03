#!/usr/bin/env python3
"""Bake CSS animation end-states into an SVG's style block.

GitHub embeds README images with <img>, and CSS animations inside an SVG loaded
that way do not run. Cards from github-readme-stats lean on animations to reveal
their content (`.stagger { opacity: 0; animation: fadeInAnimation ... }`), so
they render blank on a profile even though they look fine when opened directly.

This rewrites each `animation: <name> ...` declaration into the `to { }` block of
the matching @keyframes, which is the state the animation would have settled on.
Order matters: the substituted declarations are appended last so they win over
the starting values above them.
"""

import re
import sys
from pathlib import Path


def _block_at(text, open_brace):
    """Return (body, index_after_close) for the {...} starting at open_brace."""
    depth = 0
    for i in range(open_brace, len(text)):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return text[open_brace + 1 : i], i + 1
    raise ValueError("unbalanced braces in style block")


def collect_keyframes(css):
    """Map each @keyframes name to the declarations in its `to` (or `100%`) step."""
    frames = {}
    for m in re.finditer(r"@keyframes\s+([\w-]+)\s*\{", css):
        body, _ = _block_at(css, m.end() - 1)
        for step in re.finditer(r"(?:^|\})\s*(to|100%)\s*\{", body):
            decls, _ = _block_at(body, step.end() - 1)
            frames[m.group(1)] = decls.strip()
    return frames


def bake(css, frames):
    """Replace `animation: name ...;` with the end-state declarations it targets."""
    def sub(m):
        name = m.group(1)
        decls = frames.get(name)
        if decls is None:
            return ""
        decls = " ".join(d.strip() for d in decls.split("\n") if d.strip())
        if not decls.endswith(";"):
            decls += ";"
        return decls

    return re.sub(r"animation:\s*([\w-]+)[^;]*;", sub, css)


def process(path):
    svg = path.read_text()
    style = re.search(r"<style>(.*?)</style>", svg, re.S)
    if not style:
        return False

    css = style.group(1)
    frames = collect_keyframes(css)
    if not frames:
        return False

    baked = bake(css, frames)
    if baked == css:
        return False

    path.write_text(svg[: style.start(1)] + baked + svg[style.end(1) :])
    return True


def main(argv):
    if not argv:
        print("usage: bake-svg-animations.py <svg> [svg ...]", file=sys.stderr)
        return 2
    for name in argv:
        path = Path(name)
        print(f"{'baked   ' if process(path) else 'no-op   '} {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
