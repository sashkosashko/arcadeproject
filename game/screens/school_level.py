"""Первый уровень."""

from game import config
from game.change_screen import change_screen
from game.components import Dialog
from game.config import tilemaps
from game.screens import BaseScreen
from game.utils.api import task

SPAWN_POS = 10, 6


def _to_real_cords(x: int, y: int) -> int:
    return (
        int((x + 0.5) * 32 * config.TILE_SCALING),
        int((y + 0.5) * 32 * config.TILE_SCALING),
    )


_QUADRANS = [
    (_to_real_cords(1, 8), _to_real_cords(7, 11)),
    (_to_real_cords(12, 19), _to_real_cords(7, 11)),
    (_to_real_cords(1, 8), _to_real_cords(1, 5)),
    (_to_real_cords(12, 19), _to_real_cords(1, 5)),
]


def _beautify_answers(answer_options: list) -> str:
    """Нормализовать/укарасить/придать человеческий вид вариантам ответов."""
    return (
        f"A) {answer_options[0]} {' ' * 20} Б) {answer_options[1]}\n\n"
        f"В) {answer_options[2]} {' ' * 20} Г) {answer_options[3]}"
    )


class SchoolLevelScreen(BaseScreen):
    """Первый уровень."""

    def __init__(self) -> None:
        """Инициализация класса."""
        super().__init__(SPAWN_POS, tilemaps.SCHOOL_LEVEL)

        self.task = task()

        self.dialog = Dialog(
            title=self.task.text.replace("\n", " "),
            text=_beautify_answers(self.task.answer_options),
            pos=1,
        )

        self.quadran_x, self.quadran_y = _QUADRANS[
            self.task.answer_options.index(self.task.answer)
        ]

    def check_change_level(self) -> None:
        """Проверка события переключения между уровнями."""
        if (
            self.player.center_x >= self.quadran_x[0]
            and self.player.center_y >= self.quadran_y[0]
            and self.player.center_x <= self.quadran_x[1]
            and self.player.center_y <= self.quadran_y[1]
        ):
            change_screen("4")
