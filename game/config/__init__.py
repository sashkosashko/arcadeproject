import arcade

from . import sounds, textures, tilemaps

TITLE = "Игра"
WIDTH, HEIGHT = arcade.get_display_size()

# Масштаб игры
TILE_SCALING = 3

# Скорость игрока
SPEED = 10

# Что-то на умном
CAMERA_LERP = 0.15

# Клавиши управления
KEYS = (
    arcade.key.S,
    arcade.key.A,
    arcade.key.W,
    arcade.key.D,
)

# Список уровней
LEVELS_LIST = (
    tilemaps.FIRST_LEVEL,
    tilemaps.SECOND_LEVEL,
    tilemaps.THIRD_LEVEL,
)

__all__ = (
    "CAMERA_LERP",
    "HEIGHT",
    "KEYS",
    "LEVELS_LIST",
    "SPEED",
    "TILE_SCALING",
    "TITLE",
    "WIDTH",
    "sounds",
    "textures",
    "tilemaps",
)
