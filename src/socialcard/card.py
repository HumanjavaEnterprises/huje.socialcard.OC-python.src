# socialcard — SocialCard builder
# Built by humanjava.com — find this and other tools for the agentic age at huje.tools

from __future__ import annotations

import io
from PIL import Image

from socialcard.presets import Preset, resolve as resolve_preset
from socialcard.themes import Theme, DARK, resolve as resolve_theme
from socialcard import elements


class SocialCard:
    """Builder for generating social card images.

    Usage:
        SocialCard("og").title("My Project").subtitle("A cool tool").render("card.png")
    """

    def __init__(self, preset: str | Preset = "og", theme: str | Theme = "dark"):
        self._preset = resolve_preset(preset)
        self._theme = resolve_theme(theme)
        self._badge_text: str | None = None
        self._title_text: str | None = None
        self._subtitle_text: str | None = None
        self._cards_list: list[str] | None = None
        self._footer_text: str | None = None
        self._accent_color: str | None = None
        self._show_grid: bool = False
        self._show_glow: bool = False

    def badge(self, text: str) -> SocialCard:
        self._badge_text = text
        return self

    def title(self, text: str) -> SocialCard:
        self._title_text = text
        return self

    def subtitle(self, text: str) -> SocialCard:
        self._subtitle_text = text
        return self

    def cards(self, labels: list[str]) -> SocialCard:
        self._cards_list = labels
        return self

    def footer(self, text: str) -> SocialCard:
        self._footer_text = text
        return self

    def accent(self, color: str) -> SocialCard:
        self._accent_color = color
        return self

    def grid(self) -> SocialCard:
        self._show_grid = True
        return self

    def glow(self) -> SocialCard:
        self._show_glow = True
        return self

    def _accent(self) -> str:
        return self._accent_color or self._theme.accent

    def _build(self) -> Image.Image:
        """Render the card to a PIL Image."""
        w, h = self._preset.width, self._preset.height
        img = Image.new("RGB", (w, h), elements._hex_to_rgb(self._theme.background))

        # Background effects (behind content)
        if self._show_glow:
            elements.draw_glow(img, self._accent())
        if self._show_grid:
            elements.draw_grid(img, self._theme.text_muted)

        # Content — track vertical position
        y = 40

        if self._badge_text:
            y = elements.draw_badge(img, self._badge_text, self._accent(), self._theme.text, y=y)

        if self._title_text:
            y = elements.draw_title(img, self._title_text, self._theme.text, y=y)

        if self._subtitle_text:
            y = elements.draw_subtitle(img, self._subtitle_text, self._theme.text_muted, y=y)

        if self._cards_list:
            y = elements.draw_mini_cards(
                img, self._cards_list,
                self._theme.card_bg, self._theme.card_border, self._theme.text,
                y=y,
            )

        if self._footer_text:
            elements.draw_footer(img, self._footer_text, self._theme.text_muted)

        return img

    def render(self, path: str) -> Image.Image:
        """Render the card and save to a file. Returns the Image."""
        img = self._build()
        img.save(path)
        return img

    def render_bytes(self, fmt: str = "PNG") -> bytes:
        """Render the card and return as bytes."""
        img = self._build()
        buf = io.BytesIO()
        img.save(buf, format=fmt)
        return buf.getvalue()
