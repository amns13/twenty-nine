"""Test cases for src/cards/round.py"""
from unittest import TestCase
from src.cards.players import Player
from src.cards.round import Round
from src.cards.twentynine import TwentyNineDeck


class TestRound(TestCase):
    """Test Round class"""

    def setUp(self) -> None:
        self.players = (Player("E"), Player("N"), Player("W"), Player("S"))
        return super().setUp()

    def test_round_initialization(self):
        """round initialization: test all attributes"""
        res = Round(players=self.players, dealer=0)
        self.assertIsNone(res.trump)
        self.assertTupleEqual(self.players, res.players)
        self.assertEqual(self.players[0], res.dealer)
        self.assertListEqual([1, 2, 3, 0], res.player_ordering)
        self.assertIsNone(res.highest_bidder)
        self.assertIsNone(res.highest_bid)
        self.assertIsInstance(res.deck, TwentyNineDeck)

    def test_round_initialization_for_player_index_one(self):
        """Tets round initialization when dealer index is one"""
        res = Round(players=self.players, dealer=1)
        self.assertEqual(self.players[1], res.dealer)
        self.assertListEqual([2, 3, 0, 1], res.player_ordering)

    def test_round_initialization_for_player_index_two(self):
        """Tets round initialization when dealer index is two"""
        res = Round(players=self.players, dealer=2)
        self.assertEqual(self.players[2], res.dealer)
        self.assertListEqual([3, 0, 1, 2], res.player_ordering)

    def test_round_initialization_for_player_index_three(self):
        """Tets round initialization when dealer index is three"""
        res = Round(players=self.players, dealer=3)
        self.assertEqual(self.players[3], res.dealer)
        self.assertListEqual([0, 1, 2, 3], res.player_ordering)

    def test_round_init_with_wrong_index_value(self):
        """Test round initialization when dealer index is not in range [0,3]"""
        with self.assertRaises(ValueError):
            Round(players=self.players, dealer=4)
