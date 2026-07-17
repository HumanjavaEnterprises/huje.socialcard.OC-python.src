# social-card — drawing elements
# Built by humanjava.com — find this and other tools for the agentic age at huje.tools

import re

from PIL import Image, ImageDraw, ImageFilter
from social_card.fonts import load_font

_HEX_RE = re.compile(r'^#?[0-9a-fA-F]{6}$')


def _hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    """Convert hex color string to RGB tuple.

    Accepts '#RRGGBB' or 'RRGGBB'. Raises ValueError for invalid input.
    """
    if not isinstance(hex_color, str) or not _HEX_RE.match(hex_color):
        raise ValueError(
            f"Invalid hex color: {hex_color!r}. "
            "Expected format '#RRGGBB' or 'RRGGBB' (6 hex digits)."
        )
    h = hex_color.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def _wrap_text(text: str, font, max_width: int) -> list[str]:
    """Word-wrap text to fit within max_width pixels."""
    words = text.split()
    if not words:
        return []
    lines = []
    current = words[0]
    for word in words[1:]:
        test = f"{current} {word}"
        if font.getlength(test) <= max_width:
            current = test
        else:
            lines.append(current)
            current = word
    lines.append(current)
    return lines


def draw_badge(img: Image.Image, text: str, accent: str, text_color: str, y: int = 40,
               region: tuple[int, int] | None = None) -> int:
    """Draw a small badge/pill near the top. Centered on the image, or within `region`.

    Returns the y position after the badge.
    """
    draw = ImageDraw.Draw(img)
    font = load_font(18)
    text_w = font.getlength(text)
    pad_x, pad_y = 16, 8
    x0, x1 = region if region else (0, img.width)
    x = (x0 + x1 - text_w - pad_x * 2) // 2
    rect = [x, y, x + text_w + pad_x * 2, y + 18 + pad_y * 2]
    draw.rounded_rectangle(rect, radius=16, fill=_hex_to_rgb(accent))
    draw.text((x + pad_x, y + pad_y), text, fill=_hex_to_rgb(text_color), font=font)
    return rect[3] + 20


def draw_title(img: Image.Image, text: str, color: str, y: int = 120,
               region: tuple[int, int] | None = None) -> int:
    """Draw the main title, centered (within `region` if given), with word wrap.

    Returns y after the title. In a column (`region` set) the title is set a little
    smaller so it wraps gracefully in the narrower space.
    """
    draw = ImageDraw.Draw(img)
    x0, x1 = region if region else (0, img.width)
    col_w = x1 - x0
    font = load_font(52 if region is None else 44)
    max_width = col_w - (120 if region is None else 24)
    lines = _wrap_text(text, font, max_width)
    line_height = 62 if region is None else 52
    for line in lines:
        w = font.getlength(line)
        draw.text((x0 + (col_w - w) / 2, y), line, fill=_hex_to_rgb(color), font=font)
        y += line_height
    return y + 10


def draw_subtitle(img: Image.Image, text: str, color: str, y: int = 200,
                  region: tuple[int, int] | None = None) -> int:
    """Draw a subtitle line, centered (within `region` if given), with word wrap.

    Returns y after the subtitle.
    """
    draw = ImageDraw.Draw(img)
    x0, x1 = region if region else (0, img.width)
    col_w = x1 - x0
    font = load_font(26 if region is None else 22)
    max_width = col_w - (120 if region is None else 24)
    lines = _wrap_text(text, font, max_width)
    line_height = 36 if region is None else 31
    for line in lines:
        w = font.getlength(line)
        draw.text((x0 + (col_w - w) / 2, y), line, fill=_hex_to_rgb(color), font=font)
        y += line_height
    return y + 10


def draw_footer(img: Image.Image, text: str, color: str,
                region: tuple[int, int] | None = None) -> None:
    """Draw footer text at the bottom center of the image (or of `region`)."""
    draw = ImageDraw.Draw(img)
    font = load_font(18)
    w = font.getlength(text)
    x0, x1 = region if region else (0, img.width)
    y = img.height - 50
    draw.text((x0 + (x1 - x0 - w) / 2, y), text, fill=_hex_to_rgb(color), font=font)


