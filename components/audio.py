# audio.py
"""
Sistema de áudio do pato.
"""

import os
import winsound

_AUDIO_PATH = os.path.normpath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "sounds", "quack.wav")
)


def play_quack() -> None:
    """Toca o som de quack de forma assíncrona."""
    if os.path.exists(_AUDIO_PATH):
        winsound.PlaySound(_AUDIO_PATH, winsound.SND_FILENAME | winsound.SND_ASYNC)
    else:
        print(f"[AUDIO] Arquivo não encontrado: {_AUDIO_PATH}")