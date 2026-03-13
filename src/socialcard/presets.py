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


_MAX_DIMENSION = 4096


def custom(name: str, width: int, height: int) -> Preset:
    """Create a custom preset with arbitrary dimensions (max 4096x4096).

    Raises ValueError if either dimension exceeds the maximum.
    """
    if width > _MAX_DIMENSION or height > _MAX_DIMENSION:
        raise ValueError(
            f"Image dimensions {width}x{height} exceed maximum of "
            f"{_MAX_DIMENSION}x{_MAX_DIMENSION}"
        )
    if width <= 0 or height <= 0:
        raise ValueError(f"Image dimensions must be positive, got {width}x{height}")
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
