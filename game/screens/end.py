from game.components import Dialog
from game.config import sounds, tilemaps
from game.screens import BaseScreen


class EndScreen(BaseScreen):
    """Окончательный экран."""

    def __init__(self) -> None:
        """Инициализация класса."""
        super().__init__((0, 0), tilemaps.END)

    def show_dialogs(self) -> None:
        """Показ диалогов."""
        self.dialog = Dialog(
            "Лиза",
            "Фух... Мы справились!..",
            sounds.PHEW_WE_DID_IT,
            pos=1,
        )