def draw_mini_cards(
    img: Image.Image,
    labels: list[str],
    card_bg: str,
    card_border: str,
    text_color: str,
    y: int = 320,
    region: tuple[int, int] | None = None,
) -> int:
    """Draw rounded-rect tag chips, centered. Returns y after the cards.

    Full width (no `region`): a single centered row, as before. Within a `region`
    (column layout): chips wrap onto multiple centered rows to fit the column.
    """
    draw = ImageDraw.Draw(img)
    font = load_font(18)
    pad_x, pad_y = 16, 10
    card_height = 18 + pad_y * 2
    gap = 12
    bg = _hex_to_rgb(card_bg)
    border = _hex_to_rgb(card_border)
    tc = _hex_to_rgb(text_color)
    widths = [font.getlength(label) + pad_x * 2 for label in labels]

    if region is None:
        # Original single-row, full-width centered behavior.
        total = sum(widths) + gap * (len(labels) - 1) if labels else 0
        x = (img.width - total) / 2
        for label, w in zip(labels, widths):
            rect = [x, y, x + w, y + card_height]
            draw.rounded_rectangle(rect, radius=8, fill=bg, outline=border, width=1)
            draw.text((x + pad_x, y + pad_y), label, fill=tc, font=font)
            x += w + gap
        return y + card_height + 20

    # Column layout: wrap chips into centered rows within the region.
    x0, x1 = region
    avail = (x1 - x0) - 24
    rows: list[list[tuple[str, float]]] = []
    cur: list[tuple[str, float]] = []
    cur_w = 0.0
    for label, w in zip(labels, widths):
        add = w if not cur else w + gap
        if cur and cur_w + add > avail:
            rows.append(cur)
            cur, cur_w = [(label, w)], w
        else:
            cur.append((label, w))
            cur_w += add
    if cur:
        rows.append(cur)

    for row in rows:
        row_total = sum(w for _, w in row) + gap * (len(row) - 1)
        x = x0 + ((x1 - x0) - row_total) / 2
        for label, w in row:
            rect = [x, y, x + w, y + card_height]
            draw.rounded_rectangle(rect, radius=8, fill=bg, outline=border, width=1)
            draw.text((x + pad_x, y + pad_y), label, fill=tc, font=font)
            x += w + gap
        y += card_height + 12
    return y + 8


def draw_skill_cards(
    img: Image.Image,
    skills: list[dict],
    card_bg: str,
    card_border: str,
    text_color: str,
    text_muted: str,
    accent: str,
    y: int = 320,
) -> int:
    """Draw structured skill cards with name (accent-highlighted), subtitle, and code.

    Each skill dict should have: name (str), label (str), code (str).
    The name can contain a pipe to split prefix|suffix for accent coloring,
    e.g. "Nostr|Key" renders "Nostr" in text_color and "Key" in accent.
    """
    draw = ImageDraw.Draw(img)
    name_font = load_font(24)
    label_font = load_font(18)
    code_font = load_font(16, mono=True)

    count = len(skills)
    if count == 0:
        return y

    gap = 24
    pad_x, pad_y = 20, 16
    card_h = 110
    card_w = (img.width - 120 - gap * (count - 1)) // count
    start_x = (img.width - (card_w * count + gap * (count - 1))) / 2

    bg = _hex_to_rgb(card_bg)
    border = _hex_to_rgb(card_border)
    tc = _hex_to_rgb(text_color)
    ac = _hex_to_rgb(accent)

    for i, skill in enumerate(skills):
        cx = start_x + i * (card_w + gap)
        draw.rounded_rectangle(
            [cx, y, cx + card_w, y + card_h],
            radius=12, fill=bg, outline=border, width=1,
        )

        # Name with optional accent split
        name = skill.get("name", "")
        nx = cx + pad_x
        ny = y + pad_y
        if "|" in name:
            prefix, suffix = name.split("|", 1)
            draw.text((nx, ny), prefix, fill=tc, font=name_font)
            nx += name_font.getlength(prefix)
            draw.text((nx, ny), suffix, fill=ac, font=name_font)
        else:
            draw.text((nx, ny), name, fill=tc, font=name_font)

        # Label
        label = skill.get("label", "")
        draw.text((cx + pad_x, y + pad_y + 30), label, fill=_hex_to_rgb(text_muted), font=label_font)

        # Code
        code = skill.get("code", "")
        draw.text((cx + pad_x, y + pad_y + 60), code, fill=ac, font=code_font)

    return y + card_h + 20


