import arcade
from arcade.gui import UIManager
from arcade.gui.widgets.layout import UIAnchorLayout, UIBoxLayout

from game import config
from game.components.menu_widgets import setup_menu_widgets
from game.config import textures
from game.screens import change_screen


class GridScreen(arcade.Window):
    """Класс игры."""

    def __init__(self, level: int) -> None:
        """Инициализация класса игры."""
        super().__init__(config.WIDTH, config.HEIGHT, config.TITLE)
        self.level = level

        self.dialog = None
        self.is_menu_widgets_open = False
        self.change_x = self.change_y = 0

        self.world_camera = self.gui_camera = arcade.camera.Camera2D()

        # TODO(@iamlostshe): Сделать класс игрока
        # Эти поля можно представить в виде отдельного класса игрока
        self.player_texture = textures.MOVES_SPRITES_IDLE_PLAYER
        self.is_can_go = True
        self.speed, self.tile_scaling, self.camera_lerp = (
            config.SPEED,
            config.TILE_SCALING,
            config.CAMERA_LERP,
        )

        self.box_layout = UIBoxLayout(vertical=True, space_between=10)

        self.anchor_layout = UIAnchorLayout()
        self.anchor_layout.add(self.box_layout)

        self.manager = UIManager()
        self.manager.enable()
        self.manager.add(self.anchor_layout)

        self.set_fullscreen(True)
        self.setup()

    def setup(self) -> None:
        """Запуск игры."""
        self.player_list: arcade.SpriteList = arcade.SpriteList()
        self.tile_map = arcade.load_tilemap(
            config.LEVELS_LIST[self.level - 1],
            scaling=self.tile_scaling,
        )
        self.floor_list = self.tile_map.sprite_lists.get("floor")
        self.collision_list = self.tile_map.sprite_lists.get("collision")

        self.world_width = int(
            self.tile_map.width * self.tile_map.tile_width * self.tile_scaling,
        )
        self.world_height = int(
            self.tile_map.height * self.tile_map.tile_height * self.tile_scaling,
        )

        self.player = arcade.Sprite(self.player_texture, scale=2)
        self.player.position = (self.width // 8, self.height // 8)
        self.player_list.append(self.player)

        self.walk_textures = textures.WALK_TEXTURES

        self.texture_change_time = 0.0
        self.texture_change_delay = 0.1  # секунд на кадр
        self.is_walking = False
        self.current_texture = 0
        self.keys_pressed: list[int] = []

        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player,
            self.collision_list,
        )

    def update_animation(self, delta_time: float = 1 / 60) -> None:
        """Обновление анимации."""
        if self.is_walking:
            self.texture_change_time += delta_time
            if self.texture_change_time >= self.texture_change_delay:
                self.texture_change_time = 0
                self.current_texture += 1
                if self.current_texture > len(self.walk_textures[0]):
                    self.current_texture = 1
                if not self.keys_pressed or self.keys_pressed not in config.KEYS:
                    return

                n = config.KEYS.index(self.keys_pressed[-1])
                self.player.texture = self.walk_textures[n][self.current_texture - 1]
        else:
            self.player.texture = self.player_texture

    def on_draw(self) -> None:
        """Отрисовка игры."""
        self.clear()

        self.world_camera.use()
        self.gui_camera.use()

        for i in (self.floor_list, self.player_list, self.manager, self.dialog):
            if i is not None:
                i.draw()

    def play(self) -> None:
        self.box_layout = UIBoxLayout(vertical=True, space_between=10)

        self.is_can_go = True
        self.is_menu_widgets_open = False

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

        self.world_camera.position = (smooth_x, smooth_y)
        self.physics_engine.update()

    def on_key_press(self, key: int, _: int) -> None:
        """Обработка нажатия кнопок клавиатуры."""
        self.keys_pressed.append(key)

        if key == arcade.key.ESCAPE:
            if self.is_can_go:
                # TODO(@iamlostshe): Доработать кнопки
                # print - просто заглушка
                setup_menu_widgets(
                    (textures.button.continue_, lambda _: self.play()),
                    (textures.button.settings, print),
                    (textures.button.exit_, lambda _: change_screen("menu")),
                    box_layout=self.box_layout,
                )
                self.is_can_go = False
                self.is_menu_widgets_open = True
                return
            self.play()
            return

        if key == arcade.key.ENTER:
            self.dialog = None
            return

        if not self.is_can_go:
            return

        if key in config.KEYS:
            self.is_walking = True

        match key:
            case arcade.key.S:
                self.change_y = -self.speed
            case arcade.key.A:
                self.change_x = -self.speed
            case arcade.key.W:
                self.change_y = self.speed
            case arcade.key.D:
                self.change_x = self.speed

    def on_key_release(self, key: int, _: int) -> None:
        """Обработка отпускания кнопок клавиатуры."""
        if key in self.keys_pressed:
            self.keys_pressed.remove(key)

        if key in (arcade.key.A, arcade.key.D):
            self.change_x = 0

        elif key in (arcade.key.W, arcade.key.S):
            self.change_y = 0

        if not self.change_x and not self.change_y:
            self.is_walking = False
            self.keys_pressed = []
