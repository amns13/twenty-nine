import random
from abc import ABC, abstractmethod
from enum import Enum


class Suit(Enum):
    CLUB = "\u2663"
    HEART = "\u2661"
    DIAMOND = "\u2662"
    SPADE = "\u2660"


class Card(ABC):
    def __init__(self, suit: Suit, value: int):
        self.suit = suit
        self.value = value

    @property
    @abstractmethod
    def value(self):
        pass

    @value.setter
    @abstractmethod
    def value(self, value: int):
        pass

    def __repr__(self) -> str:
        return f"{self.suit.value}-{self.value}"


class Deck(ABC):
    def __init__(self, cards: list[Card]):
        self.cards = cards

    @property
    @abstractmethod
    def cards(self):
        pass

    @cards.setter
    @abstractmethod
    def cards(self, cards: list[Card]):
        pass

    def __repr__(self) -> str:
        return ", ".join(map(str, self.cards))

    def shuffle(self) -> None:
        random.shuffle(self.cards)
