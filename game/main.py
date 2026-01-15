"""Запуск игры."""

import arcade

from game.screens import MenuScreen

TITLE = "Игра"
WIDTH, HEIGHT = arcade.get_display_size()


def main() -> None:
    """Запуск игры."""
    MenuScreen(WIDTH, HEIGHT, TITLE)
    arcade.run()
