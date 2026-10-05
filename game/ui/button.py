"""
Класс Button — универсальная кнопка с 3 состояниями.
Умеет рисовать две строки: заголовок и подпись (например, стоимость).
"""

import pygame
from game.config import COLORS, PANEL_RADIUS
from game.config import wrap_text


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
        # 1. Цвет кнопки
        if not self.enabled:
            color = self.color_disabled
        elif self.hovered:
            color = self.color_hover
        else:
            color = self.color_normal

        # 2. Прямоугольник кнопки
        pygame.draw.rect(screen, color, self.rect, border_radius=PANEL_RADIUS)

        # 3. Режем название на строки
        from game.config import wrap_text
        max_w = self.rect.width - 20      # отступы по 10 с каждой стороны
        lines = wrap_text(self.text, self.font, max_w)

        # 4. Рисуем название (каждая строка отдельно)
        line_h = self.font.get_height()

        if self.subtitle:
            # Есть подпись — название сверху, подпись снизу
            total_h = len(lines) * line_h + 20
            y = self.rect.centery - total_h // 2 + 5

            for line in lines:
                surf = self.font.render(line, True, self.text_color)
                rect = surf.get_rect(center=(self.rect.centerx, y))
                screen.blit(surf, rect)
                y += line_h

            # Подпись
            sub_surface = self.subtitle_font.render(
                self.subtitle, True, self.subtitle_color
            )
            sub_rect = sub_surface.get_rect(
                center=(self.rect.centerx, y + 4)
            )
            screen.blit(sub_surface, sub_rect)
        else:
            # Без подписи — только название
            total_h = len(lines) * line_h
            y = self.rect.centery - total_h // 2

            for line in lines:
                surf = self.font.render(line, True, self.text_color)
                rect = surf.get_rect(center=(self.rect.centerx, y + line_h // 2))
                screen.blit(surf, rect)
                y += line_h