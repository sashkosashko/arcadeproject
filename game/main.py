"""Запуск игры."""

import arcade

from .game import StartGame

TITLE = "Игра"
WIDTH, HEIGHT = arcade.get_display_size()


def main() -> None:
    """Запуск игры."""
    StartGame(WIDTH, HEIGHT, TITLE)
    arcade.run()
