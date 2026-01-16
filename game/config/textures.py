"""Текстуры используемые в игре."""

from pathlib import Path

from arcade import load_texture

ASSETS_FOLDER = Path("assets")

GIRL = load_texture(ASSETS_FOLDER / "girl.jpeg")
CLICK = load_texture(ASSETS_FOLDER / "click.png")
CONTNORM = load_texture(ASSETS_FOLDER / "contnorm.png")
EXITNORM = load_texture(ASSETS_FOLDER / "exitnorm.png")
EXITPUSH = load_texture(ASSETS_FOLDER / "exitpush.png")
STARTNORM = load_texture(ASSETS_FOLDER / "startnorm.png")
STARTPUSH = load_texture(ASSETS_FOLDER / "startpush.png")
SETTINGPUSH = load_texture(ASSETS_FOLDER / "settingpush.png")
HOWPLAYNORM = load_texture(ASSETS_FOLDER / "howplaynorm.png")
HOWPLAYPUSH = load_texture(ASSETS_FOLDER / "howplaypush.png")
SETTINGSNORM = load_texture(ASSETS_FOLDER / "settingsnorm.png")
WALK_TEXTURES = [
    [
        load_texture(
            ASSETS_FOLDER / "moves_sprites" /
            f"{name.lower()}moves" / f"move{name}{n}.png",
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
    ASSETS_FOLDER / "moves_sprites" / "idle_player.png",
)
