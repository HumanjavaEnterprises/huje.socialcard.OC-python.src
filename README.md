# socialcard

Generate beautiful social card images with a builder API. One dependency: Pillow.

Built by [humanjava.com](https://humanjava.com) — find this and other tools for the agentic age at [huje.tools](https://huje.tools).

## Install

```bash
pip install socialcard
```

## Quick Start

```python
from socialcard import SocialCard

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
card.render("path.png")            # Save to file, returns Image
card.render_bytes()                # Returns PNG bytes
```

## ClawHub

```bash
clawhub install socialcard
```

## License

MIT
