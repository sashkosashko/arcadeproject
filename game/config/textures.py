"""Текстуры используемые в игре."""

from arcade import load_texture

CLICK = load_texture("assets/click.png")
CONTNORM = load_texture("assets/contnorm.png")
EXITNORM = load_texture("assets/exitnorm.png")
EXITPUSH = load_texture("assets/exitpush.png")
STARTNORM = load_texture("assets/startnorm.png")
STARTPUSH = load_texture("assets/startpush.png")
SETTINGPUSH = load_texture("assets/settingpush.png")
HOWPLAYNORM = load_texture("assets/howplaynorm.png")
HOWPLAYPUSH = load_texture("assets/howplaypush.png")
SETTINGSNORM = load_texture("assets/settingsnorm.png")
WALK_TEXTURES = [
    [
        load_texture(
            f"assets/moves_sprites/{name.lower()}moves/move{name}{n}.png",
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
    "assets/moves_sprites/idle_player.png",
)
