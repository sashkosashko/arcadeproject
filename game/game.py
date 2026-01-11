"""Основная механика игры."""

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


class GridGame(arcade.Window):
    """Класс игры."""

    def __init__(self, width: int, height: int, title: str) -> None:
        """Инициализация класса игры."""
        super().__init__(width, height, title)
        self.player_texture = arcade.load_texture(
            "assets/moves_sprites/idle_player.png"
        )
        self.change_x = 0
        self.change_y = 0
        self.speed = 5
        self.world_camera = arcade.camera.Camera2D()
        self.gui_camera = arcade.camera.Camera2D()
        self.tile_scaling = 4
        self.camera_lerp = 0.15

        self.set_fullscreen(True)
        self.setup()

    def setup(self) -> None:
        """Запуск игры."""
        self.player_list = arcade.SpriteList()
        map_name = "assets/my_map.tmx"
        self.tile_map = arcade.load_tilemap(map_name, scaling=self.tile_scaling)
        self.floor_list = self.tile_map.sprite_lists["floor"]
        self.collision_list = self.tile_map.sprite_lists["collision"]

        self.world_width = int(
            self.tile_map.width * self.tile_map.tile_width * self.tile_scaling,
        )
        self.world_height = int(
            self.tile_map.height * self.tile_map.tile_height * self.tile_scaling,
        )

        self.player = arcade.Sprite(self.player_texture, scale=2)
        x = self.width // 8
        y = self.height // 8
        self.player.position = (x, y)
        self.player_list.append(self.player)
        # загрузка текстур анимаций персонажа
        self.walk_textures = []
        for name in [
            "DOWN",
            "LEFT",
            "UP",
            "RIGHT",
        ]:  # строгий порядок для структуры текстур
            side_textures = []
            for n in range(1, 5):
                texture = arcade.load_texture(
                    f"assets/moves_sprites/{name.lower()}moves/move{name}{n}.png"
                )
                side_textures.append(texture)
            self.walk_textures.append(side_textures)
        self.texture_change_time = 0
        self.texture_change_delay = 0.1  # секунд на кадр
        self.is_walking = False
        self.current_texture = 0
        self.keys_pressed = []

        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player,
            self.collision_list,
        )

    def update_animation(self, delta_time: float = 1 / 60):
        """Обновление анимации"""
        if self.is_walking:
            self.texture_change_time += delta_time
            if self.texture_change_time >= self.texture_change_delay:
                self.texture_change_time = 0
                self.current_texture += 1
                if self.current_texture > len(self.walk_textures[0]):
                    self.current_texture = 1
                if self.keys_pressed[-1] == arcade.key.S:
                    n = 1
                elif self.keys_pressed[-1] == arcade.key.A:
                    n = 2
                elif self.keys_pressed[-1] == arcade.key.W:
                    n = 3
                elif self.keys_pressed[-1] == arcade.key.D:
                    n = 4
                self.player.texture = self.walk_textures[n - 1][self.current_texture - 1]
        else:
            self.player.texture = self.player_texture

    def on_draw(self) -> None:
        """Отрисовка игры."""
        self.clear()

        self.world_camera.use()
        self.floor_list.draw()
        self.player_list.draw()

        self.gui_camera.use()

    def on_update(self, _: float) -> None:
        """Действия при обновлении ."""
        self.player.change_x, self.player.change_y = self.change_x, self.change_y
        self.update_animation()

        DEAD_ZONE_W = int(self.width * 0.1)
        DEAD_ZONE_H = int(self.height * 0.1)
        cam_x, cam_y = self.world_camera.position
        dz_left = cam_x - DEAD_ZONE_W // 2
        dz_right = cam_x + DEAD_ZONE_W // 2
        dz_bottom = cam_y - DEAD_ZONE_H // 2
        dz_top = cam_y + DEAD_ZONE_H // 2

        px, py = self.player.center_x, self.player.center_y
        target_x, target_y = cam_x, cam_y

        if px < dz_left:
            target_x = px + DEAD_ZONE_W // 2
        elif px > dz_right:
            target_x = px - DEAD_ZONE_W // 2
        if py < dz_bottom:
            target_y = py + DEAD_ZONE_H // 2
        elif py > dz_top:
            target_y = py - DEAD_ZONE_H // 2

        # Не показываем «пустоту» за краями карты
        half_w = self.world_camera.viewport_width / 2
        half_h = self.world_camera.viewport_height / 2
        target_x = max(half_w, min(self.world_width - half_w, target_x))
        target_y = max(half_h, min(self.world_height - half_h, target_y))

        # Плавно к цели, аналог arcade.math.lerp_2d, но руками
        smooth_x = (1 - self.camera_lerp) * cam_x + self.camera_lerp * target_x
        smooth_y = (1 - self.camera_lerp) * cam_y + self.camera_lerp * target_y
        self.cam_target = (smooth_x, smooth_y)

        self.world_camera.position = (self.cam_target[0], self.cam_target[1])
        self.physics_engine.update()

    def on_key_press(self, key: int, _: int) -> None:
        """Обработка нажатия кнопок клавиатуры."""
        match key:
            case arcade.key.W:
                self.change_y = self.speed
                self.is_walking = True
                self.keys_pressed.append(key)
            case arcade.key.S:
                self.change_y = -self.speed
                self.is_walking = True
                self.keys_pressed.append(key)
            case arcade.key.D:
                self.change_x = self.speed
                self.is_walking = True
                self.keys_pressed.append(key)
            case arcade.key.A:
                self.change_x = -self.speed
                self.is_walking = True
                self.keys_pressed.append(key)
        if key == arcade.key.ESCAPE:
            arcade.close_window()
            MenuGame(self.width, self.height, "Меню")

    def on_key_release(self, key: int, _: int) -> None:
        """Обработка отпускания кнопок клавиатуры."""
        if key in (arcade.key.A, arcade.key.D):
            self.change_x = 0
            self.keys_pressed.remove(key)
        elif key in (arcade.key.W, arcade.key.S):
            self.change_y = 0
            self.keys_pressed.remove(key)
        if not self.change_x and not self.change_y:
            self.is_walking = False
            self.keys_pressed = []


class StartGame(arcade.Window):
    """Начальное окно игры"""

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
        GridGame(self.width, self.height, self.title)
        arcade.run()


class MenuGame(arcade.Window):
    """Начальное окно игры"""

    def __init__(self, width: int, height: int, title: str) -> None:
        super().__init__(width, height, title)
        self.manager = UIManager()
        self.manager.enable()
        self.tile_scaling = 2
        self.title = title

        self.anchor_layout = UIAnchorLayout()
        self.box_layout = UIBoxLayout(vertical=True, space_between=10)

        self.setup_widgets()

        self.anchor_layout.add(self.box_layout)
        self.manager.add(self.anchor_layout)

        self.set_fullscreen(True)
        self.setup()

    def setup_widgets(self):
        texture_normal = arcade.load_texture("assets/contnorm.png")
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
        texture_normal2 = arcade.load_texture("assets/exitnorm.png")
        texture_hovered2 = arcade.load_texture("assets/exitpush.png")
        texture_pressed2 = arcade.load_texture("assets/click.png")
        texture_button2 = UITextureButton(
            texture=texture_normal2,
            texture_hovered=texture_hovered2,
            texture_pressed=texture_pressed2,
            scale=4.0,
        )
        texture_button2.on_click = self.exit
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

    def play(self, event) -> None:
        arcade.close_window()
        GridGame(self.width, self.height, self.title)
        arcade.run()

    def exit(self, event) -> None:
        arcade.close_window()
        StartGame(self.width, self.height, self.title)
        arcade.run()
