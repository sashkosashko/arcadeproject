"""Текстуры используемые в игре."""

from pathlib import Path

from arcade import load_texture

CLICK = load_texture(Path("assets") / "click.png")
CONTNORM = load_texture(Path("assets") / "contnorm.png")
EXITNORM = load_texture(Path("assets") / "exitnorm.png")
EXITPUSH = load_texture(Path("assets") / "exitpush.png")
STARTNORM = load_texture(Path("assets") / "startnorm.png")
STARTPUSH = load_texture(Path("assets") / "startpush.png")
SETTINGPUSH = load_texture(Path("assets") / "settingpush.png")
HOWPLAYNORM = load_texture(Path("assets") / "howplaynorm.png")
HOWPLAYPUSH = load_texture(Path("assets") / "howplaypush.png")
SETTINGSNORM = load_texture(Path("assets") / "settingsnorm.png")
WALK_TEXTURES = [
    [
        load_texture(
            Path("assets") / "moves_sprites" /
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
    Path("assets") / "moves_sprites" / "idle_player.png",
)
