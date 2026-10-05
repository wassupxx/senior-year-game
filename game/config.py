"""
Константы игры «Senior year».

Палитра и шрифты — из game/docs/colors_and_fonts.md (дизайнер alesya889).
Размеры, стартовые ресурсы, условия — из docs/game_design.md (менеджер).
"""

import pygame

# ============================================================
# ОКНО
# ============================================================
WIDTH, HEIGHT = 1280, 720
FPS = 60
TITLE = "Senior Year Game"

# Радиус скругления панелей — из правил оформления
PANEL_RADIUS = 10


# ============================================================
# ЦВЕТА
# ============================================================
COLORS = {
    # --- Базовые ---
    "bg":        (75, 80, 84),      # фон
    "col1":      (138, 162, 190),   # панель 1, панель очков, кнопки "Продолжить"/"Новая игра"
    "col2":      (242, 242, 242),   # панель 2, панель 3, фон модалки, фон победы/проигрыша
    "col3":      (32, 34, 33),      # панель цели
    "col4":      (0, 0, 0, 180),    # затемнение фона (альфа-канал)

    # --- Текст ---
    "col5":      (0, 0, 0),         # основной текст, текст на карточке события
    "col6":      (255, 255, 255),   # текст на панели 4, "событие", "продолжить", "новая игра"
    "col7":      (76, 80, 84),      # доступные действия
    "col8":      (189, 189, 189),   # недоступные действия
    "col9":      (122, 126, 130),   # описание всплывающего события

    # --- Семантика ---
    "pos":       (119, 143, 96),    # зелёный (положительное)
    "neg":       (196, 0, 69),      # красный (отрицательное)
}


# ============================================================
# ШРИФТЫ
# ============================================================
# Пути к .ttf — относительно корня репозитория
FONT_PATH       = "game/assets/fonts/RubikMonoOne-Regular.ttf"
FONT_BAD_SCRIPT = "game/assets/fonts/BadScript-Regular.ttf"

# Шрифты инициализируются в main.py после pygame.init()
# Здесь только описание: ключ → (путь, размер)
FONTS_SPEC = {
    "txt1": (FONT_PATH,       20),   # панель 1, "Новая игра", описание конца игры, название события
    "txt2": (FONT_PATH,       16),   # панель 2, "действия:", панель 4
    "txt3": (FONT_BAD_SCRIPT, 42),   # "Лог событий"
    "txt4": (FONT_PATH,       30),   # "Событие", "Победа", "Школьник выбыл"
    "txt5": (FONT_PATH,       10),   # варианты действий
    "txt6": (FONT_PATH,       12),   # "Продолжить", описание всплывающего события
    "txt7": (FONT_PATH,       14),   # эффекты от события
}


# ============================================================
# ИГРОКИ
# ============================================================
PLAYER_NAMES = [
    "Student 1",
    "Student 2",
    "Student 3",
    "Student 4",
]

PLAYER_COLORS = [
    (200,  60,  60),
    ( 60, 100, 200),
    ( 60, 180,  80),
    (220, 190,  60),
]


# ============================================================
# СТАРТОВЫЕ РЕСУРСЫ (из правил)
# ============================================================
START_RESOURCES = {
    "stress":   5,    # стресс
    "money":   10,    # деньги
    "friends": 15,    # друзья
    "homework": 10,   # домашка
    "bullying":  0,   # буллинг
}


# ============================================================
# УСЛОВИЯ ПОБЕДЫ / ПОРАЖЕНИЯ
# ============================================================
WIN_STABILITY = 60    # победа при mental_stability >= 60
LOSE_BULLYING = 10    # поражение при bullying >= 10


# ============================================================
# ПУТИ К АССЕТАМ (иконки и картинки)
# ============================================================
# Иконки ресурсов — для панели ресурсов
ICON_PATHS = {
    "stress":   "game/assets/icons/Stress.png",
    "money":    "game/assets/icons/Money.png",
    "friends":  "game/assets/icons/Friend.png",
    "homework": "game/assets/icons/Homework.png",
    "bullying": "game/assets/icons/Bullying.png",
    "points":   "game/assets/icons/Points.png",   # иконка ментальной стабильности
}

# Картинки событий — для карточки события
EVENT_IMAGES = {
    "E1": "game/assets/images/Lunch.png",    # Обед
    "E2": "game/assets/images/Test.png",     # Контрольная
    "E3": "game/assets/images/Stroll.png",   # Прогул
    "E4": "game/assets/images/Delay.png",    # Опоздание
    "E5": "game/assets/images/Meet.png",     # Встреча с параллелью
    "E6": "game/assets/images/Break.png",    # Перемена
}

# Фоны панелей
IMG_EVENT_CARD = "game/assets/images/Event Card.png"
IMG_LOG_PANEL  = "game/assets/images/LogPanel.png"
IMG_WIN        = "game/assets/images/Win.png"
IMG_LOSS       = "game/assets/images/Loss.png"


# ============================================================
# ТЕКСТЫ ИНТЕРФЕЙСА
# ============================================================
TEXT_LOG_TITLE    = "Лог событий"
TEXT_EVENT_TITLE  = "Событие"
TEXT_ACTIONS      = "Действия:"
TEXT_CONTINUE     = "Продолжить"
TEXT_NEW_GAME     = "Новая игра"
TEXT_WIN          = "Победа"
TEXT_LOSS         = "Школьник выбыл"

# ============================================================
# ФОРМАТИРОВАНИЕ ЭФФЕКТОВ
# ============================================================
RESOURCE_NAMES = {
    "stress":   "стресс",
    "money":    "деньги",
    "friends":  "друзья",
    "homework": "домашка",
    "bullying": "буллинг",
}


def format_effects(effects):
    """{'friends': 3, 'stress': -2} → '+3 друзья, −2 стресс'."""
    if not effects:
        return ""
    parts = []
    for key, value in effects.items():
        sign = "+" if value > 0 else "−"
        name = RESOURCE_NAMES.get(key, key)
        parts.append(f"{sign}{abs(value)} {name}")
    return ", ".join(parts)


def format_cost(cost):
    """{'homework': 3} → '−3 домашка'"""

    parts = []
    for key, value in cost.items():
        name = RESOURCE_NAMES.get(key, key)
        parts.append(f"−{abs(value)} {name}")
    return ", ".join(parts)

def wrap_text(text, font, max_width):
    """
    Режет текст на строки по max_width пикселей.
    Возвращает список строк.
    """
    words = text.split()
    lines = []
    current = ""
    for word in words:
        test = (current + " " + word).strip()
        if font.size(test)[0] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines