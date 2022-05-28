"""Main entry point into the game."""
from src.cards.game import Game


def start_game() -> None:
    """Starts the game play."""
    Game.play()


if __name__ == "__main__":
    start_game()
