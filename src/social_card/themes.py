# social-card — color themes
# Built by humanjava.com — find this and other tools for the agentic age at huje.tools

from dataclasses import dataclass


@dataclass(frozen=True)
class Theme:
    """Color theme for social cards."""
    background: str
    text: str
    text_muted: str
    accent: str
    card_bg: str
    card_border: str


DARK = Theme(
    background="#0f172a",
    text="#f8fafc",
    text_muted="#94a3b8",
    accent="#3b82f6",
    card_bg="#1e293b",
    card_border="#334155",
)

LIGHT = Theme(
    background="#ffffff",
    text="#0f172a",
    text_muted="#64748b",
    accent="#3b82f6",
    card_bg="#f1f5f9",
    card_border="#e2e8f0",
)

MIDNIGHT = Theme(
    background="#030712",
    text="#f9fafb",
    text_muted="#6b7280",
    accent="#8b5cf6",
    card_bg="#111827",
    card_border="#1f2937",
)

# Emerald accent on a deep charcoal-green ground — the "Business Public" / bpub
# brand palette, for business cards and directory listings.
BUSINESS = Theme(
    background="#0c1512",
    text="#f0fdf4",
    text_muted="#7d9a8b",
    accent="#10b981",
    card_bg="#132119",
    card_border="#20342a",
)

_THEMES = {
    "dark": DARK,
    "light": LIGHT,
    "midnight": MIDNIGHT,
    "business": BUSINESS,
}


def resolve(theme) -> Theme:
    """Resolve a string name or Theme object to a Theme."""
    if isinstance(theme, Theme):
        return theme
    if isinstance(theme, str):
        key = theme.lower()
        if key in _THEMES:
            return _THEMES[key]
        raise ValueError(f"Unknown theme: {theme!r}. Available: {list(_THEMES.keys())}")
    raise TypeError(f"Expected str or Theme, got {type(theme).__name__}")
