from players import Player
from round import Round

class Game:
    CARDS_TO_DEAL = 4
    players = (Player('E'), Player('N'), Player('W'), Player('S'))
    scores = (0, 0)

    @classmethod
    def winner(cls) -> tuple[Player, Player] | None:
        if Game.scores[0] == 6 or Game.scores[1] == -6:
            return Game.players[0], Game.players[2]
        elif Game.scores[0] == -6 or Game.scores[1] == 6:
            return Game.players[1], Game.players[3]
        else:
            return None

    @classmethod
    def play(cls):
        dealer_index = 0
        while not Game.winner():
            round = Round(Game.players, dealer_index)
            round.play_round()
            break
