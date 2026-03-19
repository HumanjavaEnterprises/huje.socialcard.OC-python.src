"""Tests for social-card themes."""
import pytest
from social_card.themes import Theme, DARK, LIGHT, MIDNIGHT, resolve


REQUIRED_FIELDS = ["background", "text", "text_muted", "accent", "card_bg", "card_border"]


@pytest.mark.parametrize("theme", [DARK, LIGHT, MIDNIGHT])
def test_all_fields_present(theme):
    for field in REQUIRED_FIELDS:
        assert hasattr(theme, field)
        assert isinstance(getattr(theme, field), str)


def test_resolve_string():
    assert resolve("dark") is DARK
    assert resolve("LIGHT") is LIGHT
    assert resolve("Midnight") is MIDNIGHT


def test_resolve_theme_passthrough():
    assert resolve(DARK) is DARK


def test_resolve_unknown_raises():
    with pytest.raises(ValueError):
        resolve("nope")


def test_custom_theme_accepted():
    custom = Theme("#000", "#fff", "#888", "#f00", "#111", "#222")
    assert resolve(custom) is custom
