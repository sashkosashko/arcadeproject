"""Текстуры используемые в игре."""

from pathlib import Path

from arcade import load_texture

from game.types import Buttons, ButtonTexture, NumberButtonTexture

_TEXTURES_FOLDER = Path("assets") / "textures"

_BUTTONS_FOLDER = _TEXTURES_FOLDER / "buttons"
_CLICK_FOLDER = _BUTTONS_FOLDER / "click"
_NORM_FOLDER = _BUTTONS_FOLDER / "norm"
_PUSH_FOLDER = _BUTTONS_FOLDER / "push"
_NUM_FOLDER = _NORM_FOLDER / "numbers"

_CLICK = load_texture(_CLICK_FOLDER / "click.png")
_CLICK_LEVELS = load_texture(_CLICK_FOLDER / "click_levels.png")

number = NumberButtonTexture(
    *(
        ButtonTexture(
            load_texture(_NUM_FOLDER / f"{i}.png"),
            load_texture(_NUM_FOLDER / f"{i}.png"),
            _CLICK_LEVELS,
        )
        for i in range(1, 6)
    ),
)

button = Buttons(
    *(
        ButtonTexture(
            load_texture(_NORM_FOLDER / f"{i}.png"),
            load_texture(_PUSH_FOLDER / f"{i}.png"),
            _CLICK,
        )
        for i in (
            "continue",
            "exit",
            "start",
            "settings",
        )
    ),
)

WALK_TEXTURES = [
    [
        load_texture(
            _TEXTURES_FOLDER
            / "moves_sprites"
            / f"{name.lower()}moves"
            / f"move{name}{n}.png",
        )
        for n in range(1, 5)
    ]
    for name in (
        "DOWN",
        "LEFT",
        "UP",
        "RIGHT",
    )
]

MOVES_SPRITES_IDLE_PLAYER = load_texture(
    _TEXTURES_FOLDER / "moves_sprites" / "idle_player.png",
)
