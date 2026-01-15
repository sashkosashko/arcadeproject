import arcade
from arcade.gui import (
    UIManager,
    UITextureButton,
    # UIFlatButton,
    # UILabel,
    # UIInputText,
    # UITextArea,
    # UISlider,
    # UIDropdown,
    # UIMessageBox,
)
from arcade.gui.widgets.layout import UIAnchorLayout, UIBoxLayout

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
        self.box_layout = UIBoxLayout(vertical=True, space_between=10)

        self.setup_widgets()

        self.anchor_layout.add(self.box_layout)
        self.manager.add(self.anchor_layout)

        self.set_fullscreen(True)
        self.setup()

    def setup_widgets(self):
        texture_normal = arcade.load_texture("assets/startnorm.png")
        texture_hovered = arcade.load_texture("assets/startpush.png")
        texture_pressed = arcade.load_texture("assets/click.png")
        texture_button = UITextureButton(
            texture=texture_normal,
            texture_hovered=texture_hovered,
            texture_pressed=texture_pressed,
            scale=4.0,
        )
        texture_button.on_click = self.play
        texture_normal1 = arcade.load_texture("assets/settingsnorm.png")
        texture_hovered1 = arcade.load_texture("assets/settingpush.png")
        texture_pressed1 = arcade.load_texture("assets/click.png")
        texture_button1 = UITextureButton(
            texture=texture_normal1,
            texture_hovered=texture_hovered1,
            texture_pressed=texture_pressed1,
            scale=4.0,
        )
        # texture_button1.on_click =
        texture_normal2 = arcade.load_texture("assets/howplaynorm.png")
        texture_hovered2 = arcade.load_texture("assets/howplaypush.png")
        texture_pressed2 = arcade.load_texture("assets/click.png")
        texture_button2 = UITextureButton(
            texture=texture_normal2,
            texture_hovered=texture_hovered2,
            texture_pressed=texture_pressed2,
            scale=4.0,
        )
        # texture_button2.on_click =
        self.box_layout.add(texture_button)
        self.box_layout.add(texture_button1)
        self.box_layout.add(texture_button2)

    def setup(self) -> None:
        map_name = "assets/start_map.tmx"
        self.tile_map = arcade.load_tilemap(map_name, scaling=self.tile_scaling)
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
