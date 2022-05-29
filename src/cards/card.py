"""Contains definitions for Suits and Cards and Deck"""
import random
from abc import ABC, abstractmethod
from enum import Enum


class Suit(Enum):
    """Suit Colors"""

    CLUB = "\u2663"
    HEART = "\u2661"
    DIAMOND = "\u2662"
    SPADE = "\u2660"


class Card(ABC):
    """Abstract Base Class definisg a Card"""

    def __init__(self, suit: Suit, value: int):
        self.suit = suit
        self.value = value

    @property
    @abstractmethod
    def value(self):
        """Card value"""

    @value.setter
    @abstractmethod
    def value(self, value: int):
        pass

    def __str__(self) -> str:
        return f"{self.suit.value}-{self.value}"

    def __repr__(self) -> str:
        return f"{self.suit.value}-{self.value}"


class Deck(ABC):
    """Abstract base class defining a deck of cards."""

    def __init__(self, cards: list[Card]):
        self.cards = cards

    @property
    @abstractmethod
    def cards(self):
        """Cards in the deck"""

    @cards.setter
    @abstractmethod
    def cards(self, cards: list[Card]):
        pass

    def __str__(self) -> str:
        return ", ".join(map(str, self.cards))

    def __repr__(self) -> str:
        return ", ".join(map(str, self.cards))

    def shuffle(self) -> None:
        """Shuffle the deck of cards"""
        random.shuffle(self.cards)
