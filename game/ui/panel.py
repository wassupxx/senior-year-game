"""
Отрисовка панелей игры:
    - HUD (верхняя панель с именем игрока и номером хода)
    - Панель ресурсов (иконки + числа + стабильность)
    - Лог событий (слева)
    - Карточка события (справа)
"""

import pygame

from game.config import (
    WIDTH, COLORS, PANEL_RADIUS,
    TEXT_LOG_TITLE, TEXT_EVENT_TITLE,
)
from game.config import wrap_text


def draw_panel(screen, rect, color, radius=PANEL_RADIUS):
    """Рисует скруглённый прямоугольник-панель."""
    pygame.draw.rect(screen, color, rect, border_radius=radius)


# ============================================================
# HUD — верхняя панель
# ============================================================
def draw_hud(screen, fonts, gs):
    """Верхняя панель: чей ход, номер хода. Цвет = цвет игрока."""
    panel_rect = pygame.Rect(0, 0, WIDTH, 60)
    draw_panel(screen, panel_rect, gs.current_player.color)

    text = fonts["txt1"].render(
        f"Ход: {gs.current_player.name}   |   Ход №{gs.turn_number}",
        True, COLORS["col6"],
    )
    screen.blit(text, (20, 15))


# ============================================================
# Панель ресурсов
# ============================================================
def draw_resources(screen, fonts, images, gs):
    """5 ресурсов в ряд: [иконка] название число."""
    panel_rect = pygame.Rect(0, 60, WIDTH, 80)
    draw_panel(screen, panel_rect, COLORS["col1"])

    p = gs.current_player
    resources = [
        ("stress",   p.stress,   "СТРЕСС:"),
        ("money",    p.money,    "ДЕНЬГИ:"),
        ("friends",  p.friends,  "ДРУЗЬЯ:"),
        ("homework", p.homework, "ДОМАШКА:"),
        ("bullying", p.bullying, "БУЛЛИНГ:"),
    ]

    x = 40
    icon_size = 32
    for key, value, label in resources:
        # 1. Иконка
        icon = images.get(f"icon_{key}")
        if icon:
            icon_scaled = pygame.transform.scale(icon, (icon_size, icon_size))
            screen.blit(icon_scaled, (x, 78))
            x += icon_size + 8

        # 2. Подпись
        label_surface = fonts["txt5"].render(label, True, COLORS["col5"])
        screen.blit(label_surface, (x, 86))
        x += label_surface.get_width() + 8

        # 3. Число
        value_surface = fonts["txt6"].render(str(value), True, COLORS["col5"])
        screen.blit(value_surface, (x, 84))
        x += value_surface.get_width() + 30   # отступ между ресурсами

    # Стабильность справа
    stability = p.mental_stability
    text = fonts["txt2"].render(
        f"СТАБИЛЬНОСТЬ: {stability:.1f}",
        True, COLORS["col5"],
    )
    screen.blit(text, (WIDTH - 280, 85))


# ============================================================
# Лог событий
# ============================================================
def draw_log(screen, fonts, images, gs):
    panel_rect = pygame.Rect(0, 140, 400, 460)

    # Фон — картинка LogPanel
    bg = images.get("log_panel")
    if bg:
        bg_scaled = pygame.transform.scale(bg, (panel_rect.width, panel_rect.height))
        screen.blit(bg_scaled, (panel_rect.x, panel_rect.y))
    else:
        draw_panel(screen, panel_rect, COLORS["col2"])   # запасной вариант

    # Дальше — заголовок и строки лога
    title = fonts["txt3"].render(TEXT_LOG_TITLE, True, COLORS["col5"])
    screen.blit(title, (60, 180))

    y = 260
    max_w = panel_rect.width - 80  # ширина панели минус отступы
    line_h = fonts["txt6"].get_height() + 4  # высота строки с зазором

    for line in gs.log:
        wrapped = wrap_text(line, fonts["txt6"], max_w)
        for part in wrapped:
            text = fonts["txt6"].render(part, True, COLORS["col5"])
            screen.blit(text, (60, y))
            y += line_h


# ============================================================
# Карточка события
# ============================================================
def draw_event_card(screen, fonts, images, gs):
    panel_rect = pygame.Rect(420, 140, WIDTH - 440, 460)

    # Фон — картинка Event Card
    bg = images.get("event_card")
    if bg:
        bg_scaled = pygame.transform.scale(bg, (panel_rect.width, panel_rect.height))
        screen.blit(bg_scaled, (panel_rect.x, panel_rect.y))
    else:
        draw_panel(screen, panel_rect, COLORS["col2"])

    # Название события
    if gs.current_event:
        title = fonts["txt4"].render(gs.current_event.title, True, COLORS["col6"])
        screen.blit(title, (450, 160))
    else:
        text = fonts["txt2"].render(
            "Событие ещё не произошло", True, COLORS["col6"],
        )
        screen.blit(text, (450, 160))