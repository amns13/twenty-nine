from unittest import TestCase
from src.cards.players import Player
from src.cards.round import Round
from src.cards.twentynine import TwentyNineDeck


class TestRound(TestCase):
    def setUp(self) -> None:
        self.players = (Player("E"), Player("N"), Player("W"), Player("S"))
        return super().setUp()

    def test_round_initialization(self):
        res = Round(players=self.players, dealer=0)
        self.assertIsNone(res.trump)
        self.assertTupleEqual(self.players, res.players)
        self.assertEqual(self.players[0], res.dealer)
        self.assertListEqual([1, 2, 3, 0], res.player_ordering)
        self.assertIsNone(res.highest_bidder)
        self.assertIsNone(res.highest_bid)
        self.assertIsInstance(res.deck, TwentyNineDeck)

    def test_round_initialization_for_larger_player_index(self):
        res = Round(players=self.players, dealer=1)
        self.assertEqual(self.players[1], res.dealer)
        self.assertListEqual([2, 3, 0, 1], res.player_ordering)
