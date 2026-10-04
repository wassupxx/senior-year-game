"""
Класс Button — кнопка с тремя состояниями: обычная, hover, disabled.

Используется для:
    - 5 кнопок действий внизу экрана
    - кнопки «Продолжить» в модалке события
    - кнопки «Новая игра» на экране победы/поражения
"""

import pygame

from game.config import COLORS, PANEL_RADIUS


class Button:
    """Прямоугольная кнопка с текстом и тремя состояниями."""

    def __init__(self, rect, text, font,
                 color_normal=None,
                 color_hover=None,
                 color_disabled=None,
                 text_color=None):
        """
        :param rect: pygame.Rect — позиция и размер
        :param text: текст на кнопке
        :param font: pygame.font.Font — шрифт для текста
        :param color_normal: цвет в обычном состоянии
        :param color_hover: цвет при наведении
        :param color_disabled: цвет, если кнопка недоступна
        :param text_color: цвет текста
        """
        self.rect = rect
        self.text = text
        self.font = font

        # Цвета — по умолчанию из палитры дизайнера
        self.color_normal   = color_normal   or COLORS["col1"]
        self.color_hover    = color_hover    or COLORS["col1"]
        self.color_disabled = color_disabled or COLORS["col8"]
        self.text_color     = text_color     or COLORS["col6"]

        self.enabled = True        # доступна ли кнопка
        self.hovered = False       # наведена ли мышь

    # ------------------------------------------------------------
    # СОСТОЯНИЕ
    # ------------------------------------------------------------
    def set_enabled(self, enabled):
        """Включает/выключает кнопку (серое состояние, клик не работает)."""
        self.enabled = enabled

    def is_clicked(self, mouse_pos, mouse_click):
        """
        Возвращает True, если кнопка нажата.
        :param mouse_pos: позиция мыши (x, y)
        :param mouse_click: True, если была нажата левая кнопка
        """
        return (
            self.enabled
            and mouse_click
            and self.rect.collidepoint(mouse_pos)
        )

    def update_hover(self, mouse_pos):
        """Обновляет флаг наведения. Вызывать каждый кадр."""
        self.hovered = self.enabled and self.rect.collidepoint(mouse_pos)

    # ------------------------------------------------------------
    # ОТРИСОВКА
    # ------------------------------------------------------------
    def draw(self, screen):
        """Рисует кнопку на экране."""
        # 1. Выбираем цвет
        if not self.enabled:
            color = self.color_disabled
        elif self.hovered:
            color = self.color_hover
        else:
            color = self.color_normal

        # 2. Прямоугольник
        pygame.draw.rect(screen, color, self.rect, border_radius=PANEL_RADIUS)

        # 3. Текст по центру
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)