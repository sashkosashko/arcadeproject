"""Запуск игры."""

import contextlib

import arcade

from game.screens import MenuScreen

if __name__ == "__main__":
    MenuScreen()
    with contextlib.suppress(KeyboardInterrupt):
        arcade.run()
