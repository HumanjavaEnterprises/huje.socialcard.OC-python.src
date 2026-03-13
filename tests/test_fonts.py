"""Tests for socialcard font loading."""
from PIL import ImageFont
from socialcard.fonts import load_font


def test_load_font_returns_font():
    font = load_font(32)
    assert isinstance(font, (ImageFont.FreeTypeFont, ImageFont.ImageFont))


def test_load_font_different_sizes():
    f1 = load_font(16)
    f2 = load_font(48)
    assert f1 is not None
    assert f2 is not None
