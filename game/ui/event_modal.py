"""
Модальное окно события.

Показывается после roll_event(). Закрывает весь экран затемнением,
рисует название события, эффекты и кнопку «Продолжить».
"""

import pygame

from game.config import (
    WIDTH, HEIGHT, COLORS, PANEL_RADIUS,
    TEXT_EVENT_TITLE, TEXT_CONTINUE,
)
from game.ui.button import Button


class EventModal:
    """Модальное окно с событием и кнопкой «Продолжить»."""

    def __init__(self, fonts):
        """
        :param fonts: словарь шрифтов из main.load_fonts()
        """
        self.fonts = fonts

        # Затемнение фона
        self.overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 160))

        # Окно
        self.rect = pygame.Rect(
            WIDTH // 2 - 300, HEIGHT // 2 - 200, 600, 400
        )

        # Кнопка «Продолжить»
        btn_rect = pygame.Rect(
            self.rect.centerx - 100,
            self.rect.bottom - 70,
            200, 50,
        )
        self.continue_button = Button(
            rect=btn_rect,
            text=TEXT_CONTINUE,
            font=fonts["txt1"],
            color_normal=COLORS["col1"],
            color_hover=COLORS["col2"],
            text_color=COLORS["col5"],
        )

    def draw(self, screen, event, effects):
        """Рисует модалку с переданным событием."""
        # 1. Затемнение
        screen.blit(self.overlay, (0, 0))

        # 2. Окно
        pygame.draw.rect(
            screen, COLORS["col2"], self.rect,
            border_radius=PANEL_RADIUS,
        )

        # 3. Заголовок
        title = self.fonts["txt4"].render(
            event.title, True, COLORS["col5"],
        )
        title_rect = title.get_rect(center=(self.rect.centerx, self.rect.top + 60))
        screen.blit(title, title_rect)

        # 4. Описание эффектов (пока в сыром виде — потом сделаем красиво)
        effects_text = ", ".join(
            f"{k}: {v:+d}" for k, v in event.effects_1.items()
        )
        info = self.fonts["txt6"].render(
            effects_text, True, COLORS["col5"],
        )
        info_rect = info.get_rect(center=(self.rect.centerx, self.rect.top + 130))
        screen.blit(info, info_rect)

        # 5. Кнопка «Продолжить»
        self.continue_button.draw(screen)

    def update_hover(self, mouse_pos):
        """Обновляет hover кнопки «Продолжить»."""
        self.continue_button.update_hover(mouse_pos)

    def is_continue_clicked(self, mouse_pos, mouse_click):
        """Была ли нажата кнопка «Продолжить»."""
        return self.continue_button.is_clicked(mouse_pos, mouse_click)