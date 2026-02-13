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
            screens.StartScreen()
        case "1":
            screens.MotorSkillsLevelScreen()
        case "2":
            screens.PatienceLevelScreen()
        case "3":
            screens.SchoolLevelScreen()
        case "4":
            screens.EndScreen()

    arcade.run()
