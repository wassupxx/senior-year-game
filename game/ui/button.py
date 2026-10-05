"""
Класс Button — универсальная кнопка с 3 состояниями.
Умеет рисовать две строки: заголовок и подпись (например, стоимость).
"""

import pygame
from game.config import COLORS, PANEL_RADIUS


class Button:
    def __init__(self, rect, text, font,
                 subtitle="", subtitle_font=None,
                 subtitle_color=None,
                 color_normal=None,
                 color_hover=None,
                 color_disabled=None,
                 text_color=None):
        """
        :param rect: pygame.Rect — позиция и размер
        :param text: основная надпись
        :param font: шрифт для основной надписи
        :param subtitle: вторая строка (например, стоимость)
        :param subtitle_font: шрифт для второй строки
        :param subtitle_color: цвет второй строки
        """
        self.rect = rect
        self.text = text
        self.font = font
        self.subtitle = subtitle
        self.subtitle_font = subtitle_font or font
        self.subtitle_color = subtitle_color or COLORS["col5"]

        self.color_normal   = color_normal   or COLORS["col1"]
        self.color_hover    = color_hover    or COLORS["col1"]
        self.color_disabled = color_disabled or COLORS["col8"]
        self.text_color     = text_color     or COLORS["col6"]

        self.enabled = True
        self.hovered = False

    def set_enabled(self, enabled):
        self.enabled = enabled

    def update_hover(self, mouse_pos):
        self.hovered = self.enabled and self.rect.collidepoint(mouse_pos)

    def is_clicked(self, mouse_pos, mouse_click):
        return (
            self.enabled
            and mouse_click
            and self.rect.collidepoint(mouse_pos)
        )

    def draw(self, screen):
        # 1. Цвет
        if not self.enabled:
            color = self.color_disabled
        elif self.hovered:
            color = self.color_hover
        else:
            color = self.color_normal

        # 2. Прямоугольник
        pygame.draw.rect(screen, color, self.rect, border_radius=PANEL_RADIUS)

        # 3. Основная надпись — чуть выше центра
        main_surface = self.font.render(self.text, True, self.text_color)

        if self.subtitle:
            # Две строки: основная сверху, подпись снизу
            main_rect = main_surface.get_rect(
                center=(self.rect.centerx, self.rect.centery - 10)
            )
            sub_surface = self.subtitle_font.render(
                self.subtitle, True, self.subtitle_color
            )
            sub_rect = sub_surface.get_rect(
                center=(self.rect.centerx, self.rect.centery + 14)
            )
            screen.blit(main_surface, main_rect)
            screen.blit(sub_surface, sub_rect)
        else:
            # Одна строка — по центру
            main_rect = main_surface.get_rect(center=self.rect.center)
            screen.blit(main_surface, main_rect)