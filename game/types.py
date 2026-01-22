"""Типизация."""

from dataclasses import dataclass

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
    how_play: ButtonTexture
    settings: ButtonTexture


@dataclass
class NumberButtonTexture:
    """Текстура кнопки (виджета) выбора уровня (карты)."""

    one: ButtonTexture
    two: ButtonTexture
    three: ButtonTexture
    four: ButtonTexture
    five: ButtonTexture


# TODO(@iamlostshe): Сделать класс игрока
