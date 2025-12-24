"""Запуск игры."""

import arcade
from game import GridGame

TITLE = "Игра"
WIDTH, HEIGHT = arcade.get_display_size()


def main() -> None:
    """Запуск игры."""
    GridGame(WIDTH, HEIGHT, TITLE)
    arcade.run()
