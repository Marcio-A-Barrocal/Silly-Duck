# sprites.py
"""
Carregamento e seleção de sprites do pato.
Toda lógica de imagem fica aqui — a janela só consome o resultado final.
"""

import os
from PIL import Image, ImageTk

from .state import DuckState

# Tamanho final de cada sprite em pixels
_SPRITE_PX = DuckState.SPRITE_SIZE
_ASSETS    = os.path.join("assets", "images")


# =============================================================================
# PROCESSAMENTO DE IMAGEM (funções internas)
# =============================================================================

def _remove_magenta(img: Image.Image) -> Image.Image:
    """Substitui pixels magenta (fundo) por transparência."""
    data = [
        (255, 255, 255, 0) if (a < 255 or (r == 255 and g < 50 and b == 255)) else (r, g, b, a)
        for r, g, b, a in img.getdata()
    ]
    img.putdata(data)
    return img

def _process(path: str) -> Image.Image | None:
    """Abre, limpa fundo e redimensiona uma imagem. Retorna None se não existir."""
    if not os.path.exists(path):
        return None
    img = Image.open(path).convert("RGBA")
    img = _remove_magenta(img)
    return img.resize((_SPRITE_PX, _SPRITE_PX), Image.Resampling.NEAREST)

def _to_tk(img: Image.Image) -> ImageTk.PhotoImage:
    return ImageTk.PhotoImage(img)

def _mirrored_pair(path: str) -> tuple[ImageTk.PhotoImage, ImageTk.PhotoImage] | tuple[None, None]:
    """Retorna (sprite_direita, sprite_esquerda) ou (None, None) se arquivo ausente."""
    img = _process(path)
    if img is None:
        return None, None
    return _to_tk(img), _to_tk(img.transpose(Image.FLIP_LEFT_RIGHT))


# =============================================================================
# BANCO DE SPRITES
# =============================================================================

class SpriteBank:
    """
    Armazena todos os sprites carregados e expõe o sprite correto
    para o frame atual baseado no estado do pato.
    """

    def __init__(self):
        self.walk_right:   list[ImageTk.PhotoImage] = []
        self.walk_left:    list[ImageTk.PhotoImage] = []
        self.idle:         list[ImageTk.PhotoImage] = []
        self.pull_right:   list[ImageTk.PhotoImage] = []
        self.pull_left:    list[ImageTk.PhotoImage] = []
        self.bounce_right: list[ImageTk.PhotoImage] = []
        self.bounce_left:  list[ImageTk.PhotoImage] = []

    # ------------------------------------------------------------------
    # Carregamento
    # ------------------------------------------------------------------

    def _load_mirrored_sequence(self, prefix: str, count: int) -> tuple[list, list]:
        """Carrega uma sequência numerada de sprites e suas versões espelhadas."""
        rights, lefts = [], []
        for i in range(1, count + 1):
            right, left = _mirrored_pair(os.path.join(_ASSETS, f"{prefix}{i}.png"))
            if right:
                rights.append(right)
                lefts.append(left)
        return rights, lefts

    def _load_sequence(self, prefix: str) -> list:
        """Carrega sprites numerados até o primeiro arquivo ausente."""
        sprites, i = [], 1
        while True:
            img = _process(os.path.join(_ASSETS, f"{prefix}{i}.png"))
            if img is None:
                break
            sprites.append(_to_tk(img))
            i += 1
        return sprites

    def load_all(self) -> None:
        print("[SPRITES] Carregando todos os sprites...")

        self.walk_right, self.walk_left = self._load_mirrored_sequence("walk", 6)
        print(f"  walk:   {len(self.walk_right)} sprites")

        self.idle = self._load_sequence("idle")
        if not self.idle and self.walk_right:           # fallback
            self.idle = [self.walk_right[0]]
        print(f"  idle:   {len(self.idle)} sprites")

        self.pull_right, self.pull_left = self._load_mirrored_sequence("pull", 2)
        if not self.pull_right:                         # fallback
            self.pull_right = self.walk_right.copy()
            self.pull_left  = self.walk_left.copy()
        print(f"  pull:   {len(self.pull_right)} sprites")

        self.bounce_right, self.bounce_left = self._load_mirrored_sequence("bounce", 6)
        if not self.bounce_right:                       # fallback
            self.bounce_right = self.walk_right.copy()
            self.bounce_left  = self.walk_left.copy()
        print(f"  bounce: {len(self.bounce_right)} sprites")

        print("[SPRITES] Carregamento concluído!")

    @property
    def all_sprites(self) -> list:
        """Lista plana de todos os sprites — usada para manter referências fortes no Tkinter."""
        return (
            self.walk_right + self.walk_left +
            self.idle +
            self.pull_right + self.pull_left +
            self.bounce_right + self.bounce_left
        )

    # ------------------------------------------------------------------
    # Seleção de sprite por frame
    # ------------------------------------------------------------------

    def get_current(self, state: DuckState) -> ImageTk.PhotoImage | None:
        """
        Retorna o sprite correto para o frame atual.

        O estado é capturado uma única vez no início para evitar race conditions.
        Os índices são avançados ANTES da seleção do sprite — isso garante que
        a troca de direção (esquerda/direita) nunca usa um índice "do frame errado",
        eliminando o flick de um frame durante a caminhada.
        """
        fleeing = state.is_fleeing
        pulling = state.is_pulling
        idle    = state.is_idle
        facing  = state.dir_x  # 1 = direita, -1 = esquerda

        if fleeing and self.bounce_right:
            state.bounce_index = (state.bounce_index + 1) % len(self.bounce_right)
            return self.bounce_right[state.bounce_index] if facing >= 0 else self.bounce_left[state.bounce_index]

        if pulling and self.pull_right:
            state.pull_index = (state.pull_index + 1) % (len(self.pull_right) * 2)
            idx = state.pull_index // 2
            return self.pull_right[idx] if facing >= 0 else self.pull_left[idx]

        if idle and self.idle:
            state.idle_index = (state.idle_index + 1) % len(self.idle)
            return self.idle[state.idle_index]

        if self.walk_right:
            state.walk_index = (state.walk_index + 1) % len(self.walk_right)
            idx = state.walk_index
            return self.walk_right[idx] if facing >= 0 else self.walk_left[idx]

        return None