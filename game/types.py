"""Типизация."""

from dataclasses import dataclass

import arcade
from arcade.texture import Texture

from game import config

# TODO(@iamlostshe): Перевести тут всё на Pydantic BaseModel
# если кто-то останется в живых, разумеется


@dataclass
class ButtonTexture:
    """Текстура кнопки (виджета)."""

    texture: Texture
    hover_texture: Texture
    click: Texture


@dataclass
class Buttons:
    """Стандартный набор кнопок."""

    continue_: ButtonTexture
    exit_: ButtonTexture
    start: ButtonTexture
    settings: ButtonTexture


@dataclass
class NumberButtonTexture:
    """Текстура кнопки (виджета) выбора уровня (карты)."""

    one: ButtonTexture
    two: ButtonTexture
    three: ButtonTexture
    four: ButtonTexture
    five: ButtonTexture


class Player(arcade.Sprite):
    """Класс игрока."""

    can_go = True

    def __init__(
        self,
        texture: Texture,
        scale: int,
        speed: int,
        spawn_position: tuple[int],
    ) -> None:
        """Инициализация игрока."""
        x, y = (
            (spawn_position[0] + 0.5) * 32 * config.TILE_SCALING,
            (spawn_position[1] + 0.5) * 32 * config.TILE_SCALING,
        )

        super().__init__(texture, scale, x, y)
        self.speed = speed


@dataclass
class Task:
    """Задача.

    - Текст (условие).
    - Ответ.
    - Варианты ответа.
    """

    text: str
    answer: str
    answer_options: list[str]
