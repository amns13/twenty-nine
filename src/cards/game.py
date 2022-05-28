"""Contains the game class ans initializes basic config."""
from src.cards.players import Player
from src.cards.round import Round


class Game:
    """The Game class"""

    CARDS_TO_DEAL = 4
    players = (Player("E"), Player("N"), Player("W"), Player("S"))
    scores = (0, 0)

    @classmethod
    def winner(cls) -> tuple[Player, Player] | None:
        """Determines the winner of the current game.

        Returns:
            tuple[Player, Player] | None: tuple of the players of winning team.
                                            None if now clear winner yet.
        """
        if Game.scores[0] == 6 or Game.scores[1] == -6:
            return Game.players[0], Game.players[2]

        if Game.scores[0] == -6 or Game.scores[1] == 6:
            return Game.players[1], Game.players[3]

        return None

    @classmethod
    def play(cls):
        """Start the game play."""
        dealer_index = 0
        while not Game.winner():
            twenty_nine_round = Round(Game.players, dealer_index)
            twenty_nine_round.play_round()
