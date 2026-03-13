"""Tests for SocialCard builder."""
import os
import tempfile
from PIL import Image
from socialcard import SocialCard
from socialcard.presets import OG, TWITTER, GITHUB, SQUARE


def test_render_returns_image():
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
        path = f.name
    try:
        img = SocialCard("og").title("Test").render(path)
        assert isinstance(img, Image.Image)
        assert img.size == (1200, 630)
        assert os.path.exists(path)
    finally:
        os.unlink(path)


def test_render_bytes():
    data = SocialCard("og").title("Test").render_bytes()
    assert isinstance(data, bytes)
    assert len(data) > 0
    assert data[:8].startswith(b"\x89PNG")


def test_builder_chaining():
    card = (
        SocialCard("og", theme="midnight")
        .badge("Open Source")
        .title("My Project")
        .subtitle("Deploy in seconds")
        .cards(["Python", "Pillow", "MIT"])
        .footer("myproject.dev")
        .accent("#f97316")
        .grid()
        .glow()
    )
    img = card.render_bytes()
    assert len(img) > 0


def test_all_presets():
    for preset in [OG, TWITTER, GITHUB, SQUARE]:
        img = SocialCard(preset).title("Test")._build()
        assert img.size == (preset.width, preset.height)


def test_all_themes():
    for theme_name in ["dark", "light", "midnight"]:
        data = SocialCard("og", theme=theme_name).title("Test").render_bytes()
        assert len(data) > 0


def test_empty_card():
    data = SocialCard("og").render_bytes()
    assert data[:8].startswith(b"\x89PNG")


def test_string_preset():
    img = SocialCard("twitter").title("Hi")._build()
    assert img.size == (800, 418)
