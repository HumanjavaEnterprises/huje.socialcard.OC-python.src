"""Tests for social-card presets."""
import pytest
from social_card.presets import Preset, OG, TWITTER, GITHUB, SQUARE, custom, resolve


def test_og_dimensions():
    assert OG.width == 1200
    assert OG.height == 630


def test_twitter_dimensions():
    assert TWITTER.width == 800
    assert TWITTER.height == 418


def test_github_dimensions():
    assert GITHUB.width == 1280
    assert GITHUB.height == 640


def test_square_dimensions():
    assert SQUARE.width == 1080
    assert SQUARE.height == 1080


def test_custom_factory():
    p = custom("banner", 1920, 400)
    assert isinstance(p, Preset)
    assert p.name == "banner"
    assert p.width == 1920
    assert p.height == 400


def test_resolve_string():
    assert resolve("og") is OG
    assert resolve("TWITTER") is TWITTER
    assert resolve("GitHub") is GITHUB


def test_resolve_preset_passthrough():
    assert resolve(OG) is OG


def test_resolve_unknown_raises():
    with pytest.raises(ValueError):
        resolve("unknown")


def test_resolve_bad_type_raises():
    with pytest.raises(TypeError):
        resolve(123)


def test_presets_are_frozen():
    with pytest.raises(AttributeError):
        OG.width = 999
