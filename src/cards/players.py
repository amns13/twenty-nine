from __future__ import annotations

from twentynine import TwentyNineCard


class Player:
    def __init__(self, name):
        self.name = name
        self.cards: list[TwentyNineCard] | None = None

    def __repr__(self) -> str:
        return self.name
