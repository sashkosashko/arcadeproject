"""Первый уровень."""

from game.change_screen import change_screen
from game.components import Dialog
from game.config import sounds, tilemaps
from game.screens import BaseScreen


class FirstLevelScreen(BaseScreen):
    """Первый уровень."""

    def __init__(self) -> None:
        """Инициализация класса."""
        super().__init__((0, 0), tilemaps.FIRST_LEVEL)

    def show_dialogs(self) -> None:
        """Показ диалогов."""
        self.dialog = Dialog(
            "Лиза",
            "Ура!..",
            sounds.HOORAY,
            pos=1,
        )

    def check_change_level(self) -> None:
        """Проверка события переключения между уровнями."""
        if (
            self.player.center_x > 1436
            and self.player.center_x < 1816
            and self.player.center_y > 3002
            and self.player.center_y < 3292
        ):
            change_screen("grid", 2)
