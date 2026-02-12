"""Смена экрана."""

import arcade

from game import screens


def change_screen(
    screen: str,
) -> None:
    arcade.close_window()

    match screen:
        case "menu":
            screens.MenuScreen()
        case "0":
            screens.FirstLevelScreen()
        case "1":
            screens.SecondLevelScreen()
        case "2":
            screens.ThirdLevelScreen()
        case "3":
            screens.FourthLevelScreen()
        case "4":
            screens.FifthLevelScreen()

    arcade.run()
