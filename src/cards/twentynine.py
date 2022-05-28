"""Defines the card attributes specific to Twenty Nine."""
from src.cards.card import Card, Suit, Deck


# TODO: Convert this to a namedtuple.
class TwentyNineCard(Card):
    """A Twenty Nine card."""

    def __init__(self, suit: Suit, value: int):
        super().__init__(suit, value)
        self.__set_name(value)
        self.__set_score(value)

    def __set_name(self, value: int) -> None:
        match value:
            case 1:
                self._name = "A"
            case 11:
                self._name = "J"
            case 12:
                self._name = "Q"
            case 13:
                self._name = "K"
            case 7 | 8 | 9 | 10:
                self._name = str(self.value)
            case _:
                raise ValueError(f"Invalid 29 card value: {value}")

    def __set_score(self, value: int) -> None:
        match value:
            case 1 | 10:
                self._score = 1
            case 7 | 8 | 12 | 13:
                self._score = 0
            case 9:
                self._score = 2
            case 11:
                self._score = 3
            case _:
                raise ValueError(f"Invalid 29 card value: {value}")

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if value == 1 or (7 <= value <= 13):
            self._value = value
        else:
            raise ValueError(f"Invalid 29 card value: {value}")

    @property
    def score(self):
        """Score of the card"""
        return self._score

    @score.setter
    def score(self):
        raise ValueError("You can not change score of this card.")

    @property
    def name(self):
        """Name of the card"""
        return self._name

    @name.setter
    def name(self):
        raise ValueError("You can not change name of this card.")

    def __str__(self) -> str:
        return f"{self.suit.value}-{self.name}"


class TwentyNineDeck(Deck):
    """A Twenty Nine Deck. Consists card from 7 to K and A."""

    def __init__(self, cards: list[TwentyNineCard]):
        super().__init__(cards)

    @property
    def cards(self):
        return self._cards

    @cards.setter
    def cards(self, cards: list[TwentyNineCard]):
        for card in cards:
            if not isinstance(card, TwentyNineCard):
                raise ValueError(f"Invalid card for 29: {card}")
        self._cards = cards

    def top_n_cards(self, n: int) -> list[TwentyNineCard]:
        """Get top n cards from the deck.

        Args:
            n (int): Number of cards to return.

        Raises:
            TypeError: If n is not an int.

        Returns:
            list[TwentyNineCard]: List of the n cards from the top.
        """
        if not isinstance(n, int):
            raise TypeError("n should be an integer.")
        return [self.cards.pop() for _ in range(n)]
