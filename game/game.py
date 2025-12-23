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
        self.floor_list.draw()
        self.wall_list.draw()
        self.player_list.draw()

    def on_update(self, _: float) -> None:
        """Действия при обновлении ."""
        self.player.change_x, self.player.change_y = self.change_x, self.change_y
        self.physics_engine.update()

    def on_key_press(self, key: int, _: int) -> None:
        """Обработка нажатия кнопок клавиатуры."""
        match key:
            case arcade.key.UP:
                self.change_y = self.speed
            case arcade.key.DOWN:
                self.change_y = -self.speed
            case arcade.key.RIGHT:
                self.change_x = self.speed
            case arcade.key.LEFT:
                self.change_x = -self.speed
            case arcade.key.ESCAPE:
                arcade.close_window()

    def on_key_release(self, key: int, _: int) -> None:
        """Обработка отпускания кнопок клавиатуры."""
        if key in (arcade.key.LEFT, arcade.key.RIGHT):
            self.change_x = 0
        elif key in (arcade.key.UP, arcade.key.DOWN):
            self.change_y = 0
