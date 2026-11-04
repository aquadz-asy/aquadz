"""Generate the AQuadZ logo files from one definition.

Four isometric cubes fit together into one block, one colour each, clockwise from the top:
red, yellow, blue, green. Run `python3 brand/make_logo.py` from the repository root after
changing anything here; it rewrites the SVG files listed at the bottom.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Clockwise from the top (back) cube: (name, base colour, position, fly-in offset).
CUBES = [
    ("red", "#ef4444", (0.0, -0.53), (0.0, -2.2)),
    ("yellow", "#f5b301", (0.92, 0.0), (2.2, 0.0)),
    ("green", "#16b364", (-0.92, 0.0), (-2.2, 0.0)),
    ("blue", "#2f6bff", (0.0, 0.53), (0.0, 2.2)),
]
# Painting order back to front (the front cube overlaps its neighbours).
PAINT = ["red", "yellow", "green", "blue"]
# Beat order: clockwise from the top.
HOP = {"red": 0, "yellow": 1, "blue": 2, "green": 3}


def _mix(hex_colour: str, other: str, amount: float) -> str:
    a = [int(hex_colour[i : i + 2], 16) for i in (1, 3, 5)]
    b = [int(other[i : i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(x + (y - x) * amount):02x}" for x, y in zip(a, b))


def gradients() -> str:
    out = []
    for name, base, _, _ in CUBES:
        top_a, top_b = _mix(base, "#ffffff", 0.55), _mix(base, "#ffffff", 0.2)
        left_a, left_b = _mix(base, "#ffffff", 0.08), _mix(base, "#000000", 0.12)
        right_a, right_b = _mix(base, "#000000", 0.22), _mix(base, "#000000", 0.42)
        out.append(
            f'<linearGradient id="{name}-t" x1="0" y1="0" x2="1" y2="1">'
            f'<stop offset="0" stop-color="{top_a}"/><stop offset="1" stop-color="{top_b}"/></linearGradient>'
            f'<linearGradient id="{name}-l" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="{left_a}"/><stop offset="1" stop-color="{left_b}"/></linearGradient>'
            f'<linearGradient id="{name}-r" x1="0" y1="0" x2="1" y2="1">'
            f'<stop offset="0" stop-color="{right_a}"/><stop offset="1" stop-color="{right_b}"/></linearGradient>'
        )
    return "".join(out)


TOP = "0,-1 0.866,-0.5 0,0 -0.866,-0.5"
LEFT = "-0.866,-0.5 0,0 0,1 -0.866,0.5"
RIGHT = "0,0 0.866,-0.5 0.866,0.5 0,1"
OUTLINE = "0,-1 0.866,-0.5 0.866,0.5 0,1 -0.866,0.5 -0.866,-0.5"


def cube(name: str) -> str:
    return (
        f'<polygon points="{TOP}" fill="url(#{name}-t)"/>'
        f'<polygon points="{LEFT}" fill="url(#{name}-l)"/>'
        f'<polygon points="{RIGHT}" fill="url(#{name}-r)"/>'
        # light catching the top edges
        '<polyline points="-0.866,-0.5 0,0 0.866,-0.5" fill="none" stroke="#fff" stroke-opacity=".55" stroke-width=".035" stroke-linejoin="round"/>'
        '<polyline points="0,0 0,1" fill="none" stroke="#fff" stroke-opacity=".18" stroke-width=".03"/>'
    )


def mark(animated: bool, prefix: str = "") -> str:
    """The four cubes. `prefix` keeps ids unique when several marks share one page."""
    by_name = {c[0]: c for c in CUBES}
    parts = []
    for name in PAINT:
        _, _, (x, y), (dx, dy) = by_name[name]
        body = cube(name).replace("url(#", f"url(#{prefix}")
        if animated:
            parts.append(
                f'<g class="q-in" style="--dx:{dx}px;--dy:{dy}px;--i:{HOP[name]}">'
                f'<g transform="translate({x} {y})"><g class="q-beat" style="--i:{HOP[name]}">{body}</g></g></g>'
            )
        else:
            parts.append(f'<g transform="translate({x} {y})">{body}</g>')
    clip = "".join(
        f'<polygon transform="translate({x} {y})" points="{OUTLINE}"/>' for _, _, (x, y), _ in CUBES
    )
    shine = (
        f'<clipPath id="{prefix}q-clip">{clip}</clipPath>'
        f'<linearGradient id="{prefix}q-shine" x1="0" y1="0" x2="1" y2="0">'
        '<stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".45"/>'
        '<stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
    )
    grads = gradients().replace('id="', 'id="' + prefix)
    defs = "<defs>" + grads + shine + "</defs>"
    sweep = (
        f'<g clip-path="url(#{prefix}q-clip)"><rect class="q-shine" x="-3" y="-2" width="1.4" height="4" '
        f'fill="url(#{prefix}q-shine)" transform="skewX(-20)"/></g>'
        if animated
        else ""
    )
    return defs + "".join(parts) + sweep


ANIM_CSS = """
.q-in{animation:q-in .9s cubic-bezier(.2,.9,.25,1.2) both;animation-delay:calc(var(--i)*.12s)}
.q-beat{animation:q-beat 2.4s ease-in-out infinite;animation-delay:calc(1.2s + var(--i)*.18s)}
.q-shine{animation:q-shine 6s ease-in-out infinite;animation-delay:2.6s;opacity:0}
@keyframes q-in{from{transform:translate(var(--dx),var(--dy)) scale(.5);opacity:0}to{transform:none;opacity:1}}
@keyframes q-beat{0%,60%,100%{transform:none}14%{transform:scale(1.12)}30%{transform:scale(.95)}44%{transform:scale(1.02)}}
@keyframes q-shine{0%{transform:translateX(0) skewX(-20deg);opacity:0}5%{opacity:1}22%{transform:translateX(6px) skewX(-20deg);opacity:0}100%{opacity:0}}
@media (prefers-reduced-motion:reduce){.q-in,.q-beat,.q-shine{animation:none}.q-shine{display:none}}
"""

VIEW_MARK = "-1.95 -1.7 3.9 3.4"
VIEW_SQUARE = "-1.95 -1.95 3.9 3.9"


def svg(view: str, body: str, css: str = "", title: str = "AQuadZ") -> str:
    style = f"<style>{css}</style>" if css else ""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{view}" role="img" aria-label="{title}">'
        f"<title>{title}</title>{style}{body}</svg>\n"
    )


def main() -> None:
    (ROOT / "brand" / "logo-mark.svg").write_text(svg(VIEW_MARK, mark(False)))
    (ROOT / "brand" / "logo-mark-animated.svg").write_text(svg(VIEW_MARK, mark(True), ANIM_CSS))
    (ROOT / "favicon.svg").write_text(svg(VIEW_SQUARE, mark(False)))
    # Inline marks in the pages: the first brand mark on a page animates (header), the others
    # are still (footer). Ids are prefixed per occurrence so each page stays valid.
    import re

    for page in ("index.html", "privacy.html", "brand/index.html"):
        path = ROOT / page
        if not path.exists():
            continue
        html = path.read_text()
        count = 0

        def repl(match: re.Match) -> str:
            nonlocal count
            count += 1
            animated = count == 1
            prefix = f"m{count}-"
            classes = match.group(1)
            return f'<svg class="{classes}" viewBox="{VIEW_MARK}" aria-hidden="true">{mark(animated, prefix)}</svg>'

        html = re.sub(r'<svg class="(brand-mark[^"]*)".*?</svg>', repl, html, flags=re.S)
        path.write_text(html)


if __name__ == "__main__":
    main()
