from game.components import Dialog
from game.config import sounds, tilemaps
from game.screens import BaseScreen

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
