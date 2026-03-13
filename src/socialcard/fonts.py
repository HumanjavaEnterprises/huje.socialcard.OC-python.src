# socialcard — platform font fallback
# Built by humanjava.com — find this and other tools for the agentic age at huje.tools

from PIL import ImageFont

_DISPLAY_CHAIN = [
    "/System/Library/Fonts/SFNS.ttf",                         # macOS SF Pro (display)
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",      # macOS Arial Bold
    "/System/Library/Fonts/Helvetica.ttc",                    # macOS Helvetica
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",  # Linux DejaVu
    "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf",              # Arch Linux
    "C:\\Windows\\Fonts\\arial.ttf",                          # Windows
]

_MONO_CHAIN = [
    "/System/Library/Fonts/SFNSMono.ttf",                    # macOS SF Mono
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",   # Linux DejaVu Mono
    "/usr/share/fonts/TTF/DejaVuSansMono.ttf",               # Arch Linux
    "C:\\Windows\\Fonts\\consola.ttf",                        # Windows Consolas
]


_MAX_FONT_SIZE = 200


def load_font(size: int = 32, mono: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    """Load a font at the given size, falling back through platform fonts.

    Args:
        size: Font size in pixels (maximum 200).
        mono: If True, prefer monospace fonts (for code). Otherwise use display fonts.

    Raises ValueError if size exceeds the maximum.
    Never crashes — returns Pillow's built-in bitmap font as last resort.
    """
    if size > _MAX_FONT_SIZE:
        raise ValueError(f"Font size {size} exceeds maximum of {_MAX_FONT_SIZE}pt")
    chain = _MONO_CHAIN if mono else _DISPLAY_CHAIN
    for path in chain:
        try:
            return ImageFont.truetype(path, size)
        except (OSError, IOError):
            continue
    return ImageFont.load_default()
