from enum import Enum

from card import Suit
from players import Player
from twentynine import TwentyNineCard, TwentyNineDeck

PLAYERS = 4


class BidAction(Enum):
    BID = "Bid"
    PASS = "Pass"
    STAY = "Stay"


class Round:
    CARDS_TO_DEAL = 4
    MIN_BID = 16
    def __init__(self, players: list[Player], dealer: int):
        self.trump: int | Suit = None
        self.players = players
        self.dealer = players[dealer]
        self.player_ordering = self._create_palyer_ordering()
        self._initialize_and_shuffle_deck()

    def _create_palyer_ordering(self):
        dealer_index = self.players.index(self.dealer)
        return [(dealer_index + i + 1) % PLAYERS for i in range(PLAYERS)]

    def _initialize_and_shuffle_deck(self):
        card_values = (1, 7, 8, 9, 10, 11 , 12, 13)
        cards: list[TwentyNineCard] = []
        for suit in Suit:
            cards += [TwentyNineCard(suit, val) for val in card_values]

        self.deck = TwentyNineDeck(cards)
        self.deck.shuffle()

    def deal(self):
        print(f"{self.dealer} will deal the deck this round.")
        for index in self.player_ordering:
            self.players[index].cards = self.deck.top_n_cards(self.CARDS_TO_DEAL)

    def player_passed(self, choice: str) -> bool:
        return choice in ('n', 'N')

    def _next_bidder(self, eligible_to_bid: list[int], last_bidder: int | None) -> int:
        if eligible_to_bid:
            if last_bidder is None:
                return eligible_to_bid[0]
            else:
                last_bidder_index = eligible_to_bid.index(last_bidder)
                if last_bidder_index > 0:
                    return eligible_to_bid[0]
                elif len(eligible_to_bid) > 1:
                    return eligible_to_bid[1]
        return -1


    def bid(self, bidder: Player, *, action: BidAction,  cur_bid: int | None, min_bid: int, last_bidder: Player | None) -> str:
        bid = ''
        while bid not in {'y', 'n', 'Y', 'N'}:
            print(f"Your cards: {bidder.cards}")
            if not (cur_bid and last_bidder):
                bid = input(f"{bidder}, Do you want to start bidding with {min_bid}? [Y/N]...")
            elif action == BidAction.STAY:
                bid = input(f"{bidder}, {last_bidder} has put a bid for {cur_bid}. Do you want to stay? [Y/N]...")
            else:
                bid = input(f"{bidder}, {last_bidder} has put a bid for {cur_bid}. Do you want to bid for {min_bid}? [Y/N]...")

        return bid

    def bidding(self):
        eligible_to_bid = self.player_ordering[:]
        active = eligible_to_bid[0]
        last_bidder = None
        current_bid = None
        min_bid = self.MIN_BID
        next_action = BidAction.BID
        last_bid_by = None if last_bidder is None else self.players[last_bidder]
        while True:
            response = self.bid(self.players[active], min_bid=min_bid, action=next_action, cur_bid=current_bid, last_bidder=last_bid_by)
            if self.player_passed(response):
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
        else:
            print("All players passed. No one will set trump.")

    def play_round(self):
        self.deal()
        self.bidding()