def draw_grid(img: Image.Image, color: str, spacing: int = 40, opacity: int = 20) -> None:
    """Draw a subtle grid overlay."""
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    r, g, b = _hex_to_rgb(color)
    for x in range(0, img.width, spacing):
        draw.line([(x, 0), (x, img.height)], fill=(r, g, b, opacity), width=1)
    for y in range(0, img.height, spacing):
        draw.line([(0, y), (img.width, y)], fill=(r, g, b, opacity), width=1)
    img.paste(Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB"))


def draw_glow(img: Image.Image, color: str, radius: int = 120) -> None:
    """Draw a centered radial glow effect using the accent color."""
    glow = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(glow)
    r, g, b = _hex_to_rgb(color)
    cx, cy = img.width // 2, img.height // 3
    size = min(img.width, img.height) // 2
    draw.ellipse(
        [cx - size, cy - size, cx + size, cy + size],
        fill=(r, g, b, 40),
    )
    glow = glow.filter(ImageFilter.GaussianBlur(radius=radius))
    composite = Image.alpha_composite(img.convert("RGBA"), glow)
    img.paste(composite.convert("RGB"))


def draw_divider(img: Image.Image, x: int, color: str, pad: int = 90, width: int = 1) -> None:
    """Draw a faint vertical hairline between two columns."""
    draw = ImageDraw.Draw(img)
    draw.line([(x, pad), (x, img.height - pad)], fill=_hex_to_rgb(color), width=width)


def draw_portrait(
    img: Image.Image,
    source,
    region: tuple[int, int],
    ring_color: str,
    ring_width: int = 8,
    diameter: int | None = None,
) -> None:
    """Draw a circular portrait centered in `region` (vertically centered in the card).

    `source` is a file path or a PIL Image. It is center-cropped to a square, resized,
    circularly masked (anti-aliased), and given an accent ring — a "business card" look.
    """
    x0, x1 = region
    region_w = x1 - x0
    diameter = diameter or min(region_w - 48, 320)
    if diameter < 8:
        diameter = 8

    src = source if isinstance(source, Image.Image) else Image.open(source)
    src = src.convert("RGB")
    sw, sh = src.size
    s = min(sw, sh)
    src = src.crop(((sw - s) // 2, (sh - s) // 2, (sw - s) // 2 + s, (sh - s) // 2 + s))
    src = src.resize((diameter, diameter), Image.LANCZOS)

    # Anti-aliased circular mask (supersample then downsample).
    ss = 4
    mask = Image.new("L", (diameter * ss, diameter * ss), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, diameter * ss, diameter * ss], fill=255)
    mask = mask.resize((diameter, diameter), Image.LANCZOS)

    cx = (x0 + x1) // 2
    cy = img.height // 2
    px, py = cx - diameter // 2, cy - diameter // 2

    if ring_width > 0:
        ring = Image.new("RGBA", img.size, (0, 0, 0, 0))
        ImageDraw.Draw(ring).ellipse(
            [px - ring_width, py - ring_width, px + diameter + ring_width, py + diameter + ring_width],
            fill=_hex_to_rgb(ring_color) + (255,),
        )
        img.paste(Image.alpha_composite(img.convert("RGBA"), ring).convert("RGB"))

    img.paste(src, (px, py), mask)


def draw_headline(
    img: Image.Image,
    text: str,
    color: str,
    region: tuple[int, int],
    accent: str | None = None,
    size: int = 48,
) -> None:
    """Draw a large word-wrapped headline, vertically centered within `region`.

    If `accent` is given, a short accent tick is drawn above the headline.
    """
    x0, x1 = region
    col_w = x1 - x0
    draw = ImageDraw.Draw(img)
    font = load_font(size)
    lines = _wrap_text(text, font, col_w - 32)
    line_height = int(size * 1.16)
    total = line_height * len(lines)
    y = (img.height - total) // 2

    if accent:
        draw.rounded_rectangle([x0 + 16, y - 30, x0 + 16 + 46, y - 26], radius=2, fill=_hex_to_rgb(accent))

    for line in lines:
        draw.text((x0 + 16, y), line, fill=_hex_to_rgb(color), font=font)
        y += line_height
