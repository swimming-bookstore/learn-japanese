#!/usr/bin/env python3
"""LinkedIn 1080×1080 plate: katakana ネ (ne) vs レ (re).

Same plate as swimming-bookstore/how-to-devops: cream wash, tracked
kicker, serif title, navy table, bookstore footer.

Left column is ネ. Right column is レ. Under each katakana: hiragana,
then the English reading, with n and r highlighted. Title is a Can you
question and uses the katakana, not the romaji.
The subtitle is an example: ネックレス (necklace).
"""

from __future__ import annotations

from pathlib import Path

import cairo

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "linkedin-katakana-ne-re.png"
SVG = ROOT / "docs" / "linkedin-katakana-ne-re.svg"

W = H = 1080
CREAM = (1.0, 0xF9 / 255, 0xEF / 255)
NAVY = (0x1D / 255, 0x35 / 255, 0x50 / 255)
TAUPE = (0x6A / 255, 0x5C / 255, 0x4E / 255)
CREAM_HEX = "#fff9ef"
NAVY_HEX = "#1d3550"
TAUPE_HEX = "#6a5c4e"

SERIF = "Liberation Serif"
SERIF_CJK = "Noto Serif CJK JP"
SANS = "Lato"

LEFT, TOP, RIGHT, BOTTOM = 56, 278, 1024, 930
MID = 540
COLS = [
    ("ネ", "ね", "ne"),
    ("レ", "れ", "re"),
]


def set_font(cr: cairo.Context, family: str, size: float, bold: bool = False, italic: bool = False) -> None:
    cr.select_font_face(
        family,
        cairo.FONT_SLANT_ITALIC if italic else cairo.FONT_SLANT_NORMAL,
        cairo.FONT_WEIGHT_BOLD if bold else cairo.FONT_WEIGHT_NORMAL,
    )
    cr.set_font_size(size)


def center(cr: cairo.Context, x: float, y: float, text: str, family: str, size: float, fill, bold: bool = False, italic: bool = False) -> None:
    set_font(cr, family, size, bold=bold, italic=italic)
    cr.set_source_rgb(*fill)
    ext = cr.text_extents(text)
    cr.move_to(x - (ext.x_bearing + ext.width / 2), y - (ext.y_bearing + ext.height / 2))
    cr.show_text(text)


def advance(cr: cairo.Context, text: str, family: str, size: float, bold: bool = False) -> float:
    set_font(cr, family, size, bold=bold)
    return cr.text_extents(text).x_advance


def center_runs(cr: cairo.Context, x: float, baseline: float, runs: list[tuple[str, str, float, bool]], fill) -> None:
    """Draw mixed-font runs on one baseline, centered on x. Run is text, family, size, bold."""
    widths = [advance(cr, text, family, size, bold) for text, family, size, bold in runs]
    cursor = x - sum(widths) / 2
    cr.set_source_rgb(*fill)
    for (text, family, size, bold), width in zip(runs, widths):
        set_font(cr, family, size, bold=bold)
        cr.move_to(cursor, baseline)
        cr.show_text(text)
        cursor += width


def render_png() -> None:
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    cr = cairo.Context(surf)
    cr.set_source_rgb(*CREAM)
    cr.paint()

    set_font(cr, SANS, 20, bold=True)
    cr.set_source_rgb(*TAUPE)
    kicker = "JAPANESE ESSENTIAL"
    gap = 7.2
    widths = [cr.text_extents(ch).width for ch in kicker]
    tw = sum(widths) + gap * (len(kicker) - 1)
    x = (W - tw) / 2
    y = 84
    for ch, wch in zip(kicker, widths):
        xb, yb, _tw, th, _xa, _ya = cr.text_extents(ch)
        cr.move_to(x - xb, y - (yb + th / 2))
        cr.show_text(ch)
        x += wch + gap

    center_runs(
        cr,
        540,
        176,
        [
            ("Can you tell ", SERIF, 48, True),
            ("ネ", SERIF_CJK, 52, True),
            (" from ", SERIF, 48, True),
            ("レ", SERIF_CJK, 52, True),
        ],
        NAVY,
    )
    center_runs(
        cr,
        540,
        228,
        [
            ("Example: ", SERIF, 28, False),
            ("ネックレス", SERIF_CJK, 30, False),
            (" (necklace)", SERIF, 28, False),
        ],
        TAUPE,
    )

    body_top = TOP
    centers = [(LEFT + MID) / 2, (MID + RIGHT) / 2]

    cr.set_source_rgba(*NAVY, 0.045)
    cr.rectangle(MID, body_top, RIGHT - MID, BOTTOM - body_top)
    cr.fill()

    reading_baseline = 832
    for (glyph, hira, reading), cx in zip(COLS, centers):
        center(cr, cx, 500, glyph, SERIF_CJK, 188, NAVY)
        center(cr, cx, 700, hira, SERIF_CJK, 84, NAVY)
        set_font(cr, SERIF, 44, bold=True)
        letter, rest = reading[0], reading[1:]
        lb = cr.text_extents(letter)
        rb = cr.text_extents(rest)
        gap = 10
        total = lb.x_advance + gap + rb.x_advance
        start = cx - total / 2
        pad_x, pad_y = 7, 5
        cr.set_source_rgb(*NAVY)
        cr.rectangle(
            start + lb.x_bearing - pad_x,
            reading_baseline + lb.y_bearing - pad_y,
            lb.width + pad_x * 2,
            lb.height + pad_y * 2,
        )
        cr.fill()
        cr.set_source_rgb(*CREAM)
        cr.move_to(start, reading_baseline)
        cr.show_text(letter)
        cr.set_source_rgb(*NAVY)
        cr.move_to(start + lb.x_advance + gap, reading_baseline)
        cr.show_text(rest)

    cr.set_source_rgb(*NAVY)
    cr.set_line_width(2)
    cr.rectangle(LEFT, TOP, RIGHT - LEFT, BOTTOM - TOP)
    cr.stroke()

    cr.set_line_width(2)
    cr.move_to(MID, TOP)
    cr.line_to(MID, BOTTOM)
    cr.stroke()

    center(cr, 540, 992, "© 수영 책방 Swimming Bookstore", "Noto Serif CJK KR", 20, TAUPE)
    surf.write_to_png(str(OUT))


