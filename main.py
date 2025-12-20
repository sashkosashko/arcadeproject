import arcade


class GridGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.player_texture = arcade.load_texture("assets/boy.png")
        self.change_x = 0
        self.change_y = 0
        self.speed = 5

    def setup(self):
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

        self.physics_engine = arcade.PhysicsEngineSimple(self.player, self.collision_list)

    def on_draw(self):
        self.clear()
        self.floor_list.draw()
        self.wall_list.draw()
        self.player_list.draw()

    def on_update(self, delta_time: float):
        self.player.change_x = self.change_x
        self.player.change_y = self.change_y

        self.physics_engine.update()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            self.change_y = self.speed
        elif key == arcade.key.DOWN:
            self.change_y = -self.speed
        elif key == arcade.key.RIGHT:
            self.change_x = self.speed
        elif key == arcade.key.LEFT:
            self.change_x = -self.speed

    def on_key_release(self, key, modifiers):
        if key in [arcade.key.LEFT, arcade.key.RIGHT]:
            self.change_x = 0
        if key in [arcade.key.UP, arcade.key.DOWN]:
            self.change_y = 0

def setup_game(width, height, title):
    game = GridGame(width, height, title)
    game.set_fullscreen(True)
    game.setup()
    return game

def main():
    width = arcade.get_display_size()[0]
    height = arcade.get_display_size()[1]
    title = "Игра"
    setup_game(width, height, title)
    arcade.run()

if __name__ == "__main__":
    main()

