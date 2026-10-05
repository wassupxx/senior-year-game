"""
Модальное окно события.

Показывается после roll_event(). Закрывает весь экран затемнением,
рисует название события, эффекты и кнопку «Продолжить».
"""

import pygame

from game.config import (
    WIDTH, HEIGHT, COLORS, PANEL_RADIUS,
    TEXT_EVENT_TITLE, TEXT_CONTINUE,
    IMG_WIN, IMG_LOSS,
    format_effects,
    format_cost
)
from game.ui.button import Button


class EventModal:
    """Модальное окно с событием и кнопкой «Продолжить»."""

    def __init__(self, fonts, images):
        """
        :param fonts: словарь шрифтов из main.load_fonts()
        """
        self.fonts = fonts
        self.images = images

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
        """Рисует модалку: картинку события, заголовок, эффекты, кнопку."""
        # 1. Затемнение
        screen.blit(self.overlay, (0, 0))

        # 2. Прямоугольник модалки
        pygame.draw.rect(
            screen, COLORS["col2"], self.rect,
            border_radius=PANEL_RADIUS,
        )

        # 3. Картинка события — если есть
        event_img = self.images.get(f"event_{event.id}")
        if event_img:
            # Масштабируем под ширину модалки (сверху половина окна)
            img_h = 220
            img_w = self.rect.width
            img_scaled = pygame.transform.scale(event_img, (img_w, img_h))

            # Рисуем поверх верхней части модалки
            img_rect = img_scaled.get_rect(topleft=(self.rect.x, self.rect.y))
            screen.blit(img_scaled, img_rect)

            # Обрезаем скруглением — перерисовываем рамку сверху
            pygame.draw.rect(
                screen, COLORS["col2"],
                (self.rect.x, self.rect.y + img_h, self.rect.width, self.rect.height - img_h),
                border_radius=PANEL_RADIUS,
            )

        # 4. Заголовок
        title = self.fonts["txt4"].render(event.title, True, COLORS["col5"])
        title_rect = title.get_rect(center=(self.rect.centerx, self.rect.y + 250))
        screen.blit(title, title_rect)

        # 5. Эффекты
        effects_text = format_effects(effects)
        info = self.fonts["txt6"].render(effects_text, True, COLORS["col5"])
        info_rect = info.get_rect(center=(self.rect.centerx, self.rect.y + 300))
        screen.blit(info, info_rect)

        # 6. Кнопка «Продолжить»
        self.continue_button.draw(screen)

    def update_hover(self, mouse_pos):
        """Обновляет hover кнопки «Продолжить»."""
        self.continue_button.update_hover(mouse_pos)

    def is_continue_clicked(self, mouse_pos, mouse_click):
        """Была ли нажата кнопка «Продолжить»."""
        return self.continue_button.is_clicked(mouse_pos, mouse_click)


class GameModal:
    """Модалка конца игры: победа или поражение."""

    def __init__(self, fonts):
        self.fonts = fonts

        # Затемнение
        self.overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 180))

        # Прямоугольник модалки — по центру
        self.rect = pygame.Rect(
            WIDTH // 2 - 350, HEIGHT // 2 - 250, 700, 500
        )

        # Картинки победы и поражения
        try:
            self.img_win = pygame.image.load(IMG_WIN).convert_alpha()
        except (FileNotFoundError, pygame.error):
            self.img_win = None
        try:
            self.img_loss = pygame.image.load(IMG_LOSS).convert_alpha()
        except (FileNotFoundError, pygame.error):
            self.img_loss = None

        # Кнопка «Новая игра»
        btn_rect = pygame.Rect(
            self.rect.centerx - 100,
            self.rect.bottom - 70,
            200, 50,
        )
        self.new_game_button = Button(
            rect=btn_rect,
            text="Новая игра",
            font=fonts["txt1"],
            color_normal=COLORS["col1"],
            color_hover=COLORS["col2"],
            text_color=COLORS["col6"],
        )

    def draw(self, screen, winner, loser):
        """Рисует модалку. winner / loser — объекты Player или None."""
        screen.blit(self.overlay, (0, 0))

        # Фон модалки
        pygame.draw.rect(
            screen, COLORS["col2"], self.rect,
            border_radius=PANEL_RADIUS,
        )

        # Картинка — по ситуации
        img = None
        if winner:
            img = self.img_win
        elif loser:
            img = self.img_loss

        if img:
            img_h = 300
            img_w = self.rect.width
            img_scaled = pygame.transform.scale(img, (img_w, img_h))
            screen.blit(img_scaled, (self.rect.x, self.rect.y))

        # Текст
        if winner:
            text = f"{winner.name} победил!"
        elif loser:
            text = f"{loser.name} выбыл!"
        else:
            text = "Игра окончена"

        msg = self.fonts["txt4"].render(text, True, COLORS["col5"])
        msg_rect = msg.get_rect(center=(self.rect.centerx, self.rect.y + 370))
        screen.blit(msg, msg_rect)

        # Кнопка «Новая игра»
        self.new_game_button.draw(screen)

    def update_hover(self, mouse_pos):
        self.new_game_button.update_hover(mouse_pos)

    def is_new_game_clicked(self, mouse_pos, mouse_click):
        return self.new_game_button.is_clicked(mouse_pos, mouse_click)


class EliminationModal:
    """Модалка выбывания одного игрока. Игра продолжается."""

    def __init__(self, fonts):
        self.fonts = fonts

        # Затемнение
        self.overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 160))

        # Окно
        self.rect = pygame.Rect(
            WIDTH // 2 - 300, HEIGHT // 2 - 200, 600, 400
        )

        # Картинка выбывания
        try:
            self.img = pygame.image.load("game/assets/images/Loss.png").convert_alpha()
        except (FileNotFoundError, pygame.error):
            self.img = None

        # Кнопка
        btn_rect = pygame.Rect(
            self.rect.centerx - 100,
            self.rect.bottom - 70,
            200, 50,
        )
        self.continue_button = Button(
            rect=btn_rect,
            text="ПРОДОЛЖИТЬ",
            font=fonts["txt1"],
            color_normal=COLORS["col1"],
            color_hover=COLORS["col2"],
            text_color=COLORS["col6"],
        )

    def draw(self, screen, player):
        """Рисует модалку с именем выбывшего игрока."""
        screen.blit(self.overlay, (0, 0))

        # Окно
        pygame.draw.rect(
            screen, COLORS["col2"], self.rect,
            border_radius=PANEL_RADIUS,
        )

        # Картинка сверху
        if self.img:
            img_h = 220
            img_w = self.rect.width
            img_scaled = pygame.transform.scale(self.img, (img_w, img_h))
            screen.blit(img_scaled, (self.rect.x, self.rect.y))

        # Текст
        text = f"{player.name} выбыл!"
        msg = self.fonts["txt4"].render(text, True, COLORS["col5"])
        msg_rect = msg.get_rect(center=(self.rect.centerx, self.rect.y + 290))
        screen.blit(msg, msg_rect)

        # Кнопка
        self.continue_button.draw(screen)

    def update_hover(self, mouse_pos):
        self.continue_button.update_hover(mouse_pos)

    def is_continue_clicked(self, mouse_pos, mouse_click):
        return self.continue_button.is_clicked(mouse_pos, mouse_click)
