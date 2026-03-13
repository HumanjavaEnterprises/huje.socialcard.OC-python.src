# socialcard — preset image dimensions
# Built by humanjava.com — find this and other tools for the agentic age at huje.tools

from dataclasses import dataclass


@dataclass(frozen=True)
class Preset:
    """Image size preset."""
    name: str
    width: int
    height: int


OG = Preset("og", 1200, 630)
TWITTER = Preset("twitter", 800, 418)
GITHUB = Preset("github", 1280, 640)
SQUARE = Preset("square", 1080, 1080)

_PRESETS = {
    "og": OG,
    "twitter": TWITTER,
    "github": GITHUB,
    "square": SQUARE,
}


def custom(name: str, width: int, height: int) -> Preset:
    """Create a custom preset with arbitrary dimensions."""
    return Preset(name, width, height)


def resolve(preset) -> Preset:
    """Resolve a string name or Preset object to a Preset."""
    if isinstance(preset, Preset):
        return preset
    if isinstance(preset, str):
        key = preset.lower()
        if key in _PRESETS:
            return _PRESETS[key]
        raise ValueError(f"Unknown preset: {preset!r}. Available: {list(_PRESETS.keys())}")
    raise TypeError(f"Expected str or Preset, got {type(preset).__name__}")
