from __future__ import annotations

from src.cards.twentynine import TwentyNineCard


class Player:
    def __init__(self, name):
        self.name = name
        self.cards: list[TwentyNineCard] = []

    def __repr__(self) -> str:
        return self.name
