"""Contains logic for each game round in game."""
from enum import Enum

from src.cards.card import Suit
from src.cards.players import Player
from src.cards.twentynine import TwentyNineCard, TwentyNineDeck

PLAYERS = 4


def player_passed(choice: str) -> bool:
    """Check if the bidder passed."""
    return choice in ("n", "N")


class BidAction(Enum):
    """Actions available for bidding"""

    BID = "Bid"
    PASS = "Pass"
    STAY = "Stay"


class Round:
    """Describes each round of the game."""

    CARDS_TO_DEAL = 4
    MIN_BID = 16

    def __init__(self, players: tuple[Player], dealer: int):
        if not 0 <= dealer <= 3:
            raise ValueError("dealer index should be in range [0, 4]")
        self.trump: Suit | None = None
        self.players = players
        self.dealer = players[dealer]
        self.player_ordering = self._create_palyer_ordering()
        self.highest_bidder: Player | None = None
        self.highest_bid: int | None = None
        self.deck = None
        self._initialize_and_shuffle_deck()

    def _create_palyer_ordering(self) -> list[int]:
        dealer_index = self.players.index(self.dealer)
        return [(dealer_index + i + 1) % PLAYERS for i in range(PLAYERS)]

    def _initialize_and_shuffle_deck(self) -> TwentyNineDeck:
        card_values = (1, 7, 8, 9, 10, 11, 12, 13)
        cards: list[TwentyNineCard] = []
        for suit in Suit:
            cards += [TwentyNineCard(suit, val) for val in card_values]

        self.deck = TwentyNineDeck(cards)
        self.deck.shuffle()

    def deal(self):
        """
        Deal the card among the players. Starts from the next player
        from the dealer and ends with the dealer.
        """
        print(f"{self.dealer} will deal the deck this round.")
        for index in self.player_ordering:
            self.players[index].cards += self.deck.top_n_cards(self.CARDS_TO_DEAL)

    @classmethod
    def _next_bidder(cls, eligible_to_bid: list[int], last_bidder: int | None) -> int:
        if eligible_to_bid:
            if last_bidder is None:
                return eligible_to_bid[0]
            last_bidder_index = eligible_to_bid.index(last_bidder)
            if last_bidder_index > 0:
                return eligible_to_bid[0]
            return eligible_to_bid[1]
        return -1

    @staticmethod
    def bid(
        bidder: Player,
        *,
        action: BidAction,
        cur_bid: int | None,
        min_bid: int,
        last_bidder: Player | None,
    ) -> str:
        """Takes bid action from player

        Args:
            bidder (Player): Bidder
            action (BidAction): action available to the player along with pass
            cur_bid (int | None): Current highest bid. None if no bid has been called yet
            min_bid (int): Minimum possible bid
            last_bidder (Player | None): Last bidder. None if no bid has been called yet

        Returns:
            str: bid action taken: Y/N
        """
        player_action = ""
        while player_action not in {"y", "n", "Y", "N"}:
            print(f"{bidder}'s cards: {bidder.cards}")
            if not (cur_bid and last_bidder):
                player_action = input(
                    f"{bidder}, Do you want to start bidding with {min_bid}? [Y/N]..."
                )
            elif action == BidAction.STAY:
                player_action = input(
                    f"{bidder}, {last_bidder} has put a bid for {cur_bid}. Do you want to stay?"
                    " [Y/N]..."
                )
            else:
                player_action = input(
                    f"{bidder}, {last_bidder} has put a bid for {cur_bid}. Do you want to bid for"
                    f" {min_bid}? [Y/N]..."
                )

        return player_action

    def bidding(self) -> bool:
        """Runs the bidding algorithm.

        Returns:
            bool: Whether a bid was placed successfully or not.
        """
        eligible_to_bid = self.player_ordering[:]
        active = eligible_to_bid[0]
        last_bidder = None
        current_bid = None
        min_bid = self.MIN_BID
        next_action = BidAction.BID
        last_bid_by = None if last_bidder is None else self.players[last_bidder]
        while True:
            response = self.bid(
                self.players[active],
                min_bid=min_bid,
                action=next_action,
                cur_bid=current_bid,
                last_bidder=last_bid_by,
            )
            if player_passed(response):
                eligible_to_bid.remove(active)
                next_bidder = self._next_bidder(eligible_to_bid, last_bidder)
                if next_bidder == -1:
                    break
                active = next_bidder
                next_action = BidAction.BID

            elif next_action == BidAction.BID:
                next_action = BidAction.STAY if current_bid else BidAction.BID
                current_bid = min_bid
                min_bid += 1
                next_bidder = self._next_bidder(eligible_to_bid, active)
                last_bidder = active
                last_bid_by = None if last_bidder is None else self.players[last_bidder]
                active = next_bidder
            else:  # STAY
                next_action = BidAction.BID
                next_bidder = self._next_bidder(eligible_to_bid, active)
                last_bidder = active
                last_bid_by = None if last_bidder is None else self.players[last_bidder]
                active = next_bidder

        if current_bid:
            print(f"{self.players[last_bidder]} will set trump for {current_bid}")
            self.highest_bid = current_bid
            self.highest_bidder = self.players[last_bidder]
            return True

        print("All players passed. No one will set trump.")
        return False

    def get_trump(self) -> Suit:
        """Ask highest bidder to set the trump

        Returns:
            Suit: Suit selected as the trump.
        """
        trump = 0
        while not 1 <= trump <= 4:
            try:
                trump = int(
                    input(
                        f"""{self.highest_bidder}, please choose your trump color:
                        [1: Spade, 2: Heart, 3: Club, 4: Diamond]...
                        """
                    )
                )
            except ValueError:
                print("Please select an integer between 1 to 4.")
        return list(Suit)[trump - 1]

    def play_round(self):
        """Runs the gameplay for the round"""
        self.deal()
        bid_successful = self.bidding()
        if not bid_successful:
            print("Trump not set in this round. Deal again.")
            return
        self.trump = self.get_trump()
        self.deal()
        for player in self.players:
            print(f"{player} - {player.cards}")
        print(f"Trump: {self.trump.value}")
