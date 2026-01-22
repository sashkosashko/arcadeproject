"""Смена экрана."""

import arcade

from game import screens


def change_screen(
    screen: str,
    level: int | None = None,
) -> None:
    arcade.close_window()

    if screen == "grid":
        screens.GridScreen(level)
    elif screen == "menu":
        screens.MenuScreen()

    arcade.run()
