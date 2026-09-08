"""Estados compartidos por los niveles jugables.

El estado describe el ciclo común de una partida; no pertenece a un nivel
concreto. Las reglas que causan cada transición siguen en su propio nivel.
"""

from enum import Enum, auto


class EstadoJuegoNivel(Enum):
    JUGANDO = auto()
    DERROTADO = auto()
    COMPLETADO = auto()
