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

        self.set_fullscreen(True)
        self.setup()

    def setup(self) -> None:
        """Запуск игры."""
        self.player_list = arcade.SpriteList()
        map_name = "assets/mainmap.tmx"
        tile_map = arcade.load_tilemap(map_name, scaling=2)
        self.wall_list = tile_map.sprite_lists["walls"]
        self.floor_list = tile_map.sprite_lists["floor"]
        self.collision_list = tile_map.sprite_lists["collision"]

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
        position = (
            self.player.center_x,
            self.player.center_y)
        self.world_camera.position = arcade.math.lerp_2d(
            self.world_camera.position, position, 0.15)
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
