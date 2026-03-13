"""Tests for socialcard drawing elements."""
from PIL import Image
from socialcard.elements import (
    draw_badge, draw_title, draw_subtitle, draw_footer,
    draw_mini_cards, draw_grid, draw_glow,
)


def _blank():
    return Image.new("RGB", (1200, 630), (15, 23, 42))


def test_draw_badge():
    img = _blank()
    y = draw_badge(img, "Beta", "#3b82f6", "#f8fafc")
    assert isinstance(y, int)


def test_draw_title():
    img = _blank()
    y = draw_title(img, "Hello World", "#f8fafc")
    assert isinstance(y, int)


def test_draw_subtitle():
    img = _blank()
    y = draw_subtitle(img, "A subtitle here", "#94a3b8")
    assert isinstance(y, int)


def test_draw_footer():
    img = _blank()
    draw_footer(img, "example.com", "#94a3b8")


def test_draw_mini_cards():
    img = _blank()
    y = draw_mini_cards(img, ["Python", "MIT", "Fast"], "#1e293b", "#334155", "#f8fafc")
    assert isinstance(y, int)


def test_draw_mini_cards_empty():
    img = _blank()
    y = draw_mini_cards(img, [], "#1e293b", "#334155", "#f8fafc")
    assert isinstance(y, int)


def test_draw_grid():
    img = _blank()
    draw_grid(img, "#94a3b8")


def test_draw_glow():
    img = _blank()
    draw_glow(img, "#3b82f6")
