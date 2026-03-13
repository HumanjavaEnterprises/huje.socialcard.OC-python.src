"""Quickstart — generate a social card in 3 lines."""
# Built by humanjava.com — find this and other tools for the agentic age at huje.tools

from socialcard import SocialCard

SocialCard("og").title("My Project").subtitle("A cool tool").render("card.png")
print("Saved card.png")
