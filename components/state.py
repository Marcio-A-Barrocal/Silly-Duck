# state.py
"""
Estado central do pato encapsulado em uma classe.
Substitui todas as variáveis globais espalhadas por um objeto único
que pode ser passado entre módulos com clareza.
"""

import random


class DuckState:
    # ------------------------------------------------------------------
    # Configurações fixas (constantes de classe)
    # ------------------------------------------------------------------
    BASE_SPEED  = 10
    FLEE_SPEED  = 18
    SPRITE_SIZE = 64
    WINDOW_SIZE = 128

    PULL_FRAMES      = 12   # Duração do estado de puxar em frames
    PULL_COOLDOWN    = 50   # Frames de cooldown após puxar
    IDLE_AFTER_PULL  = 3    # Segundos de idle após puxar
    IDLE_AFTER_FLEE  = 2    # Segundos de idle após fugir
    FLEE_MIN_MS      = 2000
    FLEE_MAX_MS      = 4000

    def __init__(self):
        # --- Posição e movimento ---
        self.pos_x: float = 300.0
        self.pos_y: float = 300.0
        self.dir_x: int   = 1      # -1 = esquerda, 1 = direita
        self.dir_y: float = 0.0
        self.speed: float = self.BASE_SPEED

        # --- Flags de estado (mutuamente exclusivos) ---
        self.is_idle:           bool = False
        self.is_following:      bool = False
        self.is_pulling:        bool = False
        self.is_fleeing:        bool = False

        # --- Contadores de animação ---
        self.walk_index:      int = 0
        self.walk_frame_skip: int = 0  # quantos frames de loop já passaram no sprite atual
        self.idle_index:      int = 0
        self.pull_index:      int = 0
        self.bounce_index:    int = 0

        # --- Timers ---
        self.pull_timer:    int = 0
        self.pull_cooldown: int = 0

        # --- Referência à janela Tkinter (injetada em runtime) ---
        self._root = None

    # ------------------------------------------------------------------
    # Injeção de dependência da janela
    # ------------------------------------------------------------------

    def set_root(self, root) -> None:
        self._root = root

    def _schedule(self, delay_ms: int, callback) -> None:
        """Agenda um callback no loop do Tkinter de forma segura."""
        if self._root:
            self._root.after(delay_ms, callback)

    # ------------------------------------------------------------------
    # Propriedade auxiliar: pato está ocupado com alguma ação especial?
    # ------------------------------------------------------------------

    @property
    def is_busy(self) -> bool:
        return self.is_following or self.is_idle or self.is_pulling or self.is_fleeing

    # ------------------------------------------------------------------
    # Transições de estado
    # ------------------------------------------------------------------

    def _clear_active_states(self) -> None:
        """Zera todas as flags de estado antes de aplicar uma nova."""
        self.is_idle      = False
        self.is_following = False
        self.is_fleeing   = False
        # is_pulling não é zerado aqui — tem sua própria lógica de parada

    def start_following(self) -> None:
        self._clear_active_states()
        self.is_following = True
        print("[STATE] Caçando o mouse!")

    def start_pulling(self) -> None:
        self.is_idle    = False
        self.is_pulling = True
        self.pull_timer = self.PULL_FRAMES
        print("[STATE] Puxando o mouse!")

    def stop_pulling(self) -> None:
        self.is_pulling = False
        self.start_idle(self.IDLE_AFTER_PULL)
        print("[STATE] Terminou de puxar!")

    def start_idle(self, duration_seconds: int) -> None:
        self.is_idle = True
        print(f"[STATE] Descansando por {duration_seconds}s.")
        self._schedule(duration_seconds * 1000, self.stop_idle)

    def stop_idle(self) -> None:
        self.is_idle = False
        print("[STATE] Voltando a andar...")

    def start_fleeing(self) -> None:
        if self.is_fleeing:
            return
        self._clear_active_states()
        self.is_fleeing   = True
        self.bounce_index = 0
        self.speed        = self.FLEE_SPEED
        print("[STATE] Fugindoooo!")

        delay = random.randint(self.FLEE_MIN_MS, self.FLEE_MAX_MS)
        self._schedule(delay, self.stop_fleeing)

    def stop_fleeing(self) -> None:
        if not self.is_fleeing:
            return
        self.is_fleeing = False
        self.speed      = self.BASE_SPEED
        print("[STATE] Ufa, escapei.")
        self.start_idle(self.IDLE_AFTER_FLEE)

    # ------------------------------------------------------------------
    # Atualizações por frame (chamadas pelo loop de animação)
    # ------------------------------------------------------------------

    def tick_cooldown(self) -> None:
        if self.pull_cooldown > 0:
            self.pull_cooldown -= 1

    def tick_pull_timer(self) -> bool:
        """Decrementa o timer de puxar. Retorna True enquanto ainda está ativo."""
        if self.pull_timer > 0:
            self.pull_timer -= 1
            return True
        return False