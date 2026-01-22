"""Кастомное дополнение для поддержки диалоговых окон.

Пример использования:

``` python
Dialog(
    "???",
    "Ахх.. Где я?. Голова раскалывается.. Как я тут оказалась?.",
    sounds.BEGINNING,
    textures.GIRL,
)
```
"""

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
                HEIGHT // 2 - HEIGHT * 0.3,
                WIDTH * 0.85,
                HEIGHT * 0.3,
            ),
            arcade.color.BLACK,
        )
        arcade.draw_texture_rect(
            self.texture,
            arcade.rect.XYWH(
                WIDTH * 0.85,
                HEIGHT // 2 - HEIGHT * 0.3,
                HEIGHT * 0.3,
                HEIGHT * 0.3,
            ),
        )
        arcade.Text(
            self.title,
            int(WIDTH * 0.1),
            HEIGHT // 2 - HEIGHT * 0.24,
            arcade.color.WHITE,
            45,
            width=int(WIDTH * 0.35),
        ).draw()
        arcade.Text(
            self.text,
            int(WIDTH * 0.1),
            HEIGHT // 2 - HEIGHT * 0.3,
            arcade.color.WHITE,
            20,
            width=int(WIDTH * 0.35),
        ).draw()
