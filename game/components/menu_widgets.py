"""Виджеты меню.

Оболочка для удобного взаимодействия.
"""

from collections.abc import Callable

from arcade.gui import UIOnClickEvent, UITextureButton
from arcade.gui.widgets.layout import UIBoxLayout

from game.types import ButtonTexture


def setup_menu_widgets(
    *args: tuple[ButtonTexture, Callable[[UIOnClickEvent], None]],
    box_layout: UIBoxLayout,
) -> None:
    """Установка виджетов меню."""
    for b, on_click in args:
        texture_button = UITextureButton(
            texture=b.texture,
            texture_hovered=b.hover_texture,
            texture_pressed=b.click,
            scale=4.0,
        )
        texture_button.on_click = on_click
        box_layout.add(texture_button)
