#!/usr/bin/env python3
"""Build the neon banner and typing line as self-contained SVGs.

Lettering is converted to outlines (see text_to_path) because a webfont cannot
load inside an SVG that GitHub serves as an <img>. Run this after editing the
palette or the copy; the output is committed and does not need regenerating on a
schedule, unlike the data-driven cards.

    scripts/build-neon-assets.py --fonts <dir-with-ChakraPetch-*.ttf>
"""

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from text_to_path import measure, to_path  # noqa: E402

# GTA VI marketing palette: Miami sunset over a deep violet night.
NIGHT = "#0B0518"
DEEP = "#1A0B33"
PURPLE = "#4B1D80"
MAGENTA = "#C42A8E"
PINK = "#FF3D7F"
CORAL = "#FF6B4A"
ORANGE = "#FF9142"
GOLD = "#FFC24B"
AQUA = "#37D6C4"
LILAC = "#E8D9F0"
MUTED = "#9C8AB8"

NAME = "VIKTAR HUSHCHYNSKI"
KICKER = "SYSTEM ONLINE"
SUBTITLE = "SENIOR ENGINEER // CLOUD // SYSTEMS // FIRMWARE"

STACK = ["AZURE", ".NET", "C#", "RUST", "GO", "TYPESCRIPT", "LINUX", "ESP32"]

PHRASES = [
    "Twenty years of building software.",
    "Enterprise systems and cloud by day.",
    "Rust, Go and Linux tooling by night.",
    "Firmware when a project calls for it.",
]


def tidy(d):
    """Round path coordinates; full float precision triples the file size."""
    return re.sub(r"-?\d+\.\d+", lambda m: f"{float(m.group()):.2f}".rstrip("0").rstrip("."), d)


def fmt(v):
    return f"{v:.4f}".rstrip("0").rstrip(".")


def build_banner(fonts, out):
    W, H = 1200, 230
    VY = 158                      # horizon
    bold = fonts / "ChakraPetch-Bold.ttf"
    med = fonts / "ChakraPetch-Medium.ttf"

    name_size, name_track = 52, 3
    name_w = measure(NAME, bold, name_size, name_track)
    name_d, _ = to_path(NAME, bold, name_size, x=(W - name_w) / 2, y=112, tracking=name_track)

    kick_size, kick_track = 13, 7
    kick_w = measure(KICKER, med, kick_size, kick_track)
    kick_d, _ = to_path(KICKER, med, kick_size, x=(W - kick_w) / 2, y=56, tracking=kick_track)

    sub_size, sub_track = 14, 5
    sub_w = measure(SUBTITLE, med, sub_size, sub_track)
    sub_d, _ = to_path(SUBTITLE, med, sub_size, x=(W - sub_w) / 2, y=202, tracking=sub_track)

    rays = "".join(f'<line x1="600" y1="{VY}" x2="{x}" y2="{H}"/>' for x in range(-900, 2101, 110))
    hor, y, step = "", VY + 4, 3.0
    while y < H:
        hor += f'<line x1="0" y1="{y:.1f}" x2="{W}" y2="{y:.1f}"/>'
        step *= 1.42
        y += step

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{NAME} - Senior Engineer">
  <defs>
    <linearGradient id="sunset" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="{GOLD}"/>
      <stop offset="42%" stop-color="{ORANGE}"/>
      <stop offset="78%" stop-color="{PINK}"/>
      <stop offset="100%" stop-color="{MAGENTA}"/>
    </linearGradient>
    <linearGradient id="letters" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="{GOLD}"/>
      <stop offset="45%" stop-color="{ORANGE}"/>
      <stop offset="100%" stop-color="{PINK}"/>
    </linearGradient>
    <linearGradient id="floor" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="{PINK}" stop-opacity="0.6"/>
      <stop offset="100%" stop-color="{PURPLE}" stop-opacity="0.05"/>
    </linearGradient>
    <radialGradient id="halo" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0%" stop-color="{PURPLE}" stop-opacity="0.55"/>
      <stop offset="100%" stop-color="{PURPLE}" stop-opacity="0"/>
    </radialGradient>
    <pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse">
      <rect width="4" height="1.4" fill="{LILAC}" opacity="0.04"/>
    </pattern>
    <filter id="glow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="4.5" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="soft" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="3.4" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <clipPath id="frame"><rect width="{W}" height="{H}" rx="10"/></clipPath>
    <clipPath id="below"><rect y="{VY}" width="{W}" height="{H - VY}"/></clipPath>
  </defs>

  <g clip-path="url(#frame)">
    <rect width="{W}" height="{H}" fill="{NIGHT}"/>
    <rect width="{W}" height="{H}" fill="{DEEP}" opacity="0.65"/>
    <ellipse cx="600" cy="150" rx="640" ry="205" fill="url(#halo)"/>

    <circle cx="600" cy="162" r="74" fill="url(#sunset)" opacity="0.62" filter="url(#soft)"/>

    <g clip-path="url(#below)" stroke="url(#floor)" stroke-width="1" fill="none">
      {rays}
      {hor}
    </g>
    <line x1="0" y1="{VY}" x2="{W}" y2="{VY}" stroke="{PINK}" stroke-width="1.4" opacity="0.7" filter="url(#soft)"/>

    <rect width="{W}" height="{H}" fill="url(#scan)"/>
    <rect x="0" y="0" width="{W}" height="26" fill="{GOLD}" opacity="0.06">
      <animate attributeName="y" values="-30;{H}" dur="5s" repeatCount="indefinite"/>
    </rect>

    <path d="{tidy(kick_d)}" fill="{AQUA}" opacity="0.9"/>

    <g>
      <path d="{tidy(name_d)}" fill="{PINK}" opacity="0.5" transform="translate(-2.5,0)">
        <animate attributeName="transform" values="translate(-2.5,0);translate(-7,0);translate(1,0);translate(-2.5,0);translate(-2.5,0);translate(-2.5,0);translate(-2.5,0);translate(-2.5,0)" dur="4.5s" repeatCount="indefinite"/>
      </path>
      <path d="{tidy(name_d)}" fill="{AQUA}" opacity="0.45" transform="translate(2.5,0)">
        <animate attributeName="transform" values="translate(2.5,0);translate(7,0);translate(-1,0);translate(2.5,0);translate(2.5,0);translate(2.5,0);translate(2.5,0);translate(2.5,0)" dur="4.5s" repeatCount="indefinite"/>
      </path>
      <path d="{tidy(name_d)}" fill="url(#letters)" filter="url(#glow)"/>
    </g>

    <path d="{tidy(sub_d)}" fill="{LILAC}" opacity="0.92"/>
  </g>
