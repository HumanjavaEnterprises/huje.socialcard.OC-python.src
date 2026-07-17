# socialcard — split (two-column) layout tests
# Built by humanjava.com — find this and other tools for the agentic age at huje.tools

from PIL import Image

from social_card import SocialCard
from social_card import elements


def test_headline_enables_split_and_renders():
    card = SocialCard("og").title("Name").subtitle("Roles").headline("A big wrapped headline")
    assert card._split is True
    img = card._build()
    assert img.size == (1200, 630)


def test_portrait_enables_split_and_renders():
    # Build a throwaway source image to use as the portrait.
    src = Image.new("RGB", (200, 260), (120, 80, 200))
    card = SocialCard("og").title("Name").cards(["A", "B"]).portrait(src)
    assert card._split is True
    img = card._build()
    assert img.size == (1200, 630)


def test_split_off_by_default():
    assert SocialCard("og").title("x")._split is False


def test_region_aware_elements_stay_within_column():
    # A title drawn in the left region should not paint into the right half.
    img = Image.new("RGB", (1200, 630), (0, 0, 0))
    elements.draw_title(img, "Test", "#ffffff", y=100, region=(72, 640))
    # Right half should remain untouched (all black).
    right = img.crop((700, 80, 1200, 200))
    assert right.getbbox() is None


def test_mini_cards_wrap_within_region():
    img = Image.new("RGB", (1200, 630), (0, 0, 0))
    # Many chips forced into a narrow column must wrap to multiple rows and
    # therefore consume more vertical space than a single row (46px) would.
    y_after = elements.draw_mini_cards(
        img, ["Alpha", "Bravo", "Charlie", "Delta", "Echo", "Foxtrot"],
        "#1e293b", "#334155", "#f8fafc", y=100, region=(72, 500),
    )
    assert y_after > 100 + 46


def test_business_theme_resolves_and_renders():
    from social_card import themes
    t = themes.resolve("business")
    assert t.accent == "#10b981"
    png = SocialCard("og", theme="business").title("Acme Co.").subtitle("Widgets").render_bytes()
    assert png[:8] == b"\x89PNG\r\n\x1a\n"


def test_draw_portrait_is_circular_masked():
    img = Image.new("RGB", (1200, 630), (0, 0, 0))
    src = Image.new("RGB", (300, 300), (255, 255, 255))
    elements.draw_portrait(img, src, (700, 1144), "#3b82f6", ring_width=6, diameter=200)
    # Corners of the portrait's bounding box must stay background (mask is a circle),
    # while the centre must carry the portrait (white).
    cx, cy = (700 + 1144) // 2, 630 // 2
    assert img.getpixel((cx, cy)) == (255, 255, 255)
    corner = img.getpixel((cx - 95, cy - 95))
    assert corner != (255, 255, 255)