def esc(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;")


def render_svg() -> None:
    """Hand SVG of the same plate. Cairo SVG text does not embed CJK reliably."""
    left_cx = (LEFT + MID) / 2
    right_cx = (MID + RIGHT) / 2
    lines = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1080" viewBox="0 0 1080 1080" role="img" aria-label="Can you tell ネ from レ">',
        f'  <rect width="1080" height="1080" fill="{CREAM_HEX}"/>',
        "",
        f'  <text x="540" y="90" text-anchor="middle" font-family="Lato, Outfit, ui-sans-serif, system-ui, sans-serif" font-size="20" font-weight="700" letter-spacing="7.2" fill="{TAUPE_HEX}">JAPANESE ESSENTIAL</text>',
        '  <text y="176" fill="#1d3550" font-weight="700">',
        '    <tspan x="295.5" font-family="Liberation Serif, serif" font-size="48">Can you tell </tspan>',
        '    <tspan font-family="Noto Serif CJK JP, Noto Serif CJK KR, serif" font-size="52">ネ</tspan>',
        '    <tspan font-family="Liberation Serif, serif" font-size="48"> from </tspan>',
        '    <tspan font-family="Noto Serif CJK JP, Noto Serif CJK KR, serif" font-size="52">レ</tspan>',
        "  </text>",
        '  <text y="236" fill="#6a5c4e">',
        '    <tspan x="347.5" font-family="Liberation Serif, serif" font-size="28">Example: </tspan>',
        '    <tspan font-family="Noto Serif CJK JP, Noto Serif CJK KR, serif" font-size="30">ネックレス</tspan>',
        '    <tspan font-family="Liberation Serif, serif" font-size="28"> (necklace)</tspan>',
        "  </text>",
        "",
        f'  <rect x="{LEFT}" y="{TOP}" width="{RIGHT - LEFT}" height="{BOTTOM - TOP}" fill="{CREAM_HEX}" stroke="{NAVY_HEX}" stroke-width="2"/>',
        f'  <rect x="{MID}" y="{TOP}" width="{RIGHT - MID}" height="{BOTTOM - TOP}" fill="{NAVY_HEX}" fill-opacity="0.045"/>',
        f'  <line x1="{MID}" y1="{TOP}" x2="{MID}" y2="{BOTTOM}" stroke="{NAVY_HEX}" stroke-width="2"/>',
        "",
        f'  <text x="{left_cx}" y="500" text-anchor="middle" dominant-baseline="central" font-family="Noto Serif CJK JP, Noto Serif CJK KR, serif" font-size="188" fill="{NAVY_HEX}">ネ</text>',
        f'  <text x="{right_cx}" y="500" text-anchor="middle" dominant-baseline="central" font-family="Noto Serif CJK JP, Noto Serif CJK KR, serif" font-size="188" fill="{NAVY_HEX}">レ</text>',
        f'  <text x="{left_cx}" y="700" text-anchor="middle" dominant-baseline="central" font-family="Noto Serif CJK JP, Noto Serif CJK KR, serif" font-size="84" fill="{NAVY_HEX}">ね</text>',
        f'  <text x="{right_cx}" y="700" text-anchor="middle" dominant-baseline="central" font-family="Noto Serif CJK JP, Noto Serif CJK KR, serif" font-size="84" fill="{NAVY_HEX}">れ</text>',
        "",
        f'  <rect x="265" y="806" width="37" height="31" fill="{NAVY_HEX}"/>',
        f'  <rect x="751" y="806" width="32" height="31" fill="{NAVY_HEX}"/>',
        f'  <text x="271" y="832" font-family="Liberation Serif, serif" font-size="44" font-weight="700" fill="{CREAM_HEX}">n</text>',
        f'  <text x="305" y="832" font-family="Liberation Serif, serif" font-size="44" font-weight="700" fill="{NAVY_HEX}">e</text>',
        f'  <text x="757" y="832" font-family="Liberation Serif, serif" font-size="44" font-weight="700" fill="{CREAM_HEX}">r</text>',
        f'  <text x="787" y="832" font-family="Liberation Serif, serif" font-size="44" font-weight="700" fill="{NAVY_HEX}">e</text>',
        "",
        f'  <text x="540" y="998" text-anchor="middle" font-family="Noto Serif CJK KR, Liberation Serif, serif" font-size="20" fill="{TAUPE_HEX}">{esc("© 수영 책방 Swimming Bookstore")}</text>',
        "</svg>",
        "",
    ]
    SVG.write_text("\n".join(lines))


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    render_png()
    render_svg()
    print(OUT)
    print(SVG)


if __name__ == "__main__":
    main()
