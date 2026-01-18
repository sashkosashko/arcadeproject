import arcade
from arcade.gui import (
    UIManager,
    UITextureButton,
)
from arcade.gui.widgets.layout import UIAnchorLayout, UIBoxLayout

from config import textures
#from game.screens import GridScreen


class MenuScreen(arcade.Window):
    """Начальное окно игры."""

    def __init__(self, width: int, height: int, title: str) -> None:
        super().__init__(width, height, title)
        self.title = title
        self.manager = UIManager()
        self.manager.enable()
        self.tile_scaling = 2

        self.anchor_layout = UIAnchorLayout()
        self.box_layout = UIBoxLayout(vertical=True, space_between=10)
        self.box_layout2 = UIBoxLayout(vertical=False, space_between=10)

        self.setup_menu_widgets()

        self.anchor_layout.add(self.box_layout)
        self.anchor_layout.add(self.box_layout2)
        self.manager.add(self.anchor_layout)

        self.set_fullscreen(True)
        self.setup()

    def setup_menu_widgets(self) -> None:
        """Установка виджетов меню."""
        for texture, texture_hovered, on_click in (
            (textures.STARTNORM, textures.STARTPUSH, self.play),
            (textures.SETTINGSNORM, textures.SETTINGPUSH, None),
            (textures.HOWPLAYNORM, textures.HOWPLAYPUSH, None),
        ):
            texture_button = UITextureButton(
                texture=texture,
                texture_hovered=texture_hovered,
                texture_pressed=textures.CLICK,
                scale=4.0,
            )
            texture_button.on_click = on_click
            self.box_layout.add(texture_button)

    def setup(self) -> None:
        self.tile_map = arcade.load_tilemap(
            "assets/start_map.tmx",
            scaling=self.tile_scaling,
        )
        self.floor_list = self.tile_map.sprite_lists["start"]

        self.world_width = int(
            self.tile_map.width * self.tile_map.tile_width * self.tile_scaling,
        )
        self.world_height = int(
            self.tile_map.height * self.tile_map.tile_height * self.tile_scaling,
        )

    def on_draw(self) -> None:
        self.clear()
        self.floor_list.draw()
        self.manager.draw()

    def play(self, _: arcade.gui.events.UIOnClickEvent) -> None:
        arcade.close_window()
        GridScreen(self.width, self.height, self.title)
        arcade.run()