</svg>
'''
    out.write_text(svg)
    return len(svg)


def build_stack(fonts, out):
    """A row of technology chips, replacing a wall of shields.io images."""
    H, GAP, PAD_X = 40, 10, 15
    W = 900
    med = fonts / "ChakraPetch-SemiBold.ttf"
    size, track = 13, 2.4
    r = 6

    labels = [(t, measure(t, med, size, track)) for t in STACK]
    chips = [(t, w + 2 * PAD_X) for t, w in labels]
    total = sum(c[1] for c in chips) + GAP * (len(chips) - 1)
    x = (W - total) / 2

    accents = [GOLD, ORANGE, PINK, MAGENTA]
    parts = []
    for i, ((text, tw), (_, cw)) in enumerate(zip(labels, chips)):
        accent = accents[i % len(accents)]
        d, _ = to_path(text, med, size, x=x + PAD_X, y=H / 2 + size * 0.36, tracking=track)
        parts.append(
            f'  <g>\n'
            f'    <rect x="{fmt(x)}" y="{fmt((H - 26) / 2)}" width="{fmt(cw)}" height="26" rx="{r}"\n'
            f'      fill="{DEEP}" stroke="{accent}" stroke-opacity="0.45"/>\n'
            f'    <path d="{tidy(d)}" fill="{accent}"/>\n'
            f'  </g>')
        x += cw + GAP

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{", ".join(STACK)}">
{chr(10).join(parts)}
</svg>
'''
    out.write_text(svg)
    return len(svg), total


