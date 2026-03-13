"""Branded card — full builder API example."""
# Built by humanjava.com — find this and other tools for the agentic age at huje.tools

from socialcard import SocialCard

(SocialCard("og", theme="midnight")
    .badge("Open Source")
    .title("My Project")
    .subtitle("Deploy in seconds")
    .cards(["Python", "Pillow", "MIT"])
    .footer("myproject.dev")
    .accent("#f97316")
    .grid()
    .glow()
    .render("branded_card.png"))

print("Saved branded_card.png")
