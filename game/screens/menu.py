import arcade
from arcade.gui import UIManager
from arcade.gui.widgets.layout import UIAnchorLayout, UIBoxLayout

from game.components.menu_widgets import setup_menu_widgets
from game.config import textures, tilemaps
from game.screens import GridScreen


class MenuScreen(arcade.Window):
    """Начальное окно игры."""

    def __init__(self, width: int, height: int, title: str) -> None:
        super().__init__(width, height, title)
        self.title = title
        self.manager = UIManager()
        self.manager.enable()
        self.tile_scaling = 2

        self.anchor_layout = UIAnchorLayout()
        self.anchor_layout2 = UIAnchorLayout()
        self.box_layout = UIBoxLayout(vertical=True, space_between=10)
        self.box_layout2 = UIBoxLayout(vertical=False, space_between=10)

        self.anchor_layout.add(self.box_layout)
        self.anchor_layout2.add(self.box_layout2)
        self.manager.add(self.anchor_layout)

        self.set_fullscreen(True)
        self.setup()

    def setup(self) -> None:
        # TODO(@iamlostshe): Доработать кнопки
        # print - просто заглушка
        setup_menu_widgets(
            (textures.button.start, self.play),
            (textures.button.settings, print),
            (textures.button.how_play, print),
            box_layout=self.box_layout,
        )

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

    def play(self, _: arcade.gui.events.UIOnClickEvent) -> None:
        self.manager.clear()
        self.manager.add(self.anchor_layout2)

        # TODO(@iamlostshe): Доработать кнопки
        # print - просто заглушка
        setup_menu_widgets(
            (textures.number.one, lambda x: self.start_play(x, 1)),
            (textures.number.two, lambda x: self.start_play(x, 2)),
            (textures.number.three, lambda x: self.start_play(x, 3)),
            box_layout=self.box_layout2,
        )

    def start_play(self, _: arcade.gui.events.UIOnClickEvent, level: int) -> None:
        arcade.close_window()
        GridScreen(self.width, self.height, self.title, level)
        arcade.run()
