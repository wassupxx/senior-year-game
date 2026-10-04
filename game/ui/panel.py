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
    """5 иконок ресурсов + числа + ментальная стабильность."""
    panel_rect = pygame.Rect(0, 60, WIDTH, 70)
    draw_panel(screen, panel_rect, COLORS["col1"])

    p = gs.current_player
    resources = [
        ("stress",   p.stress),
        ("money",    p.money),
        ("friends",  p.friends),
        ("homework", p.homework),
        ("bullying", p.bullying),
    ]

    x = 30
    for key, value in resources:
        icon = images.get(f"icon_{key}")
        if icon:
            icon_scaled = pygame.transform.scale(icon, (40, 40))
            screen.blit(icon_scaled, (x, 75))
            x += 45

        text = fonts["txt2"].render(str(value), True, COLORS["col5"])
        screen.blit(text, (x, 85))
        x += 60

    stability = p.mental_stability
    text = fonts["txt2"].render(
        f"Стабильность: {stability:.1f}",
        True, COLORS["col5"],
    )
    screen.blit(text, (WIDTH - 300, 85))


# ============================================================
# Лог событий
# ============================================================
def draw_log(screen, fonts, images, gs):
    """Лог последних 5 событий и действий слева."""
    panel_rect = pygame.Rect(0, 140, 400, 460)
    draw_panel(screen, panel_rect, COLORS["col2"])

    title = fonts["txt3"].render(TEXT_LOG_TITLE, True, COLORS["col5"])
    screen.blit(title, (20, 150))

    y = 220
    for line in gs.log:
        text = fonts["txt6"].render(line, True, COLORS["col5"])
        screen.blit(text, (20, y))
        y += 25


# ============================================================
# Карточка события
# ============================================================
def draw_event_card(screen, fonts, images, gs):
    """Название события справа и эффекты от него."""
    panel_rect = pygame.Rect(420, 140, WIDTH - 440, 460)
    draw_panel(screen, panel_rect, COLORS["col2"])

    if gs.current_event:
        title = fonts["txt4"].render(
            gs.current_event.title, True, COLORS["col5"],
        )
        screen.blit(title, (450, 160))
    else:
        text = fonts["txt2"].render(
            "Событие ещё не произошло", True, COLORS["col9"],
        )
        screen.blit(text, (450, 160))