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


def draw_badge(img: Image.Image, text: str, accent: str, text_color: str, y: int = 40) -> int:
    """Draw a small badge/pill near the top. Returns the y position after the badge."""
    draw = ImageDraw.Draw(img)
    font = load_font(18)
    text_w = font.getlength(text)
    pad_x, pad_y = 16, 8
    x = (img.width - text_w - pad_x * 2) // 2
    rect = [x, y, x + text_w + pad_x * 2, y + 18 + pad_y * 2]
    draw.rounded_rectangle(rect, radius=16, fill=_hex_to_rgb(accent))
    draw.text((x + pad_x, y + pad_y), text, fill=_hex_to_rgb(text_color), font=font)
    return rect[3] + 20


def draw_title(img: Image.Image, text: str, color: str, y: int = 120) -> int:
    """Draw the main title, centered, with word wrap. Returns y after title."""
    draw = ImageDraw.Draw(img)
    font = load_font(52)
    max_width = img.width - 120
    lines = _wrap_text(text, font, max_width)
    line_height = 62
    for line in lines:
        w = font.getlength(line)
        draw.text(((img.width - w) / 2, y), line, fill=_hex_to_rgb(color), font=font)
        y += line_height
    return y + 10


def draw_subtitle(img: Image.Image, text: str, color: str, y: int = 200) -> int:
    """Draw a subtitle line, centered, with word wrap. Returns y after subtitle."""
    draw = ImageDraw.Draw(img)
    font = load_font(26)
    max_width = img.width - 120
    lines = _wrap_text(text, font, max_width)
    line_height = 36
    for line in lines:
        w = font.getlength(line)
        draw.text(((img.width - w) / 2, y), line, fill=_hex_to_rgb(color), font=font)
        y += line_height
    return y + 10


def draw_footer(img: Image.Image, text: str, color: str) -> None:
    """Draw footer text at the bottom center."""
    draw = ImageDraw.Draw(img)
    font = load_font(18)
    w = font.getlength(text)
    y = img.height - 50
    draw.text(((img.width - w) / 2, y), text, fill=_hex_to_rgb(color), font=font)


def draw_mini_cards(
    img: Image.Image,
    labels: list[str],
    card_bg: str,
    card_border: str,
    text_color: str,
    y: int = 320,
) -> int:
    """Draw a row of small rounded-rect cards (tags/chips). Returns y after cards."""
    draw = ImageDraw.Draw(img)
    font = load_font(18)
    pad_x, pad_y = 16, 10
    card_height = 18 + pad_y * 2
    gap = 12

    # Measure total width
    widths = [font.getlength(label) + pad_x * 2 for label in labels]
    total = sum(widths) + gap * (len(labels) - 1) if labels else 0
    x = (img.width - total) / 2

    bg = _hex_to_rgb(card_bg)
    border = _hex_to_rgb(card_border)
    tc = _hex_to_rgb(text_color)

    for label, w in zip(labels, widths):
        rect = [x, y, x + w, y + card_height]
        draw.rounded_rectangle(rect, radius=8, fill=bg, outline=border, width=1)
        draw.text((x + pad_x, y + pad_y), label, fill=tc, font=font)
        x += w + gap

    return y + card_height + 20


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
