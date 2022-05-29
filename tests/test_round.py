"""Test cases for src/cards/round.py"""
from unittest import TestCase
from unittest.mock import patch
from src.cards.players import Player
from src.cards.round import Round
from src.cards.twentynine import TwentyNineDeck, TwentyNineCard
from src.cards.card import Suit


class TestRound(TestCase):
    """Test Round class"""

    def setUp(self) -> None:
        self.players = (Player("E"), Player("N"), Player("W"), Player("S"))

        card_values = (
            10,
            9,
            11,
            12,
            13,
            1,
            7,
            8,
        )
        self.cards: list[TwentyNineCard] = []
        for suit in Suit:
            self.cards += [TwentyNineCard(suit, val) for val in card_values]
        self.cards_reversed = list(reversed(self.cards))

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

    @patch("src.cards.round.Round._initialize_and_shuffle_deck")
    def test_round_deal(self, mock_shuffle_deck):
        """Test dealing"""
        mock_shuffle_deck.return_value = TwentyNineDeck(self.cards[:])
        r = Round(players=self.players, dealer=0)
        r.deal()
        self.assertListEqual(
            r.players[r.player_ordering[0]].cards, self.cards_reversed[: r.CARDS_TO_DEAL]
        )
        self.assertListEqual(
            r.players[r.player_ordering[1]].cards,
            self.cards_reversed[r.CARDS_TO_DEAL : 2 * r.CARDS_TO_DEAL],
        )
        self.assertListEqual(
            r.players[r.player_ordering[2]].cards,
            self.cards_reversed[2 * r.CARDS_TO_DEAL : 3 * r.CARDS_TO_DEAL],
        )
        self.assertListEqual(
            r.players[r.player_ordering[3]].cards,
            self.cards_reversed[3 * r.CARDS_TO_DEAL : 4 * r.CARDS_TO_DEAL],
        )

    def test_round_next_bidder_when_no_bid_is_made_1(self):
        """Test initial value returned by next bidder."""
        res = Round.next_bidder([0, 1, 2, 3], None)
        self.assertEqual(res, 0)

    def test_next_bidder_after_first_bid(self):
        """P1 bids 16. Next P2 should be returned."""
        res = Round.next_bidder([0, 1, 2, 3], 0)
        self.assertEqual(res, 1)

    def test_next_bidder_after_second_bid(self):
        """P2 bids 17 when P1 bid 16. Next P1 should be returned."""
        res = Round.next_bidder([0, 1, 2, 3], 1)
        self.assertEqual(res, 0)

    def test_next_bidder_after_everyone_passed(self):
        """When everyone else has passed, it should return -1."""
        res = Round.next_bidder([], 1)
        self.assertEqual(res, -1)
