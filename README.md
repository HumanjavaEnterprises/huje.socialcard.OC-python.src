# social-card

Generate beautiful social card images with a builder API. One dependency: Pillow.

Built by [humanjava.com](https://humanjava.com) — find this and other tools for the agentic age at [huje.tools](https://huje.tools).

## Install

```bash
pip install social-card
```

## Quick Start

```python
from social_card import SocialCard

SocialCard("og").title("My Project").subtitle("A cool tool").render("card.png")
```

## Full Example

```python
(SocialCard("og", theme="midnight")
    .badge("Open Source")
    .title("My Project")
    .subtitle("Deploy in seconds")
    .cards(["Python", "Pillow", "MIT"])
    .footer("myproject.dev")
    .accent("#f97316")
    .grid()
    .glow()
    .render("card.png"))
```

## Presets

| Preset   | Size      | Use Case          |
|----------|-----------|-------------------|
| `og`     | 1200×630  | Open Graph / link previews |
| `twitter`| 800×418   | Twitter/X cards   |
| `github` | 1280×640  | GitHub social preview |
| `square` | 1080×1080 | Instagram / social |

## Themes

- `dark` — Navy background, blue accent
- `light` — White background, blue accent
- `midnight` — Near-black, purple accent

## API

```python
card = SocialCard(preset, theme)   # preset: str or Preset, theme: str or Theme
card.badge("text")                 # Small pill at top
card.title("text")                 # Main heading
card.subtitle("text")              # Subheading
card.cards(["a", "b", "c"])        # Tag chips
card.footer("text")                # Bottom text
card.accent("#hex")                # Override accent color
card.grid()                        # Subtle grid overlay
card.glow()                        # Radial glow effect
card.split()                       # Two-column layout (content left, visual right)
card.portrait(path_or_image)       # Circular portrait in the right column (implies split)
card.headline("text")              # Large wrapped headline in the right column (implies split)
card.render("path.png")            # Save to file, returns Image
card.render_bytes()                # Returns PNG bytes
```

## Split layout (business card)

Set a `portrait` or `headline` to switch to a two-column card: the badge / title /
subtitle / cards stack in the left column, and the visual sits on the right.

```python
# Business card — circular avatar on the right
(SocialCard("og", theme="dark")
    .badge("@vveerrgg").title("Vveerrgg")
    .subtitle("Developer · Creator · Tech Enthusiast")
    .cards(["Nostr", "Bitcoin", "Lightning", "Web"])
    .footer("vveerrgg.online")
    .accent("#0984e3")
    .portrait("avatar.png")          # local path or a PIL Image
    .grid().glow()
    .render("card.png"))

# Headline on the right instead of an image
(SocialCard("og", theme="midnight")
    .title("Vergel Evans")
    .subtitle("UX Architect · Service Design Strategist")
    .headline("I design the systems underneath the screens.")
    .accent("#9B87FF")
    .render("card.png"))
```

The left column is vertically centered, chips wrap to fit the narrower column, and a
faint divider separates the two sides.

## ClawHub

```bash
clawhub install social-card
```

## License

MIT