def build_typing(fonts, out):
    W, H = 900, 48
    CX, BASE = W / 2, 32
    CPS_TYPE, CPS_DEL = 17.0, 45.0
    HOLD, GAP = 1.9, 0.25
    CUR_W, CUR_GAP, PAD = 11, 6, 10
    semi = fonts / "ChakraPetch-SemiBold.ttf"
    size, track = 22, 0.6

    widths = [measure(p, semi, size, track) for p in PHRASES]
    left = [CX - w / 2 for w in widths]
    paths = [tidy(to_path(p, semi, size, x=left[i], y=BASE, tracking=track)[0])
             for i, p in enumerate(PHRASES)]

    type_t = [len(p) / CPS_TYPE for p in PHRASES]
    del_t = [len(p) / CPS_DEL for p in PHRASES]

    # Frame 0 shows phrase 0 already typed, so a viewer whose browser refuses to
    # advance the animation still reads a finished sentence.
    marks = {0: {"hold_end": HOLD}}
    t = HOLD + del_t[0]
    marks[0]["del_end"] = t
    t += GAP
    for i in range(1, len(PHRASES)):
        marks[i] = {"start": t, "typed": t + type_t[i]}
        t = marks[i]["typed"] + HOLD
        marks[i]["hold_end"] = t
        t += del_t[i]
        marks[i]["del_end"] = t
        t += GAP
    marks[0]["retype_start"] = t
    LOOP = t + type_t[0]

    def kt(vals):
        out_ = [min(max(v, 0.0), 1.0) for v in vals]
        for i in range(1, len(out_)):
            out_[i] = max(out_[i], out_[i - 1])
        return ";".join(fmt(v) for v in out_)

    def clip(i, times, vals, static):
        return (f'<clipPath id="t{i}"><rect x="{fmt(left[i] - PAD)}" y="0" height="{H}" width="{fmt(static)}">\n'
                f'      <animate attributeName="width" dur="{fmt(LOOP)}s" repeatCount="indefinite"\n'
                f'        keyTimes="{kt(times)}" values="{";".join(fmt(v) for v in vals)}"/></rect></clipPath>')

    m, full0 = marks[0], widths[0] + 2 * PAD
    clips = [clip(0, [0, m["hold_end"] / LOOP, m["del_end"] / LOOP, m["retype_start"] / LOOP, 1],
                  [full0, full0, 0, 0, full0], full0)]
    for i in range(1, len(PHRASES)):
        m, fi = marks[i], widths[i] + 2 * PAD
        clips.append(clip(i, [0, m["start"] / LOOP, m["typed"] / LOOP, m["hold_end"] / LOOP,
                              m["del_end"] / LOOP, 1], [0, 0, fi, fi, 0, 0], 0))

    end = lambda i: left[i] + widths[i] + CUR_GAP
    pts = [(0.0, end(0)), (marks[0]["hold_end"], end(0)), (marks[0]["del_end"], left[0])]
    for i in range(1, len(PHRASES)):
        m = marks[i]
        pts += [(m["start"], left[i]), (m["typed"], end(i)), (m["hold_end"], end(i)), (m["del_end"], left[i])]
    pts += [(marks[0]["retype_start"], left[0]), (LOOP, end(0))]

    bodies = "\n".join(
        f'    <g clip-path="url(#t{i})"><path d="{paths[i]}" fill="url(#line)"/></g>'
        for i in range(len(PHRASES)))

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{PHRASES[0]}">
  <defs>
    <linearGradient id="line" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{GOLD}"/>
      <stop offset="50%" stop-color="{ORANGE}"/>
      <stop offset="100%" stop-color="{PINK}"/>
    </linearGradient>
{chr(10).join('    ' + c for c in clips)}
  </defs>

{bodies}

  <rect y="13" width="{CUR_W}" height="23" fill="{PINK}" x="{fmt(end(0))}">
    <animate attributeName="x" dur="{fmt(LOOP)}s" repeatCount="indefinite"
      keyTimes="{kt([p[0] / LOOP for p in pts])}" values="{';'.join(fmt(p[1]) for p in pts)}"/>
    <animate attributeName="opacity" dur="1s" repeatCount="indefinite"
      keyTimes="0;0.49;0.5;0.99;1" values="1;1;0.15;0.15;1"/>
  </rect>
</svg>
'''
    out.write_text(svg)
    return len(svg), LOOP, max(widths)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fonts", required=True, type=Path)
    ap.add_argument("--out", default=Path("assets"), type=Path)
    a = ap.parse_args()

    n = build_banner(a.fonts, a.out / "banner-neon.svg")
    print(f"banner-neon.svg  {n:>7} bytes")
    n, loop, widest = build_typing(a.fonts, a.out / "typing-neon.svg")
    print(f"typing-neon.svg  {n:>7} bytes  loop={loop:.1f}s  widest phrase={widest:.0f}px")
    n, row = build_stack(a.fonts, a.out / "stack-neon.svg")
    print(f"stack-neon.svg   {n:>7} bytes  row width={row:.0f}px")


if __name__ == "__main__":
    main()
