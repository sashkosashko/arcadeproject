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
    arcade.key.S, arcade.key.DOWN, 167503724544,
    arcade.key.A, arcade.key.LEFT, 163208757248,
    arcade.key.W, arcade.key.UP, 107374182400,
    arcade.key.D, arcade.key.RIGHT, 171798691840,
)

__all__ = (
    "CAMERA_LERP",
    "HEIGHT",
    "KEYS",
    "SPEED",
    "TILE_SCALING",
    "TITLE",
    "WIDTH",
    "sounds",
    "textures",
    "tilemaps",
)

