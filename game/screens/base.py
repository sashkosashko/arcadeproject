import random
from pathlib import Path

import arcade
from arcade.gui import UIManager
from arcade.gui.widgets.layout import UIAnchorLayout, UIBoxLayout
from arcade.particles import EmitMaintainCount, Emitter, FadeParticle

from game import config
from game.change_screen import change_screen
from game.components import Dialog, setup_menu_widgets
from game.config import textures
from game.types import Player


class BaseScreen(arcade.Window):
    """Класс игры."""

    def __init__(
        self,
        spawn_position: tuple[float, float],
        tile_map: Path,
    ) -> None:
        """Инициализация класса игры."""
        # Параметры, передаваемые в __init__
        super().__init__(config.WIDTH, config.HEIGHT, config.TITLE)

        # Инициализация переменных
        self.dialog: Dialog | None = None
        self.is_menu_widgets_open = self.is_walking = False
        self.change_x = self.change_y = self.current_texture = 0
        self.texture_change_time = 0.0
        self.texture_change_delay = 0.1  # секунд на кадр
        self.keys_pressed: list[int] = []

        # Настройка камер / окон
        self.set_fullscreen(True)
        self.world_camera = self.gui_camera = arcade.camera.Camera2D()

        # Инициализация игрока
        self.player_texture = textures.MOVES_SPRITES_IDLE_PLAYER
        self.player = Player(self.player_texture, 2, config.SPEED, spawn_position)

        self.player_list: arcade.SpriteList = arcade.SpriteList()
        self.player_list.append(self.player)

        # Частицы для следа
        self.emitters = []
        self.SPARK_TEX = [
            arcade.make_soft_circle_texture(16, arcade.color.PASTEL_YELLOW),
            arcade.make_soft_circle_texture(16, arcade.color.PEACH),
            arcade.make_soft_circle_texture(16, arcade.color.BABY_BLUE),
            arcade.make_soft_circle_texture(16, arcade.color.ELECTRIC_CRIMSON),
        ]

        # Создаем след для игрока
        self.trail = self.make_trail(self.player)
        self.emitters.append(self.trail)

        # Меню
        self.box_layout = UIBoxLayout(vertical=True, space_between=10)
        self.anchor_layout = UIAnchorLayout()
        self.anchor_layout.add(self.box_layout)
        self.manager = UIManager()
        self.manager.enable()
        self.manager.add(self.anchor_layout)

        # Загрузка карты и мира
        self.tile_map = arcade.load_tilemap(
            tile_map,
            scaling=config.TILE_SCALING,
        )
        self.floor_list, self.collision_list = (
            self.tile_map.sprite_lists.get("floor"),
            self.tile_map.sprite_lists.get("collision"),
        )
        self.world_width, self.world_height = (
            int(self.tile_map.width * self.tile_map.tile_width * config.TILE_SCALING),
            int(self.tile_map.height * self.tile_map.tile_height * config.TILE_SCALING),
        )

        # Настройка физики
        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player,
            self.collision_list,
        )

    def make_trail(self, attached_sprite, maintain: int = 30):
        """Создает эмиттер для следа за игроком."""
        return Emitter(
            center_xy=(attached_sprite.center_x, attached_sprite.center_y),
            emit_controller=EmitMaintainCount(maintain),
            particle_factory=lambda _: FadeParticle(
                filename_or_texture=random.choice(self.SPARK_TEX),
                change_xy=arcade.math.rand_in_circle((0.0, 0.0), 1.6),
                lifetime=random.uniform(0.3, 0.5),
                start_alpha=220,
                end_alpha=0,
                scale=random.uniform(0.2, 0.35),
            ),
        )

    def check_change_level(self) -> None:
        """Проверка события переключения между уровнями."""

    def update_animation(self, delta_time: float = 1 / 60) -> None:
        """Обновление анимации."""
        if self.is_walking:
            self.texture_change_time += delta_time
            if self.texture_change_time >= self.texture_change_delay:
                self.texture_change_time = 0
                self.current_texture += 1
                if self.current_texture > len(textures.WALK_TEXTURES[0]):
                    self.current_texture = 1
                if not self.keys_pressed or self.keys_pressed[-1] not in config.KEYS:
                    return

                n = config.KEYS.index(self.keys_pressed[-1]) // 3
                self.player.texture = textures.WALK_TEXTURES[n][
                    self.current_texture - 1
                ]
        else:
            self.player.texture = self.player_texture

    def on_draw(self) -> None:
        """Отрисовка игры."""
        self.clear()

        self.world_camera.use()
        self.gui_camera.use()

        for i in (self.floor_list, self.dialog, self.player_list, self.manager):
            if i is not None:
                i.draw()

        # Отрисовка частиц
        for e in self.emitters:
            e.draw()

    def play(self) -> None:
        self.box_layout = UIBoxLayout(vertical=True, space_between=10)

        self.player.can_go = True
        self.is_menu_widgets_open = False

    def on_update(self, delta_time: float) -> None:
        """Действия при обновлении."""
        self.player.change_x, self.player.change_y = self.change_x, self.change_y
        self.update_animation(delta_time)

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
        smooth_x = (1 - config.CAMERA_LERP) * cam_x + config.CAMERA_LERP * target_x
        smooth_y = (1 - config.CAMERA_LERP) * cam_y + config.CAMERA_LERP * target_y

        # Обновление позиции частиц следа за игроком
        self.trail.center_x = self.player.center_x
        self.trail.center_y = self.player.center_y

        # Обновление частиц
        for e in self.emitters:
            e.update(delta_time)

        self.world_camera.position = (smooth_x, smooth_y)
        self.physics_engine.update()

        self.check_change_level()

    def on_key_press(self, key: int, _: int) -> None:
        """Обработка нажатия кнопок клавиатуры."""
        self.keys_pressed.append(key)

        if key == arcade.key.ESCAPE:
            if self.player.can_go:
                setup_menu_widgets(
                    (textures.button.continue_, lambda _: self.play()),
                    (textures.button.exit_, lambda _: change_screen("menu")),
                    box_layout=self.box_layout,
                )
                self.player.can_go = False
                self.is_menu_widgets_open = True
                return
            self.play()
            return

        if key == arcade.key.ENTER:
            self.dialog = None
            return

        if not self.player.can_go:
            return

        if key in config.KEYS:
            self.is_walking = True
            n = config.KEYS.index(key) // 3

            match n:
                case 0:
                    self.change_y = -self.player.speed
                case 1:
                    self.change_x = -self.player.speed
                case 2:
                    self.change_y = self.player.speed
                case 3:
                    self.change_x = self.player.speed

        print(
            self.player.center_x,
            self.player.center_y,
        )

    def on_key_release(self, key: int, _: int) -> None:
        """Обработка отпускания кнопок клавиатуры."""
        if key in self.keys_pressed:
            self.keys_pressed.remove(key)

        if key in config.KEYS:
            n = config.KEYS.index(key) // 3
            if n in (1, 3):
                self.change_x = 0

            elif n in (0, 2):
                self.change_y = 0

        if not self.change_x and not self.change_y:
            self.is_walking = False
            self.keys_pressed = []
