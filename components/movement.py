# movement.py
"""
Lógica de movimentação do pato.
Todas as funções recebem `state` e `screen` como parâmetros
em vez de importar globais — facilita testes e leitura.
"""

import random
import pyautogui

from .state import DuckState


# =============================================================================
# TIPOS AUXILIARES
# =============================================================================

def _get_screen() -> tuple[int, int]:
    """Retorna (largura, altura) da tela principal."""
    return pyautogui.size()

def _clamp_to_screen(state: DuckState) -> None:
    """Impede o pato de sair dos limites da tela."""
    w, h = _get_screen()
    state.pos_x = max(0, min(state.pos_x, w - state.WINDOW_SIZE))
    state.pos_y = max(0, min(state.pos_y, h - state.WINDOW_SIZE))


# =============================================================================
# MODOS DE MOVIMENTO
# =============================================================================

def walk_random(state: DuckState) -> None:
    """
    Movimento aleatório pela tela.
    Vira o pato nas bordas e muda direção ocasionalmente.
    """
    w, h  = _get_screen()
    margin = 50

    # Vira nas bordas
    if state.pos_x <= margin:
        state.dir_x = 1
    elif state.pos_x >= w - state.WINDOW_SIZE - margin:
        state.dir_x = -1
    elif state.pos_y <= margin:
        state.dir_y = 1.0
    elif state.pos_y >= h - state.WINDOW_SIZE - margin:
        state.dir_y = -1.0
    elif random.random() < 0.03:
        # Mudança aleatória de direção (~3% de chance por frame)
        if random.random() < 0.80:
            roll = random.random()
            if roll < 0.60:
                pass  # mantém direção vertical atual
            elif roll < 0.80:
                state.dir_y = max(-1.0, state.dir_y - 0.3)
            else:
                state.dir_y = min(1.0, state.dir_y + 0.3)
        else:
            state.dir_x = random.choice([-1, 1])
            state.dir_y = random.uniform(-0.5, 0.5)

    # Normaliza o vetor para que movimentos diagonais não sejam mais rápidos
    # que movimentos horizontais/verticais. Sem isso, andar na diagonal 45°
    # percorre ~1.41x mais distância por frame do que andar em linha reta.
    magnitude = (state.dir_x ** 2 + state.dir_y ** 2) ** 0.5
    if magnitude > 0:
        state.pos_x += (state.dir_x / magnitude) * state.speed
        state.pos_y += (state.dir_y / magnitude) * state.speed

    _clamp_to_screen(state)


def follow_mouse(state: DuckState, on_catch) -> None:
    """
    Move o pato em direção ao cursor.
    Chama `on_catch()` quando alcança o mouse.
    """
    mx, my = pyautogui.position()
    target_x = mx - state.SPRITE_SIZE
    target_y = my - state.SPRITE_SIZE

    dx = target_x - state.pos_x
    dy = target_y - state.pos_y
    dist = (dx**2 + dy**2) ** 0.5

    if dist < state.speed:
        state.is_following = False
        on_catch()
        return

    state.dir_x = 1 if dx >= 0 else -1
    state.dir_y = (dy / dist) * 0.8 if dist > 0 else 0.0

    state.pos_x += state.dir_x * state.speed * abs(dx / dist)
    state.pos_y += state.dir_y * state.speed * 0.85


def flee_from_mouse(state: DuckState) -> None:
    """Move o pato na direção oposta ao cursor."""
    mx, my = pyautogui.position()

    dx = state.pos_x - (mx - state.SPRITE_SIZE)
    dy = state.pos_y - (my - state.SPRITE_SIZE)
    dist = (dx**2 + dy**2) ** 0.5

    if dist > 0:
        state.dir_x = 1 if dx >= 0 else -1
        nx, ny = dx / dist, dy / dist
    else:
        nx = float(random.choice([-1, 1]))
        ny = float(random.choice([-1, 1]))
        state.dir_x = int(nx)

    state.pos_x += nx * state.speed
    state.pos_y += ny * state.speed
    _clamp_to_screen(state)


def pull_step(state: DuckState) -> bool:
    """
    Um passo do movimento de 'puxar'.
    Retorna False quando o timer esgota (indica que deve parar).
    """
    if not state.tick_pull_timer():
        state.stop_pulling()
        return False

    state.pos_x += -state.dir_x * 2          # Recua na direção oposta
    state.pos_y += random.uniform(-0.5, 0.5)  # Leve oscilação vertical
    _clamp_to_screen(state)
    return True