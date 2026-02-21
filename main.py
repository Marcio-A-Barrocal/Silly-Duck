# main.py
"""
Ponto de entrada do Desktop Duck.

Responsabilidades:
  - Criar o DuckState compartilhado
  - Iniciar a thread do cérebro (decisões autônomas)
  - Iniciar a janela Tkinter (animação + eventos)
"""

import random
import threading
import time

from components.state  import DuckState
from components.window import create_window


# =============================================================================
# CÉREBRO DO PATO
# =============================================================================

def _brain_loop(state: DuckState) -> None:
    """
    Toma decisões autônomas em intervalos aleatórios.
    Roda em thread separada para não bloquear a interface.
    """
    print("[BRAIN] Cérebro ativado!")

    while True:
        time.sleep(random.randint(8, 15))

        if state.is_busy:
            continue  # Pato já está ocupado, não interrompe

        roll = random.random()

        if roll < 0.30:
            print("[BRAIN] Vou caçar o mouse!")
            state.start_following()
        elif roll < 0.50:
            secs = random.randint(3, 5)
            print(f"[BRAIN] Vou descansar por {secs}s.")
            state.start_idle(secs)
        else:
            print("[BRAIN] Continuando a andar...")


# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    print("[MAIN] Iniciando Desktop Duck...")

    state = DuckState()  # Estado compartilhado entre todas as threads

    brain = threading.Thread(target=_brain_loop, args=(state,), daemon=True)
    brain.start()

    create_window(state)  # Bloqueia até a janela ser fechada

    print("[MAIN] Desktop Duck encerrado.")