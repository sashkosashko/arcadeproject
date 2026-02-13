"""Конечная заставка."""

import arcade

from game.components import Dialog
from game.config import sounds, tilemaps
from game.screens import BaseScreen
from game.utils.manage_time import get_status

SPAWN_POS = (380, 330)


class EndScreen(BaseScreen):
    """Окончательный экран."""

    def __init__(self) -> None:
        """Инициализация класса."""
        super().__init__(SPAWN_POS, tilemaps.END)

        self.dialog = Dialog(
            "Лиза",
            "Фух... Мы справились!..",
            sounds.PHEW_WE_DID_IT,
            pos=1,
        )

        result = get_status()

        message_box = arcade.gui.UIMessageBox(
            width=300,
            height=200,
            message_text=result,
            buttons=("Ура!",),
        )
        self.manager.add(message_box)
