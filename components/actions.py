# actions.py
"""
Ações do pato sobre o mouse do sistema (pyautogui).
Separado de movement.py pois interage com hardware externo.
"""

import random
import time
import threading

import pyautogui

from .state import DuckState


def annoy_mouse() -> None:
    """Chacoalha o cursor em movimentos pequenos e aleatórios."""
    print("[ACTIONS] Bagunçando o mouse!")
    for _ in range(10):
        pyautogui.moveRel(
            random.randint(-25, 25),
            random.randint(-25, 25),
            duration=0.05,
        )


def drag_mouse_with_beak(dir_x: int) -> None:
    """
    Puxa o cursor sincronizado com o movimento do pato (thread separada).

    Args:
        dir_x: Direção que o pato está olhando (1 = direita, -1 = esquerda).
               O mouse é puxado na direção oposta para simular resistência.
    """
    pull_dir = -dir_x

    def _pull():
        print("[ACTIONS] Puxando o mouse com o bico!")
        for _ in range(DuckState.PULL_FRAMES):
            pyautogui.moveRel(pull_dir * 2, random.randint(-1, 1), duration=0.05)
            time.sleep(0.05)

    threading.Thread(target=_pull, daemon=True).start()


def on_catch_mouse(state: DuckState) -> None:
    """
    Decide o que acontece quando o pato alcança o mouse.
    Chamado por movement.follow_mouse() via callback.
    """
    print("[ACTIONS] Peguei o mouse!")

    if state.pull_cooldown > 0 or random.random() < 0.5:
        annoy_mouse()
        state.start_idle(2)
    else:
        state.start_pulling()
        drag_mouse_with_beak(state.dir_x)
        state.pull_cooldown = state.PULL_COOLDOWN