# socialcard — platform font fallback
# Built by humanjava.com — find this and other tools for the agentic age at huje.tools

from PIL import ImageFont

_FONT_CHAIN = [
    "/System/Library/Fonts/SFNSMono.ttf",                    # macOS SF Mono
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",      # macOS Arial Bold
    "/System/Library/Fonts/Helvetica.ttc",                    # macOS Helvetica
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",  # Linux DejaVu
    "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf",              # Arch Linux
    "C:\\Windows\\Fonts\\arial.ttf",                          # Windows
]


def load_font(size: int = 32) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    """Load a font at the given size, falling back through platform fonts.

    Never crashes — returns Pillow's built-in bitmap font as last resort.
    """
    for path in _FONT_CHAIN:
        try:
            return ImageFont.truetype(path, size)
        except (OSError, IOError):
            continue
    return ImageFont.load_default()
