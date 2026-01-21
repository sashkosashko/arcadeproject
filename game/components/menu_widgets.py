"""Виджеты меню.

Оболочка для удобного взаимодействия.
"""

from arcade.gui import UITextureButton
from arcade.gui.widgets.layout import UIBoxLayout

from game.config import textures


def setup_menu_widgets(widgets: tuple, box_layout: UIBoxLayout) -> None:
    """Установка виджетов меню."""
    for texture, texture_hovered, on_click in widgets:
        texture_button = UITextureButton(
            texture=texture,
            texture_hovered=texture_hovered,
            texture_pressed=textures.CLICK,
            scale=4.0,
        )
        texture_button.on_click = on_click
        box_layout.add(texture_button)
