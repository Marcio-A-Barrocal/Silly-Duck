# window.py
"""
Interface gráfica do pato.
Responsabilidade única: criar a janela e rodar o loop de animação.
Toda lógica de estado, movimento e sprites vive em outros módulos.
"""

import time
import tkinter as tk

from .state   import DuckState
from .sprites import SpriteBank
from . import movement
from . import actions
from . import audio


# =============================================================================
# LOOP DE ANIMAÇÃO
# =============================================================================

def _animation_loop(root: tk.Tk, label: tk.Label, state: DuckState, bank: SpriteBank) -> None:
    """
    Loop principal de animação — chamado a cada ~100ms via root.after().
    Atualiza estado → movimento → sprite → posição da janela.
    """
    frame_start = time.time()

    # --- Tick de timers ---
    state.tick_cooldown()

    # --- Movimento ---
    if state.is_pulling:
        movement.pull_step(state)
    elif state.is_fleeing:
        movement.flee_from_mouse(state)
    elif state.is_following:
        movement.follow_mouse(state, on_catch=lambda: actions.on_catch_mouse(state))
    elif not state.is_idle:
        movement.walk_random(state)

    # --- Sprite ---
    sprite = bank.get_current(state)
    if sprite:
        # Guarda o sprite ANTERIOR antes de sobrescrever.
        # Sem isso, quando walk_index volta ao frame 0 (fim do ciclo),
        # o Tkinter pode rodar o GC no exato instante da troca e exibir
        # um frame transparente — o "flick branco" visível na animação.
        label._prev_image = label.image  # mantém o frame antigo vivo por +1 ciclo
        label.image = sprite
        label.config(image=sprite)

    # --- Posição da janela ---
    # update_idletasks() força o Tkinter a processar a imagem antes de mover
    # a janela, evitando o double-draw que causa ghost/flickering.
    root.update_idletasks()
    root.geometry(f"{state.WINDOW_SIZE}x{state.WINDOW_SIZE}+{int(state.pos_x)}+{int(state.pos_y)}")

    # --- Agenda próximo frame compensando o tempo gasto ---
    elapsed_ms = int((time.time() - frame_start) * 1000)
    root.after(max(1, 100 - elapsed_ms), lambda: _animation_loop(root, label, state, bank))


# =============================================================================
# CRIAÇÃO DA JANELA
# =============================================================================

def create_window(state: DuckState) -> None:
    """
    Cria a janela transparente, carrega sprites e inicia o loop de animação.

    Args:
        state: Instância compartilhada do DuckState (criada em main.py).
    """
    print("[WINDOW] Criando janela...")

    root = tk.Tk()
    state.set_root(root)

    # Janela sem borda, sempre no topo, com cor de transparência
    root.overrideredirect(True)
    root.attributes("-topmost", True)

    TRANSPARENT = "#ff00ff"
    root.configure(bg=TRANSPARENT)
    root.wm_attributes("-transparentcolor", TRANSPARENT)

    # Carrega sprites
    bank = SpriteBank()
    bank.load_all()

    if not bank.walk_right:
        print("[WINDOW] ERRO: Nenhum sprite carregado. Abortando.")
        return

    # Label que exibe o sprite — sem bordas ou padding extra
    label = tk.Label(root, image=bank.walk_right[0], bg=TRANSPARENT, bd=0, highlightthickness=0)
    label.place(x=0, y=0, width=state.WINDOW_SIZE, height=state.WINDOW_SIZE)
    label.image = bank.walk_right[0]       # referência inicial obrigatória
    label._prev_image = bank.walk_right[0] # evita AttributeError no primeiro frame

    # Mantém referência forte de todos os sprites para evitar garbage collection
    root._sprite_refs = bank.all_sprites

    # Clique no pato: quack + fuga
    def _on_click(event):
        if not state.is_pulling:
            audio.play_quack()
            state.start_fleeing()

    label.bind("<Button-1>", _on_click)

    print("[WINDOW] Iniciando animação...")
    _animation_loop(root, label, state, bank)
    root.mainloop()