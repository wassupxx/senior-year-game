"""
Точка входа игры «Ещё один день в школе».

Конечный автомат: EVENT_MODAL → CHOOSE_ACTION → (CHOOSE_TARGET) → EVENT_MODAL.
"""

import sys
import pygame

from game.config import (
    WIDTH, HEIGHT, FPS, TITLE,
    COLORS, FONTS_SPEC, PANEL_RADIUS,
    ICON_PATHS, IMG_LOG_PANEL, IMG_EVENT_CARD,
)
from game.logic.game_state import GameState
from game.logic.events_pool import ACTIONS
from game.ui.button import Button
from game.ui.panel import (
    draw_hud, draw_resources, draw_log, draw_event_card,
)
from game.ui.event_modal import EventModal


# ─── Состояния игры ───
STATE_EVENT_MODAL   = "EVENT_MODAL"
STATE_CHOOSE_ACTION = "CHOOSE_ACTION"
STATE_CHOOSE_TARGET = "CHOOSE_TARGET"
STATE_GAME_OVER     = "GAME_OVER"


def load_fonts():
    fonts = {}
    for key, (path, size) in FONTS_SPEC.items():
        try:
            fonts[key] = pygame.font.Font(path, size)
        except FileNotFoundError:
            print(f"[WARN] Шрифт не найден: {path}")
            fonts[key] = pygame.font.SysFont("arial", size)
    return fonts


def load_images():
    images = {}
    paths = {
        "log_panel":  IMG_LOG_PANEL,
        "event_card": IMG_EVENT_CARD,
        **{f"icon_{k}": v for k, v in ICON_PATHS.items()},
    }
    for key, path in paths.items():
        try:
            images[key] = pygame.image.load(path).convert_alpha()
        except (FileNotFoundError, pygame.error):
            print(f"[WARN] Картинка не найдена: {path}")
            images[key] = None
    return images


def create_action_buttons(fonts):
    """Создаёт 5 кнопок действий."""
    buttons = []
    btn_width, btn_height, gap = 230, 60, 10
    x, y = 20, 640
    for action in ACTIONS:
        rect = pygame.Rect(x, y, btn_width, btn_height)
        buttons.append(
            Button(
                rect=rect, text=action.title, font=fonts["txt5"],
                color_hover=COLORS["col2"],
            )
        )
        x += btn_width + gap
    return buttons


def create_target_buttons(fonts, gs):
    """Создаёт кнопки выбора цели для каждого игрока, кроме текущего."""
    buttons = []
    btn_width, btn_height, gap = 200, 60, 15
    y = 640
    targets = [i for i in range(len(gs.players)) if i != gs.current_player_index]
    total_width = len(targets) * btn_width + (len(targets) - 1) * gap
    x = (WIDTH - total_width) // 2
    for i in targets:
        rect = pygame.Rect(x, y, btn_width, btn_height)
        buttons.append((
            i,
            Button(
                rect=rect,
                text=gs.players[i].name,
                font=fonts["txt5"],
                color_normal=gs.players[i].color,
                color_hover=COLORS["col2"],
                text_color=COLORS["col6"],
            ),
        ))
        x += btn_width + gap
    return buttons


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()

    fonts = load_fonts()
    images = load_images()
    gs = GameState()
    gs.roll_event()

    # Кнопки действий — создаются один раз
    action_buttons = create_action_buttons(fonts)

    # Модалка события
    modal = EventModal(fonts)

    # Кнопки выбора цели — пересоздаются при входе в CHOOSE_TARGET
    target_buttons = []

    state = STATE_EVENT_MODAL
    selected_action = None

    running = True
    while running:
        mouse_click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_click = True

        mouse_pos = pygame.mouse.get_pos()
        screen.fill(COLORS["bg"])

        # ─── Рисуем основные панели ───
        draw_hud(screen, fonts, gs)
        draw_resources(screen, fonts, images, gs)
        draw_log(screen, fonts, images, gs)
        draw_event_card(screen, fonts, images, gs)

        # ─── Рисуем кнопки в зависимости от состояния ───
        if state == STATE_CHOOSE_ACTION:
            for btn, action in zip(action_buttons, ACTIONS):
                btn.set_enabled(gs.can_do_action(action))
                btn.update_hover(mouse_pos)
                btn.draw(screen)

                if btn.is_clicked(mouse_pos, mouse_click):
                    selected_action = action
                    # Если у действия есть эффект на цель — переходим к выбору цели
                    if action.target_effects:
                        target_buttons = create_target_buttons(fonts, gs)
                        state = STATE_CHOOSE_TARGET
                    else:
                        # Действие без цели — выполняем и переходим к следующему
                        gs.do_action(action)
                        gs.next_turn()
                        if gs.game_over:
                            state = STATE_GAME_OVER
                        else:
                            gs.roll_event()
                            state = STATE_EVENT_MODAL

        elif state == STATE_CHOOSE_TARGET:
            # Рисуем 3 кнопки игроков-целей
            for index, btn in target_buttons:
                btn.update_hover(mouse_pos)
                btn.draw(screen)

                if btn.is_clicked(mouse_pos, mouse_click):
                    # Выполняем действие с выбранной целью
                    gs.do_action(selected_action, target_index=index)
                    gs.next_turn()
                    selected_action = None
                    target_buttons = []
                    if gs.game_over:
                        state = STATE_GAME_OVER
                    else:
                        gs.roll_event()
                        state = STATE_EVENT_MODAL

        elif state == STATE_EVENT_MODAL:
            # Кнопки действий серые, пока модалка открыта
            for btn in action_buttons:
                btn.set_enabled(False)
                btn.draw(screen)

            if gs.current_event:
                modal.update_hover(mouse_pos)
                modal.draw(screen, gs.current_event, gs.current_event_effects)

                if modal.is_continue_clicked(mouse_pos, mouse_click):
                    state = STATE_CHOOSE_ACTION

        elif state == STATE_GAME_OVER:
            # Рисуем сообщение о победе/поражении
            if gs.winner:
                text = f"{gs.winner.name} победил!"
            elif gs.loser:
                text = f"{gs.loser.name} выбыл!"
            else:
                text = "Игра окончена"

            msg = fonts["txt4"].render(text, True, COLORS["col6"])
            msg_rect = msg.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(msg, msg_rect)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()