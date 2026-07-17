# social-card — SocialCard builder
# Built by humanjava.com — find this and other tools for the agentic age at huje.tools

from __future__ import annotations

import io
import os
from PIL import Image

from social_card.presets import Preset, resolve as resolve_preset
from social_card.themes import Theme, DARK, resolve as resolve_theme
from social_card import elements

_ALLOWED_RENDER_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.webp'}
_ALLOWED_BYTE_FORMATS = {'PNG', 'JPEG', 'WEBP'}
_MAX_TITLE_LEN = 200
_MAX_SUBTITLE_LEN = 500
_MAX_FOOTER_LEN = 200
_MAX_BADGE_LEN = 100


class SocialCard:
    """Builder for generating social card images.

    Usage:
        SocialCard("og").title("My Project").subtitle("A cool tool").render("card.png")
    """

    def __init__(self, preset: str | Preset = "og", theme: str | Theme = "dark"):
        self._preset = resolve_preset(preset)
        if self._preset.width > 4096 or self._preset.height > 4096:
            raise ValueError(
                f"Image dimensions {self._preset.width}x{self._preset.height} "
                f"exceed maximum of 4096x4096"
            )
        if self._preset.width <= 0 or self._preset.height <= 0:
            raise ValueError(
                f"Image dimensions must be positive, "
                f"got {self._preset.width}x{self._preset.height}"
            )
        self._theme = resolve_theme(theme)
        self._badge_text: str | None = None
        self._title_text: str | None = None
        self._subtitle_text: str | None = None
        self._cards_list: list[str] | None = None
        self._skill_cards_list: list[dict] | None = None
        self._footer_text: str | None = None
        self._accent_color: str | None = None
        self._show_grid: bool = False
        self._show_glow: bool = False
        self._portrait_source = None
        self._headline_text: str | None = None
        self._split: bool = False

    def badge(self, text: str) -> SocialCard:
        if len(text) > _MAX_BADGE_LEN:
            raise ValueError(f"Badge text exceeds {_MAX_BADGE_LEN} characters ({len(text)} given)")
        self._badge_text = text
        return self

    def title(self, text: str) -> SocialCard:
        if len(text) > _MAX_TITLE_LEN:
            raise ValueError(f"Title text exceeds {_MAX_TITLE_LEN} characters ({len(text)} given)")
        self._title_text = text
        return self

    def subtitle(self, text: str) -> SocialCard:
        if len(text) > _MAX_SUBTITLE_LEN:
            raise ValueError(f"Subtitle text exceeds {_MAX_SUBTITLE_LEN} characters ({len(text)} given)")
        self._subtitle_text = text
        return self

    def cards(self, labels: list[str]) -> SocialCard:
        self._cards_list = labels
        return self

    def skill_cards(self, skills: list[dict]) -> SocialCard:
        """Add structured skill cards. Each dict: name, label, code.

        Use pipe in name for accent split: "Nostr|Key" → "Nostr" + "Key" (accented).
        """
        self._skill_cards_list = skills
        return self

    def footer(self, text: str) -> SocialCard:
        if len(text) > _MAX_FOOTER_LEN:
            raise ValueError(f"Footer text exceeds {_MAX_FOOTER_LEN} characters ({len(text)} given)")
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

    def split(self, enabled: bool = True) -> SocialCard:
        """Enable the two-column layout (content left, visual right)."""
        self._split = enabled
        return self

    def portrait(self, source) -> SocialCard:
        """Set a circular portrait for the right column (business-card look).

        `source` is a local file path or a PIL Image. Enables the split layout.
        """
        self._portrait_source = source
        self._split = True
        return self

    def headline(self, text: str) -> SocialCard:
        """Set a large wrapped headline for the right column. Enables the split layout."""
        if len(text) > _MAX_TITLE_LEN:
            raise ValueError(f"Headline text exceeds {_MAX_TITLE_LEN} characters ({len(text)} given)")
        self._headline_text = text
        self._split = True
        return self

    def _accent(self) -> str:
        return self._accent_color or self._theme.accent

    def _render_stack(self, img: Image.Image, y: int, region: tuple[int, int] | None) -> int:
        """Render badge/title/subtitle/cards as a vertical stack. Returns the ending y."""
        if self._badge_text:
            y = elements.draw_badge(img, self._badge_text, self._accent(), self._theme.text, y=y, region=region)
        if self._title_text:
            y = elements.draw_title(img, self._title_text, self._theme.text, y=y, region=region)
        if self._subtitle_text:
            y = elements.draw_subtitle(img, self._subtitle_text, self._theme.text_muted, y=y, region=region)
        if self._cards_list:
            y = elements.draw_mini_cards(
                img, self._cards_list,
                self._theme.card_bg, self._theme.card_border, self._theme.text,
                y=y, region=region,
            )
        return y

    def _build(self) -> Image.Image:
        """Render the card to a PIL Image."""
        w, h = self._preset.width, self._preset.height
        img = Image.new("RGB", (w, h), elements._hex_to_rgb(self._theme.background))

        # Background effects (behind content)
        if self._show_glow:
            elements.draw_glow(img, self._accent())
        if self._show_grid:
            elements.draw_grid(img, self._theme.text_muted)

        # Two-column split layout (content left, portrait/headline right).
        if self._split and (self._portrait_source is not None or self._headline_text is not None):
            left = (72, int(w * 0.54))
            right = (int(w * 0.54), w - 56)
            # Measure the left stack on a scratch image so we can vertically center it.
            scratch = Image.new("RGB", (w, h))
            content_h = self._render_stack(scratch, 40, left) - 40
            start_y = max(48, (h - content_h) // 2)
            self._render_stack(img, start_y, left)
            elements.draw_divider(img, int(w * 0.54), self._theme.card_border)
            if self._portrait_source is not None:
                elements.draw_portrait(img, self._portrait_source, right, self._accent())
            elif self._headline_text:
                elements.draw_headline(img, self._headline_text, self._theme.text, right, accent=self._accent())
            if self._footer_text:
                elements.draw_footer(img, self._footer_text, self._theme.text_muted, region=left)
            return img

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

        if self._skill_cards_list:
            y = elements.draw_skill_cards(
                img, self._skill_cards_list,
                self._theme.card_bg, self._theme.card_border, self._theme.text,
                self._theme.text_muted, self._accent(),
                y=y,
            )

        if self._footer_text:
            elements.draw_footer(img, self._footer_text, self._theme.text_muted)

        return img

    def render(self, path: str) -> Image.Image:
        """Render the card and save to a file. Returns the Image.

        Raises ValueError for path traversal attempts or disallowed extensions.
        """
        resolved = os.path.realpath(path)
        if '..' in os.path.normpath(resolved).split(os.sep):
            raise ValueError(f"Path traversal detected in output path: {path!r}")
        ext = os.path.splitext(resolved)[1].lower()
        if ext not in _ALLOWED_RENDER_EXTENSIONS:
            raise ValueError(
                f"Disallowed file extension {ext!r}. "
                f"Allowed: {sorted(_ALLOWED_RENDER_EXTENSIONS)}"
            )
        img = self._build()
        img.save(resolved)
        return img

    def render_bytes(self, fmt: str = "PNG") -> bytes:
        """Render the card and return as bytes.

        Raises ValueError for unknown image formats.
        """
        fmt_upper = fmt.upper()
        if fmt_upper not in _ALLOWED_BYTE_FORMATS:
            raise ValueError(
                f"Unknown image format {fmt!r}. "
                f"Allowed: {sorted(_ALLOWED_BYTE_FORMATS)}"
            )
        img = self._build()
        buf = io.BytesIO()
        img.save(buf, format=fmt_upper)
        return buf.getvalue()
