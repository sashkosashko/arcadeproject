"""Типизация."""

from dataclasses import dataclass

import arcade
from arcade.texture import Texture


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

    def __init__(self, texture: Texture, scale: int, speed: int) -> None:
        """Инициализация игрока."""
        super().__init__(texture, scale)
        self.speed = speed
