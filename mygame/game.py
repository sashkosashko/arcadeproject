"""Основная механика игры."""

import arcade


class GridGame(arcade.Window):
    """Класс игры."""

    def __init__(self, width: int, height: int, title: str) -> None:
        """Инициализация класса игры."""
        super().__init__(width, height, title)
        self.player_texture = arcade.load_texture("assets/boy.png")
        self.change_x = 0
        self.change_y = 0
        self.speed = 5
        self.world_camera = arcade.camera.Camera2D()
        self.gui_camera = arcade.camera.Camera2D()
        self.tile_scaling = 2
        self.camera_lerp = 0.15

        self.set_fullscreen(True)
        self.setup()

    def setup(self) -> None:
        """Запуск игры."""
        self.player_list = arcade.SpriteList()
        map_name = "assets/mainmap.tmx"
        self.tile_map = arcade.load_tilemap(map_name, scaling=self.tile_scaling)
        self.wall_list = self.tile_map.sprite_lists["walls"]
        self.floor_list = self.tile_map.sprite_lists["floor"]
        self.collision_list = self.tile_map.sprite_lists["collision"]

        self.world_width = int(
            self.tile_map.width * self.tile_map.tile_width * self.tile_scaling)
        self.world_height = int(
            self.tile_map.height * self.tile_map.tile_height * self.tile_scaling)

        self.player = arcade.Sprite(self.player_texture, scale=0.2)
        x = self.width // 2
        y = self.height // 2
        self.player.position = (x, y)
        self.player_list.append(self.player)

        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player,
            self.collision_list,
        )

    def on_draw(self) -> None:
        """Отрисовка игры."""
        self.clear()

        self.world_camera.use()
        self.wall_list.draw()
        self.floor_list.draw()
        self.player_list.draw()

        self.gui_camera.use()

    def on_update(self, _: float) -> None:
        """Действия при обновлении ."""
        self.player.change_x, self.player.change_y = self.change_x, self.change_y

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
            case arcade.key.S:
                self.change_y = -self.speed
            case arcade.key.D:
                self.change_x = self.speed
            case arcade.key.A:
                self.change_x = -self.speed
            case arcade.key.ESCAPE:
                arcade.close_window()

    def on_key_release(self, key: int, _: int) -> None:
        """Обработка отпускания кнопок клавиатуры."""
        if key in (arcade.key.A, arcade.key.D):
            self.change_x = 0
        elif key in (arcade.key.W, arcade.key.S):
            self.change_y = 0
