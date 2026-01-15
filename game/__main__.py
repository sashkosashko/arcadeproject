"""Запуск игры."""

import arcade

from game.screens import MenuScreen

TITLE = "Игра"
WIDTH, HEIGHT = arcade.get_display_size()

if __name__ == "__main__":
    MenuScreen(WIDTH, HEIGHT, TITLE)
    arcade.run()
