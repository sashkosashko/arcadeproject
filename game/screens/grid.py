import arcade
from arcade.gui import (
    UIManager,
    UITextureButton,
)
from arcade.gui.widgets.layout import UIAnchorLayout, UIBoxLayout

from game.config import textures, sounds

# Масштаб игры
TILE_SCALING = 4

# Скорость игрока
SPEED = 5

# Что-то на умном
CAMERA_LERP = 0.15


class GridScreen(arcade.Window):
    """Класс игры."""

    def __init__(self, width: int, height: int, title: str) -> None:
        """Инициализация класса игры."""
        super().__init__(width, height, title)
        self.player_texture = textures.MOVES_SPRITES_IDLE_PLAYER

        self.world_camera = arcade.camera.Camera2D()
        self.gui_camera = arcade.camera.Camera2D()

        self.change_x = self.change_y = 0
        self.speed, self.tile_scaling, self.camera_lerp = (
            SPEED,
            TILE_SCALING,
            CAMERA_LERP,
        )

        self.box_layout = UIBoxLayout(vertical=True, space_between=10)

        self.anchor_layout = UIAnchorLayout()
        self.anchor_layout.add(self.box_layout)

        self.manager = UIManager()
        self.manager.enable()
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
        """Запуск игры."""
        sounds.BEGINNING.play()

        self.player_list = arcade.SpriteList()
        self.tile_map = arcade.load_tilemap(
            "assets/my_map.tmx",
            scaling=self.tile_scaling,
        )
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

        # Загрузка текстур анимаций персонажа
        self.walk_textures = textures.WALK_TEXTURES

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
        """Обновление анимации."""
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
                self.player.texture = self.walk_textures[n - 1][
                    self.current_texture - 1
                ]
        else:
            self.player.texture = self.player_texture

    def on_draw(self) -> None:
        """Отрисовка игры."""
        self.clear()

        self.world_camera.use()
        self.floor_list.draw()
        self.player_list.draw()
        self.manager.draw()

        self.gui_camera.use()

    def play(self, event) -> None:
        self.manager.clear()
        self.flag = True

    def exit(self, event) -> None:
        arcade.close_window()

    def on_update(self, _: float) -> None:
        """Действия при обновлении ."""
        self.player.change_x, self.player.change_y = self.change_x, self.change_y
        self.update_animation()

        dead_zone_w = int(self.width * 0.1)
        dead_zone_h = int(self.height * 0.1)
        cam_x, cam_y = self.world_camera.position
        dz_left = cam_x - dead_zone_w // 2
        dz_right = cam_x + dead_zone_w // 2
        dz_bottom = cam_y - dead_zone_h // 2
        dz_top = cam_y + dead_zone_h // 2

        px, py = self.player.center_x, self.player.center_y
        target_x, target_y = cam_x, cam_y

        if px < dz_left:
            target_x = px + dead_zone_w // 2
        elif px > dz_right:
            target_x = px - dead_zone_w // 2
        if py < dz_bottom:
            target_y = py + dead_zone_h // 2
        elif py > dz_top:
            target_y = py - dead_zone_h // 2

        # Не показываем "пустоту" за краями карты
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
        self.is_walking = True

        match key:
            case arcade.key.W:
                self.change_y = self.speed
                self.keys_pressed.append(key)
            case arcade.key.S:
                self.change_y = -self.speed
                self.keys_pressed.append(key)
            case arcade.key.D:
                self.change_x = self.speed
                self.keys_pressed.append(key)
            case arcade.key.A:
                self.change_x = -self.speed
                self.keys_pressed.append(key)
                self.is_walking = False
            case arcade.key.ESCAPE:
                self.setup_menu_widgets()

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
