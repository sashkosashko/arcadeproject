"""Кастомное дополнение для поддержки диалоговых окон."""

import arcade

WIDTH, HEIGHT = arcade.get_display_size()


class Dialog:
    """Кастомное дополнение для поддержки диалоговых окон."""

    def __init__(
        self,
        title: str,
        text: str,
        sound: arcade.sound.Sound,
        texture: arcade.texture.texture.Texture,
    ) -> None:
        """Инициализация параметров и воспроизведение аудио."""
        self.title = title
        self.text = text
        self.texture = texture

        arcade.play_sound(sound)

    def draw(self) -> None:
        """Отображение далогового окна."""
        arcade.draw_rect_filled(
            arcade.rect.XYWH(
                WIDTH // 2,
                HEIGHT // 2 - HEIGHT * .3,
                WIDTH * .85,
                HEIGHT * .3,
            ),
            arcade.color.BLACK,
        )
        arcade.draw_texture_rect(
            self.texture,
            arcade.rect.XYWH(
                WIDTH * .85,
                HEIGHT // 2 - HEIGHT * .3,
                HEIGHT * .3,
                HEIGHT * .3,
            ),
        )
        arcade.Text(
            self.title,
            int(WIDTH * .1),
            HEIGHT // 2 - HEIGHT * .24,
            arcade.color.WHITE,
            45,
            width=int(WIDTH * .35),
        ).draw()
        arcade.Text(
            self.text,
            int(WIDTH * .1),
            HEIGHT // 2 - HEIGHT * .3,
            arcade.color.WHITE,
            20,
            width=int(WIDTH * .35),
        ).draw()
