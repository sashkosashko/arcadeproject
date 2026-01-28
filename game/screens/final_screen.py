import arcade
from arcade.gui import UIManager, UILabel
from arcade.gui.widgets.layout import UIAnchorLayout, UIBoxLayout

from game import config
from game.components.menu_widgets import setup_menu_widgets
from game.config import textures
from game.screens import change_screen


class FinalScreen(arcade.Window):
    """Финальное окно игры."""

    def __init__(self, time, total) -> None:
        super().__init__(WIDTH, HEIGHT, TITLE)
        arcade.set_background_color(arcade.color.BLACK)
        self.title = TITLE
        self.manager = UIManager()
        self.manager.enable()
        self.tile_scaling = 2

        self.anchor_layout = UIAnchorLayout()
        self.box_layout = UIBoxLayout(vertical=True, space_between=10)

        self.anchor_layout.add(self.box_layout)
        self.manager.add(self.box_layout)

        self.set_fullscreen(True)
        self.setup()

    def setup_widgets(self):
        text_area = UITextArea(text=f"Уровень завершен!\nВремя прохождения:\n{self.time}\nОчков набрано:\n{self.total}", 
                       width=200, 
                       height=100, 
                       font_size=14)
        self.box_layout.add(text_area)

    def setup(self) -> None:
        self.setup_widgets()
        self.setup_widgets()
        self.tile_map = arcade.load_tilemap(
            tilemaps.START_MAP,
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
